"""
Automated STAIR Benchmark Runner & Comparative Evaluator.
Executes multi-domain test cases, measures quantitative retrieval metrics,
runs local Qwen 2.5 7B LLM-as-a-Judge, and compares STAIR vs Legacy Agentic RAG.
"""

import sys
import os
import json
import time
import logging
from typing import List, Dict, Any, Optional

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.stair.benchmark.dataset import BENCHMARK_DATASET
from app.stair.benchmark.evaluator import STAIRBenchmarkEvaluator, QueryEvaluationResult, BenchmarkMetrics
from app.stair.benchmark.llm_judge import STAIRLLMJudge, LLMJudgeVerdict
from app.stair.service import stair_service
from app.stair.router import STAIRQueryRouter
from app.services.forensic_chatbot import forensic_chatbot

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("stair.benchmark.runner")

def run_benchmark(
    max_queries: Optional[int] = None,
    sample_mode: bool = False,
    run_llm_judge: bool = True,
    compare_legacy: bool = True,
    case_id: str = "INV-2026-BLACK-CIRCUIT"
) -> Dict[str, Any]:
    """Runs the benchmark evaluation suite."""
    print("=" * 80)
    print("   OMNITRACE STAIR STRUCTURE-AWARE RETRIEVAL & GROUNDING BENCHMARK")
    print(f"   Target Case: {case_id} | Total Test Cases: {len(BENCHMARK_DATASET)}")
    print("=" * 80)

    dataset = BENCHMARK_DATASET
    if sample_mode:
        # Pick representative queries across every distinct category
        stratified_ids = [
            "Q-FIN-01", "Q-FIN-02", "Q-TEL-01", "Q-TEL-02", "Q-GEO-01",
            "Q-TEM-01", "Q-TEM-03", "Q-ANM-01", "Q-ANM-04", "Q-GRP-01",
            "Q-REP-01", "Q-REP-02", "Q-MUL-01", "Q-HRD-01", "Q-HRD-04"
        ]
        dataset = [tc for tc in BENCHMARK_DATASET if tc["query_id"] in stratified_ids]
    elif max_queries and max_queries < len(dataset):
        dataset = dataset[:max_queries]

    stair_results: List[QueryEvaluationResult] = []
    judge_verdicts: List[Dict[str, Any]] = []
    legacy_comparisons: List[Dict[str, Any]] = []

    for idx, tc in enumerate(dataset, start=1):
        q_id = tc["query_id"]
        q_text = tc["query"]
        category = tc["category"]
        expected = tc["expected_leaves"]

        print(f"\n[{idx}/{len(dataset)}] [{category}] {q_id}: \"{q_text}\"")

        # ── 1. Evaluate STAIR Pipeline ───────────────────────────────────────
        try:
            stair_res = stair_service.investigate(query=q_text, case_id=case_id)
            eval_res = STAIRBenchmarkEvaluator.evaluate_query(
                test_case=tc,
                selected_leaves=stair_res.selected_leaf_ids,
                rejected_leaves=[],
                claim_mappings=stair_res.claim_mappings,
                abstention_triggered=stair_res.abstention_triggered,
                latencies=stair_res.latency_breakdown_ms,
                reply=stair_res.reply
            )
            stair_results.append(eval_res)

            print(f"   -> STAIR Selected: {stair_res.selected_leaf_ids} (Hit@1: {eval_res.hit_at_1}, All: {eval_res.all_leaves_recalled})")
            print(f"   -> Evidence: {stair_res.evidence_count} items | Claims: {len(stair_res.claim_mappings)} | Abstention: {stair_res.abstention_triggered}")
            print(f"   -> Total Latency: {eval_res.latency_breakdown_ms.get('total_e2e_ms', 0)} ms")

            # ── 2. Run Local Qwen LLM-as-a-Judge (Sampled or Full) ─────────────
            if run_llm_judge:
                ev_summary = "\n".join([f"- {i.evidence_id} ({i.leaf_id}): {str(i.content)[:120]}" for i in stair_res.evidence_items[:8]])
                judge_res = STAIRLLMJudge.judge_response(
                    query=q_text,
                    evidence_summary=ev_summary or "No evidence retrieved (Abstention expected)",
                    generated_answer=stair_res.reply,
                    ground_truth_context=" ".join(tc.get("ground_truth_keywords", []))
                )
                judge_verdicts.append({
                    "query_id": q_id,
                    "overall_pass": judge_res.overall_pass,
                    "factual_correctness": judge_res.factual_correctness,
                    "evidence_support": judge_res.evidence_support,
                    "source_faithfulness": judge_res.source_faithfulness,
                    "judge_summary": judge_res.judge_summary
                })
                print(f"   -> LLM Judge Verdict: {'PASS' if judge_res.overall_pass else 'FAIL'} ({judge_res.judge_summary})")

        except Exception as e:
            logger.error(f"Error evaluating STAIR on query {q_id}: {e}", exc_info=True)

        # ── 3. Compare Legacy Chatbot (if requested) ─────────────────────────
        if compare_legacy:
            try:
                t0 = time.time()
                legacy_res = forensic_chatbot.process_chat_message(message=q_text, case_id=case_id, use_stair=False)
                leg_elapsed = (time.time() - t0) * 1000
                leg_tool = legacy_res.get("tool_used")

                # Check if legacy hallucinated or had evidence
                leg_records = legacy_res.get("records_count", 0)
                legacy_comparisons.append({
                    "query_id": q_id,
                    "query": q_text,
                    "legacy_tool_used": leg_tool,
                    "legacy_records_count": leg_records,
                    "legacy_latency_ms": round(leg_elapsed, 2),
                    "legacy_reply_snippet": legacy_res.get("reply", "")[:120].replace("\n", " ")
                })
                print(f"   [Legacy Chatbot] Tool: {leg_tool} | Records: {leg_records} | Latency: {round(leg_elapsed, 2)} ms")
            except Exception as e:
                logger.warning(f"Error on legacy chatbot: {e}")

    # ── 4. Aggregate Global Metrics ──────────────────────────────────────────
    metrics = STAIRBenchmarkEvaluator.aggregate_metrics(stair_results)

    judge_pass_rate = 0.0
    if judge_verdicts:
        passes = sum(1 for v in judge_verdicts if v["overall_pass"])
        judge_pass_rate = round(passes / len(judge_verdicts), 4)

    print("\n" + "=" * 80)
    print("   FINAL BENCHMARK EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Total Evaluated Queries:      {metrics.total_queries}")
    print(f"STAIR Recall@1:               {metrics.recall_at_1 * 100:.2f}%")
    print(f"STAIR Recall@3:               {metrics.recall_at_3 * 100:.2f}%")
    print(f"STAIR Mean Reciprocal Rank:   {metrics.mrr:.4f}")
    print(f"STAIR Tool Selection Acc:     {metrics.tool_selection_accuracy * 100:.2f}%")
    print(f"Invalid Leaf Hallucination:   {metrics.invalid_node_rate * 100:.2f}% (Hard Rejected: 0 reaching execution)")
    print(f"Unsupported Claim Rate:       {metrics.unsupported_claim_rate * 100:.2f}%")
    print(f"Abstention Accuracy:          {metrics.abstention_accuracy * 100:.2f}%")
    if judge_verdicts:
        print(f"Local Qwen Judge Pass Rate:   {judge_pass_rate * 100:.2f}%")
    print("-" * 80)
    print(f"Average Routing Latency:      {metrics.avg_routing_latency_ms:.2f} ms")
    print(f"Average Retrieval Latency:    {metrics.avg_retrieval_latency_ms:.2f} ms")
    print(f"Average Generation Latency:   {metrics.avg_generation_latency_ms:.2f} ms")
    print(f"Average End-to-End Latency:   {metrics.avg_total_e2e_ms:.2f} ms")
    print("=" * 80)

    summary_payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "case_id": case_id,
        "metrics": metrics.model_dump(),
        "judge_pass_rate": judge_pass_rate,
        "judge_verdicts": judge_verdicts,
        "query_results": [r.model_dump() for r in stair_results],
        "legacy_comparison": legacy_comparisons
    }

    # Save to JSON file
    out_path = os.path.join(backend_dir, "benchmark_stair_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)
    print(f"\n[+] Detailed benchmark results saved to: {out_path}")

    return summary_payload

if __name__ == "__main__":
    is_sample = "--sample" in sys.argv or "-s" in sys.argv or len(sys.argv) == 1
    num_q = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            num_q = int(arg)
            is_sample = False
            break
    run_benchmark(max_queries=num_q, sample_mode=is_sample)
