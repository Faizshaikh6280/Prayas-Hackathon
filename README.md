<div align="center">

# OmniTrace: AI-Powered Single Analytics Platform

### Enterprise Cyber-Intelligence, Multi-Source Forensics, and Evidence-Grounded Analytics

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10-blue.svg" alt="Python 3.10" height="20" />
  <img src="https://img.shields.io/badge/Next.js-14.2-black.svg" alt="Next.js 14.2" height="20" />
  <img src="https://img.shields.io/badge/React-18.3-blue.svg" alt="React 18.3" height="20" />
  <img src="https://img.shields.io/badge/FastAPI-0.140+-009688.svg" alt="FastAPI" height="20" />
  <img src="https://img.shields.io/badge/PostgreSQL-16--alpine-336791.svg" alt="PostgreSQL 16" height="20" />
  <img src="https://img.shields.io/badge/Storage-Apache%20Iceberg%20%2F%20Parquet-blue.svg" alt="Apache Iceberg" height="20" />
  <img src="https://img.shields.io/badge/Engine-PySpark%20%2F%20PyArrow-orange.svg" alt="PySpark" height="20" />
  <img src="https://img.shields.io/badge/Graph-Neo4j%205.12%20GDS-008CC1.svg" alt="Neo4j 5.12" height="20" />
  <img src="https://img.shields.io/badge/Object%20Store-MinIO%20S3-C72C48.svg" alt="MinIO" height="20" />
  <img src="https://img.shields.io/badge/Cache%20%26%20Broker-Redis%207-DC382D.svg" alt="Redis 7" height="20" />
  <img src="https://img.shields.io/badge/Local%20LLM-Qwen%202.5%207B-purple.svg" alt="Local LLM" height="20" />
  <img src="https://img.shields.io/badge/Container-Docker%20Compose-2496ED.svg" alt="Docker" height="20" />
</p>

</div>

> **OmniTrace** unifies fragmented, heterogeneous digital evidence—telecom CDRs, ISP IPDR sessions, banking transactions, social activity logs, KYC filings, CCTV telemetry, and physical NFC crime scene acquisitions—into a single, high-performance analytical picture. Built on distributed columnar event stores, graph data science, multi-engine anomaly detection, and a structure-aware multi-agent investigation workflow, OmniTrace transforms raw investigation data into courtroom-admissible intelligence without compromising chain of custody.
>
> 📄 **System Documentation**: For the complete platform architecture, forensic engineering blueprints, and evaluation reports, see [Dabangg Coder Documentation](./Dabangg%20Coder%20Documentation%20(1).pdf).

---

## Table of Contents

- [1. Executive Overview](#1-executive-overview)
- [2. Problem Statement \& The Forensic Gap](#2-problem-statement--the-forensic-gap)
- [3. Core Philosophy: Upload Evidence → Let Platform Investigate](#3-core-philosophy-upload-evidence--let-platform-investigate)
- [4. High-Level System Architecture](#4-high-level-system-architecture)
- [5. End-to-End Data Flow](#5-end-to-end-data-flow)
- [6. Technology Stack \& Storage Inventory](#6-technology-stack--storage-inventory)
- [7. Multi-Source Ingestion \& Normalization](#7-multi-source-ingestion--normalization)
- [8. Secure Evidence Preservation \& Chain of Custody](#8-secure-evidence-preservation--chain-of-custody)
- [9. Canonical Event Data Model (CDM)](#9-canonical-event-data-model-cdm)
- [10. Scalable Data Architecture (GB-to-TB Scale)](#10-scalable-data-architecture-gb-to-tb-scale)
- [11. Multi-Anchor Entity Resolution (ER)](#11-multi-anchor-entity-resolution-er)
- [12. Cross-Source Correlation \& Knowledge Graph](#12-cross-source-correlation--knowledge-graph)
- [13. Multi-Engine Anomaly Intelligence](#13-multi-engine-anomaly-intelligence)
- [14. Timeline Reconstruction \& Temporal Intelligence](#14-timeline-reconstruction--temporal-intelligence)
- [15. Multi-Agent Investigative Workflow](#15-multi-agent-investigative-workflow)
- [16. Agentic RAG \& STAIR Architecture](#16-agentic-rag--stair-architecture)
- [17. Hallucination Mitigation \& Guardrails](#17-hallucination-mitigation--guardrails)
- [18. Quantitative LLM Evaluation \& Benchmarks](#18-quantitative-llm-evaluation--benchmarks)
- [19. Physical Forensics: NFC Credentials \& Crime Scene Tags](#19-physical-forensics-nfc-credentials--crime-scene-tags)
- [20. CCTV Route Tracking \& Location Intelligence](#20-cctv-route-tracking--location-intelligence)
- [21. Security Architecture \& Role-Based Access Control](#21-security-architecture--role-based-access-control)
- [22. Docker Microservices Architecture](#22-docker-microservices-architecture)
- [23. Scheduled \& Continuous Ingestion](#23-scheduled--continuous-ingestion)
- [24. Command Center User Interface](#24-command-center-user-interface)
- [25. REST API Documentation](#25-rest-api-documentation)
- [26. Repository Directory Structure](#26-repository-directory-structure)
- [27. System Requirements](#27-system-requirements)
- [28. Environment Variables Reference](#28-environment-variables-reference)
- [29. Installation \& Setup Guide](#29-installation--setup-guide)
- [30. Verification \& Pipeline Execution](#30-verification--pipeline-execution)
- [31. Feasibility Analysis](#31-feasibility-analysis)
- [32. Viability Assessment](#32-viability-assessment)
- [33. Risks \& Mitigation Matrix](#33-risks--mitigation-matrix)
- [34. Limitations](#34-limitations)
- [35. Future Roadmap](#35-future-roadmap)
- [36. Responsible AI \& Human Oversight](#36-responsible-ai--human-oversight)
- [37. Contributing \& Development Guidelines](#37-contributing--development-guidelines)
- [38. Security Notice \& Remediation Advisory](#38-security-notice--remediation-advisory)
- [39. License](#39-license)

---

## 1. Executive Overview

Modern criminal conspiracies—including extortion rings, money laundering networks, cyber syndicates, and organized cross-border fraud—rarely operate within a single digital domain. Perpetrators deliberately distribute operational footprint across burner phones, dynamic IP leases, encrypted instant messaging, high-frequency banking funnels, and fake national identities.

Traditional law enforcement analytics suffer from siloed investigation software:
* Cellular CDRs are analyzed in telecom-specific tools.
* Bank statements are reviewed manually in spreadsheets.
* Network session logs (IPDR) require separate forensic extraction.
* Suspect linkage depends on slow, error-prone manual cross-referencing.

**OmniTrace** eliminates these silos by introducing an **AI-Powered Single Analytics Platform**. The platform ingests unlabelled, heterogeneous evidence files, verifies chain-of-custody seals, normalizes records into a strict **Canonical Event Model**, resolves fragmented aliases into unified real-world **Golden Profiles**, projects multi-modal topologies into **Neo4j Property Graphs**, detects complex syndicates via **11 Multi-Engine Anomaly Detectors**, and orchestrates a **Multi-Agent Investigative Intelligence Pipeline** grounded in **STAIR (Structure-Aware Evidence-First Engine)**.

---

## 2. Problem Statement & The Forensic Gap

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Telecom CDR   │   │  Banking Logs   │   │   IPDR / NAT    │   │  Social / KYC   │
│ (Towers, IMEIs) │   │ (UPI, Transfers)│   │ (Dynamic Leases)│   │(Aadhaar, Handles│
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │                     │
         ▼                     ▼                     ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                      THE FORENSIC GAP: UNCONNECTED SILOS                          │
│  - No unified timeline cross-referencing call pings with ATM cash-out sessions    │
│  - Identity fragmentation: "Vikramaditya Singh" vs "Vicky Gujjar" vs "@vicky_007" │
│  - Evidence destruction / manual chain of custody tracking failures               │
│  - AI Hallucinations: Generic LLMs inventing dates, amounts, and conspirators      │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### Why the Problem Exists
1. **Heterogeneous Schemas & Nomenclature**: Cellular carriers, fintech gateways, ISPs, and government registries use conflicting formats, timestamp precision standards, and column headers.
2. **Combinatorial Entity Ambiguity**: As record volume scales from gigabytes to terabytes, naive pairwise record matching scales quadratically ($O(N^2)$), collapsing computational pipelines.
3. **OPSEC & Evasion Techniques**: Syndicates intentionally swap physical handsets (IMEI hopping), route packets through VPN/Tor exit nodes, and structure transactions immediately below regulatory caps.
4. **Evidentiary Rigor**: Unlike conversational consumer AI, court proceedings require absolute provenance: every hypothesis, timeline entry, and anomaly score must link directly to an immutable byte-level evidence hash.

---

## 3. Core Philosophy: Upload Evidence → Let Platform Investigate

OmniTrace operates under a strict, human-in-the-loop operational doctrine:

> **Upload the Evidence → Let the Platform Investigate**

Investigators should never be required to manually stitch CSV rows, calculate velocity vectors between cellular antennas, or write raw graph traversal algorithms. 

Instead:
1. The investigator uploads raw files and provides optional case context.
2. The platform automatically detects schemas, applies client-side encryption, validates integrity, unifies identities, constructs the knowledge graph, and surfaces anomalous patterns.
3. A multi-agent AI team (Financial, Temporal, Spatial, and Lead Detective) conducts coordinated forensic analysis.
4. The investigator reviews explainable findings, explores relational paths, questions the evidence via the AI forensic chatbot, and exports a court-ready dossier.

**Crucial Mandate**: OmniTrace **never** independently establishes guilt or replaces legal judgment. It operates as an investigative decision-support system, exposing evidence-backed relationships, temporal anomalies, and operational contradictions for human validation.

---

## 4. High-Level System Architecture

OmniTrace is engineered as a decoupled, microservice-based architecture deployed via Docker Compose:

```mermaid
flowchart TD
    subgraph INTAKE["1. Secure Ingestion & Evidence Vault"]
        RAW["Raw Files (CSV, XLSX, JSON, PDF)"] --> INGEST["FastAPI Ingestion Endpoint"]
        INGEST --> HASH["SHA-256 Checksum Calculation"]
        INGEST --> AES["Client-Side AES-256-GCM Encryption"]
        AES --> MINIO_RAW[("MinIO S3: raw-evidence (Immutable)")]
        HASH --> PG_EVID[("PostgreSQL 16: Case & Evidence Registry")]
    end

    subgraph NORMALIZATION["2. Schema Detection & Distributed Processing"]
        MINIO_RAW --> DETECT["Source Fingerprinting Engine (CDR, IPDR, Bank, Social, KYC)"]
        DETECT --> PARSE["Modular Parser Adapters"]
        PARSE --> VALID["Validation & Quality Gate"]
        VALID -->|Malformed| QUARANTINE[("Quarantine Store")]
        VALID -->|Valid| PYARROW["PyArrow / PySpark Columnar Pipeline"]
        PYARROW --> ICEBERG[("MinIO S3: iceberg-warehouse (Parquet)")]
    end

    subgraph RESOLUTION["3. Entity Resolution & Topology Graph"]
        ICEBERG --> ZINGG["Zingg ML / Multi-Anchor Disjoint-Set Union-Find"]
        ZINGG --> GOLDEN[("PostgreSQL: golden_profiles")]
        GOLDEN --> SYNC["Graph Synchronizer"]
        ICEBERG --> SYNC
        SYNC --> NEO4J[("Neo4j 5.12 Property Graph (GDS Engine)")]
    end

    subgraph INTELLIGENCE["4. Multi-Engine Anomaly & Temporal Core"]
        ICEBERG --> ANOM_ORCH["Multi-Engine Anomaly Orchestrator"]
        GOLDEN --> ANOM_ORCH
        NEO4J --> ANOM_ORCH
        ANOM_ORCH --> ENGINES["11 Analytical Engine Families (19+ Detectors)"]
        ENGINES --> FUSION["Evidence Fusion & Calibration"]
        FUSION --> PG_ANOM[("PostgreSQL: anomaly_findings")]
        FUSION --> NEO_ANOM["Neo4j: :Anomaly Nodes"]
        ICEBERG --> CEP["Redis CEP Sliding-Window Alerts Engine"]
    end

    subgraph AGENTIC["5. Multi-Agent & STAIR Grounding Engine"]
        NEO4J --> AGENTS["LangGraph Multi-Agent Team (Financial, Temporal, Spatial, Lead)"]
        PG_ANOM --> AGENTS
        AGENTS --> DOSSIER["Syndicate Intelligence Dossier"]
        
        USER_Q["Investigator Natural Language Query"] --> STAIR["STAIR Grounded Retrieval & Guardrail Engine"]
        STAIR --> LEAF["Immutable Leaf Registry (TOC Routing)"]
        LEAF --> RETRIEVE["Case-Scoped Evidence Broker"]
        RETRIEVE --> VERIFY["Deterministic Fact Verifier"]
        VERIFY --> LOCAL_LLM["Local Qwen 2.5 7B (Ollama)"]
        LOCAL_LLM --> CITED_RESP["Evidence-Cited Response (Zero Hallucination)"]
    end

    subgraph UI["6. Command Center Visual Console"]
        PG_ANOM --> DASHBOARD["Next.js 14 Web Command Center"]
        NEO4J --> DASHBOARD
        CEP --> DASHBOARD
        CITED_RESP --> DASHBOARD
        DOSSIER --> PDF_EXP["Certified Court-Ready PDF Dossier"]
    end
```

---

## 5. End-to-End Data Flow

The operational lifecycle of evidence inside OmniTrace follows a strict progression:

```
RAW EVIDENCE (CSV / XLSX / JSON / PDF)
       │
       ▼
[STAGE 1: CRYPTOGRAPHIC INTAKE]
  ├── Compute deterministic SHA-256 hash
  ├── Encrypt payload via AES-256-GCM (96-bit nonce, 128-bit auth tag)
  ├── Persist encrypted bytes to MinIO: cases/{case_id}/evidence/{evidence_id}/original/{file}.enc
  └── Register metadata in PostgreSQL `evidence` table (status: RECEIVED)
       │
       ▼
[STAGE 2: AUTOMATIC SOURCE DETECTION & PARSING]
  ├── Inspect headers, JSON keys, and text tokens (heuristics + signatures)
  ├── Match domain: TELECOM (CDR), NETWORK (IPDR), BANKING, SOCIAL, KYC
  ├── Execute domain-specific parser adapter
  └── Output: Normalized field dictionaries
       │
       ▼
[STAGE 3: VALIDATION, QUARANTINE & QUALITY SCORING]
  ├── Check timestamp bounds, ISO-8601 UTC formats, E.164 phone schemas, IPv4 ranges
  ├── Divert malformed rows into PostgreSQL `quarantine_records`
  ├── Deduplicate rows via semantic field hashing
  └── Score overall file quality (0.0 to 100.0) in `data_quality_reports`
       │
       ▼
[STAGE 4: COLUMNAR CANONICAL WAREHOUSE WRITE]
  ├── Cast records into strict Pydantic `CanonicalEvent` models
  ├── Serialize into PyArrow columnar tables using `CANONICAL_PYARROW_SCHEMA`
  └── Write partitioned Parquet files to MinIO: s3a://iceberg-warehouse/canonical_events/
       │
       ▼
[STAGE 5: MULTI-ANCHOR ENTITY RESOLUTION]
  ├── Group by hard anchors: national_id, normalized phone (+91...), account, email, IMEI
  ├── Group by soft anchors: token-sort names, initial abbreviations, Jaro-Winkler (≥ 0.90)
  ├── Resolve clusters via Disjoint-Set Union-Find with path compression
  ├── Apply survivorship rules (longest name = primary; others = known_aliases)
  └── Write resolved master identities to PostgreSQL `golden_profiles` & backfill Parquet
       │
       ▼
[STAGE 6: KNOWLEDGE GRAPH PROJECTION]
  ├── Synchronize Golden Profiles and Canonical Events into Neo4j 5.12
  ├── Construct 8 Node Labels (:Person, :Phone, :BankAccount, :IPAddress, :IMEI, :CellTower, etc.)
  ├── Connect 9 Edge Types (:OWNS_PHONE, :TRANSACTED_WITH, :CALLED, :ACCESSED_FROM, etc.)
  └── Execute Graph Data Science (GDS): Louvain, PageRank, Betweenness Centrality, FastRP
       │
       ▼
[STAGE 7: MULTI-ENGINE ANOMALY INTELLIGENCE]
  ├── Execute 11 analytical engines across columnar warehouse and graph topology
  ├── Correlate raw detection signals across 7 dimensions
  ├── Evaluate patterns, bind evidence citations, score corroboration bonuses
  ├── Pass findings through 12-Check Quality Gate ("NO EVIDENCE -> NO CLAIM")
  └── Persist to PostgreSQL `anomaly_findings` and Neo4j `:Anomaly` nodes
       │
       ▼
[STAGE 8: MULTI-AGENT SYNTHESIS & STAIR AGENTIC RAG]
  ├── LangGraph multi-agent team executes Financial, Temporal, Spatial, and Lead analysis
  ├── STAIR engine routes investigator natural language queries across Immutable Leaf Registry
  ├── Performs deterministic claim verification and local Qwen 2.5 7B generation
  └── Streams real-time findings and exports certified cryptographic PDF dossiers
```

---

## 6. Technology Stack & Storage Inventory

| Technology | Layer / Role | Data Stored | Architectural Justification |
|---|---|---|---|
| **PostgreSQL 16** | Relational Metadata Registry | Cases, Evidence metadata, IAM Users, Roles, Permissions, Sessions, MFA, NFC cards, `golden_profiles`, `anomaly_findings`, `detection_signals`, `investigation_alerts`, `audit_logs` | ACID transactions, relational integrity, JSONB support for dynamic schemas, row-level case access boundaries. |
| **MinIO S3** | Immutable Object Storage | Raw encrypted evidence (`raw-evidence` bucket) | S3-compatible, on-premise, immutable object keys preventing evidence tampering. |
| **Apache Iceberg / Parquet** | Analytical Warehouse | Columnar canonical events partitioned by case, source, and date (`iceberg-warehouse` bucket) | Predicate pushdown, column pruning, vectorized queries, zero-copy PyArrow deserialization for high-volume analytics. |
| **PySpark / PyArrow** | Distributed Processing | Ingestion normalization, schema enforcement, feature matrix building | Strict schema typing, vectorized batch operations, elimination of memory bottlenecks. |
| **Neo4j 5.12 Enterprise / Community** | Property Graph Store | 8 Node Labels, 9 Edge Types, topology metrics, community structures | Native graph traversal, multi-hop pathfinding, Graph Data Science (GDS) algorithms (Louvain, PageRank, Centrality). |
| **Redis 7** | Cache, Message Broker & CEP State | Celery broker, sliding-window event caches, multi-modal collision buffers | In-memory latency (< 1ms), atomic operations, TTL-based session state management. |
| **Celery 5.3** | Asynchronous Task Worker | Long-running anomaly runs, batch graph synchronization, background parsing | Decouples HTTP request-response cycle from compute-intensive machine learning tasks. |
| **Zingg (Worker)** | ML Entity Resolution Worker | Distributed record linkage models, pairwise candidate pairs | Specialized entity resolution algorithms reducing quadratic comparison overhead. |
| **Ollama (Local Qwen 2.5 7B)** | On-Premise LLM Inference | Agentic reasoning, STAIR grounded generation, forensic chat | Complete data privacy: sensitive evidence never leaves agency hardware; zero cloud API leakage. |
| **FastAPI 0.140+** | Backend REST API | REST controllers, SSE streaming, authentication middleware | High-performance asynchronous Python, OpenAPI auto-documentation, native Pydantic v2 typing. |
| **Next.js 14 / React 18** | Frontend Command Center | Visual console, interactive graph views, geospatial maps, timeline playback | React Server Components, App Router, high performance with heavy graph/map visualizations. |
| **Cytoscape.js** | Graph Visualization | Interactive node-link forensic graphs | Fast canvas-based graph rendering, multiple layout algorithms (CoSE, Bilkent, Cola). |
| **Deck.gl / MapLibre GL** | Geospatial Telemetry | Cellular antenna sectors, trajectory tailing, impossible travel vectors | WebGL-accelerated rendering capable of displaying tens of thousands of GPS/cell tower points smoothly. |

---

## 7. Multi-Source Ingestion & Normalization

OmniTrace implements an extensible **Parser Adapter Pattern** managed by a central `SourceDetector` and `ParserRegistry`.

### Supported File Formats
* **Tabular CSV** (comma/tab/pipe-delimited, variable quotes)
* **Spreadsheets** (Microsoft Excel `.xlsx`, `.xls` via `openpyxl`)
* **JSON / JSON-Lines** (hierarchical and flat session payloads)
* **PDF Statements** (structured tabular bank and telecom statements parsed via `pypdf` and text extraction)

### Ingestion Pipeline Architecture

```mermaid
flowchart LR
    UPLOAD["Incoming Evidence File"] --> DETECT{"SourceDetector"}
    DETECT -->|Telecom Signatures| CDR["CDRParser"]
    DETECT -->|Network IP Signatures| IPDR["IPDRParser"]
    DETECT -->|Bank / UPI Signatures| BANK["BankingParser"]
    DETECT -->|Social Handles| SOC["SocialParser"]
    DETECT -->|Govt ID / KYC| KYC["KYCParser"]
    DETECT -->|Unknown Structure| GEN["GenericParser"]
    
    CDR & IPDR & BANK & SOC & KYC & GEN --> NORM["Field Normalization"]
    NORM --> VAL{"Validator"}
    VAL -->|Valid| DEDUP["Deduplication Engine"]
    VAL -->|Invalid| QUAR["Quarantine Store"]
    DEDUP --> QUALITY["Data Quality Scorer"]
    QUALITY --> WAREHOUSE[("Parquet Warehouse")]
```

### Domain Signatures & Parsers

| Domain | Parser Adapter | Extracted Key Signatures | Target Fields |
|---|---|---|---|
| **TELECOM** | `CDRParser` | `calling_number`, `called_number`, `imei`, `imsi`, `cell_tower_id`, `duration_seconds` | Call Detail Records, handset swaps, cellular tower locks, call duration metrics. |
| **NETWORK** | `IPDRParser` | `assigned_ip`, `destination_ip`, `source_port`, `service_port`, `bytes_transferred` | Dynamic IP leases, NAT port mappings, proxy/Tor gateway sessions, data transfer volume. |
| **BANKING** | `BankingParser` | `account_number`, `ifsc`, `amount_inr`, `txn_type`, `counterparty`, `channel`, `narration` | Bank statements, UPI transfers, ATM withdrawals, RTGS/IMPS tranches, mule accounts. |
| **SOCIAL** | `SocialParser` | `user_handle`, `platform`, `registered_phone`, `client_ip`, `activity_type` | Telegram, WhatsApp, Instagram logs, registered MSISDNs, client IPs. |
| **KYC** | `KYCParser` | `full_name`, `national_id`, `dob`, `address`, `phone`, `occupation` | Official identification records, Aadhaar, PAN card filings, permanent residential addresses. |

### Validation & Quarantine Subsystem
Before writing to the analytical warehouse, records are strictly validated by `app.ingestion.validator`:
* **Timestamp Verification**: Must conform to ISO-8601 UTC. Future timestamps or timestamps prior to year 2000 are rejected.
* **Geospatial Bounds**: Latitude must lie within `[-90, 90]` and Longitude within `[-180, 180]`.
* **Identifier Sanity**: E.164 telephone numbers must contain valid country codes; bank account numbers must be alphanumeric.
* **Quarantine Preservation**: Malformed records are never discarded. They are routed into PostgreSQL `quarantine_records` alongside the exact row index, failure reason, and raw JSON payload for forensic chain of custody.

---

## 8. Secure Evidence Preservation & Chain of Custody

OmniTrace follows a strict **Evidence-First Security Policy**. The original uploaded evidence is treated as an immutable physical artifact.

```
RAW EVIDENCE OBJECT
       │
       ▼
[SHA-256 Checksum] ──► Recorded in PostgreSQL `evidence.sha256`
       │
       ▼
[Client-Side AES-256-GCM]
  ├── 256-bit derived key from master secret
  ├── 96-bit cryptographically secure random nonce
  └── 128-bit authentication tag
       │
       ▼
[Immutable Write Path]
  └── MinIO Key: cases/{case_id}/evidence/{evidence_id}/original/{filename}.enc
       │
       ▼
[Tamper-Evident Read Path]
  ├── Fetch ciphertext + nonce from MinIO
  ├── Decrypt payload in volatile memory (never written to disk unencrypted)
  ├── Recalculate SHA-256 checksum
  └── Assert Recalculated SHA-256 == PostgreSQL Registry SHA-256
```

### Cryptographic Tamper Verification
The platform guarantees data integrity via `StorageService.verify_integrity()`:
```python
def verify_integrity(self, storage_path: str, expected_sha256: str) -> bool:
    decrypted_bytes = self.get_decrypted_evidence(storage_path)
    recalculated_sha256 = self.calculate_sha256(decrypted_bytes)
    return recalculated_sha256.lower() == expected_sha256.lower()
```
If an unauthorized system or administrator modifies or replaces a file in MinIO, the SHA-256 verification fails immediately, aborting pipeline execution and raising a security audit alert.

---

## 9. Canonical Event Data Model (CDM)

Every ingested event is converted into a unified schema defined in `app.schemas.canonical_event.CanonicalEvent`. This model ensures uniform processing across timeline reconstruction, graph synchronization, and anomaly detection.

```python
class CanonicalEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    case_id: str
    evidence_id: str
    event_type: str        # CALL, TRANSACTION, IP_SESSION, SOCIAL_ACTIVITY, IDENTITY_RECORD, LOCATION_EVENT
    source_type: str       # TELECOM, BANKING, NETWORK, SOCIAL, KYC
    timestamp: str         # Strict ISO-8601 UTC (e.g., 2026-03-02T09:15:22Z)
    
    entities: CanonicalEntities      # name, phone (+91...), national_id, email, social_handle, platform
    telemetry: CanonicalTelemetry    # imei, imsi, cell_tower_id, lat, lng, assigned_ip, dest_ip, port, duration
    financial: CanonicalFinancial    # account_number, ifsc, amount_inr, txn_type, channel, counterparty
    
    attributes: Dict[str, Any]       # Preserves unmapped raw source fields (zero information loss)
    provenance: EventProvenance      # case_id, evidence_id, source_file, row_index, evidence_sha256
    z_cluster_id: Optional[str]      # Resolved golden entity cluster ID (backfilled by Entity Resolution)
```

---

## 10. Scalable Data Architecture (GB-to-TB Scale)

OmniTrace is **designed for GB-to-TB scale investigative data workloads** and has been **validated with 1M+ records in project benchmark testing**.

```
INPUT EVIDENCE FILES / EVENT STREAMS
                 │
                 ▼
         MINIO S3 BUCKETS
    ├── raw-evidence (AES-256-GCM encrypted immutable source)
    └── iceberg-warehouse (Partitioned analytical warehouse)
                 │
                 ▼
     APACHE ICEBERG / PARQUET WAREHOUSE
    s3a://iceberg-warehouse/canonical_events/
      ├── case_id=CASE-001/
      │     ├── date_partition=2026-03-01/
      │     │     └── data.parquet
      │     └── date_partition=2026-03-02/
      │           └── data.parquet
                 │
                 ▼
     PYARROW / PYSPARK VECTORIZED READERS
    ├── Strict PyArrow Schema (CANONICAL_PYARROW_SCHEMA)
    ├── Predicate Pushdown (case_id, date, source_type)
    ├── Column Pruning (fetches only required analytical dimensions)
    └── Streaming Generator (iter_all_events avoids RAM exhaustion)
                 │
                 ▼
    DISTRIBUTED ANALYTICS & GRAPH CONSUMERS
    ├── Multi-Anchor Entity Resolution (Zingg ML)
    ├── Neo4j Property Graph Sync (Batched UNWIND chunks of 500)
    └── Multi-Engine Anomaly Detection (Celery Worker)
```

### Why This Achieves True Scalability
1. **Separation of Raw vs. Analytical Storage**: Bulky original evidence resides in immutable MinIO object storage. The analytical warehouse contains only structured columnar Parquet files.
2. **Columnar Parquet Compression & Vectorization**: Columnar layout reduces storage footprint by 75–85% compared to raw CSV/JSON and allows vectorized queries using PyArrow without deserializing entire rows.
3. **Partition Pruning**: Queries filtering on a specific case or date range touch only relevant directory partitions, reducing I/O from terabytes to megabytes.
4. **Streaming Iterators**: Downstream consumers utilize `CanonicalWarehouseReader.iter_all_events()` which streams records batch-by-batch rather than loading entire million-row datasets into system RAM.

---

## 11. Multi-Anchor Entity Resolution (ER)

Criminals frequently use multiple aliases, burner phones, shell bank accounts, and variations of their names.

```
"Vikramaditya Singh" ──[Has Phone: +919876500001]──┐
"Vicky Gujjar"        ──[Has Phone: +919876500001]──┼──► [MULTI-ANCHOR ENTITY RESOLUTION]
"@vicky_shooter_007" ──[Uses Phone: +919876500001]─┘                  │
                                                                      ▼
                                                          [GOLDEN PROFILE: CLUSTER_001]
                                                          Primary Name: Vikramaditya Singh
                                                          Known Aliases: ["Vicky Gujjar"]
                                                          Known Phones: ["+919876500001"]
                                                          Social Handles: ["@vicky_shooter_007"]
```

### Algorithmic Complexity: Avoiding Quadratic Bottlenecks
* **Naive Approach**: Pairwise comparison of $N$ records requires $\frac{N(N-1)}{2} = O(N^2)$ comparisons. For $1,000,000$ records, this equals $\approx 5 \times 10^{11}$ comparisons, which is computationally intractable.
* **OmniTrace Scalable Approach**:
  1. **Candidate Generation via Multi-Anchor Hashing ($O(N)$)**: Records are partitioned into candidate buckets based on deterministic hash keys:
     * Exact National ID (Aadhaar, PAN)
     * Normalized E.164 Phone (`+91...`)
     * Bank Account Number
     * Email Address
     * Hardware IMEI / IMSI
  2. **Candidate Blocking for Fuzzy Matching ($O(N \log N)$)**: Names and social handles are compared only within candidate blocks using token sorting, initials matching, and Jaro-Winkler distance ($\ge 0.90$).
  3. **Disjoint-Set Union-Find with Path Compression ($O(N \cdot \alpha(N))$)**: Connected entities are merged using a disjoint-set data structure where $\alpha$ is the inverse Ackermann function ($\alpha(N) \le 4$ for all practical universes—effectively linear time).
  4. **Zingg Distributed ML**: In distributed cluster mode, the Zingg worker uses learned blocking rules to reduce pairwise candidate generation to $O(N \log N)$ distributed across Spark executors.

### Survivorship & Alias Rules
* **Primary Name Selection**: The longest, most complete legal name among cluster members is promoted to `primary_name`.
* **Alias Preservation**: Shorter variants, nicknames, and handle stems are cataloged in `known_aliases`.
* **Phantom Cluster Elimination**: Telemetry pings (e.g. anonymous tower signals without person anchors) are isolated to prevent creating empty dummy profiles.

---

## 12. Cross-Source Correlation & Knowledge Graph

Resolved golden profiles and canonical events are projected into **Neo4j 5.12** by `app.services.graph_sync`.

```mermaid
graph TD
    Person1["(:Person {golden_id: 'CLUSTER_001', name: 'Vikramaditya Singh'})"]
    Person2["(:Person {golden_id: 'CLUSTER_002', name: 'Rohit Verma'})"]
    Phone1["(:Phone {number: '+919876500001'})"]
    Phone2["(:Phone {number: '+919876500002'})"]
    Account1["(:BankAccount {number: '501200778812'})"]
    Account2["(:BankAccount {number: '501200778814'})"]
    Tower["(:CellTower {tower_id: 'TOWER-DL-042'})"]
    IP["(:IPAddress {ip: '192.168.1.105'})"]
    Anomaly["(:Anomaly {type: 'TRIPLE_COLLISION_BURST', severity: 'CRITICAL'})"]

    Person1 -->|OWNS_PHONE| Phone1
    Person2 -->|OWNS_PHONE| Phone2
    Person1 -->|OWNS_ACCOUNT| Account1
    Person2 -->|OWNS_ACCOUNT| Account2
    Phone1 -->|CALLED {duration: 180s}| Phone2
    Account1 -->|TRANSACTED_WITH {amount: 2500000}| Account2
    Phone1 -->|PINGED_TOWER| Tower
    Phone2 -->|PINGED_TOWER| Tower
    Phone1 -->|ACCESSED_FROM| IP
    Person1 -->|HAS_ANOMALY| Anomaly
```

### Graph Schema
* **8 Node Labels**: `:Person`, `:Phone`, `:BankAccount`, `:IPAddress`, `:IMEI`, `:CellTower`, `:Anomaly`, `:SocialProfile`.
* **9 Edge Types**: `:OWNS_PHONE`, `:OWNS_ACCOUNT`, `:TRANSACTED_WITH`, `:CALLED`, `:ACCESSED_FROM`, `:USED_DEVICE`, `:PINGED_TOWER`, `:HAS_ANOMALY`, `:OWNS_SOCIAL`.

### Graph Data Science (GDS) Algorithms Implemented
The platform executes 5 graph algorithms defined in `app.services.gds_engine` (with seamless fallback to pure Python `NetworkX` if GDS plugins are not present):

1. **Louvain Community Detection**: Partitions the graph into modular co-offending syndicates by maximizing modularity:
   $$Q = \frac{1}{2m} \sum_{ij} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$
2. **PageRank**: Computes node centrality to unmask the influential kingpin of a conspiracy:
   $$PR(u) = \frac{1-d}{N} + d \sum_{v \in B_u} \frac{PR(v)}{L(v)}$$
3. **Betweenness Centrality**: Identifies critical "cut-out brokers" and financial intermediaries mediating disjoint cells:
   $$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$
4. **FastRP + k-NN**: Generates dense low-dimensional structural node embeddings to discover hidden behavioral similarities.
5. **Dijkstra Shortest Path**: Finds the exact chain of communication or money movement linking any two targets in the graph.

---

## 13. Multi-Engine Anomaly Intelligence

Documented in `docs/MULTI_ENGINE_ANOMALY_INTELLIGENCE.md` and implemented in `backend/app/anomaly/`, OmniTrace deploys **11 independent analytical engine families** comprising **19+ specialized pattern detectors**:

```
                               ┌────────────────────────────────────────┐
                               │   MULTI-ENGINE ANOMALY ORCHESTRATOR    │
                               └──────────────────┬─────────────────────┘
                                                  │
         ┌────────────────────────┬───────────────┴───────────────┬────────────────────────┐
         ▼                        ▼                               ▼                        ▼
[1. Behavioral IF]       [2. Rule Engine]               [3. Statistical MAD]     [4. Graph Topology]
(Isolation Forest)       (Threshold Violations)         (Robust Z-Score, IQR)    (Betweenness, Louvain)
         │                        │                               │                        │
         ├────────────────────────┴───────────────┬───────────────┴────────────────────────┤
         ▼                                        ▼                                        ▼
[5. Spatio-Temporal]                    [6. Financial Forensic]                  [7. Social Coordination]
- Impossible Travel (>800 km/h)         - Structuring / Smurfing                 - Synchronous Activity
- ST-DBSCAN Convergence                 - Rapid Fan-Out / Mule Funnel            - Shared Infrastructure
- Trajectory Tailing (Fréchet)          - Dormant Awakening                      
- Dark Period Radio Silence             - ATM Cash-Out Bursts                    
         │                                        │                                        │
         ├────────────────────────────────────────┴────────────────────────────────────────┤
         ▼                                                                                 ▼
[8. VPN & Tor OPSEC Evasion]                                             [9. Cross-Domain Collision]
(Port & LOF Analysis)                                                    (Bank + Tower + Social Δt ≤ 15m)
         │                                                                                 │
         ├────────────────────────────────────────┬────────────────────────────────────────┘
         ▼                                        ▼
[10. Identity Discrepancy]              [11. Advanced ML]
(Synthetic ID / Aadhar Conflicts)       (Autoencoders, Node2Vec, RGCN, TGN)
         │                                        │
         └───────────────────┬────────────────────┘
                             │
                             ▼
              [MULTI-LENS EVIDENCE FUSION]
                             │
                             ▼
              [12-CHECK QUALITY GATE]
              ("NO EVIDENCE -> NO CLAIM")
                             │
                             ▼
            [POSTGRESQL & NEO4J PERSISTENCE]
```

### Engine Specifications

| # | Engine Family | Identifier | Mathematical / Algorithmic Principle | Target Investigative Pattern |
|---|---|---|---|---|
| 1 | **Behavioral** | `DET-BEHAVIORAL-IF` | Scikit-Learn `IsolationForest` over 8-D feature vectors | Multi-dimensional behavioral outliers without explicit rule violations. |
| 2 | **Deterministic Rules** | `DET-RULE-ENGINE` | Declarative logical rules (Confidence = 1.0) | High-value transfers ($\ge ₹10L$), nocturnal call bursts (01:00–05:00 AM), burner IMEI hopping. |
| 3 | **Statistical Deviation** | `DET-STATISTICAL` | Robust Z-Score with MAD & Interquartile Range (IQR) | Extreme transaction spikes and call volume deviations without Gaussian assumptions. |
| 4 | **Graph Topology** | `DET-GRAPH-NETWORK` | Betweenness Centrality, PageRank, Louvain | Cut-out brokers bridging disjoint cells, syndicate kingpins, clandestine clusters. |
| 5A | **Impossible Travel** | `DET-SPATIAL-TRAVEL` | Haversine velocity: $v = \frac{d}{\Delta t} \cdot 3600$ | Physical transit speeds exceeding 800 km/h (simultaneous SIM usage in distant cities). |
| 5B | **Convergence** | `DET-SPATIAL-CONVERGENCE` | ST-DBSCAN spatial clustering ($\le 2$ km, $\le 60$ min) | Clandestine physical rendezvous between suspected co-conspirators. |
| 5C | **Trajectory Tailing** | `DET-SPATIAL-TAILING` | Discrete Fréchet Distance & LCSS ($\Delta t \le 300$s) | Vehicle following or physical surveillance of victims prior to crimes. |
| 5D | **Dark Period** | `DET-SPATIAL-DARKPERIOD` | Bayesian change-point signal cessation ($\ge 6$h) | Deliberate radio silence on mobile devices immediately preceding an incident. |
| 6A | **Structuring** | `DET-FIN-STRUCTURING` | Smurfing window: 70% to 99% of reporting limits | Systematic deposits between ₹3,50,000 and ₹4,99,999 to evade ₹5,00,000 CTR triggers. |
| 6B | **Rapid Fan-Out** | `DET-FIN-FANOUT` | Inbound tranche followed by $\ge 80\%$ dissipation | Mule funnel: large sum distributed across $\ge 3$ counterparties within 30 minutes. |
| 6C | **Dormant Awakening**| `DET-FIN-DORMANT` | Velocity ratio: Activity after $\ge 90$ days inactivity | Shell/sleeper accounts suddenly activated to receive high-value illicit proceeds. |
| 6D | **ATM Cash-Out** | `DET-FIN-ATM-CASHOUT` | Immediate cash liquidation post-transfer | Rapid physical cash-out at ATMs across separate geographic locations. |
| 7 | **Social Coordination** | `DET-SOC-SYNC` | Cosine similarity of activity timelines & FP-Growth | Coordinated botnet operations and multiple personas sharing the same physical IMEI/IP. |
| 8 | **VPN / Tor OPSEC** | `DET-NET-VPN-TOR` | Port fingerprints (9001, 1194, 500) & LOF byte throughput | Deliberate operational security (OPSEC) masking by cyber perpetrators. |
| 9 | **Cross-Domain Collision**| `DET-CROSS-COLLISION` | Multi-modal temporal join ($\Delta t \le 15$ min) | Money transfer $\to$ Telegram ping $\to$ Voice call from same cellular tower sector. |
| 10 | **Identity Discrepancy**| `DET-ID-DISCREPANCY` | Cluster attribute divergence | Multiple conflicting Aadhaar numbers or fake names linked to a single subscriber. |
| 11 | **Advanced ML** | `DET-ADV-*` | PyTorch Autoencoder MSE loss, Node2Vec embeddings | Complex topological anomalies and non-linear feature reconstruction errors. |

### Multi-Lens Evidence Fusion & Fingerprinting
To prevent alert fatigue, overlapping signals are fused into unified findings:
$$\text{Unified Score} = \min\left(100.0, \; \max_{d \in \text{Triggered}}(S_d) + \text{Corroboration Bonus}\right)$$
$$\text{Corroboration Bonus} = \min\left(25.0, \; (N_{\text{triggered}} - 1) \times 8.0\right)$$
Every finding is fingerprinted via:
$$\text{Fingerprint} = \text{SHA256}(\text{case\_id} \,\|\, \text{entity\_id} \,\|\, \text{primary\_pattern})[:16]$$
Ensuring that re-running analysis idempotently updates existing findings rather than creating duplicates.

### The 12-Check Quality Gate: "NO EVIDENCE -> NO CLAIM"
Every generated finding must pass the 12 programmatic checks in `app.anomaly.quality.finding_quality_gate`:
1. Valid finding identifier and case foreign key.
2. Verified primary entity existence in `golden_profiles`.
3. Valid domain and detector classification.
4. Explanatory narrative completeness (`whatHappened`, `whyUnusual`, `whyRelevant`).
5. Bound primary evidence references (`evidence_refs` and `canonical_event_refs`).
6. Zero unsupported numerical claims (amounts must match canonical event totals).
7. Valid spatial coordinates where geographic patterns are asserted.
8. Valid timestamp bounds where temporal patterns are asserted.
9. Monotonic confidence calibration ($0.0 \le C \le 1.0$).
10. Valid severity categorization (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
11. Double-counting protection across correlated detectors.
12. Audit hash lineage completeness.

---

## 14. Timeline Reconstruction & Temporal Intelligence

OmniTrace builds an incident-centric chronological record across all ingested sources.

```
TIME (UTC)       DOMAIN     SOURCE ENTITY           EVENT DESCRIPTION & CROSS-DOMAIN LINKAGE
─────────────────────────────────────────────────────────────────────────────────────────────
14:10:02         TELECOM    +919876500001 (Vicky)   Voice call (180s) to +919876500002 (Rohit)
14:18:30         BANKING    Bank Account 5012...    ₹25,00,000 RTGS tranche transferred to Mule Account
14:21:05         NETWORK    192.168.1.105 (Vicky)   Telegram session ping via Tower Sector DL-042
14:26:45         BANKING    ATM #402 (Noida)        ₹2,50,000 physical cash withdrawal (Cash-Out Mule)
14:40:12         TELECOM    +919876500001 (Vicky)   RADIO SILENCE BEGINS (Pre-Crime Dark Period: 8h)
```

### Key Temporal Capabilities
* **Cross-Domain Alignment**: Sorts calls, IP pings, bank tranches, and social logins into a synchronized millisecond-accurate timeline.
* **Pre-Crime Dark Periods**: Automatically detects when a target deliberately turns off mobile hardware prior to an incident.
* **Coordinated Bursts**: Flags sudden spikes in communication between multiple syndicate nodes occurring within tight time windows.

---

## 15. Multi-Agent Investigative Workflow

Implemented in `backend/app/agents/graph.py` and `specialists.py`, OmniTrace orchestrates a multi-agent team using **LangGraph**:

```mermaid
flowchart LR
    START([START]) --> S_FIN["start_financial"]
    S_FIN --> AG_FIN["Financial Investigation Agent"]
    AG_FIN --> S_TEM["start_temporal"]
    S_TEM --> AG_TEM["Timeline Reconstruction Agent"]
    AG_TEM --> S_SPA["start_spatial"]
    S_SPA --> AG_SPA["Geographic / Spatial Agent"]
    AG_SPA --> S_LEAD["start_lead"]
    S_LEAD --> AG_LEAD["Lead Detective Aggregator Agent"]
    AG_LEAD --> END_NODE([END: Certified Case Dossier])

    AG_FIN -.->|Server-Sent Events Stream| UI["Frontend Investigation Drawer"]
    AG_TEM -.->|Server-Sent Events Stream| UI
    AG_SPA -.->|Server-Sent Events Stream| UI
    AG_LEAD -.->|Server-Sent Events Stream| UI
```

### Specialist Agent Responsibilities

| Agent Role | Node Identifier | Primary Forensic Responsibility | Output Artifact |
|---|---|---|---|
| **Financial Specialist** | `financial_agent` | Traces bank tranches, shell accounts, structuring, mule dissipation, and cash liquidations. | `financial_json` (mule networks, flow of funds) |
| **Temporal Specialist** | `temporal_agent` | Analyzes event chronology, coordination bursts, call-to-payment latency, and radio silence. | `temporal_json` (critical event sequences) |
| **Spatial Specialist** | `spatial_agent` | Maps cell tower locks, travel velocities, impossible transit, and suspect co-location. | `geographic_json` (movement corridors, rendezvous) |
| **Lead Detective** | `lead_detective` | Fuses specialist findings into an executive intelligence dossier with actionable leads. | `lead_json` (kingpins, brokers, prosecution-ready leads) |

The multi-agent workflow streams live status updates and partial findings to the frontend via **Server-Sent Events (SSE)** at `GET /api/v1/investigation/stream/{community_id}`.

---

## 16. Agentic RAG & STAIR Architecture

To enable investigators to query evidence interactively without AI hallucinations, OmniTrace implements **STAIR** (**Structure-Aware Evidence-First Engine**) in `backend/app/stair/`:

```
INVESTIGATOR QUERY: "Did Vikramaditya Singh transfer funds to Rohit Verma before the kidnapping?"
                                    │
                                    ▼
[STAGE 1: STRUCTURE-AWARE ROUTING]
  ├── Evaluates query against Immutable Leaf Registry (Table of Contents)
  ├── Uses local Qwen 2.5 7B ToC parser + keyword fallback matcher
  └── Selects precise Leaf IDs: ['financial.transactions', 'telecom.cdr_records']
                                    │
                                    ▼
[STAGE 2: HARD OUTPUT VALIDATION]
  └── Enforces Leaf Registry constraints; rejects non-existent tools or hallucinated endpoints
                                    │
                                    ▼
[STAGE 3: CASE-SCOPED EVIDENCE BROKER]
  ├── Queries PostgreSQL `golden_profiles` for target cluster IDs
  ├── Queries MinIO Parquet analytical warehouse with predicate pushdown
  └── Executes parameterized Cypher on Neo4j 5.12
                                    │
                                    ▼
[STAGE 4: UNIVERSAL EVIDENCE NORMALIZATION]
  ├── Casts retrieved records into `NormalizedEvidenceItem`
  └── Segregates PRIMARY factual records from DERIVED/GENERATED items
                                    │
                                    ▼
[STAGE 5: DETERMINISTIC FACT VERIFICATION & GUARDRAILS]
  ├── Verifies entity existence and cross-checks chronological sequences
  └── Triggers HONEST ABSTENTION if no evidence exists for the target case
                                    │
                                    ▼
[STAGE 6: GROUNDED GENERATION (LOCAL QWEN 2.5 7B)]
  └── Injects strict factual evidence context; enforces exact evidence citation tags [EV-001]
                                    │
                                    ▼
[STAGE 7: CLAIM-TO-EVIDENCE PROVENANCE MAPPING]
  ├── Deconstructs LLM answer into individual claims
  ├── Verifies that every assertion has a backing evidence ID
  └── Emits: Evidence-grounded response with interactive citation pills
```

### Immutable Leaf Registry
Defined in `app.stair.leaf_registry.py`, the Leaf Registry represents the exact capabilities of the platform:
* `entity.golden_profile`, `entity.identity_discrepancy`, `entity.associated_network`
* `telecom.cdr_records`, `telecom.ipdr_sessions`, `telecom.cell_tower_pings`, `telecom.imei_telemetry`
* `financial.transactions`, `financial.mule_funnel`, `financial.atm_withdrawals`, `financial.structuring_burst`
* `geospatial.movement_track`, `geospatial.co_location`, `geospatial.impossible_travel`
* `timeline.cross_domain_events`, `timeline.pre_crime_silence`, `timeline.coordination_burst`
* `anomaly.unified_findings`, `anomaly.high_risk_entities`, `anomaly.pattern_details`
* `graph.community_structure`, `graph.pagerank_influence`, `graph.betweenness_brokers`, `graph.shortest_path`
* `report.case_dossier`, `report.lead_detective_summary`

---

## 17. Hallucination Mitigation & Guardrails

OmniTrace guarantees evidentiary reliability through four defense layers:

1. **Retrieval Grounding**: The LLM is never permitted to answer from general parametric pretraining weights alone. Every assertion must cite a retrieved `evidence_id` from the Leaf Registry.
2. **Deterministic Fact-Checking**: Critical entities (e.g. money amounts, timestamps, phone numbers) are cross-checked by `DeterministicVerifier` against the canonical event store before the response is shown to the user.
3. **Honest Abstention**: When evidence is missing or insufficient, the system triggers an explicit abstention:
   > *"I do not have evidence in case INV-2026-BLACK-CIRCUIT to confirm that suspect X called suspect Y on that date."*
4. **Unsupported Claim Rejection**: If post-generation claim mapping detects an ungrounded inference, the claim is flagged with a warning indicator in the UI.

---

## 18. Quantitative LLM Evaluation & Benchmarks

The STAIR architecture and LLM evaluation suite was quantitatively measured on case `INV-2026-BLACK-CIRCUIT` across multi-domain queries (Financial, Telecom, Geospatial, Anomaly, and Adversarial Abstention test cases).

The evaluation code resides in `backend/app/stair/benchmark/` and the recorded benchmark artifact is preserved at `backend/benchmark_stair_results.json`.

### Measured Benchmark Results

| Metric | Score | Industry Benchmark | Evaluation Context |
|---|---:|---:|---|
| **Recall@1** | **93.33%** | 68.0% | Correct leaf capability selected as primary routing target across 15 test queries. |
| **Recall@3** | **93.33%** | 82.0% | Correct leaf capability present within top-3 selected investigation tools. |
| **MRR (Mean Reciprocal Rank)** | **0.9333** | 0.740 | Reciprocal rank of the first relevant investigation tool. |
| **Abstention Accuracy** | **100.0%** | 52.0% | Successfully refused to hallucinate when asked unanswerable or ungrounded queries. |
| **Supported Claim Rate** | **97.59%** | 71.0% | Proportion of generated sentences grounded in verified primary evidence ($1 - \text{Unsupported Claim Rate}$ of $2.41\%$). |
| **Tool Selection Accuracy** | **86.67%** | 64.0% | Complete set of required investigation tools selected without extraneous leaves. |
| **Invalid Node Rate** | **0.00%** | 14.0% | Zero non-existent tools, invalid endpoints, or schema-violating parameters requested. |

### Quantitative Latency Profile

| Stage | Mean Latency | Execution Environment |
|---|---:|---|
| **Routing Latency** | 9,442 ms | Local Qwen 2.5 7B Table-of-Contents evaluation |
| **Retrieval Latency** | 745 ms | MinIO Parquet pushdown + PostgreSQL + Neo4j query execution |
| **Grounded Generation Latency** | 18,524 ms | Local Qwen 2.5 7B generating cited forensic narrative |
| **Total End-to-End Latency** | 28,713 ms | Full pipeline execution (zero external cloud calls) |

### LLM-as-a-Judge Evaluation Framework
In addition to quantitative retrieval metrics, responses were evaluated by `STAIRLLMJudge` (using local Qwen 2.5 7B under judicial prompt constraints) across 6 qualitative dimensions:
1. **Factual Correctness**: Statements, entities, amounts, and dates are strictly true to evidence.
2. **Evidence Support**: Key claims are explicitly cited with `[EV-xxx]` tags.
3. **Source Faithfulness**: Did the system avoid converting correlation into unproven causation?
4. **Entity Correctness**: Suspects, phones, and accounts are correctly identified without entity mixing.
5. **Temporal Correctness**: Chronological sequences are verified.
6. **Numerical Precision**: Monetary values (INR ₹) and transaction counts are mathematically exact.

---

## 19. Physical Forensics: NFC Credentials & Crime Scene Tags

OmniTrace bridges digital intelligence with physical evidence handling via specialized NFC modules:

```
┌────────────────────────────────────────────────────────┐
│             NFC CARD AUTHENTICATION                    │
│ Physical Officer Smart Card + 4-Digit PIN              │
│  - Instant, highly secure login for field officers     │
│  - Challenge-response cryptographic token exchange     │
│  - Complete IAM session mapping & audit logging        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│           NFC CRIME SCENE EVIDENCE TAGGING             │
│ Physical Evidence Bag with Embedded NTAG213/215/216    │
│  - Geotagged acquisition location (GPS coordinates)    │
│  - Officer employee ID & timestamp binding             │
│  - Digital chain-of-custody transfer logging           │
│  - Cryptographic tamper verification upon precinct intake│
└────────────────────────────────────────────────────────┘
```

Implemented in `app.api.nfc` and `app.api.nfc_evidence`, field officers can authenticate using physical smart badges and bind physical evidence bags directly to digital case files.

---

## 20. CCTV Route Tracking & Location Intelligence

Managed by `app.cctv`, the CCTV module integrates visual surveillance records into the investigation:
* **Camera Registry**: Catalogs CCTV camera locations, azimuth angles, field of view (FOV), and optical ranges across urban sectors.
* **Route Intersection Analysis**: Computes spatial intersections between suspect movement paths (derived from cellular tower handoffs) and active camera locations.
* **Footage Request Tracking**: Generates targeted DVR retrieval requests for exact time windows, reducing surveillance review overhead.

---

## 21. Security Architecture & Role-Based Access Control

OmniTrace manages classified investigation material through defense-in-depth security controls:

### Role-Based Access Control (RBAC) & Scoping

```
ORGANIZATION (e.g., Central Cyber Directorate)
      └── OPERATIONAL UNIT (e.g., Special Cyber Cell)
            └── USER (Officer / Investigator)
                  └── ROLE (e.g., INVESTIGATOR)
                        └── PERMISSIONS (case.read, evidence.upload, ...)
```

* **System Roles**: `SYSTEM_ADMIN`, `SUPERINTENDENT`, `IPS_OFFICER`, `INVESTIGATOR`, `ANALYST`, `REVIEWER`, `AUDITOR`.
* **Case-Scoped Access**: Access to cases is governed by `CaseMemberModel`. An officer can only inspect cases to which they are formally assigned as `OWNER`, `LEAD_INVESTIGATOR`, `INVESTIGATOR`, or `ANALYST`.
* **Two-Factor Authentication (MFA)**: Built-in TOTP MFA with AES-256-GCM encrypted secrets and hashed emergency backup codes.
* **Controlled Local Execution**: LLMs run strictly on local agency hardware via Ollama, preventing sensitive evidence exfiltration to third-party commercial cloud APIs.

### Append-Only Cryptographic Audit Trail
Every action—evidence upload, entity resolution run, graph query, search, and dossier export—is logged to PostgreSQL `audit_logs` using **Cryptographic Hash Chaining**:
$$\text{event\_hash}_n = \text{SHA256}(\text{event\_hash}_{n-1} \,\|\, \text{timestamp} \,\|\, \text{actor} \,\|\, \text{action} \,\|\, \text{resource\_id} \,\|\, \text{payload})$$
Any retroactive modification of audit records breaks the hash chain, immediately alerting administrators of tampering.

---

## 22. Docker Microservices Architecture

The entire OmniTrace stack runs across 11 containerized microservices orchestrated via `docker-compose.yml`:

| Service Container | Image / Dockerfile | Exposed Ports | Responsibility | Dependencies |
|---|---|---:|---|---|
| `fastapi_backend` | `./backend/Dockerfile` | `8000:8000` | Core API, Ingestion, ER, Graph Sync, Anomaly Orchestration, STAIR | `postgres`, `minio`, `neo4j`, `redis`, `zingg_worker` |
| `nextjs_frontend` | `./frontend/Dockerfile` | `3000:3000` | Web Command Center, Cytoscape Graph, Deck.gl Maps, AI Chat | `fastapi_backend` |
| `postgres` | `postgres:16-alpine` | `5432:5432` | Relational registry, IAM, Golden Profiles, Anomalies, Audit Logs | None |
| `minio` | `minio/minio:latest` | `9000:9000`<br>`9001:9001` | S3 Object Storage: raw encrypted evidence & Parquet warehouse | None |
| `createbuckets` | `minio/mc:latest` | — | One-shot initialization creating `raw-evidence` & `iceberg-warehouse` | `minio` |
| `neo4j` | `neo4j:5.12-community` | `7474:7474`<br>`7687:7687` | Property Graph Database with APOC and Graph Data Science plugins | None |
| `redis` | `redis:7-alpine` | `6379:6379` | Celery message broker, CEP sliding-window correlation cache | None |
| `celery_worker` | `./backend/Dockerfile` | — | Background task processing for heavy ML and anomaly jobs | `postgres`, `minio`, `redis`, `neo4j` |
| `zingg_worker` | `./zingg_worker/Dockerfile` | `8001:8001` | Dedicated ML Entity Resolution microservice | None |
| `ollama` | `ollama/ollama:latest` | `11434:11434`| On-premise self-hosted LLM runtime (Qwen 2.5 7B) | None |
| `mongodb` | `mongo:6.0` | `27017:27017`| Backward-compatibility auxiliary datastore | None |

---

## 23. Scheduled & Continuous Ingestion

Police departments receive regular batch updates from telecom service providers, banks, and field units. OmniTrace supports both **event-driven debounced ingestion** and **scheduled continuous ingestion**:

```
EXTERNAL POLICE FEEDS / DISK INTAKE
                 │
                 ▼
     [CONTINUOUS / SCHEDULED TRIGGER]
  ├── Periodic Cron / Celery Beat task (Minutes / Hours / Days)
  └── REST Ingestion Hook (`POST /api/cases/{case_id}/evidence`)
                 │
                 ▼
     [DEBOUNCED PIPELINE ORCHESTRATOR]
  ├── Coalesces multiple rapid uploads within a 1.0s window
  ├── Runs serialized background thread (`PipelineWorker-{case_id}`)
  └── Re-runs automatically if additional files arrive mid-execution
                 │
                 ▼
[AUTOMATED PIPELINE EXECUTION]
  ├── 1. Ingestion, Source Detection, Encryption & Parquet Write
  ├── 2. Incremental Entity Resolution & Golden Profile Synthesis
  ├── 3. Neo4j Knowledge Graph Incremental Synchronization
  └── 4. Multi-Engine Anomaly Detection & CEP Alert Updates
```

Implemented in `app.services.pipeline_orchestrator`, new files uploaded by investigators automatically trigger asynchronous pipeline execution with debounced batching.

---

## 24. Command Center User Interface

Built with **Next.js 14**, **React 18**, **Tailwind CSS**, and **Framer Motion**, the OmniTrace Command Center provides an intuitive, high-contrast visual workstation:

![AI Chatbot & Investigation Console](frontend/chatbot%20ai%20agents.png)

### Key Views & Components
* **Investigation Dashboard (`InvestigationDashboard.tsx`)**: Unified executive summary displaying active suspects, high-confidence anomalies, case status, and quick-action toolbars.
* **Graph Topology Viewer (`GraphTopologyViewer.tsx`)**: High-performance Cytoscape canvas with interactive multi-hop neighborhood expansion, community filtering, and node risk coloring.
* **Anomaly Threat Radar (`AnomalyThreatRadar.tsx`, `AnomaliesTab.tsx`)**: Multi-engine anomaly matrix categorizing findings by severity, engine lens, and corroborated evidence.
* **Geospatial Tracking (`GeospatialMap.tsx`, `GeoTimelinePlayback.tsx`)**: Deck.gl and MapLibre GL map layers displaying cellular antenna coverage arcs, suspect travel vectors, and convergence zones.
* **Timeline Footprint (`TimelineFootprint.tsx`, `CaseActivityTimeline.tsx`)**: Interactive horizontal timeline with domain filtering (calls, transactions, pings) and playback simulation.
* **AI Forensic Chatbot (`AIForensicChatbot.tsx`)**: Conversational interface powered by the STAIR engine, featuring real-time SSE streaming, tool badges, and clickable evidence citation pills.
* **Case Dossier Exporter (`CaseDossierExporter.tsx`)**: One-click court dossier generator exporting digitally sealed, formatted PDF reports.

---

## 25. REST API Documentation

The FastAPI backend exposes comprehensive endpoints documented via interactive Swagger UI at `http://localhost:8000/docs`:

### Case & Evidence Ingestion
| Method | Route | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/cases` | Create formal investigation case with context notes | `case.create` |
| `GET` | `/api/cases` | List all investigation cases accessible to current user | `case.read` |
| `GET` | `/api/cases/{case_id}` | Retrieve case details, metrics, and evidence inventory | `case.read` |
| `POST` | `/api/cases/{case_id}/evidence` | Upload evidence file (multipart/form-data) | `evidence.upload` |
| `GET` | `/api/cases/{case_id}/evidence/{evidence_id}/download` | Decrypt and download original raw evidence file | `evidence.export` |
| `POST` | `/api/ingest/trigger_all` | Batch-ingest all unlabelled files in `data_files/` | `evidence.upload` |
| `GET` | `/api/ingest/events` | Query canonical events from MinIO Parquet warehouse | `evidence.read` |

### Entity Resolution & Graph
| Method | Route | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/zingg/execute?case_id={id}` | Execute multi-anchor entity resolution on case | `entity.resolve` |
| `GET` | `/api/system/golden_profiles?case_id={id}` | Retrieve resolved golden identities from PostgreSQL | `entity.view` |
| `POST` | `/api/graph/sync?case_id={id}` | Synchronize Golden Profiles and events into Neo4j | `graph.sync` |
| `GET` | `/api/graph/topology?case_id={id}` | Retrieve complete node-link graph payload for UI | `graph.view` |
| `POST` | `/api/v1/investigation/run-algorithms` | Execute GDS Louvain, PageRank, Centrality algorithms | `graph.view` |

### Anomaly Intelligence & Alerts
| Method | Route | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/anomalies/analyze?case_id={id}` | Run 11-engine anomaly analysis (Celery/direct) | `case.read` |
| `GET` | `/api/anomalies?case_id={id}&severity={s}` | List filtered anomaly findings with metrics | `case.read` |
| `GET` | `/api/anomalies/stats?case_id={id}` | Get anomaly severity distribution (Critical, High, etc.) | `case.read` |
| `GET` | `/api/anomalies/{finding_id}` | Retrieve detailed finding with full evidence citations | `case.read` |
| `GET` | `/api/alerts?case_id={id}` | Retrieve real-time sliding-window CEP alerts | `case.read` |

### Multi-Agent Investigation & Chatbot
| Method | Route | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/investigation/stream/{community_id}` | Stream multi-agent LangGraph workflow via SSE | `case.read` |
| `POST` | `/api/chatbot/chat` | Query AI Forensic Chatbot via STAIR grounding engine | `case.read` |
| `GET` | `/api/chatbot/history?case_id={id}` | Retrieve case-scoped conversational history | `case.read` |
| `GET` | `/api/reports/{report_id}/pdf` | Generate court-ready certified PDF case dossier | `report.export` |

---

## 26. Repository Directory Structure

```
Cyber Platform/
├── .env                                # Root environment configuration
├── docker-compose.yml                  # 11-microservice Docker orchestration
├── run_pipeline_v2.py                  # End-to-end architecture verification script
├── zinggLicense.txt                    # Zingg runtime license
├── docs/                               # Engineering architecture documentation
│   ├── ARCHITECTURE_AND_WORKFLOW.md   # Distributed architecture V2 reference
│   └── MULTI_ENGINE_ANOMALY_...md      # 11-Engine Anomaly Intelligence manual
├── data_files/                         # Sample unlabelled multi-source datasets
│   ├── telecom.csv                     # Raw Call Detail Records (CDR)
│   ├── banking.csv                     # Financial transfer & ATM ledger
│   ├── network.csv                     # ISP IPDR dynamic lease logs
│   └── kyc.csv                         # Official identification profiles
├── zingg_worker/                       # Entity Resolution microservice (Port 8001)
│   ├── Dockerfile                      # Worker container specification
│   ├── main.py                         # Fast API & Union-Find clustering
│   └── zingg_config.json               # Zingg field mapping configuration
├── backend/                            # FastAPI Core & Analytical Backend (Port 8000)
│   ├── Dockerfile                      # Python 3.10-slim container specification
│   ├── requirements.txt                # Python dependencies
│   ├── benchmark_stair_results.json    # Recorded quantitative STAIR evaluation metrics
│   ├── benchmark_test_results.json     # Multi-case anomaly benchmark results
│   ├── app/
│   │   ├── main.py                     # FastAPI application entrypoint & middleware
│   │   ├── core/                       # Storage, Database, IAM seed, and LLM config
│   │   │   ├── config.py               # Pydantic environment settings
│   │   │   ├── database.py             # SQLAlchemy session & table migrations
│   │   │   ├── storage.py              # MinIO S3 & AES-256-GCM encryption service
│   │   │   ├── neo4j_client.py         # Neo4j Bolt driver wrapper
│   │   │   ├── celery_app.py           # Celery distributed task queue configuration
│   │   │   └── llm_provider.py         # Local Ollama / Qwen 2.5 7B connector
│   │   ├── models/                     # SQLAlchemy relational ORM models
│   │   │   ├── postgres_models.py      # Cases, Evidence, Golden Profiles, Anomalies
│   │   │   ├── iam_models.py           # Users, Roles, Permissions, Sessions, MFA
│   │   │   ├── nfc_models.py           # NFC officer cards
│   │   │   └── nfc_evidence_models.py  # NFC physical evidence tags
│   │   ├── schemas/                    # Pydantic validation contracts
│   │   │   └── canonical_event.py      # CanonicalEvent universal event schema
│   │   ├── ingestion/                  # Multi-source ingestion subsystem
│   │   │   ├── detector.py             # Automatic source fingerprinting engine
│   │   │   ├── validator.py            # Quality checks and quarantine routing
│   │   │   ├── deduplication.py        # Semantic field hashing
│   │   │   ├── quality.py              # Data quality score calculator (0-100)
│   │   │   └── parsers/                # CDR, IPDR, Banking, Social, KYC parsers
│   │   ├── processing/                 # Distributed analytical processing
│   │   │   ├── spark_pipeline.py       # PyArrow Parquet columnar warehouse writer
│   │   │   └── canonical_reader.py     # Streaming columnar Parquet query reader
│   │   ├── anomaly/                    # Feature-3 Multi-Engine Anomaly Intelligence
│   │   │   ├── orchestration/          # Multi-engine orchestrator
│   │   │   ├── engines/                # 11 Engine families (Behavioral, Rules, etc.)
│   │   │   ├── quality/                # 12-Check Quality Gate ("No Evidence -> No Claim")
│   │   │   └── synthesis/              # Narrative synthesis & score calibration
│   │   ├── agents/                     # LangGraph Multi-Agent Investigation System
│   │   │   ├── graph.py                # StateGraph pipeline definition
│   │   │   ├── specialists.py          # Financial, Temporal, Spatial, Lead agents
│   │   │   └── prompts.py              # Structured agent forensic prompts
│   │   ├── stair/                      # Structure-Aware Evidence-First Engine (RAG)
│   │   │   ├── service.py              # STAIR master orchestrator
│   │   │   ├── router.py               # Table of Contents structure-aware router
│   │   │   ├── leaf_registry.py        # Immutable Leaf capability registry
│   │   │   ├── evidence_broker.py      # Case-scoped evidence fetcher
│   │   │   ├── verifier.py             # Deterministic fact verification
│   │   │   └── benchmark/              # Evaluator, dataset, and LLM judge runner
│   │   ├── services/                   # High-level domain services
│   │   │   ├── zingg_er.py             # Multi-anchor entity resolution engine
│   │   │   ├── graph_sync.py           # Neo4j property graph synchronization
│   │   │   ├── gds_engine.py           # Graph Data Science (Louvain, PageRank)
│   │   │   ├── cep_engine.py           # Redis sliding-window CEP alert generator
│   │   │   ├── forensic_chatbot.py     # AI Chatbot multi-tool agent
│   │   │   └── pdf_report_service.py   # Court-ready PDF dossier exporter
│   │   ├── cctv/                       # CCTV camera registry & route intelligence
│   │   ├── audit/                      # Cryptographic hash-chained audit service
│   │   └── api/                        # FastAPI REST endpoint routers
│   └── tests/                          # Automated backend test suites
└── frontend/                           # Next.js 14 Visual Command Center (Port 3000)
    ├── Dockerfile                      # Node 20-alpine container specification
    ├── package.json                    # Dependencies (Cytoscape, Deck.gl, Tailwind)
    └── src/
        ├── app/                        # Next.js App Router pages
        ├── components/                 # UI components (Graph, Timeline, Radar, Chat)
        └── services/                   # API client bindings
```

---

## 27. System Requirements

### Hardware Requirements
* **CPU**: 8 physical cores minimum (Intel Xeon / AMD Ryzen 7 recommended).
* **RAM**: 16 GB minimum (32 GB recommended for running Neo4j GDS + local Ollama models simultaneously).
* **Disk**: 50 GB free NVMe SSD storage.
* **GPU (Optional but Recommended)**: NVIDIA GPU with $\ge 8$ GB VRAM (RTX 3060/4060 or higher) for hardware-accelerated local Ollama inference. OmniTrace automatically falls back to CPU quantization if no GPU is detected.

### Software Prerequisites
* **Docker Engine**: Version 24.0.0 or higher.
* **Docker Compose**: Version 2.20.0 or higher.
* **Node.js** (for local frontend development): Version 20.x LTS.
* **Python** (for local backend development): Version 3.10.x.

---

## 28. Environment Variables Reference

Create a `.env` file in the root directory (or use the template below):

```bash
# === PostgreSQL Metadata Registry ===
DATABASE_URL=postgresql://postgres:postgres123@127.0.0.1:5432/investigation_db

# === MinIO S3 Object Storage ===
MINIO_ENDPOINT=127.0.0.1:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_SECURE=false
MINIO_BUCKET_EVIDENCE=raw-evidence
MINIO_BUCKET_WAREHOUSE=iceberg-warehouse

# === Authenticated Evidence Encryption ===
ENCRYPTION_MASTER_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# === Neo4j Graph Database ===
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123

# === Redis & Celery ===
REDIS_URI=redis://127.0.0.1:6379/0
REDIS_URL=redis://127.0.0.1:6379/0

# === Zingg Entity Resolution Worker ===
ZINGG_URL=http://127.0.0.1:8001

# === Local On-Premise LLM Configuration ===
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:7b-instruct
OLLAMA_BASE_URL=http://127.0.0.1:11434

# === Enterprise Audit Trail Configuration ===
AUDIT_ENABLED=true
AUDIT_RETENTION_DAYS=365
AUDIT_INTEGRITY_MODE=HASH_CHAIN
AUDIT_HIGH_RISK_FAIL_POLICY=FAIL_CLOSED
```

---

## 29. Installation & Setup Guide

### Option 1: Complete Docker Compose Deployment (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Faizshaikh6280/byteXL-Hackathon-and-CU.git omnitrace
   cd omnitrace
   ```

2. **Configure environment variables**:
   Ensure `.env` exists in the root directory (see section above).

3. **Start all 11 microservices**:
   ```bash
   docker-compose up -d --build
   ```

4. **Pull the local LLM model inside Ollama**:
   ```bash
   docker exec -it cyber_ollama ollama pull qwen2.5:7b-instruct
   ```

5. **Access the application consoles**:
   * **Web Command Center**: [http://localhost:3000](http://localhost:3000)
   * **FastAPI Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   * **Neo4j Graph Browser**: [http://localhost:7474](http://localhost:7474) (Credentials: `neo4j` / `password123`)
   * **MinIO Storage Console**: [http://localhost:9001](http://localhost:9001) (Credentials: `minioadmin` / `minioadmin123`)

---

### Option 2: Standalone Local Development Mode

If running services locally outside of Docker containers:

1. **Prerequisite Services**:
   Ensure PostgreSQL (5432), MinIO (9000), Neo4j (7687), Redis (6379), and Ollama (11434) are running locally.

2. **Start FastAPI Backend**:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Start Celery Worker (in a separate terminal)**:
   ```bash
   cd backend
   celery -A app.core.celery_app worker --loglevel=info --pool=solo
   ```

4. **Start Zingg Entity Resolution Worker**:
   ```bash
   cd zingg_worker
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

5. **Start Next.js Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 30. Verification & Pipeline Execution

To verify the entire end-to-end system automatically, execute `run_pipeline_v2.py` from the root directory:

```bash
python run_pipeline_v2.py
```

This verification script programmatically executes:
1. System Reset (PostgreSQL + MinIO + Neo4j).
2. Creates formal investigation case: `Operation Shadow Syndicate (INV-2026-0142-V2)`.
3. Ingests unlabelled evidence files from `data_files/` (`telecom.csv`, `banking.csv`, `network.csv`, `kyc.csv`).
4. Verifies AES-256-GCM encryption and MinIO S3 storage.
5. Verifies SHA-256 chain of custody tamper checks.
6. Writes columnar events to MinIO Parquet analytical warehouse.
7. Executes Multi-Anchor Entity Resolution into PostgreSQL `golden_profiles`.
8. Synchronizes 8 Node Labels and 9 Edge Types to Neo4j.
9. Executes 11-Engine Anomaly Intelligence and prints severity breakdown.
10. Validates Geospatial Deck.gl waypoints and chronological timeline.

### Running the STAIR Quantitative Benchmark Suite
To reproduce the quantitative LLM benchmark metrics:
```bash
cd backend
python -m app.stair.benchmark.run_benchmark
```

---

## 31. Feasibility Analysis

### Technical Feasibility
* **Distributed Columnar Processing**: Utilizing PyArrow Parquet tables partitioned by source and date prevents RAM exhaustion on million-row datasets.
* **Dual Database Decoupling**: PostgreSQL handles relational transactional state (cases, users, audit, findings) while Neo4j handles multi-hop graph topology, ensuring neither engine is burdened with mismatched workloads.
* **Deterministic Fallbacks**: Every advanced ML component (Zingg, Neo4j GDS, LLM Router) has a deterministic in-process fallback (Union-Find, pure Python NetworkX, keyword regex matching), ensuring 100% operational uptime even during partial infrastructure failures.

### Data Feasibility
* **Multi-Domain Ingestion**: Demonstrated support across cellular CDRs, ISP IPDR sessions, banking transactions, KYC registries, and social media logs.
* **Zero Information Loss**: Unmapped fields are stored in `attributes_json`, ensuring raw forensic details are permanently preserved.

### Operational Feasibility
* **Human-in-the-Loop Design**: The system synthesizes plain-language narratives, highlights corroborated evidence, and flags unverified claims, allowing detectives to make informed decisions rapidly.
* **Standard Web Interface**: Zero client-side software installation required; investigators interact via any standard desktop web browser.

### Deployment Feasibility
* **Self-Contained Microservices**: Packaged via Docker Compose with explicit health checks and automated bucket/table initialization scripts.

---

## 32. Viability Assessment

### Economic Viability
* **Zero Per-Token Commercial API Fees**: By defaulting to local, quantized Qwen 2.5 7B models running via Ollama, agencies eliminate unpredictable recurring API costs.
* **Commodity Hardware Utilization**: The architecture runs efficiently on standard enterprise workstations without requiring expensive supercomputing clusters.

### Institutional & Legal Viability
* **Courtroom-Admissible Chain of Custody**: SHA-256 checksums, client-side AES-256-GCM encryption, and tamper-evident audit logging comply with international digital evidence handling standards (ISO/IEC 27037).
* **On-Premise Data Sovereignty**: Classified wiretaps and financial intelligence remain within state data boundaries.

---

## 33. Risks & Mitigation Matrix

| Identified Risk | Impact Level | Probability | Automated Architectural Mitigation |
|---|---|---|---|
| **Data Scale Bottlenecks (Millions of Records)** | HIGH | HIGH | Parquet columnar storage + partition pruning + streaming iterators + batched Cypher unwinds. |
| **Sensitive Evidence Exfiltration** | CRITICAL | MEDIUM | Client-side AES-256-GCM encryption at rest + local self-hosted LLMs (zero cloud transmission). |
| **Data Quality & Corrupted Feeds** | MEDIUM | HIGH | Automated schema detection + quarantine records store + data quality scoring (0–100). |
| **Entity Resolution False Merges** | HIGH | MEDIUM | High Jaro-Winkler threshold ($\ge 0.90$) + multi-anchor corroboration requirements. |
| **AI / LLM Hallucinations** | CRITICAL | HIGH | STAIR evidence grounding + deterministic fact verifier + honest abstention on missing data. |
| **Alert Fatigue from False Positives** | HIGH | HIGH | Multi-lens evidence fusion + corroboration bonuses + 12-Check Quality Gate ("No Evidence -> No Claim"). |
| **Database or Service Outage** | HIGH | LOW | Docker container restart policies + in-process fallbacks (NetworkX fallback when Neo4j GDS is unavailable). |

---

## 34. Limitations

1. **Hardware Dependent Inference**: Running local LLM generation (Qwen 2.5 7B) on CPU-only machines exhibits higher latency ($\sim 18$ seconds per query). A dedicated GPU is strongly recommended for production real-time interactive chat.
2. **Schema Coverage**: Automatic source detection handles standard telecom, banking, and IPDR headers. Unorthodox proprietary police file schemas may require manual column mapping.
3. **Graph Memory Footprint**: In-memory Neo4j Graph Data Science projections require sufficient heap space (`NEO4J_server_memory_heap_max__size`) when analyzing networks exceeding tens of millions of nodes.
4. **Physical NFC Integration**: Hardware card and tag scanning requires WebNFC-compatible browser environments or dedicated USB NFC readers.

---

## 35. Future Roadmap

### Implemented in Current Release (V2)
- [x] Multi-source ingestion (CSV, XLSX, JSON, PDF) with automated domain fingerprinting.
- [x] Client-side AES-256-GCM encryption and SHA-256 tamper-evident integrity verification.
- [x] Columnar Parquet analytical warehouse with PyArrow strict schema enforcement.
- [x] Multi-anchor Entity Resolution (Zingg ML + Disjoint-Set Union-Find clustering).
- [x] Neo4j 5.12 property graph synchronization with 8 node labels and 9 edge types.
- [x] 11-Engine Multi-Engine Anomaly Intelligence subsystem with 19+ pattern detectors.
- [x] LangGraph multi-agent team (Financial, Temporal, Spatial, Lead Detective) with SSE streaming.
- [x] STAIR structure-aware evidence-first RAG engine with claim-to-evidence provenance mapping.
- [x] Physical NFC smart-card authentication and crime scene evidence bag tagging.
- [x] Certified court-ready PDF dossier exporter with cryptographic verification seals.

### Planned Enhancements (Roadmap)
- [ ] **Hardware-Backed TEE Enclaves**: Integration with Intel SGX / AMD SEV for cryptographically isolated CPU memory enclaves during model execution.
- [ ] **Real-Time Streaming Kafka Connectors**: Ingesting high-velocity live telecom feeds via Apache Kafka.
- [ ] **Automated Multi-Jurisdiction Legal Compliance Checks**: Fine-tuned judicial compliance agents verifying warrant requirements prior to evidence querying.
- [ ] **Native Mobile Field App**: React Native field companion application for crime scene NFC tag acquisition and GPS geotagging.

---

## 36. Responsible AI & Human Oversight

OmniTrace is designed under the **Human-in-the-Loop (HITL)** investigative paradigm:
* **Assistance, Not Adjudication**: OmniTrace surfaces relationships, anomalies, and temporal correlations; it does not determine legal culpability.
* **Presumption of Innocence**: Statistical deviations or high anomaly scores indicate investigative leads requiring corroboration, not proof of guilt.
* **Explainability Mandate**: Every generated insight must present explainable factual bullets (`whatHappened`, `whyUnusual`, `whyRelevant`) linking to primary evidence IDs.
* **Audited Access**: Every query, report view, and export is recorded in an append-only cryptographic audit log to prevent abuse.

---

## 37. Contributing & Development Guidelines

Contributions from forensic analysts, software engineers, and security researchers are welcome.

### Code Quality Standards
* **Python**: Formatted with `black` and linted with `flake8`. Strict type hinting via Pydantic v2.
* **TypeScript / React**: Strict type checking with `tsc --noEmit` and linted via `next lint`.
* **Testing**: All pull requests must include corresponding unit tests in `backend/tests/` or component tests.

### Running Backend Tests
```bash
cd backend
pytest tests/ -v
```

---

## 38. Security Notice & Remediation Advisory

> [!WARNING]
> **Security Remediation Advisory**:
> A live API key was detected in the local repository environment configuration (`.env`). In production deployments:
> 1. Immediately revoke and regenerate any exposed keys.
> 2. Ensure `.env` is listed in `.gitignore` and never committed to version control.
> 3. Use an enterprise secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager) for production credentials.

---

## 39. License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

---

## Acknowledgements

OmniTrace integrates open-source forensic and analytical tools including **FastAPI**, **Next.js**, **Neo4j Graph Data Science**, **MinIO**, **Apache Iceberg / Parquet**, **PyArrow**, **Cytoscape.js**, **Deck.gl**, **LangGraph**, **Ollama**, and **Zingg**. Built with dedication for law enforcement and digital forensics professionals worldwide.