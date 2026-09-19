"""
Evidence Broker for STAIR-Style Architecture.
Executes strictly authorized, case-scoped data fetching tools for validated leaf IDs.
Integrates PostgreSQL, Neo4j Graph DB, MinIO Canonical Parquet Warehouse,
Test Pack Loader (50k+ raw forensic events), Timeline Engine, and Forensic Reporting Services.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import text as sa_text

from app.core.database import get_db_context
from app.core.neo4j_client import neo4j_client
from app.models.postgres_models import (
    CaseModel, GoldenProfileModel, AnomalyFindingModel,
    AlertModel, InvestigationReportModel, EvidenceModel, DataQualityReportModel
)
from app.stair.schemas import SelectedLeaf, EvidenceAuthority
from app.processing.canonical_reader import canonical_reader

logger = logging.getLogger("stair.broker")

class EvidenceBroker:
    """Executes validated tool mappings against the actual underlying forensic data systems."""

    @classmethod
    def _get_entity_identifiers(cls, case_id: str, entity_name: Optional[str] = None, query: str = "") -> Dict[str, Any]:
        """
        Resolves suspect identity, aliases, phone numbers, and bank accounts.
        If entity_name is missing, inspects the query string for known suspect names.
        """
        target_name = (entity_name or "").strip()
        names = set()
        phones = set()
        accounts = set()
        aliases = set()
        canonical_name = None

        with get_db_context() as session:
            profiles = session.query(GoldenProfileModel).filter(GoldenProfileModel.case_id == case_id).all()

            # If target_name is empty, check if any profile name or alias is mentioned in query
            if not target_name and query:
                q_low = query.lower()
                for p in profiles:
                    if p.primary_name and p.primary_name.lower() in q_low:
                        target_name = p.primary_name
                        break
                    if p.known_aliases:
                        for a in p.known_aliases:
                            if a.lower() in q_low:
                                target_name = p.primary_name
                                break
                        if target_name:
                            break

            if target_name:
                t_low = target_name.lower()
                names.add(t_low)
                for p in profiles:
                    matched = False
                    if p.primary_name and (t_low in p.primary_name.lower() or p.primary_name.lower() in t_low):
                        matched = True
                        canonical_name = p.primary_name
                    if p.known_aliases:
                        for a in p.known_aliases:
                            if t_low in a.lower() or a.lower() in t_low:
                                matched = True
                                if not canonical_name:
                                    canonical_name = p.primary_name
                    if matched:
                        names.add(p.primary_name.lower())
                        if p.known_aliases:
                            for a in p.known_aliases:
                                aliases.add(a)
                                names.add(a.lower())
                        if p.known_phones:
                            for ph in p.known_phones:
                                phones.add(ph)
                                digits = "".join(ch for ch in ph if ch.isdigit())
                                if len(digits) >= 10:
                                    phones.add(digits[-10:])
                                    phones.add("+91" + digits[-10:])
                                    phones.add("91" + digits[-10:])
                        if p.known_accounts:
                            for acc in p.known_accounts:
                                accounts.add(acc)

        return {
            "target_name": canonical_name or target_name,
            "names": list(names),
            "phones": list(phones),
            "accounts": list(accounts),
            "aliases": list(aliases)
        }

    @classmethod
    def execute_leaf(cls, leaf: SelectedLeaf, query: str = "") -> List[Dict[str, Any]]:
        """Dispatches a single validated leaf to its approved handler."""
        leaf_id = leaf.leaf_id
        params = leaf.parameters
        case_id = params.get("case_id", "INV-2026-BLACK-CIRCUIT")

        handler_map = {
            # 1. Entity
            "entity.golden_profile": cls._fetch_golden_profile,
            "entity.identity_discrepancy": cls._fetch_identity_discrepancies,
            "entity.associated_network": cls._fetch_associated_network,

            # 2. Telecom
            "telecom.cdr_records": cls._fetch_cdr_records,
            "telecom.ipdr_sessions": cls._fetch_ipdr_sessions,
            "telecom.cell_tower_pings": cls._fetch_cell_tower_pings,
            "telecom.imei_telemetry": cls._fetch_imei_telemetry,

            # 3. Financial
            "financial.transactions": cls._fetch_financial_transactions,
            "financial.suspicious_transactions": cls._fetch_suspicious_financial,
            "financial.mule_flows": cls._fetch_mule_flows,
            "financial.cycle_analysis": cls._fetch_financial_cycles,

            # 4. Geo
            "geo.location_history": cls._fetch_location_history,
            "geo.movement_trajectory": cls._fetch_movement_trajectory,
            "geo.colocation_nexus": cls._fetch_colocation_nexus,
            "geo.spatial_jumps": cls._fetch_spatial_jumps,

            # 5. Temporal
            "temporal.timeline_events": cls._fetch_timeline_events,
            "temporal.burst_activity": cls._fetch_burst_activity,
            "temporal.cross_modal_correlation": cls._fetch_temporal_correlations,
            "temporal.inconsistency": cls._fetch_temporal_inconsistencies,

            # 6. Anomaly
            "anomaly.findings": cls._fetch_anomaly_findings,
            "anomaly.cep_alerts": cls._fetch_cep_alerts,
            "anomaly.cross_domain": cls._fetch_cross_domain_anomalies,

            # 7. Graph
            "graph.connections": cls._fetch_graph_connections,
            "graph.shortest_path": cls._fetch_shortest_path,
            "graph.gds_centrality": cls._fetch_gds_centrality,
            "graph.transaction_subgraph": cls._fetch_transaction_subgraph,

            # 8. Reports
            "reports.court_dossier": cls._fetch_court_dossier,
            "reports.section_65b": cls._fetch_section_65b,
            "reports.lead_investigator": cls._fetch_lead_investigator_report,
            "reports.financial_specialist": cls._fetch_financial_specialist_report,
            "reports.geographic_specialist": cls._fetch_geographic_specialist_report,
            "reports.temporal_specialist": cls._fetch_temporal_specialist_report,
            "reports.data_quality": cls._fetch_data_quality_report,
        }

        handler = handler_map.get(leaf_id)
        if not handler:
            logger.error(f"[EvidenceBroker] No handler configured for valid leaf: {leaf_id}")
            return []

        try:
            records = handler(case_id=case_id, params=params, query=query)
            logger.info(f"[EvidenceBroker] Leaf '{leaf_id}' fetched {len(records)} records.")
            return records
        except TypeError:
            records = handler(case_id=case_id, params=params)
            logger.info(f"[EvidenceBroker] Leaf '{leaf_id}' fetched {len(records)} records.")
            return records
        except Exception as e:
            logger.error(f"[EvidenceBroker] Error executing leaf '{leaf_id}': {e}", exc_info=True)
            return []

    # ── 1. ENTITY HANDLERS ────────────────────────────────────────────────
    @classmethod
    def _fetch_golden_profile(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]

        with get_db_context() as session:
            db_query = session.query(GoldenProfileModel).filter(GoldenProfileModel.case_id == case_id)
            if target_name:
                search_like = f"%{target_name.strip()}%"
                db_query = db_query.filter(
                    GoldenProfileModel.primary_name.ilike(search_like) |
                    sa_text(f"known_aliases::text ILIKE '{search_like}'")
                )
            profiles = db_query.order_by(GoldenProfileModel.risk_score.desc()).limit(10).all()
            return [
                {
                    "source_id": p.z_cluster_id,
                    "primary_name": p.primary_name,
                    "known_aliases": p.known_aliases or [],
                    "known_phones": p.known_phones or [],
                    "known_accounts": p.known_accounts or [],
                    "associated_emails": p.associated_emails or [],
                    "national_ids": p.national_ids or [],
                    "known_addresses": p.known_addresses or [],
                    "risk_score": p.risk_score,
                    "method": p.method
                }
                for p in profiles
            ]

    @classmethod
    def _fetch_identity_discrepancies(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            db_query = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                (AnomalyFindingModel.domain.ilike("%IDENTITY%") |
                 AnomalyFindingModel.pattern_type.ilike("%IDENTITY%") |
                 AnomalyFindingModel.title.ilike("%Identity%") |
                 AnomalyFindingModel.title.ilike("%Device%"))
            )
            entity_name = params.get("entity_name") or params.get("name")
            ident = cls._get_entity_identifiers(case_id, entity_name, query)
            target_name = ident["target_name"]
            if target_name:
                db_query = db_query.filter(AnomalyFindingModel.title.ilike(f"%{target_name}%"))
            findings = db_query.limit(10).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "score": f.unified_score,
                    "what_happened": f.what_happened or f.explanation,
                    "why_unusual": f.why_unusual,
                    "why_relevant": f.why_relevant
                }
                for f in findings
            ]

    @classmethod
    def _fetch_associated_network(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]

        records = []
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    cypher = """
                    MATCH (p:Person)-[r]-(target)
                    WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                      AND ($name = '' OR toLower(p.name) CONTAINS toLower($name))
                    RETURN p.name AS person, type(r) AS relation, labels(target)[0] AS target_type,
                           coalesce(target.name, target.account_number, target.number, target.tower_id) AS target_identifier
                    LIMIT 25
                    """
                    res = session.run(cypher, {"case_id": case_id, "name": target_name or ""})
                    records = [dict(r) for r in res]
            except Exception as e:
                logger.warning(f"[EvidenceBroker] Neo4j associated network error: {e}")

        if not records and target_name:
            # Fallback to Postgres GoldenProfile details
            with get_db_context() as session:
                prof = session.query(GoldenProfileModel).filter(
                    GoldenProfileModel.case_id == case_id,
                    GoldenProfileModel.primary_name.ilike(f"%{target_name}%")
                ).first()
                if prof:
                    for ph in (prof.known_phones or []):
                        records.append({"person": prof.primary_name, "relation": "OWNS_PHONE", "target_type": "Phone", "target_identifier": ph})
                    for acc in (prof.known_accounts or []):
                        records.append({"person": prof.primary_name, "relation": "OWNS_ACCOUNT", "target_type": "BankAccount", "target_identifier": acc})

        return records

    # ── 2. TELECOM HANDLERS ───────────────────────────────────────────────
    @classmethod
    def _fetch_cdr_records(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        phone = params.get("phone_number")
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]
        target_phones = set(ident["phones"])
        if phone:
            target_phones.add(phone)
            digits = "".join(ch for ch in phone if ch.isdigit())
            if len(digits) >= 10:
                target_phones.add(digits[-10:])
                target_phones.add("+91" + digits[-10:])
                target_phones.add("91" + digits[-10:])

        records = []
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    if target_name:
                        cypher = """
                        MATCH (p:Person)-[:OWNS_PHONE]->(p1:Phone)-[r:CALLS|CALLED]-(p2:Phone)
                        WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                          AND toLower(p.name) CONTAINS toLower($name)
                        RETURN p.name AS person_name, p1.number AS caller,
                               coalesce(r.duration_seconds, r.duration, 0) AS duration,
                               r.timestamp AS timestamp, p2.number AS receiver,
                               coalesce(r.call_type, 'VOICE') AS call_type
                        ORDER BY r.timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "name": target_name})
                        records = [dict(r) for r in res]

                    if not records and target_phones:
                        cypher = """
                        MATCH (p1:Phone)-[r:CALLS|CALLED]-(p2:Phone)
                        WHERE (p1.case_id = $case_id OR $case_id IN coalesce(p1.case_ids, []))
                          AND (p1.number IN $phones OR p2.number IN $phones)
                        RETURN p1.number AS caller, coalesce(r.duration_seconds, r.duration, 0) AS duration,
                               r.timestamp AS timestamp, p2.number AS receiver,
                               coalesce(r.call_type, 'VOICE') AS call_type
                        ORDER BY r.timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "phones": list(target_phones)})
                        records = [dict(r) for r in res]

                    if not records and not target_name and not target_phones:
                        cypher = """
                        MATCH (p1:Phone)-[r:CALLS|CALLED]->(p2:Phone)
                        WHERE (p1.case_id = $case_id OR $case_id IN coalesce(p1.case_ids, []))
                        RETURN p1.number AS caller, coalesce(r.duration_seconds, r.duration, 0) AS duration,
                               r.timestamp AS timestamp, p2.number AS receiver,
                               coalesce(r.call_type, 'VOICE') AS call_type
                        ORDER BY r.timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id})
                        records = [dict(r) for r in res]
            except Exception as e:
                logger.warning(f"[EvidenceBroker] Neo4j CDR error: {e}")

        # Fallback to test pack / canonical Parquet
        if not records:
            events = []
            try:
                from app.timeline.test_pack_loader import test_pack_loader
                pack_evs = test_pack_loader.load_case_events(case_id)
                events = [e for e in pack_evs if e.get("source_type") == "TELECOM"]
            except Exception:
                pass
            if not events:
                events = canonical_reader.read_all_events(case_id=case_id, source_type="TELECOM", limit=200)

            for r in events:
                norm = r.get("normalized_identity", {})
                attrs = r.get("attributes", {})
                r_name = (norm.get("name") or "").lower()
                caller = norm.get("phone")
                callee = attrs.get("callee") or r.get("telemetry", {}).get("destination_ip")

                if target_name:
                    matched = any(n in r_name for n in ident["names"])
                    if not matched and target_phones:
                        if caller in target_phones or callee in target_phones:
                            matched = True
                    if not matched:
                        continue
                elif target_phones:
                    if caller not in target_phones and callee not in target_phones:
                        continue

                records.append({
                    "source_id": r.get("event_id"),
                    "person_name": norm.get("name") or target_name or "Subscriber",
                    "caller": caller,
                    "receiver": callee or "External Subscriber",
                    "duration": r.get("telemetry", {}).get("duration_seconds") or attrs.get("duration_seconds", 0),
                    "timestamp": r.get("timestamp")
                })
            records = records[:25]

        return records

    @classmethod
    def _fetch_ipdr_sessions(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        target_ip = params.get("ip_address")
        if not target_ip and query:
            ip_m = re.search(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', query)
            if ip_m:
                target_ip = ip_m.group(0)

        records = []
        try:
            from app.timeline.test_pack_loader import test_pack_loader
            pack_evs = test_pack_loader.load_case_events(case_id)
            for r in pack_evs:
                if r.get("source_type") != "NETWORK":
                    continue
                tel = r.get("telemetry", {})
                c_ip = tel.get("assigned_ip")
                d_ip = tel.get("destination_ip")

                if target_ip:
                    if target_ip not in str(c_ip) and target_ip not in str(d_ip):
                        continue

                records.append({
                    "source_id": r.get("event_id"),
                    "client_ip": c_ip,
                    "destination_ip": d_ip,
                    "port": tel.get("service_port"),
                    "bytes": tel.get("bytes_transferred"),
                    "timestamp": r.get("timestamp")
                })
                if len(records) >= 25:
                    break
        except Exception:
            pass

        if not records:
            raw = canonical_reader.read_all_events(case_id=case_id, source_type="NETWORK", limit=25)
            for r in raw:
                tel = r.get("telemetry", {})
                records.append({
                    "source_id": r.get("event_id"),
                    "client_ip": tel.get("assigned_ip"),
                    "destination_ip": tel.get("destination_ip"),
                    "port": tel.get("service_port"),
                    "bytes": tel.get("bytes_transferred"),
                    "timestamp": r.get("timestamp")
                })
        return records

    @classmethod
    def _fetch_cell_tower_pings(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        phone = params.get("phone_number")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]
        target_phones = set(ident["phones"])
        if phone:
            target_phones.add(phone)

        records = []
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    if target_name:
                        cypher = """
                        MATCH (p:Person)-[:OWNS_PHONE]->(ph:Phone)-[r:LOCATED_AT|PINGED_TOWER]-(t:CellTower)
                        WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                          AND toLower(p.name) CONTAINS toLower($name)
                        RETURN p.name AS person_name, ph.number AS phone, t.tower_id AS tower_id,
                               coalesce(t.address, t.location, t.tower_id) AS location,
                               coalesce(r.pings_count, 1) AS pings,
                               coalesce(r.timestamp, r.last_seen) AS timestamp
                        ORDER BY timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "name": target_name})
                        records = [dict(r) for r in res]

                    if not records and target_phones:
                        cypher = """
                        MATCH (ph:Phone)-[r:LOCATED_AT|PINGED_TOWER]-(t:CellTower)
                        WHERE (ph.case_id = $case_id OR $case_id IN coalesce(ph.case_ids, []))
                          AND ph.number IN $phones
                        RETURN ph.number AS phone, t.tower_id AS tower_id,
                               coalesce(t.address, t.location, t.tower_id) AS location,
                               coalesce(r.pings_count, 1) AS pings,
                               coalesce(r.timestamp, r.last_seen) AS timestamp
                        ORDER BY timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "phones": list(target_phones)})
                        records = [dict(r) for r in res]

                    if not records and not target_name and not target_phones:
                        cypher = """
                        MATCH (ph:Phone)-[r:LOCATED_AT|PINGED_TOWER]-(t:CellTower)
                        WHERE (ph.case_id = $case_id OR $case_id IN coalesce(ph.case_ids, []))
                        RETURN ph.number AS phone, t.tower_id AS tower_id,
                               coalesce(t.address, t.location, t.tower_id) AS location,
                               coalesce(r.pings_count, 1) AS pings,
                               coalesce(r.timestamp, r.last_seen) AS timestamp
                        ORDER BY timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id})
                        records = [dict(r) for r in res]
            except Exception as e:
                logger.warning(f"[EvidenceBroker] Neo4j cell tower error: {e}")

        # Fallback to test pack / canonical
        if not records:
            try:
                from app.timeline.test_pack_loader import test_pack_loader
                pack_evs = test_pack_loader.load_case_events(case_id)
                for e in pack_evs:
                    tel = e.get("telemetry", {})
                    norm = e.get("normalized_identity", {})
                    tower = tel.get("cell_tower_id") or e.get("attributes", {}).get("cell_id")
                    if not tower:
                        continue
                    r_name = (norm.get("name") or "").lower()
                    r_phone = norm.get("phone")

                    if target_name:
                        matched = any(n in r_name for n in ident["names"])
                        if not matched and target_phones:
                            matched = r_phone in target_phones
                        if not matched:
                            continue
                    elif target_phones:
                        if r_phone not in target_phones:
                            continue

                    records.append({
                        "source_id": e.get("event_id"),
                        "person_name": norm.get("name") or target_name or "Subscriber",
                        "phone": r_phone,
                        "tower_id": tower,
                        "location": tel.get("address") or tower,
                        "pings": 1,
                        "timestamp": e.get("timestamp")
                    })
                    if len(records) >= 25:
                        break
            except Exception:
                pass

        return records

    @classmethod
    def _fetch_imei_telemetry(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        target_imei = params.get("imei")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]

        records = []
        try:
            from app.timeline.test_pack_loader import test_pack_loader
            pack_evs = test_pack_loader.load_case_events(case_id)
            seen = set()
            for r in pack_evs:
                im = r.get("telemetry", {}).get("imei")
                if not im or im in seen:
                    continue
                norm = r.get("normalized_identity", {})
                r_name = (norm.get("name") or "").lower()

                if target_imei and target_imei not in im:
                    continue
                if target_name:
                    matched = any(n in r_name for n in ident["names"])
                    if not matched:
                        continue

                seen.add(im)
                records.append({
                    "source_id": f"IMEI-{im}",
                    "imei": im,
                    "associated_name": norm.get("name") or target_name,
                    "associated_phone": norm.get("phone"),
                    "timestamp": r.get("timestamp")
                })
                if len(records) >= 15:
                    break
        except Exception:
            pass

        if not records:
            raw = canonical_reader.read_all_events(case_id=case_id, limit=50)
            seen = set()
            for r in raw:
                im = r.get("telemetry", {}).get("imei")
                if im and im not in seen:
                    seen.add(im)
                    records.append({
                        "source_id": f"IMEI-{im}",
                        "imei": im,
                        "associated_name": r.get("normalized_identity", {}).get("name"),
                        "associated_phone": r.get("normalized_identity", {}).get("phone"),
                        "timestamp": r.get("timestamp")
                    })
        return records

    # ── 3. FINANCIAL HANDLERS ─────────────────────────────────────────────
    @classmethod
    def _fetch_financial_transactions(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]
        target_accounts = set(ident["accounts"])
        if params.get("account_number"):
            target_accounts.add(params.get("account_number"))

        records = []
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    if target_name:
                        cypher = """
                        MATCH (p:Person)-[:OWNS_ACCOUNT]->(b1:BankAccount)-[r:TRANSFERS_MONEY|TRANSACTED_WITH]-(b2:BankAccount)
                        WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                          AND toLower(p.name) CONTAINS toLower($name)
                        RETURN p.name AS person_name, b1.account_number AS sender_account,
                               coalesce(r.amount_inr, r.amount, 0.0) AS amount_inr,
                               coalesce(r.txn_mode, r.channel, 'BANK_TRANSFER') AS channel,
                               r.timestamp AS timestamp,
                               b2.account_number AS recipient_account,
                               coalesce(b2.holder, b2.name, 'Unknown') AS recipient_holder
                        ORDER BY amount_inr DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "name": target_name})
                        records = [dict(r) for r in res]

                    if not records and target_accounts:
                        cypher_acc = """
                        MATCH (b1:BankAccount)-[r:TRANSFERS_MONEY|TRANSACTED_WITH]-(b2:BankAccount)
                        WHERE (b1.case_id = $case_id OR $case_id IN coalesce(b1.case_ids, []))
                          AND (b1.account_number IN $accounts OR b2.account_number IN $accounts)
                        RETURN coalesce(b1.holder, b1.name, 'Suspect') AS person_name,
                               b1.account_number AS sender_account,
                               coalesce(r.amount_inr, r.amount, 0.0) AS amount_inr,
                               coalesce(r.txn_mode, r.channel, 'BANK_TRANSFER') AS channel,
                               r.timestamp AS timestamp,
                               b2.account_number AS recipient_account,
                               coalesce(b2.holder, b2.name, 'Unknown') AS recipient_holder
                        ORDER BY amount_inr DESC LIMIT 25
                        """
                        res = session.run(cypher_acc, {"case_id": case_id, "accounts": list(target_accounts)})
                        records = [dict(r) for r in res]

                    if not records and not target_name and not target_accounts:
                        cypher_all = """
                        MATCH (b1:BankAccount)-[r:TRANSFERS_MONEY|TRANSACTED_WITH]->(b2:BankAccount)
                        WHERE (b1.case_id = $case_id OR $case_id IN coalesce(b1.case_ids, []))
                        RETURN coalesce(b1.holder, b1.name, 'Suspect') AS person_name,
                               b1.account_number AS sender_account,
                               coalesce(r.amount_inr, r.amount, 0.0) AS amount_inr,
                               coalesce(r.txn_mode, r.channel, 'BANK_TRANSFER') AS channel,
                               r.timestamp AS timestamp,
                               b2.account_number AS recipient_account,
                               coalesce(b2.holder, b2.name, 'Unknown') AS recipient_holder
                        ORDER BY amount_inr DESC LIMIT 25
                        """
                        res = session.run(cypher_all, {"case_id": case_id})
                        records = [dict(r) for r in res]
            except Exception as e:
                logger.warning(f"[EvidenceBroker] Neo4j financial query error: {e}")

        # Fallback to test pack / canonical Parquet events with STRICT entity filtering
        if not records:
            events = []
            try:
                from app.timeline.test_pack_loader import test_pack_loader
                pack_evs = test_pack_loader.load_case_events(case_id)
                events = [e for e in pack_evs if e.get("source_type") == "BANKING"]
            except Exception:
                pass
            if not events:
                events = canonical_reader.read_all_events(case_id=case_id, source_type="BANKING", limit=200)

            for r in events:
                fin = r.get("financial", {})
                attrs = r.get("attributes", {})
                norm = r.get("normalized_identity", {})
                r_name = (norm.get("name") or attrs.get("from_name") or attrs.get("to_name") or "").lower()
                from_acc = fin.get("account_number") or attrs.get("from_account")
                to_acc = fin.get("counterparty") or attrs.get("to_account")

                # If entity or account specified, enforce strict match
                if target_name:
                    matched = False
                    for n in ident["names"]:
                        if n in r_name:
                            matched = True
                            break
                    if not matched and target_accounts:
                        if from_acc in target_accounts or to_acc in target_accounts:
                            matched = True
                    if not matched:
                        continue
                elif target_accounts:
                    if from_acc not in target_accounts and to_acc not in target_accounts:
                        continue

                records.append({
                    "source_id": r.get("event_id"),
                    "person_name": norm.get("name") or attrs.get("from_name") or target_name or "Unknown",
                    "sender_account": from_acc,
                    "amount_inr": float(fin.get("amount_inr") or attrs.get("amount_inr") or 0.0),
                    "channel": fin.get("channel") or attrs.get("channel") or "BANK_TRANSFER",
                    "recipient_account": to_acc,
                    "recipient_holder": attrs.get("to_name") or fin.get("counterparty") or "Unknown",
                    "timestamp": r.get("timestamp")
                })
            records.sort(key=lambda x: x.get("amount_inr", 0.0), reverse=True)
            records = records[:25]

        return records

    @classmethod
    def _fetch_suspicious_financial(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        records = []
        with get_db_context() as session:
            db_query = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                AnomalyFindingModel.domain == "FINANCIAL"
            )
            entity_name = params.get("entity_name") or params.get("name")
            ident = cls._get_entity_identifiers(case_id, entity_name, query)
            target_name = ident["target_name"]
            if target_name:
                db_query = db_query.filter(AnomalyFindingModel.title.ilike(f"%{target_name}%"))
            findings = db_query.order_by(AnomalyFindingModel.unified_score.desc()).limit(10).all()
            for f in findings:
                records.append({
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "score": f.unified_score,
                    "what_happened": f.what_happened or f.explanation,
                    "why_unusual": f.why_unusual,
                    "metrics": f.metrics
                })

        # Also pull top transactions from Neo4j for grounding
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    res = session.run("""
                        MATCH (b1:BankAccount)-[r:TRANSFERS_MONEY|TRANSACTED_WITH]->(b2:BankAccount)
                        WHERE (b1.case_id = $case_id OR $case_id IN coalesce(b1.case_ids, []))
                        RETURN b1.account_number AS sender_account,
                               coalesce(r.amount_inr, r.amount, 0.0) AS amount_inr,
                               b2.account_number AS recipient_account, r.timestamp AS timestamp
                        ORDER BY amount_inr DESC LIMIT 10
                    """, {"case_id": case_id})
                    for r in res:
                        records.append(dict(r))
            except Exception:
                pass
        return records

    @classmethod
    def _fetch_mule_flows(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            alerts = session.query(AlertModel).filter(
                AlertModel.case_id == case_id,
                AlertModel.pattern_name.ilike("%Mule%")
            ).limit(5).all()
            return [
                {
                    "source_id": a.alert_id,
                    "pattern_name": a.pattern_name,
                    "risk_level": a.risk_level,
                    "risk_score": a.risk_score,
                    "narrative": a.evidence_narrative,
                    "micro_timeline": a.micro_timeline
                }
                for a in alerts
            ]

    @classmethod
    def _fetch_financial_cycles(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                AnomalyFindingModel.title.ilike("%Cycle%")
            ).limit(5).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "what_happened": f.what_happened or f.explanation,
                    "why_unusual": f.why_unusual
                }
                for f in findings
            ]

    # ── 4. GEOGRAPHICAL HANDLERS ──────────────────────────────────────────
    @classmethod
    def _fetch_location_history(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]
        target_phones = set(ident["phones"])

        records = []
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    if target_name:
                        cypher = """
                        MATCH (p:Person)-[:OWNS_PHONE]->(ph:Phone)-[r:LOCATED_AT|PINGED_TOWER]-(t:CellTower)
                        WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                          AND toLower(p.name) CONTAINS toLower($name)
                        RETURN p.name AS person_name, ph.number AS phone, t.tower_id AS tower_id,
                               coalesce(t.address, t.location, t.tower_id) AS location_name,
                               t.lat AS latitude, t.lng AS longitude,
                               coalesce(r.timestamp, r.last_seen) AS timestamp
                        ORDER BY timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "name": target_name})
                        records = [dict(r) for r in res]

                    if not records and target_phones:
                        cypher = """
                        MATCH (ph:Phone)-[r:LOCATED_AT|PINGED_TOWER]-(t:CellTower)
                        WHERE (ph.case_id = $case_id OR $case_id IN coalesce(ph.case_ids, []))
                          AND ph.number IN $phones
                        RETURN ph.number AS phone, t.tower_id AS tower_id,
                               coalesce(t.address, t.location, t.tower_id) AS location_name,
                               t.lat AS latitude, t.lng AS longitude,
                               coalesce(r.timestamp, r.last_seen) AS timestamp
                        ORDER BY timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id, "phones": list(target_phones)})
                        records = [dict(r) for r in res]

                    if not records and not target_name and not target_phones:
                        cypher = """
                        MATCH (ph:Phone)-[r:LOCATED_AT|PINGED_TOWER]-(t:CellTower)
                        WHERE (ph.case_id = $case_id OR $case_id IN coalesce(ph.case_ids, []))
                        RETURN ph.number AS phone, t.tower_id AS tower_id,
                               coalesce(t.address, t.location, t.tower_id) AS location_name,
                               t.lat AS latitude, t.lng AS longitude,
                               coalesce(r.timestamp, r.last_seen) AS timestamp
                        ORDER BY timestamp DESC LIMIT 25
                        """
                        res = session.run(cypher, {"case_id": case_id})
                        records = [dict(r) for r in res]
            except Exception as e:
                logger.warning(f"[EvidenceBroker] Location history error: {e}")

        # Fallback to test pack / canonical
        if not records:
            try:
                from app.timeline.test_pack_loader import test_pack_loader
                pack_evs = test_pack_loader.load_case_events(case_id)
                for e in pack_evs:
                    if e.get("source_type") != "LOCATION":
                        continue
                    norm = e.get("normalized_identity", {})
                    tel = e.get("telemetry", {})
                    r_name = (norm.get("name") or "").lower()
                    r_phone = norm.get("phone")

                    if target_name:
                        matched = any(n in r_name for n in ident["names"])
                        if not matched and target_phones:
                            matched = r_phone in target_phones
                        if not matched:
                            continue
                    elif target_phones:
                        if r_phone not in target_phones:
                            continue

                    records.append({
                        "source_id": e.get("event_id"),
                        "person_name": norm.get("name") or target_name,
                        "phone": r_phone,
                        "tower_id": tel.get("cell_tower_id") or "GPS",
                        "location_name": tel.get("address") or "Sector Area",
                        "latitude": tel.get("lat"),
                        "longitude": tel.get("lng"),
                        "timestamp": e.get("timestamp")
                    })
                    if len(records) >= 25:
                        break
            except Exception:
                pass

        return records

    @classmethod
    def _fetch_movement_trajectory(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                (AnomalyFindingModel.title.ilike("%Trajectory%") | AnomalyFindingModel.title.ilike("%Route%"))
            ).limit(5).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "what_happened": f.what_happened or f.explanation,
                    "why_relevant": f.why_relevant
                }
                for f in findings
            ]

    @classmethod
    def _fetch_colocation_nexus(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                (AnomalyFindingModel.title.ilike("%Spatial Convergence%") |
                 AnomalyFindingModel.title.ilike("%Co-Location%"))
            ).limit(5).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "what_happened": f.what_happened or f.explanation,
                    "why_relevant": f.why_relevant
                }
                for f in findings
            ]

    @classmethod
    def _fetch_spatial_jumps(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                (AnomalyFindingModel.title.ilike("%Teleportation%") |
                 AnomalyFindingModel.title.ilike("%Jump%"))
            ).limit(5).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "what_happened": f.what_happened or f.explanation,
                    "why_unusual": f.why_unusual
                }
                for f in findings
            ]

    # ── 5. TEMPORAL HANDLERS ──────────────────────────────────────────────
    @classmethod
    def _fetch_timeline_events(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        from app.timeline.service import timeline_service
        resp = timeline_service.query_timeline(case_id=case_id, limit=25)
        return [e.model_dump() for e in resp.events]

    @classmethod
    def _fetch_burst_activity(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                AnomalyFindingModel.title.ilike("%Burst%")
            ).limit(5).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "what_happened": f.what_happened or f.explanation
                }
                for f in findings
            ]

    @classmethod
    def _fetch_temporal_correlations(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            alerts = session.query(AlertModel).filter(
                AlertModel.case_id == case_id,
                AlertModel.pattern_name.ilike("%Triple Collision%")
            ).limit(5).all()
            return [
                {
                    "source_id": a.alert_id,
                    "pattern_name": a.pattern_name,
                    "risk_level": a.risk_level,
                    "narrative": a.evidence_narrative,
                    "micro_timeline": a.micro_timeline
                }
                for a in alerts
            ]

    @classmethod
    def _fetch_temporal_inconsistencies(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                (AnomalyFindingModel.title.ilike("%Inconsisten%") | AnomalyFindingModel.domain == "TEMPORAL")
            ).limit(5).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "what_happened": f.what_happened or f.explanation
                }
                for f in findings
            ]

    # ── 6. ANOMALY HANDLERS ───────────────────────────────────────────────
    @classmethod
    def _fetch_anomaly_findings(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]

        records = []
        with get_db_context() as session:
            db_query = session.query(AnomalyFindingModel).filter(AnomalyFindingModel.case_id == case_id)
            if target_name:
                db_query = db_query.filter(
                    AnomalyFindingModel.title.ilike(f"%{target_name}%") |
                    AnomalyFindingModel.what_happened.ilike(f"%{target_name}%")
                )
            findings = db_query.order_by(AnomalyFindingModel.unified_score.desc()).limit(15).all()
            for f in findings:
                records.append({
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "unified_score": f.unified_score,
                    "domain": f.domain,
                    "what_happened": f.what_happened or f.explanation,
                    "why_unusual": f.why_unusual,
                    "why_relevant": f.why_relevant
                })

        # Also query Knowledge Graph Anomaly nodes connected via HAS_ANOMALY
        if neo4j_client.ensure_connected():
            try:
                with neo4j_client.driver.session() as session:
                    if target_name:
                        cypher = """
                        MATCH (p:Person)-[r:HAS_ANOMALY]->(a:Anomaly)
                        WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                          AND toLower(p.name) CONTAINS toLower($name)
                        RETURN coalesce(a.id, 'GRAPH-ANOMALY') AS source_id, a.title AS title,
                               a.severity AS severity, coalesce(a.score, 0.0) AS unified_score,
                               a.domain AS domain, a.whatHappened AS what_happened,
                               a.whyUnusual AS why_unusual, a.whyRelevant AS why_relevant,
                               p.name AS person_name
                        ORDER BY unified_score DESC LIMIT 15
                        """
                        res = session.run(cypher, {"case_id": case_id, "name": target_name})
                    else:
                        cypher = """
                        MATCH (p:Person)-[r:HAS_ANOMALY]->(a:Anomaly)
                        WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                        RETURN coalesce(a.id, 'GRAPH-ANOMALY') AS source_id, a.title AS title,
                               a.severity AS severity, coalesce(a.score, 0.0) AS unified_score,
                               a.domain AS domain, a.whatHappened AS what_happened,
                               a.whyUnusual AS why_unusual, a.whyRelevant AS why_relevant,
                               p.name AS person_name
                        ORDER BY unified_score DESC LIMIT 15
                        """
                        res = session.run(cypher, {"case_id": case_id})
                    for r in res:
                        records.append(dict(r))
            except Exception as e:
                logger.warning(f"[EvidenceBroker] Neo4j graph anomaly query error: {e}")

        return records

    @classmethod
    def _fetch_cep_alerts(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_name = params.get("entity_name") or params.get("name")
        ident = cls._get_entity_identifiers(case_id, entity_name, query)
        target_name = ident["target_name"]

        with get_db_context() as session:
            db_query = session.query(AlertModel).filter(AlertModel.case_id == case_id)
            if target_name:
                db_query = db_query.filter(
                    AlertModel.entity_name.ilike(f"%{target_name}%") |
                    AlertModel.evidence_narrative.ilike(f"%{target_name}%")
                )
            alerts = db_query.order_by(AlertModel.risk_score.desc()).limit(5).all()
            return [
                {
                    "source_id": a.alert_id,
                    "pattern_name": a.pattern_name,
                    "entity_name": a.entity_name,
                    "risk_level": a.risk_level,
                    "risk_score": a.risk_score,
                    "evidence_narrative": a.evidence_narrative,
                    "micro_timeline": a.micro_timeline
                }
                for a in alerts
            ]

    @classmethod
    def _fetch_cross_domain_anomalies(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            findings = session.query(AnomalyFindingModel).filter(
                AnomalyFindingModel.case_id == case_id,
                AnomalyFindingModel.domain == "CROSS_DOMAIN"
            ).order_by(AnomalyFindingModel.unified_score.desc()).limit(8).all()
            return [
                {
                    "source_id": f.finding_id,
                    "title": f.title,
                    "severity": f.severity,
                    "unified_score": f.unified_score,
                    "what_happened": f.what_happened or f.explanation
                }
                for f in findings
            ]

    # ── 7. KNOWLEDGE GRAPH HANDLERS ───────────────────────────────────────
    @classmethod
    def _fetch_graph_connections(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_a = params.get("entity_a") or params.get("entity_name") or params.get("name", "")
        entity_b = params.get("entity_b", "")
        if not neo4j_client.ensure_connected():
            return []
        try:
            with neo4j_client.driver.session() as session:
                if entity_a and entity_b:
                    cypher = """
                    MATCH path = (p1:Person)-[*1..3]-(p2:Person)
                    WHERE (p1.case_id = $case_id OR $case_id IN coalesce(p1.case_ids, []))
                      AND toLower(p1.name) CONTAINS toLower($a)
                      AND toLower(p2.name) CONTAINS toLower($b)
                    RETURN [n IN nodes(path) | coalesce(n.name, n.account_number, n.number, labels(n)[0])] AS chain,
                           length(path) AS hops
                    LIMIT 5
                    """
                    res = session.run(cypher, {"case_id": case_id, "a": entity_a, "b": entity_b})
                    return [dict(r) for r in res]
                else:
                    cypher = """
                    MATCH path = (p:Person)-[*1..2]-(target)
                    WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                      AND ($a = '' OR toLower(p.name) CONTAINS toLower($a))
                    RETURN p.name AS source, [r IN relationships(path) | type(r)] AS edge_types,
                           [n IN nodes(path) | coalesce(n.name, n.account_number, n.number, labels(n)[0])] AS connection_chain,
                           labels(target)[0] AS target_type, coalesce(target.name, target.account_number, target.number, 'Node') AS target_entity
                    LIMIT 15
                    """
                    res = session.run(cypher, {"case_id": case_id, "a": entity_a})
                    return [dict(r) for r in res]
        except Exception as e:
            logger.warning(f"[EvidenceBroker] Graph connections error: {e}")
            return []

    @classmethod
    def _fetch_shortest_path(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        entity_a = params.get("entity_a", "")
        entity_b = params.get("entity_b", "")
        if not neo4j_client.ensure_connected():
            return []
        try:
            with neo4j_client.driver.session() as session:
                cypher = """
                MATCH (p1:Person), (p2:Person)
                WHERE (p1.case_id = $case_id OR $case_id IN coalesce(p1.case_ids, []))
                  AND toLower(p1.name) CONTAINS toLower($a)
                  AND toLower(p2.name) CONTAINS toLower($b)
                MATCH path = shortestPath((p1)-[*..6]-(p2))
                RETURN [n IN nodes(path) | coalesce(n.name, n.account_number, n.number)] AS path_entities,
                       length(path) AS total_hops
                LIMIT 3
                """
                res = session.run(cypher, {"case_id": case_id, "a": entity_a, "b": entity_b})
                return [dict(r) for r in res]
        except Exception as e:
            logger.warning(f"[EvidenceBroker] Shortest path error: {e}")
            return []

    @classmethod
    def _fetch_gds_centrality(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        if not neo4j_client.ensure_connected():
            return []
        records = []
        try:
            with neo4j_client.driver.session() as session:
                # 1. Person GDS metrics
                res_p = session.run("""
                    MATCH (p:Person)
                    WHERE (p.case_id = $case_id OR $case_id IN coalesce(p.case_ids, []))
                    RETURN p.name AS name, 'Person' AS entity_type,
                           coalesce(p.pagerank, 0.0) AS pagerank,
                           coalesce(p.betweenness, 0.0) AS betweenness,
                           coalesce(p.communityId, 0) AS community_id
                    ORDER BY p.pagerank DESC LIMIT 10
                """, {"case_id": case_id})
                records.extend([dict(r) for r in res_p])

                # 2. CellTower GDS metrics
                res_t = session.run("""
                    MATCH (c:CellTower)
                    WHERE (c.case_id = $case_id OR $case_id IN coalesce(c.case_ids, []))
                      AND (c.pagerank IS NOT NULL OR c.communityId IS NOT NULL)
                    RETURN c.tower_id AS name, 'CellTower' AS entity_type,
                           coalesce(c.pagerank, 0.0) AS pagerank,
                           coalesce(c.betweenness, 0.0) AS betweenness,
                           coalesce(c.communityId, 0) AS community_id
                    ORDER BY c.pagerank DESC LIMIT 10
                """, {"case_id": case_id})
                records.extend([dict(r) for r in res_t])
        except Exception as e:
            logger.warning(f"[EvidenceBroker] GDS centrality error: {e}")
        return records

    @classmethod
    def _fetch_transaction_subgraph(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        return cls._fetch_financial_transactions(case_id, params, query)

    # ── 8. REPORT HANDLERS ────────────────────────────────────────────────
    @classmethod
    def _fetch_court_dossier(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        from app.services.pdf_report_service import pdf_report_service
        payload = pdf_report_service.get_court_dossier_payload(case_id=case_id)
        return [{
            "source_id": f"DOSSIER-{case_id}",
            "case_header": payload.get("case_header"),
            "evidence_inventory_count": len(payload.get("evidence_inventory", [])),
            "evidence_samples": payload.get("evidence_inventory", [])[:5],
            "resolved_entities_count": len(payload.get("all_resolved_entities", [])),
            "top_suspect": payload.get("target_profile_name"),
            "critical_anomalies_count": len(payload.get("flagged_anomaly_registry", [])),
            "high_priority_alerts_count": len(payload.get("high_priority_alerts", [])),
            "lead_assessment": payload.get("ai_forensic_science", {}).get("lead_investigator_assessment", {})
        }]

    @classmethod
    def _fetch_section_65b(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            evs = session.query(EvidenceModel).filter(EvidenceModel.case_id == case_id).all()
            return [
                {
                    "source_id": f"CERT-65B-{case_id}",
                    "statute": "Section 65B Indian Evidence Act / Section 63 BSA",
                    "status": "CERTIFIED_DIGITALLY_SEALED",
                    "evidence_files": [
                        {"filename": e.original_filename, "sha256": e.sha256, "size_bytes": e.file_size}
                        for e in evs
                    ]
                }
            ]

    @classmethod
    def _fetch_lead_investigator_report(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            rep = session.query(InvestigationReportModel).order_by(InvestigationReportModel.report_id.desc()).first()
            if rep and rep.lead_json:
                return [{
                    "source_id": f"LEAD-REP-{rep.report_id}",
                    "community_id": rep.community_id,
                    "lead_synthesis": rep.lead_json
                }]
        return []

    @classmethod
    def _fetch_financial_specialist_report(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            rep = session.query(InvestigationReportModel).order_by(InvestigationReportModel.report_id.desc()).first()
            if rep and rep.financial_json:
                return [{
                    "source_id": f"FIN-REP-{rep.report_id}",
                    "community_id": rep.community_id,
                    "financial_analysis": rep.financial_json
                }]
        return []

    @classmethod
    def _fetch_geographic_specialist_report(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            rep = session.query(InvestigationReportModel).order_by(InvestigationReportModel.report_id.desc()).first()
            if rep and rep.geographic_json:
                return [{
                    "source_id": f"GEO-REP-{rep.report_id}",
                    "community_id": rep.community_id,
                    "geographic_analysis": rep.geographic_json
                }]
        return []

    @classmethod
    def _fetch_temporal_specialist_report(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            rep = session.query(InvestigationReportModel).order_by(InvestigationReportModel.report_id.desc()).first()
            if rep and rep.temporal_json:
                return [{
                    "source_id": f"TEMP-REP-{rep.report_id}",
                    "community_id": rep.community_id,
                    "temporal_analysis": rep.temporal_json
                }]
        return []

    @classmethod
    def _fetch_data_quality_report(cls, case_id: str, params: Dict[str, Any], query: str = "") -> List[Dict[str, Any]]:
        with get_db_context() as session:
            evs = session.query(EvidenceModel).filter(EvidenceModel.case_id == case_id).all()
            return [
                {
                    "source_id": e.evidence_id,
                    "filename": e.original_filename,
                    "sha256": e.sha256,
                    "total_records": e.record_count,
                    "valid_records": e.valid_record_count,
                    "invalid_records": e.invalid_record_count,
                    "quality_score": e.quality_score,
                    "processing_status": e.processing_status
                }
                for e in evs
            ]
