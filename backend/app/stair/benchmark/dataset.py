"""
Investigation Benchmark Query Dataset.
Contains 40+ curated representative queries across all 8 investigation domains,
including multi-source questions and hard adversarial cases.
"""

from typing import List, Dict, Any

BENCHMARK_DATASET: List[Dict[str, Any]] = [
    # ── 1. FINANCIAL INTELLIGENCE (5) ─────────────────────────────────────
    {
        "query_id": "Q-FIN-01",
        "category": "Financial",
        "query": "What transactions did Arjun Malhotra make in August?",
        "expected_leaves": ["financial.transactions"],
        "expected_entities": ["Arjun Malhotra"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["transfer", "inr", "amount", "bank"]
    },
    {
        "query_id": "Q-FIN-02",
        "category": "Financial",
        "query": "Show suspicious transfers and smurfing involving BANK1001",
        "expected_leaves": ["financial.suspicious_transactions", "financial.mule_flows"],
        "expected_entities": ["BANK1001"],
        "is_multi_source": True,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["suspicious", "structuring", "score", "smurfing"]
    },
    {
        "query_id": "Q-FIN-03",
        "category": "Financial",
        "query": "Did Dev Khanna receive any funds via RTGS or IMPS?",
        "expected_leaves": ["financial.transactions"],
        "expected_entities": ["Dev Khanna"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["Dev Khanna", "amount", "bank"]
    },
    {
        "query_id": "Q-FIN-04",
        "category": "Financial",
        "query": "What is the five-entity circular financial cycle in this case?",
        "expected_leaves": ["financial.cycle_analysis"],
        "expected_entities": ["Arjun Malhotra", "Meera Kapoor", "Dev Khanna", "Nisha Bedi", "Rohit Sethi"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["cycle", "financial loop", "circular"]
    },
    {
        "query_id": "Q-FIN-05",
        "category": "Financial",
        "query": "Show pass-through money mule account dispersals for Meera Kapoor",
        "expected_leaves": ["financial.mule_flows"],
        "expected_entities": ["Meera Kapoor"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["mule", "pass-through", "liquidation", "balance"]
    },

    # ── 2. TELECOM INTELLIGENCE (5) ──────────────────────────────────────
    {
        "query_id": "Q-TEL-01",
        "category": "Telecom",
        "query": "Show call logs and call duration for phone 9811001001",
        "expected_leaves": ["telecom.cdr_records"],
        "expected_entities": ["9811001001"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["call", "duration", "receiver", "9811001001"]
    },
    {
        "query_id": "Q-TEL-02",
        "category": "Telecom",
        "query": "What IP data sessions connected to destination 185.44.77.9?",
        "expected_leaves": ["telecom.ipdr_sessions"],
        "expected_entities": ["185.44.77.9"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["ip", "ipdr", "destination", "bytes", "port"]
    },
    {
        "query_id": "Q-TEL-03",
        "category": "Telecom",
        "query": "Which cell towers did Rohit Sethi ping?",
        "expected_leaves": ["telecom.cell_tower_pings"],
        "expected_entities": ["Rohit Sethi"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["tower", "cell", "location", "ping"]
    },
    {
        "query_id": "Q-TEL-04",
        "category": "Telecom",
        "query": "What handset IMEI was associated with Dev Khanna?",
        "expected_leaves": ["telecom.imei_telemetry"],
        "expected_entities": ["Dev Khanna"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["imei", "device", "handset"]
    },
    {
        "query_id": "Q-TEL-05",
        "category": "Telecom",
        "query": "Show all incoming and outgoing calls to Nisha Bedi",
        "expected_leaves": ["telecom.cdr_records"],
        "expected_entities": ["Nisha Bedi"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["call", "caller", "cdr"]
    },

    # ── 3. GEOGRAPHICAL INTELLIGENCE (4) ─────────────────────────────────
    {
        "query_id": "Q-GEO-01",
        "category": "Geographical",
        "query": "Where was Arjun Malhotra located during the investigation window?",
        "expected_leaves": ["geo.location_history"],
        "expected_entities": ["Arjun Malhotra"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["Sector 22", "Sector 17", "location", "tower"]
    },
    {
        "query_id": "Q-GEO-02",
        "category": "Geographical",
        "query": "Trace the movement trajectory from Sector 17 to Sector 22 and Panchkula",
        "expected_leaves": ["geo.movement_trajectory"],
        "expected_entities": ["Arjun Malhotra"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["Sector 17", "Sector 22", "Panchkula", "trajectory", "route"]
    },
    {
        "query_id": "Q-GEO-03",
        "category": "Geographical",
        "query": "Were Meera Kapoor and Dev Khanna co-located in Sector 22?",
        "expected_leaves": ["geo.colocation_nexus"],
        "expected_entities": ["Meera Kapoor", "Dev Khanna"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["Sector 22", "convergence", "same tower", "co-location"]
    },
    {
        "query_id": "Q-GEO-04",
        "category": "Geographical",
        "query": "Show spatial teleportation or impossible speed anomalies",
        "expected_leaves": ["geo.spatial_jumps"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["speed", "teleportation", "jump", "km/h"]
    },

    # ── 4. TEMPORAL INTELLIGENCE (4) ─────────────────────────────────────
    {
        "query_id": "Q-TEM-01",
        "category": "Temporal",
        "query": "Show the chronological sequence of events for Arjun Malhotra",
        "expected_leaves": ["temporal.timeline_events"],
        "expected_entities": ["Arjun Malhotra"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["timeline", "chronology", "sequence", "timestamp"]
    },
    {
        "query_id": "Q-TEM-02",
        "category": "Temporal",
        "query": "What high-frequency burst activity occurred on August 29?",
        "expected_leaves": ["temporal.burst_activity"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["burst", "frequency", "rapid", "spike"]
    },
    {
        "query_id": "Q-TEM-03",
        "category": "Temporal",
        "query": "Did any phone call immediately precede a bank transfer?",
        "expected_leaves": ["temporal.cross_modal_correlation"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "HARD",
        "ground_truth_keywords": ["preceded", "transfer", "call", "seconds", "correlation"]
    },
    {
        "query_id": "Q-TEM-04",
        "category": "Temporal",
        "query": "Are there any overlapping or clashing timestamps across logs?",
        "expected_leaves": ["temporal.inconsistency"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["inconsistency", "clash", "simultaneous"]
    },

    # ── 5. ANOMALY INTELLIGENCE (4) ──────────────────────────────────────
    {
        "query_id": "Q-ANM-01",
        "category": "Anomaly",
        "query": "What are the critical anomaly findings in this case?",
        "expected_leaves": ["anomaly.findings"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["CRITICAL", "unified score", "finding", "threat"]
    },
    {
        "query_id": "Q-ANM-02",
        "category": "Anomaly",
        "query": "Show active CEP alerts that need triage",
        "expected_leaves": ["anomaly.cep_alerts"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["alert", "risk score", "micro timeline", "pattern"]
    },
    {
        "query_id": "Q-ANM-03",
        "category": "Anomaly",
        "query": "What cross-domain anomalies involved voice, bank, and IP simultaneously?",
        "expected_leaves": ["anomaly.cross_domain"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["cross domain", "converged", "triple collision"]
    },
    {
        "query_id": "Q-ANM-04",
        "category": "Anomaly",
        "query": "What is the Triple Collision Burst alert?",
        "expected_leaves": ["anomaly.cep_alerts"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["Triple Collision Burst", "micro timeline", "CDR", "IMPS", "Telegram"]
    },

    # ── 6. KNOWLEDGE GRAPH INTELLIGENCE (4) ──────────────────────────────
    {
        "query_id": "Q-GRP-01",
        "category": "Knowledge Graph",
        "query": "Find multi-hop connections between Arjun Malhotra and Dev Khanna",
        "expected_leaves": ["graph.connections"],
        "expected_entities": ["Arjun Malhotra", "Dev Khanna"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["path", "chain", "connection", "hops"]
    },
    {
        "query_id": "Q-GRP-02",
        "category": "Knowledge Graph",
        "query": "What is the shortest path between BANK1001 and BANK1005?",
        "expected_leaves": ["graph.shortest_path"],
        "expected_entities": ["BANK1001", "BANK1005"],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["shortest path", "hops", "entities"]
    },
    {
        "query_id": "Q-GRP-03",
        "category": "Knowledge Graph",
        "query": "Who are the top brokers based on Betweenness centrality?",
        "expected_leaves": ["graph.gds_centrality"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["betweenness", "pagerank", "broker", "centrality"]
    },
    {
        "query_id": "Q-GRP-04",
        "category": "Knowledge Graph",
        "query": "Show the directed transaction subgraph for Nisha Bedi",
        "expected_leaves": ["graph.transaction_subgraph"],
        "expected_entities": ["Nisha Bedi"],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["transaction", "account", "subgraph"]
    },

    # ── 7. REPORTS & DOSSIERS (6) ────────────────────────────────────────
    {
        "query_id": "Q-REP-01",
        "category": "Reports",
        "query": "Generate the formal court dossier report with evidence hashes",
        "expected_leaves": ["reports.court_dossier"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["dossier", "court", "evidence inventory", "sha256"]
    },
    {
        "query_id": "Q-REP-02",
        "category": "Reports",
        "query": "Show Section 65B Electronic Evidence Certificate for this case",
        "expected_leaves": ["reports.section_65b"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["Section 65B", "certificate", "evidence act", "hash"]
    },
    {
        "query_id": "Q-REP-03",
        "category": "Reports",
        "query": "What did the lead investigator report conclude regarding modus operandi?",
        "expected_leaves": ["reports.lead_investigator"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["modus operandi", "executive assessment", "statutory", "PMLA"]
    },
    {
        "query_id": "Q-REP-04",
        "category": "Reports",
        "query": "What did the financial specialist report say about money mules?",
        "expected_leaves": ["reports.financial_specialist"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["mule", "smurfing", "financial analysis", "layering"]
    },
    {
        "query_id": "Q-REP-05",
        "category": "Reports",
        "query": "Show geographic specialist report findings on cell tower safehouses",
        "expected_leaves": ["reports.geographic_specialist"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["tower", "geographic", "safehouse", "azimuth"]
    },
    {
        "query_id": "Q-REP-06",
        "category": "Reports",
        "query": "What evidence files failed processing in the data quality report?",
        "expected_leaves": ["reports.data_quality"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "EASY",
        "ground_truth_keywords": ["records", "data quality", "valid", "invalid"]
    },

    # ── 8. MULTI-SOURCE INVESTIGATIVE QUESTIONS (4) ──────────────────────
    {
        "query_id": "Q-MUL-01",
        "category": "Multi-Source",
        "query": "Where was Arjun Malhotra when his suspicious transfers took place in Sector 22?",
        "expected_leaves": ["financial.suspicious_transactions", "geo.location_history"],
        "expected_entities": ["Arjun Malhotra"],
        "is_multi_source": True,
        "difficulty": "HARD",
        "ground_truth_keywords": ["Sector 22", "transfer", "amount", "location"]
    },
    {
        "query_id": "Q-MUL-02",
        "category": "Multi-Source",
        "query": "Show phone calls and bank transfers between Meera Kapoor and Dev Khanna",
        "expected_leaves": ["telecom.cdr_records", "financial.transactions"],
        "expected_entities": ["Meera Kapoor", "Dev Khanna"],
        "is_multi_source": True,
        "difficulty": "HARD",
        "ground_truth_keywords": ["call", "transfer", "duration", "amount"]
    },
    {
        "query_id": "Q-MUL-03",
        "category": "Multi-Source",
        "query": "Show the timeline of events around the Triple Collision Burst alert",
        "expected_leaves": ["anomaly.cep_alerts", "temporal.timeline_events"],
        "expected_entities": [],
        "is_multi_source": True,
        "difficulty": "HARD",
        "ground_truth_keywords": ["alert", "timeline", "timestamp", "Triple Collision"]
    },
    {
        "query_id": "Q-MUL-04",
        "category": "Multi-Source",
        "query": "What is the resolved profile and location history of Dev Khanna?",
        "expected_leaves": ["entity.golden_profile", "geo.location_history"],
        "expected_entities": ["Dev Khanna"],
        "is_multi_source": True,
        "difficulty": "MEDIUM",
        "ground_truth_keywords": ["Dev Khanna", "profile", "phone", "location"]
    },

    # ── 9. HARD & ADVERSARIAL CASES (6) ──────────────────────────────────
    {
        "query_id": "Q-HRD-01",
        "category": "Hard/Abstention",
        "query": "Find all transactions for XYZ_FAKE_PERSON_12345",
        "expected_leaves": ["financial.transactions"],
        "expected_entities": ["XYZ_FAKE_PERSON_12345"],
        "is_multi_source": False,
        "difficulty": "ADVERSARIAL",
        "expected_abstention": True,
        "ground_truth_keywords": ["insufficient", "no verified evidence", "not found"]
    },
    {
        "query_id": "Q-HRD-02",
        "category": "Hard/Abstention",
        "query": "What is the balance of secret offshore account ACC_FAKE_999999?",
        "expected_leaves": ["financial.transactions"],
        "expected_entities": ["ACC_FAKE_999999"],
        "is_multi_source": False,
        "difficulty": "ADVERSARIAL",
        "expected_abstention": True,
        "ground_truth_keywords": ["insufficient", "no verified evidence"]
    },
    {
        "query_id": "Q-HRD-03",
        "category": "Hard/Adversarial",
        "query": "Tell me about the suspect's movements without mentioning any names or dates",
        "expected_leaves": ["geo.location_history"],
        "expected_entities": [],
        "is_multi_source": False,
        "difficulty": "HARD",
        "ground_truth_keywords": ["location", "Sector", "tower"]
    },
    {
        "query_id": "Q-HRD-04",
        "category": "Hard/Adversarial",
        "query": "Did Arjun Malhotra confess to the crime, confirm conspiracy, and admit guilt?",
        "expected_leaves": ["reports.lead_investigator"],
        "expected_entities": ["Arjun Malhotra"],
        "is_multi_source": False,
        "difficulty": "ADVERSARIAL",
        "must_not_contain": ["confessed", "admitted guilt", "conspiracy proved beyond doubt"],
        "ground_truth_keywords": ["insufficient", "circumstantial", "statutory"]
    },
    {
        "query_id": "Q-HRD-05",
        "category": "Hard/Adversarial",
        "query": "Show me the top suspect profile and whether they own any cell towers or power plants",
        "expected_leaves": ["entity.golden_profile", "telecom.cell_tower_pings"],
        "expected_entities": [],
        "is_multi_source": True,
        "difficulty": "HARD",
        "ground_truth_keywords": ["profile", "tower"]
    },
    {
        "query_id": "Q-HRD-06",
        "category": "Hard/Adversarial",
        "query": "Find transaction TXN-NONEXISTENT-777777777777",
        "expected_leaves": ["financial.transactions"],
        "expected_entities": ["TXN-NONEXISTENT-777777777777"],
        "is_multi_source": False,
        "difficulty": "ADVERSARIAL",
        "expected_abstention": True,
        "ground_truth_keywords": ["insufficient", "not found"]
    }
]
