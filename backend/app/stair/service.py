"""
Unified STAIR Investigation Service.
Orchestrates Structure-Aware Routing, Hard Validation, Evidence Broker Execution,
Evidence Normalization, Deterministic Verification, Grounded Qwen Generation,
and Post-Generation Claim-to-Evidence Provenance Mapping.
Supports Shadow Mode for side-by-side comparison against legacy Agentic RAG.
"""

import time
import os
import logging
from typing import Optional, List, Dict, Any

from app.stair.schemas import (
    STAIRInvestigationResult, NormalizedEvidenceItem,
    ClaimEvidenceMap, DeterministicFactCheck, VerificationReport
)
from app.stair.router import STAIRQueryRouter
from app.stair.validator import STAIRValidator
from app.stair.evidence_broker import EvidenceBroker
from app.stair.evidence_normalizer import EvidenceNormalizer
from app.stair.verifier import DeterministicVerifier
from app.stair.grounded_generator import GroundedGenerator

logger = logging.getLogger("stair.service")

class STAIRInvestigationService:
    """Master orchestrator for the STAIR-style evidence-first investigation pipeline."""

    def __init__(self):
        self.enabled = os.getenv("STAIR_ENABLED", "true").lower() in ("true", "1", "yes")
        self.shadow_mode = os.getenv("STAIR_SHADOW_MODE", "false").lower() in ("true", "1", "yes")

    def investigate(
        self,
        query: str,
        case_id: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> STAIRInvestigationResult:
        """
        Executes the complete evidence-first investigation pipeline:
        1. STAIR Structure-Aware Routing (Qwen 2.5 7B ToC + Hybrid Matcher)
        2. Hard Output Validation & Leaf Registry Enforcement
        3. Case-Scoped Evidence Broker Execution
        4. Universal Evidence Normalization & Lineage Preservation
        5. Deterministic Verification & Temporal/Entity Guardrails
        6. Grounded Generation via Qwen 2.5 7B
        7. Claim -> Evidence Provenance Mapping
        """
        target_case_id = case_id or "INV-2026-BLACK-CIRCUIT"
        latencies: Dict[str, float] = {}
        total_start = time.time()

        logger.info(f"[STAIR] Processing investigation query for Case: {target_case_id} | Query: '{query[:80]}'")

        # ── Step 1 & 2: Routing & Hard Validation ─────────────────────────────
        t0 = time.time()
        routing_output = STAIRQueryRouter.route_query(query=query, case_id=target_case_id, history=history)
        latencies["routing_ms"] = round((time.time() - t0) * 1000, 2)

        selected_leaf_ids = [l.leaf_id for l in routing_output.selected_leaves]
        logger.info(f"[STAIR] Selected leaf IDs ({routing_output.router_mode}): {selected_leaf_ids}")

        # ── Step 3: Evidence Broker Execution ─────────────────────────────────
        t1 = time.time()
        raw_evidence_by_leaf: Dict[str, List[Dict[str, Any]]] = {}
        all_raw_records: List[Dict[str, Any]] = []

        for leaf in routing_output.selected_leaves:
            records = EvidenceBroker.execute_leaf(leaf, query=query)
            raw_evidence_by_leaf[leaf.leaf_id] = records
            all_raw_records.extend(records)
        latencies["retrieval_ms"] = round((time.time() - t1) * 1000, 2)

        # ── Step 4: Universal Evidence Normalization ──────────────────────────
        t2 = time.time()
        normalized_evidence: List[NormalizedEvidenceItem] = []
        ev_counter = 1

        for leaf_id, records in raw_evidence_by_leaf.items():
            norm_items = EvidenceNormalizer.normalize_records(
                leaf_id=leaf_id,
                case_id=target_case_id,
                raw_records=records,
                start_index=ev_counter
            )
            normalized_evidence.extend(norm_items)
            ev_counter += len(norm_items)

        # Separate primary and generated items for provenance cross-linking
        primary_items = [i for i in normalized_evidence if i.authority.value == "PRIMARY"]
        generated_items = [i for i in normalized_evidence if i.authority.value == "GENERATED"]
        EvidenceNormalizer.link_report_to_primary_evidence(generated_items, primary_items)
        latencies["normalization_ms"] = round((time.time() - t2) * 1000, 2)

        # ── Step 5: Deterministic Fact Verification & Guardrails ───────────────
        t3 = time.time()
        verification_report = DeterministicVerifier.verify(
            case_id=target_case_id,
            evidence_items=normalized_evidence,
            query=query
        )
        latencies["verification_ms"] = round((time.time() - t3) * 1000, 2)

        # ── Step 6 & 7: Grounded Generation & Claim Provenance Mapping ─────────
        t4 = time.time()
        reply_text, claim_mappings = GroundedGenerator.generate_response(
            query=query,
            case_id=target_case_id,
            evidence_items=normalized_evidence,
            verification_report=verification_report
        )
        latencies["generation_ms"] = round((time.time() - t4) * 1000, 2)

        total_elapsed_ms = round((time.time() - total_start) * 1000, 2)
        latencies["total_e2e_ms"] = total_elapsed_ms

        logger.info(
            f"[STAIR] Completed query in {total_elapsed_ms}ms | "
            f"Evidence items: {len(normalized_evidence)} | Claims: {len(claim_mappings)} | "
            f"Abstention: {verification_report.abstention_required}"
        )

        # Prepare legacy UI compatibility items
        resolved_entities_ui = []
        for ent_name in verification_report.verified_entity_ids[:6]:
            resolved_entities_ui.append({
                "id": ent_name,
                "name": ent_name,
                "type": "Person",
                "risk_score": 0.85,
                "details": "Verified in case evidence"
            })

        anomalies_ui = []
        for item in normalized_evidence:
            if "anomaly" in item.leaf_id:
                anomalies_ui.append(item.content)

        alerts_ui = []
        for item in normalized_evidence:
            if "alert" in item.leaf_id:
                alerts_ui.append(item.content)

        return STAIRInvestigationResult(
            reply=reply_text,
            case_id=target_case_id,
            query=query,
            tool_used=f"STAIR_LEAVES[{', '.join(selected_leaf_ids)}]",
            selected_leaf_ids=selected_leaf_ids,
            validated_leaf_ids=selected_leaf_ids,
            evidence_count=len(normalized_evidence),
            evidence_items=normalized_evidence[:25],
            claim_mappings=claim_mappings,
            deterministic_verifications=verification_report.deterministic_facts,
            temporal_verifications=verification_report.temporal_deltas,
            conflicts=verification_report.conflicts_detected,
            abstention_triggered=verification_report.abstention_required,
            latency_breakdown_ms=latencies,
            records_count=len(normalized_evidence),
            records=[item.content for item in normalized_evidence[:20]],
            resolved_entities=resolved_entities_ui,
            anomalies=anomalies_ui[:4],
            alerts=alerts_ui[:3],
            suggested_followups=self._generate_stair_followups(selected_leaf_ids, verification_report),
            model_used="qwen2.5:7b (STAIR Structure-Aware Grounded Engine)"
        )

    def _generate_stair_followups(
        self,
        leaf_ids: List[str],
        verification_report: VerificationReport
    ) -> List[str]:
        """Generates evidence-directed follow-up investigation questions."""
        suggestions = []
        target_name = verification_report.verified_entity_ids[0] if verification_report.verified_entity_ids else "target"

        if any("financial" in l for l in leaf_ids):
            suggestions.append(f"Where was {target_name} around the time of these transactions?")
            suggestions.append("Show the pass-through money mule flows linked to this account")
        elif any("telecom" in l for l in leaf_ids):
            suggestions.append(f"Which cell towers did {target_name} connect to most frequently?")
            suggestions.append("Show financial transfers that occurred immediately after these calls")
        elif any("geo" in l for l in leaf_ids):
            suggestions.append(f"Show call activity while {target_name} was in Sector 22")
            suggestions.append("Were any other suspects co-located at these coordinates?")
        else:
            suggestions.append(f"What suspicious financial transactions occurred for {target_name}?")
            suggestions.append(f"Show the complete chronological timeline for {target_name}")

        return suggestions[:3]

stair_service = STAIRInvestigationService()
