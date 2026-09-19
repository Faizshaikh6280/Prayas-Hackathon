"""
Pydantic Schemas and Data Models for STAIR-Style Structure-Aware Retrieval
and Evidence-First Investigation Architecture.
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
import datetime

def utcnow_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

class EvidenceAuthority(str, Enum):
    """
    Evidence hierarchy:
    PRIMARY: Direct observational records (bank transactions, CDR, IPDR, cell tower pings, raw files).
    DERIVED: Algorithmic computations, anomalies, GDS metrics, spatial clusters, entity resolutions.
    GENERATED: AI-generated summaries, lead dossiers, LLM narratives. Never silently treated as primary.
    """
    PRIMARY = "PRIMARY"
    DERIVED = "DERIVED"
    GENERATED = "GENERATED"

class LeafParameterRequirement(BaseModel):
    name: str
    param_type: str = "string"
    required: bool = False
    description: str = ""

class LeafDefinition(BaseModel):
    """Immutable investigation leaf node specification."""
    leaf_id: str
    domain: str
    name: str
    description: str
    authority: EvidenceAuthority
    primary_source: str
    handler_method: str
    parameters: List[LeafParameterRequirement] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)

class SelectedLeaf(BaseModel):
    leaf_id: str
    reason: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0

class STAIRRoutingOutput(BaseModel):
    query: str
    case_id: str
    selected_leaves: List[SelectedLeaf] = Field(default_factory=list)
    rejected_leaves: List[str] = Field(default_factory=list)
    is_multi_source: bool = False
    routing_latency_ms: float = 0.0
    router_mode: str = "qwen_toc"  # "qwen_toc", "deterministic_hybrid", "fallback"

class NormalizedEvidenceItem(BaseModel):
    """
    Universal forensic evidence record preserving strict provenance and lineage.
    """
    evidence_id: str
    case_id: str
    leaf_id: str
    source_type: str                    # e.g. canonical_transaction, cdr_record, golden_profile
    source_id: str                      # primary record key in DB or warehouse
    authority: EvidenceAuthority        # PRIMARY, DERIVED, GENERATED
    entity_ids: List[str] = Field(default_factory=list)
    timestamp: Optional[str] = None
    content: Dict[str, Any] = Field(default_factory=dict)
    derived_from: List[str] = Field(default_factory=list)  # underlying primary evidence IDs if DERIVED/GENERATED
    report_id: Optional[str] = None
    provenance: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=utcnow_iso)

class DeterministicFactCheck(BaseModel):
    metric_name: str
    computed_value: Union[float, int, str, None]
    unit: Optional[str] = None
    record_count: int = 0
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    is_exact: bool = True

class TemporalDeltaCheck(BaseModel):
    event_a_id: str
    event_b_id: str
    event_a_time: str
    event_b_time: str
    delta_seconds: float
    description: str

class EvidenceConflict(BaseModel):
    conflict_type: str
    description: str
    source_a_id: str
    source_a_value: Any
    source_b_id: str
    source_b_value: Any

class VerificationReport(BaseModel):
    case_id: str
    deterministic_facts: List[DeterministicFactCheck] = Field(default_factory=list)
    temporal_deltas: List[TemporalDeltaCheck] = Field(default_factory=list)
    conflicts_detected: List[EvidenceConflict] = Field(default_factory=list)
    abstention_required: bool = False
    abstention_reason: Optional[str] = None
    verified_entity_ids: List[str] = Field(default_factory=list)

class ClaimEvidenceMap(BaseModel):
    claim_id: str
    claim_text: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    is_supported: bool = True
    authority_level: EvidenceAuthority = EvidenceAuthority.PRIMARY
    verification_note: str = ""

class STAIRInvestigationResult(BaseModel):
    """Complete end-to-end response contract returned by the STAIR investigation engine."""
    reply: str
    case_id: str
    query: str
    tool_used: str = "STAIR_EVIDENCE_BROKER"
    selected_leaf_ids: List[str] = Field(default_factory=list)
    validated_leaf_ids: List[str] = Field(default_factory=list)
    evidence_count: int = 0
    evidence_items: List[NormalizedEvidenceItem] = Field(default_factory=list)
    claim_mappings: List[ClaimEvidenceMap] = Field(default_factory=list)
    deterministic_verifications: List[DeterministicFactCheck] = Field(default_factory=list)
    temporal_verifications: List[TemporalDeltaCheck] = Field(default_factory=list)
    conflicts: List[EvidenceConflict] = Field(default_factory=list)
    abstention_triggered: bool = False
    latency_breakdown_ms: Dict[str, float] = Field(default_factory=dict)
    
    # Backward compatibility fields for legacy frontend
    generated_cypher: Optional[str] = None
    sql_query: Optional[str] = None
    records_count: int = 0
    records: List[Dict[str, Any]] = Field(default_factory=list)
    resolved_entities: List[Dict[str, Any]] = Field(default_factory=list)
    anomalies: List[Dict[str, Any]] = Field(default_factory=list)
    alerts: List[Dict[str, Any]] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    model_used: str = "qwen2.5:7b (STAIR Structure-Aware Grounded Engine)"
