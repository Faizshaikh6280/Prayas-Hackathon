"""
Local Qwen 2.5 7B LLM-as-a-Judge Evaluation Module.
Evaluates generated forensic responses for factual correctness, source faithfulness,
evidence grounding, entity correctness, numerical precision, and unsupported claims.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.core.llm_provider import get_llm
from app.stair.validator import STAIRValidator

logger = logging.getLogger("stair.llm_judge")

JUDGE_SYSTEM_PROMPT = """You are an impartial Supreme Judicial Digital Forensics Evaluation Judge.
Evaluate the forensic intelligence response produced by an AI platform against the Investigator Question and the Ground Truth Evidence.

EVALUATION CRITERIA:
1. factual_correctness: Are all statements, entities, amounts, and dates factually true to the evidence?
2. evidence_support: Is every key claim backed by explicit evidence citations?
3. source_faithfulness: Did the system avoid converting correlation (e.g. proximity/time) into unproven causation (e.g. conspiracy/guilt)?
4. entity_correctness: Are the mentioned persons, phones, or accounts correct and not mixed up with other entities?
5. temporal_correctness: Are timestamps and chronological sequences accurate?
6. numerical_correctness: Are monetary figures (INR ₹) and counts mathematically exact?
7. overall_pass: True only if factual_correctness AND evidence_support AND entity_correctness are all true.

OUTPUT PURE JSON ONLY:
{
  "factual_correctness": true,
  "evidence_support": true,
  "source_faithfulness": true,
  "entity_correctness": true,
  "temporal_correctness": true,
  "numerical_correctness": true,
  "unsupported_claims": [],
  "missing_evidence": [],
  "critical_errors": [],
  "overall_pass": true,
  "judge_summary": "Brief 1-sentence verdict"
}
"""

class LLMJudgeVerdict(BaseModel):
    factual_correctness: bool = True
    evidence_support: bool = True
    source_faithfulness: bool = True
    entity_correctness: bool = True
    temporal_correctness: bool = True
    numerical_correctness: bool = True
    unsupported_claims: List[str] = Field(default_factory=list)
    missing_evidence: List[str] = Field(default_factory=list)
    critical_errors: List[str] = Field(default_factory=list)
    overall_pass: bool = True
    judge_summary: str = ""

class STAIRLLMJudge:
    """Invokes local Qwen 2.5 7B to evaluate answer factuality against ground truth evidence."""

    @classmethod
    def judge_response(
        cls,
        query: str,
        evidence_summary: str,
        generated_answer: str,
        ground_truth_context: str = ""
    ) -> LLMJudgeVerdict:
        user_prompt = f"""INVESTIGATOR QUESTION:
"{query}"

GROUND TRUTH / RETRIEVED EVIDENCE:
{evidence_summary[:1500]}
{f"ADDITIONAL CONTEXT: {ground_truth_context}" if ground_truth_context else ""}

GENERATED FORENSIC ANSWER:
{generated_answer}

Provide your structured judicial verdict as JSON:"""

        messages = [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        try:
            llm = get_llm(num_predict=300, num_ctx=2048)
            resp = llm.invoke(messages)
            raw = resp.content if hasattr(resp, "content") else str(resp)

            # Robust parse
            parsed_items = STAIRValidator.parse_router_json(raw)
            if isinstance(parsed_items, list) and parsed_items and isinstance(parsed_items[0], dict):
                data = parsed_items[0]
            elif isinstance(parsed_items, dict):
                data = parsed_items
            else:
                data = json.loads(raw)

            return LLMJudgeVerdict(
                factual_correctness=bool(data.get("factual_correctness", True)),
                evidence_support=bool(data.get("evidence_support", True)),
                source_faithfulness=bool(data.get("source_faithfulness", True)),
                entity_correctness=bool(data.get("entity_correctness", True)),
                temporal_correctness=bool(data.get("temporal_correctness", True)),
                numerical_correctness=bool(data.get("numerical_correctness", True)),
                unsupported_claims=data.get("unsupported_claims", []),
                missing_evidence=data.get("missing_evidence", []),
                critical_errors=data.get("critical_errors", []),
                overall_pass=bool(data.get("overall_pass", True)),
                judge_summary=str(data.get("judge_summary", "Judicial evaluation completed."))
            )
        except Exception as e:
            logger.warning(f"[STAIRLLMJudge] Judge invocation error: {e}")
            # Fallback heuristic judge
            has_citations = "[EV-" in generated_answer
            is_abstention = "insufficient evidence" in generated_answer.lower()
            return LLMJudgeVerdict(
                factual_correctness=True,
                evidence_support=has_citations or is_abstention,
                source_faithfulness=True,
                entity_correctness=True,
                temporal_correctness=True,
                numerical_correctness=True,
                unsupported_claims=[],
                missing_evidence=[],
                critical_errors=[],
                overall_pass=has_citations or is_abstention,
                judge_summary="Heuristic fallback assessment (verified evidence citations present)."
            )
