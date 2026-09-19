"""
Quantitative Benchmark Evaluator for STAIR Architecture.
Computes Recall@1, Recall@3, MRR, Invalid-Node Rate, Tool Selection Accuracy,
Unsupported Claim Rate, and Latency Profiles.
"""

import math
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class BenchmarkMetrics(BaseModel):
    total_queries: int = 0
    recall_at_1: float = 0.0
    recall_at_3: float = 0.0
    mrr: float = 0.0
    invalid_node_rate: float = 0.0
    tool_selection_accuracy: float = 0.0
    unsupported_claim_rate: float = 0.0
    abstention_accuracy: float = 0.0
    avg_routing_latency_ms: float = 0.0
    avg_retrieval_latency_ms: float = 0.0
    avg_generation_latency_ms: float = 0.0
    avg_total_e2e_ms: float = 0.0

class QueryEvaluationResult(BaseModel):
    query_id: str
    query: str
    category: str
    expected_leaves: List[str]
    selected_leaves: List[str]
    rejected_leaves: List[str] = Field(default_factory=list)
    hit_at_1: bool = False
    hit_at_3: bool = False
    reciprocal_rank: float = 0.0
    all_leaves_recalled: bool = False
    has_invalid_node: bool = False
    claims_count: int = 0
    unsupported_claims_count: int = 0
    abstention_expected: bool = False
    abstention_triggered: bool = False
    latency_breakdown_ms: Dict[str, float] = Field(default_factory=dict)
    reply_snippet: str = ""

class STAIRBenchmarkEvaluator:
    """Evaluates STAIR query routing and evidence-first responses against ground truth."""

    @classmethod
    def evaluate_query(
        cls,
        test_case: Dict[str, Any],
        selected_leaves: List[str],
        rejected_leaves: List[str],
        claim_mappings: List[Any],
        abstention_triggered: bool,
        latencies: Dict[str, float],
        reply: str
    ) -> QueryEvaluationResult:
        expected = [e.lower().strip() for e in test_case.get("expected_leaves", [])]
        selected = [s.lower().strip() for s in selected_leaves]

        # 1. Recall@1
        hit_1 = False
        if selected and expected and selected[0] in expected:
            hit_1 = True

        # 2. Recall@3
        hit_3 = False
        for s in selected[:3]:
            if s in expected:
                hit_3 = True
                break

        # 3. Reciprocal Rank
        rr = 0.0
        for rank_idx, s in enumerate(selected, start=1):
            if s in expected:
                rr = 1.0 / rank_idx
                break

        # 4. All leaves recalled (Tool selection accuracy)
        all_recalled = False
        if expected:
            all_recalled = all(e in selected for e in expected)

        # 5. Invalid node check
        has_invalid = len(rejected_leaves) > 0

        # 6. Claims analysis
        total_claims = len(claim_mappings)
        unsupported = sum(1 for c in claim_mappings if not getattr(c, "is_supported", True))

        # 7. Abstention check
        expected_abstention = test_case.get("expected_abstention", False)

        return QueryEvaluationResult(
            query_id=test_case.get("query_id", ""),
            query=test_case.get("query", ""),
            category=test_case.get("category", ""),
            expected_leaves=expected,
            selected_leaves=selected,
            rejected_leaves=rejected_leaves,
            hit_at_1=hit_1,
            hit_at_3=hit_3,
            reciprocal_rank=rr,
            all_leaves_recalled=all_recalled,
            has_invalid_node=has_invalid,
            claims_count=total_claims,
            unsupported_claims_count=unsupported,
            abstention_expected=expected_abstention,
            abstention_triggered=abstention_triggered,
            latency_breakdown_ms=latencies,
            reply_snippet=reply[:120].replace("\n", " ")
        )

    @classmethod
    def aggregate_metrics(cls, results: List[QueryEvaluationResult]) -> BenchmarkMetrics:
        """Calculates global benchmark metrics across all evaluated queries."""
        if not results:
            return BenchmarkMetrics()

        n = len(results)
        r1_sum = sum(1 for r in results if r.hit_at_1)
        r3_sum = sum(1 for r in results if r.hit_at_3)
        mrr_sum = sum(r.reciprocal_rank for r in results)
        tool_acc_sum = sum(1 for r in results if r.all_leaves_recalled)
        invalid_sum = sum(1 for r in results if r.has_invalid_node)

        total_claims = sum(r.claims_count for r in results)
        total_unsupported = sum(r.unsupported_claims_count for r in results)
        unsupported_rate = (total_unsupported / total_claims) if total_claims > 0 else 0.0

        # Abstention accuracy
        abstention_cases = [r for r in results if r.abstention_expected]
        abstention_hits = sum(1 for r in abstention_cases if r.abstention_triggered)
        abstention_acc = (abstention_hits / len(abstention_cases)) if abstention_cases else 1.0

        # Latencies
        avg_routing = sum(r.latency_breakdown_ms.get("routing_ms", 0.0) for r in results) / n
        avg_retrieval = sum(r.latency_breakdown_ms.get("retrieval_ms", 0.0) for r in results) / n
        avg_generation = sum(r.latency_breakdown_ms.get("generation_ms", 0.0) for r in results) / n
        avg_e2e = sum(r.latency_breakdown_ms.get("total_e2e_ms", 0.0) for r in results) / n

        return BenchmarkMetrics(
            total_queries=n,
            recall_at_1=round(r1_sum / n, 4),
            recall_at_3=round(r3_sum / n, 4),
            mrr=round(mrr_sum / n, 4),
            invalid_node_rate=round(invalid_sum / n, 4),
            tool_selection_accuracy=round(tool_acc_sum / n, 4),
            unsupported_claim_rate=round(unsupported_rate, 4),
            abstention_accuracy=round(abstention_acc, 4),
            avg_routing_latency_ms=round(avg_routing, 2),
            avg_retrieval_latency_ms=round(avg_retrieval, 2),
            avg_generation_latency_ms=round(avg_generation, 2),
            avg_total_e2e_ms=round(avg_e2e, 2)
        )
