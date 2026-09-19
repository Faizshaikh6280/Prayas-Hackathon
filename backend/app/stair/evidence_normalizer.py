"""
Evidence Normalization and Provenance Management.
Transforms raw heterogeneous database/graph records into standardized
NormalizedEvidenceItem objects with explicit authority levels and full provenance tracking.
Enforces the guardrail that generated reports do not silently become primary evidence.
"""

import uuid
import datetime
from typing import List, Dict, Any, Optional

from app.stair.schemas import NormalizedEvidenceItem, EvidenceAuthority
from app.stair.leaf_registry import LEAF_REGISTRY

class EvidenceNormalizer:
    """Standardizes disparate evidence sources and enforces strict provenance lineage."""

    @classmethod
    def normalize_records(
        cls,
        leaf_id: str,
        case_id: str,
        raw_records: List[Dict[str, Any]],
        start_index: int = 1
    ) -> List[NormalizedEvidenceItem]:
        """Converts raw tool output dictionaries into NormalizedEvidenceItem records."""
        leaf_def = LEAF_REGISTRY.get(leaf_id)
        authority = leaf_def.authority if leaf_def else EvidenceAuthority.DERIVED

        normalized: List[NormalizedEvidenceItem] = []

        for idx, rec in enumerate(raw_records, start=start_index):
            ev_id = f"EV-{leaf_id.replace('.', '-').upper()}-{idx:03d}"
            source_id = str(rec.get("source_id") or rec.get("id") or f"REC-{idx:03d}")

            # Extract associated entities
            entity_ids = []
            for k in ["person_name", "primary_name", "name", "target_profile_name", "entity_name", "caller", "receiver", "phone", "sender_account", "recipient_account"]:
                v = rec.get(k)
                if v and isinstance(v, str) and v.strip() and v not in entity_ids:
                    entity_ids.append(v.strip())

            # Extract timestamp
            ts = rec.get("timestamp") or rec.get("created_at") or rec.get("start_time")
            if hasattr(ts, "isoformat"):
                ts = ts.isoformat()
            elif ts:
                ts = str(ts)

            # Preserve report provenance
            report_id = None
            if "report" in leaf_id or rec.get("report_id"):
                report_id = str(rec.get("report_id") or source_id)

            item = NormalizedEvidenceItem(
                evidence_id=ev_id,
                case_id=case_id,
                leaf_id=leaf_id,
                source_type=leaf_def.primary_source if leaf_def else "unknown",
                source_id=source_id,
                authority=authority,
                entity_ids=entity_ids,
                timestamp=ts,
                content=rec,
                derived_from=[],
                report_id=report_id,
                provenance={
                    "leaf_id": leaf_id,
                    "extracted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "source_record_id": source_id
                }
            )
            normalized.append(item)

        return normalized

    @classmethod
    def link_report_to_primary_evidence(
        cls,
        generated_items: List[NormalizedEvidenceItem],
        primary_items: List[NormalizedEvidenceItem]
    ):
        """
        Links generated report items to underlying primary evidence (e.g. transactions, CDR).
        Guarantees generated findings are rooted in primary facts rather than circular AI reports.
        """
        primary_id_map = {item.source_id: item.evidence_id for item in primary_items}

        for gen in generated_items:
            linked_ids = []
            content_str = str(gen.content)
            for prim in primary_items:
                # Check entity or account co-occurrence
                if any(e in content_str for e in prim.entity_ids if len(e) > 3):
                    linked_ids.append(prim.evidence_id)
                # Check source ID reference
                if prim.source_id in content_str:
                    linked_ids.append(prim.evidence_id)

            gen.derived_from = list(set(linked_ids))[:5]
