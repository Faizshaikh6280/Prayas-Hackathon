# Prayas-Hackathon

## Unified Cyber-Intelligence & Forensic Analytics Platform

An enterprise-grade, full-stack Cyber-Intelligence, Data Forensics, and High-Performance Web Application built for law enforcement, intelligence, and financial investigation agencies.

---

## 🌟 Key Architecture & Capabilities

1. **Multi-Source Ingestion & Evidence Vault**: Extensible `BaseIngestor` adapter pattern for CDR, Bank, IPDR, Social Media CSVs, and PDF files. Cryptographic SHA-256 chain-of-custody seals applied upon upload.
2. **Deterministic & Probabilistic Entity Resolution (Zingg)**: Entity linkage engine to resolve aliases across names, phone numbers, IP addresses, and accounts into unified `golden_entity_id` profiles.
3. **Dual Persistence Layer**:
   - **MongoDB**: Raw document storage with spatial indexing for geospatial radius queries.
   - **Neo4j**: Topology graph store supporting multi-hop Cypher queries and relational path analysis.
4. **Hybrid Anomaly Engine & Real-Time Alerts**:
   - 19 analytical pattern engines (Structuring, ATM Cash-Out, Coordinated Flow, Impossible Travel, Convergence, Tailing, Digital Footprint) with unified evidence fusion.
   - Unsupervised Isolation Forest model and Neo4j Graph Data Science smurfing cycle & centrality detection.
5. **STAIR Structure-Aware Evidence-First Engine**:
   - Zero hallucination conversational forensic analysis powered by local LLM (`qwen2.5:7b-instruct`).
   - Claim verification and leaf evidence grounding.
6. **Command Center UI**:
   - Built with Next.js (App Router), React, Tailwind CSS, Cytoscape.js, MapLibre GL, and Framer Motion.
   - High-contrast investigative themes, relational graph exploration, timeline forensics, and automated dossier export.
7. **Security & Audit Vault**: OAuth2 JWT authentication and append-only cryptographic audit logs.

---

## 🚀 Quick Start Guide

### Option 1: Docker Compose (Recommended)
```bash
docker-compose up -d
```
Access the application:
- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Neo4j Graph Browser**: [http://localhost:7474](http://localhost:7474)
- **MinIO S3 Console**: [http://localhost:9001](http://localhost:9001)

### Option 2: Standalone Local Mode
```bash
# 1. Start FastAPI Backend (Port 8000)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Start Next.js Frontend (Port 3000)
cd frontend
npm run dev
```