"""
Hard Output Validation & Guardrail Verification for STAIR Router.
Ensures zero hallucinated leaf IDs, tools, or sources can ever reach execution.
Strictly validates case scoping and sanitizes extracted parameters.
"""

import json
import re
import logging
from typing import List, Dict, Any, Tuple, Optional
from app.stair.schemas import SelectedLeaf, STAIRRoutingOutput
from app.stair.leaf_registry import LeafCatalog, LEAF_REGISTRY

logger = logging.getLogger("stair.validator")

class STAIRValidator:
    """Hard-validation gatekeeper between the LLM router and the Evidence Broker."""

    @classmethod
    def parse_router_json(cls, raw_output: str) -> List[Dict[str, Any]]:
        """Robustly parses JSON array of leaf selections from raw LLM text."""
        if not raw_output:
            return []

        cleaned = raw_output.strip()

        # 1. Strip markdown fences if present
        fence_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned)
        if fence_match:
            cleaned = fence_match.group(1).strip()

        # 2. Try standard json.loads
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                return parsed
            if isinstance(parsed, dict):
                # Might be wrapped in {"leaves": [...]} or {"selected_leaves": [...]}
                for key in ["selected_leaves", "leaves", "results", "selection"]:
                    if key in parsed and isinstance(parsed[key], list):
                        return parsed[key]
                # Or single leaf object
                if "leaf_id" in parsed:
                    return [parsed]
        except Exception:
            pass

        # 3. Extract outermost array brackets [...]
        first_bracket = cleaned.find('[')
        last_bracket = cleaned.rfind(']')
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            candidate = cleaned[first_bracket:last_bracket + 1]
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass

        # 4. Use json_repair library
        try:
            from json_repair import repair_json
            repaired = repair_json(cleaned, return_objects=True)
            if isinstance(repaired, list):
                return repaired
            if isinstance(repaired, dict):
                for key in ["selected_leaves", "leaves", "results", "selection"]:
                    if key in repaired and isinstance(repaired[key], list):
                        return repaired[key]
                if "leaf_id" in repaired:
                    return [repaired]
        except Exception as e:
            logger.warning(f"[STAIRValidator] json_repair error: {e}")

        # 5. Regex extraction of leaf IDs as last resort
        found_leaves = []
        leaf_matches = re.findall(r'([a-z_]+\.[a-z_]+)', cleaned)
        for lm in leaf_matches:
            if LeafCatalog.is_valid_leaf_id(lm):
                found_leaves.append({"leaf_id": lm, "reason": "Extracted via token scan", "parameters": {}})

        return found_leaves

    @classmethod
    def sanitize_parameter_value(cls, val: Any) -> Any:
        """Sanitizes user/LLM input values to prevent injection and memory issues."""
        if isinstance(val, str):
            # Strip dangerous SQL / Cypher / shell mutation tokens
            forbidden_substrings = [
                "DROP TABLE", "DELETE FROM", "UPDATE ", "INSERT INTO",
                "DETACH DELETE", "CREATE (", "CALL DBMS", "LOAD CSV",
                ";--", "/*", "*/"
            ]
            upper_val = val.upper()
            for forb in forbidden_substrings:
                if forb in upper_val:
                    logger.warning(f"[STAIRValidator] Sanitizing suspicious parameter value: {val}")
                    return ""
            return val[:200].strip()
        elif isinstance(val, (int, float, bool)):
            return val
        elif isinstance(val, list):
            return [cls.sanitize_parameter_value(x) for x in val[:20]]
        elif isinstance(val, dict):
            return {str(k)[:50]: cls.sanitize_parameter_value(v) for k, v in list(val.items())[:20]}
        return str(val)[:200]

    @classmethod
    def validate_and_filter_selections(
        cls,
        raw_items: List[Dict[str, Any]],
        case_id: str
    ) -> Tuple[List[SelectedLeaf], List[str]]:
        """
        Validates parsed leaf entries against the immutable LeafCatalog.
        Rejects nonexistent or hallucinated leaf IDs.
        Enforces case scoping and parameter sanitization.
        """
        validated_leaves: List[SelectedLeaf] = []
        rejected_leaves: List[str] = []
        seen_leaf_ids = set()

        for item in raw_items:
            leaf_id = None
            if isinstance(item, str):
                leaf_id = item.strip().lower()
                reason = "Direct string selection"
                params = {}
            elif isinstance(item, dict):
                leaf_id = str(item.get("leaf_id", "")).strip().lower()
                reason = str(item.get("reason", "Selected by router")).strip()
                params = item.get("parameters", {}) or {}
            else:
                continue

            if not leaf_id:
                continue

            # Hard Check: Leaf ID MUST exist in the immutable registry
            if not LeafCatalog.is_valid_leaf_id(leaf_id):
                logger.warning(f"[STAIRValidator] REJECTING hallucinated/invalid leaf ID: '{leaf_id}'")
                rejected_leaves.append(leaf_id)
                continue

            # Deduplicate selections
            if leaf_id in seen_leaf_ids:
                continue
            seen_leaf_ids.add(leaf_id)

            # Sanitize parameters and enforce case isolation
            sanitized_params = {
                "case_id": case_id
            }
            if isinstance(params, dict):
                for k, v in params.items():
                    if k != "case_id":
                        sanitized_params[str(k).strip()] = cls.sanitize_parameter_value(v)

            validated_leaves.append(
                SelectedLeaf(
                    leaf_id=leaf_id,
                    reason=reason,
                    parameters=sanitized_params,
                    confidence=1.0
                )
            )

        # Safety: Cap total leaves at 5 to enforce context minimization and avoid runaway queries
        if len(validated_leaves) > 5:
            logger.info(f"[STAIRValidator] Capping {len(validated_leaves)} leaves to top 5.")
            validated_leaves = validated_leaves[:5]

        return validated_leaves, rejected_leaves
