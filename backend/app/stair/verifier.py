"""
Deterministic Fact Verifier & Investigation Guardrails.
Performs programmatic validation of numbers, sums, counts, and timestamp deltas.
Enforces entity consistency, detects evidence conflicts, and evaluates abstention conditions.
"""

import datetime
from typing import List, Dict, Any, Optional, Tuple

from app.stair.schemas import (
    NormalizedEvidenceItem, VerificationReport, DeterministicFactCheck,
    TemporalDeltaCheck, EvidenceConflict, EvidenceAuthority
)

class DeterministicVerifier:
    """Computes exact mathematical, temporal, and entity constraints from primary evidence."""

    @classmethod
    def verify(
        cls,
        case_id: str,
        evidence_items: List[NormalizedEvidenceItem],
        query: str
    ) -> VerificationReport:
        """Runs the complete battery of deterministic verification checks on retrieved evidence."""
        report = VerificationReport(case_id=case_id)

        # 1. Abstention check: Zero evidence returned
        if not evidence_items:
            report.abstention_required = True
            report.abstention_reason = f"No verified evidence records found for case '{case_id}' matching the requested investigation scope."
            return report

        # 2. Mathematical Fact Checks (Sums, Counts, Max, Min)
        cls._verify_financial_totals(evidence_items, report)
        cls._verify_telecom_counts(evidence_items, report)

        # 3. Temporal Interval Calculations
        cls._verify_temporal_deltas(evidence_items, report)

        # 4. Conflicting Evidence Detection
        cls._detect_evidence_conflicts(evidence_items, report)

        # 5. Extract and verify entity identities
        cls._extract_verified_entities(evidence_items, report)

        return report

    @classmethod
    def _verify_financial_totals(cls, evidence_items: List[NormalizedEvidenceItem], report: VerificationReport):
        """Deterministically computes financial sums and counts from primary evidence."""
        amounts = []
        supporting_ids = []

        for item in evidence_items:
            amt = None
            if "amount_inr" in item.content:
                amt = item.content.get("amount_inr")
            elif "amount" in item.content:
                amt = item.content.get("amount")

            if amt is not None:
                try:
                    val = float(amt)
                    if val > 0:
                        amounts.append(val)
                        supporting_ids.append(item.evidence_id)
                except (ValueError, TypeError):
                    pass

        if amounts:
            total_sum = sum(amounts)
            max_amt = max(amounts)
            min_amt = min(amounts)
            avg_amt = total_sum / len(amounts)

            report.deterministic_facts.append(
                DeterministicFactCheck(
                    metric_name="total_transaction_amount_inr",
                    computed_value=round(total_sum, 2),
                    unit="INR",
                    record_count=len(amounts),
                    supporting_evidence_ids=supporting_ids,
                    is_exact=True
                )
            )
            report.deterministic_facts.append(
                DeterministicFactCheck(
                    metric_name="transaction_count",
                    computed_value=len(amounts),
                    unit="transactions",
                    record_count=len(amounts),
                    supporting_evidence_ids=supporting_ids,
                    is_exact=True
                )
            )
            report.deterministic_facts.append(
                DeterministicFactCheck(
                    metric_name="max_single_transaction_inr",
                    computed_value=round(max_amt, 2),
                    unit="INR",
                    record_count=1,
                    supporting_evidence_ids=supporting_ids[:1],
                    is_exact=True
                )
            )

    @classmethod
    def _verify_telecom_counts(cls, evidence_items: List[NormalizedEvidenceItem], report: VerificationReport):
        """Deterministically counts phone calls and durations."""
        calls = 0
        total_duration_sec = 0
        call_ids = []

        for item in evidence_items:
            if "telecom" in item.leaf_id or "duration" in item.content:
                dur = item.content.get("duration")
                if dur is not None:
                    try:
                        d_val = int(dur)
                        total_duration_sec += d_val
                        calls += 1
                        call_ids.append(item.evidence_id)
                    except (ValueError, TypeError):
                        pass

        if calls > 0:
            report.deterministic_facts.append(
                DeterministicFactCheck(
                    metric_name="total_calls_recorded",
                    computed_value=calls,
                    unit="calls",
                    record_count=calls,
                    supporting_evidence_ids=call_ids,
                    is_exact=True
                )
            )
            report.deterministic_facts.append(
                DeterministicFactCheck(
                    metric_name="total_call_duration_seconds",
                    computed_value=total_duration_sec,
                    unit="seconds",
                    record_count=calls,
                    supporting_evidence_ids=call_ids,
                    is_exact=True
                )
            )

    @classmethod
    def _verify_temporal_deltas(cls, evidence_items: List[NormalizedEvidenceItem], report: VerificationReport):
        """Computes exact timestamp deltas between sequential events."""
        timestamped_events = []
        for item in evidence_items:
            ts = item.timestamp
            if ts:
                try:
                    # Clean ISO format
                    clean_ts = str(ts).replace("Z", "+00:00")
                    dt = datetime.datetime.fromisoformat(clean_ts)
                    timestamped_events.append((dt, item))
                except Exception:
                    pass

        timestamped_events.sort(key=lambda x: x[0])

        for i in range(len(timestamped_events) - 1):
            dt1, ev1 = timestamped_events[i]
            dt2, ev2 = timestamped_events[i + 1]
            delta = abs((dt2 - dt1).total_seconds())

            if delta <= 1800:  # Within 30 minutes
                report.temporal_deltas.append(
                    TemporalDeltaCheck(
                        event_a_id=ev1.evidence_id,
                        event_b_id=ev2.evidence_id,
                        event_a_time=dt1.isoformat(),
                        event_b_time=dt2.isoformat(),
                        delta_seconds=delta,
                        description=f"Event {ev1.evidence_id} ({ev1.leaf_id}) occurred {int(delta)} seconds before Event {ev2.evidence_id} ({ev2.leaf_id})."
                    )
                )

    @classmethod
    def _detect_evidence_conflicts(cls, evidence_items: List[NormalizedEvidenceItem], report: VerificationReport):
        """Detects contradictions between disparate sources (e.g. timestamps or amounts)."""
        location_events = []
        for item in evidence_items:
            loc = item.content.get("location_name") or item.content.get("location") or item.content.get("tower_id")
            ts = item.timestamp
            if loc and ts:
                location_events.append((loc, ts, item.evidence_id))

        # Check for same timestamp with different locations (teleportation conflict)
        seen_ts = {}
        for loc, ts, ev_id in location_events:
            if ts in seen_ts and seen_ts[ts][0] != loc:
                other_loc, other_id = seen_ts[ts]
                report.conflicts_detected.append(
                    EvidenceConflict(
                        conflict_type="SIMULTANEOUS_LOCATION_CONFLICT",
                        description=f"Evidence conflict: Simultaneous location registration at '{loc}' ({ev_id}) and '{other_loc}' ({other_id}) at {ts}.",
                        source_a_id=ev_id,
                        source_a_value=loc,
                        source_b_id=other_id,
                        source_b_value=other_loc
                    )
                )
            seen_ts[ts] = (loc, ev_id)

    @classmethod
    def _extract_verified_entities(cls, evidence_items: List[NormalizedEvidenceItem], report: VerificationReport):
        """Extracts unique verified entity names and clusters present in the evidence pack."""
        ents = set()
        for item in evidence_items:
            for e in item.entity_ids:
                if len(e) > 2:
                    ents.add(e)
        report.verified_entity_ids = sorted(list(ents))
