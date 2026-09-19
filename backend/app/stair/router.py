"""
STAIR-Style Structure-Aware Query Router (Zero Fine-Tuning).
Uses the existing local Qwen 2.5 7B model through hierarchical ToC prompting
and deterministic regex-based hybrid routing.
"""

import time
import json
import re
import logging
from typing import Optional, List, Dict, Any

from app.core.llm_provider import get_llm
from app.stair.schemas import STAIRRoutingOutput, SelectedLeaf
from app.stair.leaf_registry import LeafCatalog
from app.stair.validator import STAIRValidator

logger = logging.getLogger("stair.router")

ROUTER_SYSTEM_PROMPT = """You are an expert law enforcement retrieval router for an investigation platform.
Your task is to select the valid investigation leaf sections needed to answer the investigator's query.

CRITICAL PROTOCOLS:
1. DO NOT answer the investigator's question.
2. DO NOT invent section IDs or tool names. Select ONLY IDs listed in the Investigation Structure below.
3. For multi-domain questions (e.g. asking about suspicious transfers AND suspect locations), select MULTIPLE relevant leaf IDs.
4. Extract any explicit entity names, phone numbers, or accounts from the query into the "parameters" object.
5. Output ONLY a valid JSON array of objects. No markdown, no prose, no explanations outside JSON.

OUTPUT JSON SCHEMA:
[
  {
    "leaf_id": "exact.leaf_id.from.structure",
    "reason": "brief rationale why this leaf is needed",
    "parameters": {
      "entity_name": "extracted name or null",
      "account_number": "extracted account or null",
      "phone_number": "extracted phone or null"
    }
  }
]

{toc_block}
"""

class STAIRQueryRouter:
    """Structure-aware query router directing queries to authorized leaf nodes without fine-tuning."""

    @classmethod
    def check_deterministic_hybrid_route(cls, query: str, case_id: str) -> Optional[List[SelectedLeaf]]:
        """
        Fast deterministic hybrid routing for unambiguous regex-based identifiers or standard commands.
        Bypasses LLM latency for instant 0ms routing when high-confidence patterns exist.
        """
        q = query.strip()
        q_low = q.lower()
        selected: List[SelectedLeaf] = []

        # 1. Direct Section 65B inquiry
        if any(k in q_low for k in ["section 65b", "65b", "evidence certificate", "bsa 63"]):
            selected.append(SelectedLeaf(
                leaf_id="reports.section_65b",
                reason="Direct request for Section 65B Electronic Evidence Certificate",
                parameters={"case_id": case_id}
            ))
            return selected

        # 2. Direct Court Dossier / Formal Dossier inquiry
        if any(k in q_low for k in ["court dossier", "formal dossier", "prosecution brief", "dossier report"]):
            selected.append(SelectedLeaf(
                leaf_id="reports.court_dossier",
                reason="Direct request for formal court dossier report",
                parameters={"case_id": case_id}
            ))
            return selected

        # 3. Direct Phone Number (E.164 or 10-digit Indian mobile)
        phone_match = re.search(r'\b(?:\+91[\-\s]?)?[6-9]\d{9}\b', q)
        if phone_match and not any(k in q_low for k in ["where", "location", "tower", "transfer", "bank"]):
            selected.append(SelectedLeaf(
                leaf_id="telecom.cdr_records",
                reason="Direct phone number CDR lookup",
                parameters={"case_id": case_id, "phone_number": phone_match.group(0).replace(" ", "").replace("-", "")}
            ))
            return selected

        # 4. Direct IPv4 lookup
        ip_match = re.search(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', q)
        if ip_match and not any(k in q_low for k in ["where", "location", "who", "transfer"]):
            selected.append(SelectedLeaf(
                leaf_id="telecom.ipdr_sessions",
                reason="Direct IPv4 session lookup",
                parameters={"case_id": case_id, "ip_address": ip_match.group(0)}
            ))
            return selected

        # 5. Direct 15-digit IMEI lookup
        imei_match = re.search(r'\b\d{14,16}\b', q)
        if imei_match and "imei" in q_low:
            selected.append(SelectedLeaf(
                leaf_id="telecom.imei_telemetry",
                reason="Direct IMEI handset lookup",
                parameters={"case_id": case_id, "imei": imei_match.group(0)}
            ))
            return selected

        return None

    @classmethod
    def route_query(
        cls,
        query: str,
        case_id: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> STAIRRoutingOutput:
        """
        Routes an investigator query to valid leaf IDs using local Qwen 2.5 7B
        with ToC prompt injection and hard validation.
        """
        start_time = time.time()

        # Step 1: Check fast deterministic hybrid route
        deterministic_match = cls.check_deterministic_hybrid_route(query, case_id)
        if deterministic_match:
            elapsed_ms = (time.time() - start_time) * 1000
            return STAIRRoutingOutput(
                query=query,
                case_id=case_id,
                selected_leaves=deterministic_match,
                rejected_leaves=[],
                is_multi_source=len(deterministic_match) > 1,
                routing_latency_ms=round(elapsed_ms, 2),
                router_mode="deterministic_hybrid"
            )

        # Step 2: Build STAIR Prompt with complete Investigation Hierarchy ToC
        toc_block = LeafCatalog.get_toc_prompt_block()
        system_instruction = ROUTER_SYSTEM_PROMPT.replace("{toc_block}", toc_block)

        # Extract target entity name hint if mentioned in query
        name_hint = ""
        name_regex = re.search(r'(?:for|of|about|against|by|target)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', query)
        if name_regex:
            name_hint = f"\nDetected Target Entity Hint: {name_regex.group(1)}"

        user_content = f"ACTIVE CASE ID: {case_id}\nINVESTIGATOR QUERY: \"{query}\"{name_hint}\n\nSelect the required leaf IDs as JSON array:"

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ]

        raw_llm_output = ""
        try:
            # Low temperature (0.0) for strict deterministic leaf selection
            llm = get_llm(num_predict=250, num_ctx=2048)
            resp = llm.invoke(messages)
            raw_llm_output = resp.content if hasattr(resp, "content") else str(resp)
        except Exception as e:
            logger.warning(f"[STAIRRouter] LLM routing invocation failed: {e}")

        # Step 3: Hard Output Validation
        parsed_items = STAIRValidator.parse_router_json(raw_llm_output)
        validated_leaves, rejected_leaves = STAIRValidator.validate_and_filter_selections(parsed_items, case_id)

        # Step 4: Fallback if LLM produced empty or invalid leaves
        router_mode = "qwen_toc"
        if not validated_leaves:
            logger.info("[STAIRRouter] Validation resulted in 0 leaves. Falling back to keyword candidate match.")
            fallback_leaf_ids = LeafCatalog.fast_keyword_match(query)
            if not fallback_leaf_ids:
                # Default safe exploration leaf
                fallback_leaf_ids = ["entity.golden_profile"]

            for fl_id in fallback_leaf_ids[:3]:
                validated_leaves.append(SelectedLeaf(
                    leaf_id=fl_id,
                    reason="Keyword heuristic recovery",
                    parameters={"case_id": case_id}
                ))
            router_mode = "fallback"

        # Enrich leaf parameters with target entity name if missing
        if name_regex:
            detected_name = name_regex.group(1).strip()
            for leaf in validated_leaves:
                if not leaf.parameters.get("entity_name"):
                    leaf.parameters["entity_name"] = detected_name

        elapsed_ms = (time.time() - start_time) * 1000

        return STAIRRoutingOutput(
            query=query,
            case_id=case_id,
            selected_leaves=validated_leaves,
            rejected_leaves=rejected_leaves,
            is_multi_source=len(validated_leaves) > 1,
            routing_latency_ms=round(elapsed_ms, 2),
            router_mode=router_mode
        )
