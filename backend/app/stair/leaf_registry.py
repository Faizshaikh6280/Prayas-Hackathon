"""
Immutable Leaf Registry & Investigation Hierarchy (Table of Contents).
Represents the exact machine-readable investigation capabilities and report structures
derived from the OmniTrace platform codebase.
"""

from typing import Dict, List, Optional, Any
from app.stair.schemas import LeafDefinition, EvidenceAuthority, LeafParameterRequirement

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMMUTABLE LEAF REGISTRY DEFINITION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL_LEAF_DEFINITIONS: List[LeafDefinition] = [
    # ── 1. ENTITY INTELLIGENCE ───────────────────────────────────────────
    LeafDefinition(
        leaf_id="entity.golden_profile",
        domain="entity",
        name="Golden Entity Profile",
        description="Resolved master suspect identity from Zingg ML, including primary names, aliases, phones, bank accounts, emails, national IDs, and risk score.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:golden_profiles",
        handler_method="fetch_golden_profile",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Name or partial alias of the person"),
            LeafParameterRequirement(name="cluster_id", param_type="string", description="Zingg cluster identifier")
        ],
        keywords=["suspect", "profile", "identity", "alias", "who is", "who are", "cluster", "national id", "aadhaar", "pan"]
    ),
    LeafDefinition(
        leaf_id="entity.identity_discrepancy",
        domain="entity",
        name="Identity & Hardware Discrepancies",
        description="Mismatched subscriber details, unusual phone/IMEI swaps, or alias contradictions across telecom, KYC, and device registers.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings",
        handler_method="fetch_identity_discrepancies",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["discrepancy", "mismatch", "fake name", "alternate identity", "swapped phone", "alias variant"]
    ),
    LeafDefinition(
        leaf_id="entity.associated_network",
        domain="entity",
        name="Associated Entity Network",
        description="Directly associated persons, co-signers, family members, or immediate collaborators linked to an entity in the graph.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:Person",
        handler_method="fetch_associated_network",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["associates", "contacts", "family", "linked persons", "collaborators", "network members"]
    ),

    # ── 2. TELECOM INTELLIGENCE ──────────────────────────────────────────
    LeafDefinition(
        leaf_id="telecom.cdr_records",
        domain="telecom",
        name="Call Detail Records (CDR)",
        description="Observational cellular call records: caller, receiver, call duration, timestamp, and call frequency between subscribers.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:CALLED / warehouse:cdr",
        handler_method="fetch_cdr_records",
        parameters=[
            LeafParameterRequirement(name="phone_number", param_type="string", description="Phone number or MSISDN"),
            LeafParameterRequirement(name="entity_name", param_type="string", description="Person name associated with phone")
        ],
        keywords=["call", "cdr", "dialed", "received call", "call duration", "phone logs", "talk time"]
    ),
    LeafDefinition(
        leaf_id="telecom.ipdr_sessions",
        domain="telecom",
        name="IP Detail Records (IPDR)",
        description="Digital network and application data session logs: client IP, destination IP, port, duration, bytes transferred, and proxy/Telegram gateways.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:IPAddress / warehouse:ipdr",
        handler_method="fetch_ipdr_sessions",
        parameters=[
            LeafParameterRequirement(name="ip_address", param_type="string", description="Target IPv4 or subnet address"),
            LeafParameterRequirement(name="entity_name", param_type="string", description="Person name")
        ],
        keywords=["ip", "ipdr", "ip address", "session", "telegram", "proxy", "vpn", "destination ip", "port"]
    ),
    LeafDefinition(
        leaf_id="telecom.cell_tower_pings",
        domain="telecom",
        name="Cell Tower Telemetry & BTS Pings",
        description="Cellular antenna sector locks, base station IDs (BTS), tower locations, azimuths, and pings registered by handsets.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:PINGED_TOWER / warehouse:cdr",
        handler_method="fetch_cell_tower_pings",
        parameters=[
            LeafParameterRequirement(name="tower_id", param_type="string", description="Cell tower identifier"),
            LeafParameterRequirement(name="phone_number", param_type="string", description="Handset phone number")
        ],
        keywords=["tower", "cell tower", "bts", "sector", "antenna", "signal ping", "cell lock", "tower id"]
    ),
    LeafDefinition(
        leaf_id="telecom.imei_telemetry",
        domain="telecom",
        name="IMEI & Handset Telemetry",
        description="Physical handset device identifiers (15-digit IMEI), device manufacturer/model, and dual-SIM handset sharing.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:IMEI / warehouse:device_inventory",
        handler_method="fetch_imei_telemetry",
        parameters=[
            LeafParameterRequirement(name="imei", param_type="string", description="15-digit IMEI number"),
            LeafParameterRequirement(name="entity_name", param_type="string", description="Suspect name")
        ],
        keywords=["imei", "device", "handset", "hardware", "dual sim", "burner phone", "phone serial"]
    ),

    # ── 3. FINANCIAL INTELLIGENCE ────────────────────────────────────────
    LeafDefinition(
        leaf_id="financial.transactions",
        domain="financial",
        name="Canonical Bank Transactions",
        description="Observational ledger banking transactions: sender account, recipient account, amount in INR, channel (IMPS, RTGS, UPI, NEFT), and timestamp.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:TRANSACTED_WITH / warehouse:bank_statement",
        handler_method="fetch_financial_transactions",
        parameters=[
            LeafParameterRequirement(name="account_number", param_type="string", description="Specific bank account"),
            LeafParameterRequirement(name="entity_name", param_type="string", description="Account holder or sender/recipient name"),
            LeafParameterRequirement(name="min_amount", param_type="float", description="Minimum transfer amount threshold")
        ],
        keywords=["bank", "account", "transfer", "transaction", "amount", "money", "inr", "rupees", "payment", "imps", "neft", "rtgs", "upi"]
    ),
    LeafDefinition(
        leaf_id="financial.suspicious_transactions",
        domain="financial",
        name="Suspicious Financial Transactions",
        description="High-value, round-tripping, anomalous spikes, or structuring patterns flagged as suspicious by financial anomaly detectors.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings / neo4j",
        handler_method="fetch_suspicious_financial",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Person name"),
            LeafParameterRequirement(name="account_number", param_type="string", description="Bank account number")
        ],
        keywords=["suspicious transfer", "suspicious transaction", "unusual money", "structuring", "flagged transaction", "smurfing"]
    ),
    LeafDefinition(
        leaf_id="financial.mule_flows",
        domain="financial",
        name="Pass-Through Money Mule Flows",
        description="High-velocity pass-through accounts where large inflows are liquidated or dispersed within minutes to evade automated thresholds.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings / postgres:investigation_alerts",
        handler_method="fetch_mule_flows",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Person or account holder"),
            LeafParameterRequirement(name="account_number", param_type="string", description="Bank account")
        ],
        keywords=["mule", "pass through", "money mule", "rapid liquidation", "immediate outflow", "dispersion"]
    ),
    LeafDefinition(
        leaf_id="financial.cycle_analysis",
        domain="financial",
        name="Multi-Hop Financial Cycles & Hawala Conduits",
        description="Cyclic transaction paths where money returns to the originator or circulates through 3-5 intermediary accounts.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings / neo4j:path",
        handler_method="fetch_financial_cycles",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Person or account"),
            LeafParameterRequirement(name="min_hops", param_type="int", description="Minimum hops in cycle")
        ],
        keywords=["cycle", "circular transfer", "round trip", "financial loop", "hawala", "layering path"]
    ),

    # ── 4. GEOGRAPHICAL INTELLIGENCE ─────────────────────────────────────
    LeafDefinition(
        leaf_id="geo.location_history",
        domain="geo",
        name="Geographical Location History",
        description="Chronological spatial locations, addresses, cell tower sectors, and coordinates visited by a target device or individual.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="warehouse:geospatial / neo4j:CellTower",
        handler_method="fetch_location_history",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name"),
            LeafParameterRequirement(name="location_name", param_type="string", description="Specific locality or sector")
        ],
        keywords=["location", "where was", "visited", "address", "coordinates", "gps", "geographic", "place", "safehouse"]
    ),
    LeafDefinition(
        leaf_id="geo.movement_trajectory",
        domain="geo",
        name="Sequential Movement Trajectory",
        description="Ordered sequence of spatial hops and transit routes across sectors, cities, or jurisdictional corridors over time.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="geo_service:movement_engine",
        handler_method="fetch_movement_trajectory",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name"),
            LeafParameterRequirement(name="date", param_type="string", description="Specific date or day window")
        ],
        keywords=["trajectory", "route", "movement", "travel", "path", "transit", "moved from", "trip", "journey"]
    ),
    LeafDefinition(
        leaf_id="geo.colocation_nexus",
        domain="geo",
        name="Physical Co-Location Analysis",
        description="Episodes where two or more distinct target devices/persons were locked to the same cell tower or spatial perimeter within a narrow time window.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="geo_service:overlap_engine / postgres:investigation_alerts",
        handler_method="fetch_colocation_nexus",
        parameters=[
            LeafParameterRequirement(name="entity_a", param_type="string", description="First person or phone"),
            LeafParameterRequirement(name="entity_b", param_type="string", description="Second person or phone")
        ],
        keywords=["co-location", "together", "same place", "meeting", "spatial convergence", "same tower", "co-occurrence"]
    ),
    LeafDefinition(
        leaf_id="geo.spatial_jumps",
        domain="geo",
        name="Impossible Speed & Spatial Jump Anomalies",
        description="Consecutive location pings separated by distance requiring impossible physical velocity (>200 km/h), indicating proxy/VPN spoofing or multi-device sharing.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings:SPATIAL",
        handler_method="fetch_spatial_jumps",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["teleportation", "spatial jump", "impossible speed", "velocity anomaly", "fast transit", "impossible travel"]
    ),

    # ── 5. TEMPORAL INTELLIGENCE ─────────────────────────────────────────
    LeafDefinition(
        leaf_id="temporal.timeline_events",
        domain="temporal",
        name="Canonical Timeline Events",
        description="Chronologically sorted multi-domain canonical event stream with exact timestamps, source lineage, and verified actors.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="timeline_service:canonical_events",
        handler_method="fetch_timeline_events",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Person name"),
            LeafParameterRequirement(name="start_time", param_type="string", description="Start timestamp ISO"),
            LeafParameterRequirement(name="end_time", param_type="string", description="End timestamp ISO")
        ],
        keywords=["timeline", "chronology", "sequence of events", "when did", "timestamp", "what happened at", "chronological order"]
    ),
    LeafDefinition(
        leaf_id="temporal.burst_activity",
        domain="temporal",
        name="High-Frequency Activity Bursts",
        description="Bursts of rapid, concentrated events across telecommunications, banking, and IP layers occurring within narrow time windows.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="timeline_service:burst_detector",
        handler_method="fetch_burst_activity",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["burst", "activity spike", "sudden activity", "high frequency", "flurry", "rapid events"]
    ),
    LeafDefinition(
        leaf_id="temporal.cross_modal_correlation",
        domain="temporal",
        name="Cross-Modal Temporal Correlations",
        description="Correlated multi-channel triggers where an action in one domain directly precedes another (e.g. phone call 4 minutes before an IMPS bank transfer).",
        authority=EvidenceAuthority.DERIVED,
        primary_source="timeline_service:correlation_engine / postgres:investigation_alerts",
        handler_method="fetch_temporal_correlations",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["correlation", "call before transfer", "trigger", "preceded", "synchronized", "collision burst", "tight timing"]
    ),
    LeafDefinition(
        leaf_id="temporal.inconsistency",
        domain="temporal",
        name="Temporal Inconsistencies & Clashing Timestamps",
        description="Overlapping or contradictory event timestamps for the same identity across independent source logs.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="timeline_service:inconsistency_detector",
        handler_method="fetch_temporal_inconsistencies",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["inconsistency", "conflicting time", "simultaneous", "overlapping session", "clash"]
    ),

    # ── 6. ANOMALY INTELLIGENCE ──────────────────────────────────────────
    LeafDefinition(
        leaf_id="anomaly.findings",
        domain="anomaly",
        name="Unified Anomaly Findings & Proof Briefs",
        description="Machine-detected investigative findings from all 11+ analytical engines: domain, unified score, severity, explanation, and why relevant.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings",
        handler_method="fetch_anomaly_findings",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target suspect name"),
            LeafParameterRequirement(name="severity", param_type="string", description="CRITICAL, HIGH, MEDIUM, LOW"),
            LeafParameterRequirement(name="domain", param_type="string", description="FINANCIAL, TELECOM, SPATIAL, etc.")
        ],
        keywords=["anomaly", "unusual", "threat", "detection", "finding", "risk score", "proof brief", "severity"]
    ),
    LeafDefinition(
        leaf_id="anomaly.cep_alerts",
        domain="anomaly",
        name="Complex Event Processing (CEP) Alerts",
        description="Real-time multi-modal alerts with micro-timelines and risk levels (Triple Collision Burst, Spatio-Temporal Jump, Pass-Through Mule).",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:investigation_alerts",
        handler_method="fetch_cep_alerts",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name"),
            LeafParameterRequirement(name="pattern_name", param_type="string", description="Alert pattern name")
        ],
        keywords=["alert", "warning", "cep", "triple collision", "triage", "micro timeline", "urgent alert"]
    ),
    LeafDefinition(
        leaf_id="anomaly.cross_domain",
        domain="anomaly",
        name="Cross-Domain Activity Collisions",
        description="Anomalies involving simultaneous or near-simultaneous evidence convergence across CDR, banking, IPDR, and location domains.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:anomaly_findings:CROSS_DOMAIN",
        handler_method="fetch_cross_domain_anomalies",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Suspect name")
        ],
        keywords=["cross domain", "multi modal anomaly", "converged channels", "composite threat"]
    ),

    # ── 7. KNOWLEDGE GRAPH INTELLIGENCE ──────────────────────────────────
    LeafDefinition(
        leaf_id="graph.connections",
        domain="graph",
        name="Multi-Hop Graph Entity Connections",
        description="1 to 3 hop relationship paths linking persons, accounts, phone numbers, and IP addresses in the Neo4j knowledge graph.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:MATCH_PATHS",
        handler_method="fetch_graph_connections",
        parameters=[
            LeafParameterRequirement(name="entity_a", param_type="string", description="First entity name/id"),
            LeafParameterRequirement(name="entity_b", param_type="string", description="Second entity name/id"),
            LeafParameterRequirement(name="max_hops", param_type="int", description="Maximum hop distance (1-3)")
        ],
        keywords=["connected to", "relationship", "hops", "link between", "how are they connected", "network path", "graph"]
    ),
    LeafDefinition(
        leaf_id="graph.shortest_path",
        domain="graph",
        name="Dijkstra Shortest Path",
        description="The shortest directed or undirected traversal chain between two distinct target entities in the graph.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="neo4j:shortestPath",
        handler_method="fetch_shortest_path",
        parameters=[
            LeafParameterRequirement(name="entity_a", param_type="string", description="Source entity name/id"),
            LeafParameterRequirement(name="entity_b", param_type="string", description="Destination entity name/id")
        ],
        keywords=["shortest path", "shortest route", "closest connection", "direct path between", "distance"]
    ),
    LeafDefinition(
        leaf_id="graph.gds_centrality",
        domain="graph",
        name="Graph Data Science (GDS) Centrality",
        description="Algorithmic graph metrics: Louvain community clusters, PageRank influence, and Betweenness centrality bridges.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="neo4j:GDS / postgres:investigation_reports",
        handler_method="fetch_gds_centrality",
        parameters=[
            LeafParameterRequirement(name="community_id", param_type="int", description="Syndicate community ID"),
            LeafParameterRequirement(name="metric_type", param_type="string", description="pagerank, betweenness, louvain")
        ],
        keywords=["pagerank", "betweenness", "centrality", "kingpin", "broker", "bridge node", "louvain", "modularity"]
    ),
    LeafDefinition(
        leaf_id="graph.transaction_subgraph",
        domain="graph",
        name="Directed Transaction Subgraph",
        description="Visualizable node-and-edge subgraph representing fund transfers between suspect bank accounts.",
        authority=EvidenceAuthority.PRIMARY,
        primary_source="neo4j:TRANSACTED_WITH",
        handler_method="fetch_transaction_subgraph",
        parameters=[
            LeafParameterRequirement(name="entity_name", param_type="string", description="Target person name")
        ],
        keywords=["transaction graph", "fund flow visual", "account network", "subgraph"]
    ),

    # ── 8. REPORTS & DOSSIERS ────────────────────────────────────────────
    LeafDefinition(
        leaf_id="reports.court_dossier",
        domain="reports",
        name="Formal Court-Ready Case Dossier",
        description="Full 7-section court dossier summary: evidence inventory with SHA-256 hashes, golden profiles, anomaly briefs, alerts, and audit seals.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="pdf_report_service:get_court_dossier_payload",
        handler_method="fetch_court_dossier",
        parameters=[
            LeafParameterRequirement(name="section_id", param_type="string", description="Optional specific section")
        ],
        keywords=["court dossier", "dossier", "formal report", "case report", "investigation summary", "prosecution brief"]
    ),
    LeafDefinition(
        leaf_id="reports.section_65b",
        domain="reports",
        name="Section 65B Electronic Evidence Certificate",
        description="Statutory Certificate under Section 65B Indian Evidence Act / Section 63 BSA certifying electronic record hash integrity and custody.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="pdf_report_service:generate_section_65b_certificate_pdf",
        handler_method="fetch_section_65b_certificate",
        parameters=[],
        keywords=["section 65b", "65b", "evidence certificate", "bsa 63", "electronic evidence certificate", "admissibility"]
    ),
    LeafDefinition(
        leaf_id="reports.lead_investigator",
        domain="reports",
        name="Lead AI Investigator Prosecutorial Dossier",
        description="Senior prosecutorial case synthesis: executive assessment, 4-phase modus operandi, legal directives (BNS/PMLA), and key targets.",
        authority=EvidenceAuthority.GENERATED,
        primary_source="postgres:investigation_reports:lead_json",
        handler_method="fetch_lead_investigator_report",
        parameters=[
            LeafParameterRequirement(name="community_id", param_type="int", description="Community ID")
        ],
        keywords=["lead investigator report", "lead dossier", "prosecutorial synthesis", "modus operandi", "legal actions", "executive assessment"]
    ),
    LeafDefinition(
        leaf_id="reports.financial_specialist",
        domain="reports",
        name="Financial Specialist Intelligence Report",
        description="Financial agent report: money mule identification, structured smurfing patterns, layering conduits, and account freeze orders.",
        authority=EvidenceAuthority.GENERATED,
        primary_source="postgres:investigation_reports:financial_json",
        handler_method="fetch_financial_specialist_report",
        parameters=[],
        keywords=["financial specialist report", "financial analysis report", "laundering analysis", "mule report"]
    ),
    LeafDefinition(
        leaf_id="reports.geographic_specialist",
        domain="reports",
        name="Geographical Specialist Intelligence Report",
        description="Geographic agent report: cell tower triangulation, safehouse clusters, border transit corridors, and raid coordinates.",
        authority=EvidenceAuthority.GENERATED,
        primary_source="postgres:investigation_reports:geographic_json",
        handler_method="fetch_geographic_specialist_report",
        parameters=[],
        keywords=["geographic specialist report", "spatial report", "movement report", "safehouse report", "tower analysis report"]
    ),
    LeafDefinition(
        leaf_id="reports.temporal_specialist",
        domain="reports",
        name="Temporal Specialist Intelligence Report",
        description="Temporal agent report: CDR burst timing, off-hours operational windows, trigger-to-transfer sync, and conspiracy timelines.",
        authority=EvidenceAuthority.GENERATED,
        primary_source="postgres:investigation_reports:temporal_json",
        handler_method="fetch_temporal_specialist_report",
        parameters=[],
        keywords=["temporal specialist report", "timeline report", "timing report", "burst report"]
    ),
    LeafDefinition(
        leaf_id="reports.data_quality",
        domain="reports",
        name="Evidence Ingestion & Data Quality Report",
        description="Ingestion validation metrics: total records, valid/invalid/duplicate record counts, missing field ratios, and quality scores.",
        authority=EvidenceAuthority.DERIVED,
        primary_source="postgres:data_quality_reports / postgres:evidence",
        handler_method="fetch_data_quality_report",
        parameters=[],
        keywords=["data quality", "ingestion status", "invalid records", "missing fields", "evidence files", "file upload"]
    )
]

# Quick lookup map by leaf_id
LEAF_REGISTRY: Dict[str, LeafDefinition] = {leaf.leaf_id: leaf for leaf in ALL_LEAF_DEFINITIONS}

class LeafCatalog:
    """Manages the hierarchical tree and formats prompts for structure-aware routing."""

    @classmethod
    def get_all_leaves(cls) -> List[LeafDefinition]:
        return ALL_LEAF_DEFINITIONS

    @classmethod
    def get_leaf(cls, leaf_id: str) -> Optional[LeafDefinition]:
        return LEAF_REGISTRY.get(leaf_id)

    @classmethod
    def is_valid_leaf_id(cls, leaf_id: str) -> bool:
        return leaf_id in LEAF_REGISTRY

    @classmethod
    def get_toc_prompt_block(cls) -> str:
        """
        Builds a compact, structured Table of Contents (ToC) representation of all valid leaves
        for inclusion in the Qwen 2.5 7B routing prompt.
        """
        lines = ["=== INVESTIGATION STRUCTURE (TABLE OF CONTENTS) ==="]
        current_domain = ""
        for leaf in ALL_LEAF_DEFINITIONS:
            if leaf.domain != current_domain:
                current_domain = leaf.domain
                lines.append(f"\n[{current_domain.upper()} INTELLIGENCE]")
            lines.append(f"- {leaf.leaf_id}: {leaf.name} — {leaf.description} (Authority: {leaf.authority.value})")
        lines.append("\n===================================================")
        return "\n".join(lines)

    @classmethod
    def fast_keyword_match(cls, query: str) -> List[str]:
        """
        Fast deterministic heuristic matching that identifies obvious leaf IDs from query text.
        Used as a candidate recommender or fallback.
        """
        q_low = query.lower()
        matched_leaves: List[str] = []

        for leaf in ALL_LEAF_DEFINITIONS:
            for kw in leaf.keywords:
                # Word boundary check for short keywords
                if len(kw) <= 4:
                    if f" {kw} " in f" {q_low} " or q_low.startswith(f"{kw} ") or q_low.endswith(f" {kw}"):
                        if leaf.leaf_id not in matched_leaves:
                            matched_leaves.append(leaf.leaf_id)
                        break
                else:
                    if kw in q_low:
                        if leaf.leaf_id not in matched_leaves:
                            matched_leaves.append(leaf.leaf_id)
                        break

        return matched_leaves
