import re
import unicodedata
from typing import Any

from graphmodel.domain.models import (
    AssertionStatus,
    Conflict,
    ConflictStatus,
    ConflictType,
    Evidence,
    GraphLayer,
    Node,
    Provenance,
    SemanticPublicationStatus,
    generate_canonical_id,
    generate_provenance_id,
)
from graphmodel.domain.requirements import Requirement
from graphmodel.graph.store import Graph
from graphmodel.reconciliation.models import (
    Cardinality,
    CorrespondenceType,
    CrossSystemReconciliationResult,
    FactorType,
    ReconciliationCandidate,
    ReconciliationFactor,
    ReconciliationProposal,
    SystemIdentity,
    generate_multi_reconciliation_id,
    generate_reconciliation_id,
)

# Standardized enterprise domain synonym mapping for deterministic comparison
DOMAIN_SYNONYMS: dict[str, str] = {
    "account": "customer",
    "accounts": "customer",
    "buyer": "customer",
    "buyers": "customer",
    "client": "customer",
    "clients": "customer",
    "customer": "customer",
    "customers": "customer",
    "customer_account": "customer",
    "item": "product",
    "items": "product",
    "line_item": "order_item",
    "line_items": "order_item",
    "material": "product",
    "materials": "product",
    "order": "order",
    "orders": "order",
    "order_detail": "order_item",
    "order_details": "order_item",
    "order_header": "order",
    "order_headers": "order_item",
    "order_item": "order_item",
    "order_items": "order_item",
    "order_line": "order_item",
    "order_lines": "order_item",
    "part": "product",
    "parts": "product",
    "product": "product",
    "products": "product",
    "product_master": "product",
    "purchase_order": "order",
    "purchase_orders": "order",
    "sales_line": "order_item",
    "sales_lines": "order_item",
    "sales_order": "order",
    "sales_orders": "order",
    "sku": "product",
    "skus": "product",
}

DATA_TYPE_COMPATIBILITY_GROUPS: dict[str, set[str]] = {
    "integer": {"int", "int2", "int4", "int8", "integer", "bigint", "smallint", "serial", "bigserial"},
    "text": {"text", "varchar", "char", "character varying", "string"},
    "numeric": {"numeric", "decimal", "float", "float4", "float8", "real", "double precision", "money"},
    "temporal": {"date", "time", "timestamp", "timestamptz", "timestamp with time zone", "datetime"},
    "boolean": {"bool", "boolean"},
}


def _tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase words, splitting camelCase, snake_case, and whitespace."""
    if not text:
        return []
    nfc = unicodedata.normalize("NFC", str(text).strip())
    # Split camelCase
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", nfc)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Split non-alphanumeric
    tokens = [t.lower() for t in re.split(r"[^a-zA-Z0-9]+", s2) if t.strip()]
    return tokens


def _stem(token: str) -> str:
    """Basic deterministic morphological stemming for plurals."""
    t = token.lower()
    if t.endswith("ies") and len(t) > 4:
        return t[:-3] + "y"
    if t.endswith("es") and len(t) > 4 and not t.endswith("sses"):
        return t[:-2]
    if t.endswith("s") and len(t) > 3 and not t.endswith("ss"):
        return t[:-1]
    return t


def _compute_token_similarity(text1: str, text2: str) -> float:
    """Compute deterministic token Jaccard similarity with domain synonym substitution and stemming."""
    tokens1 = _tokenize(text1)
    tokens2 = _tokenize(text2)
    if not tokens1 or not tokens2:
        return 0.0

    syn1 = {DOMAIN_SYNONYMS.get(t, DOMAIN_SYNONYMS.get(_stem(t), _stem(t))) for t in tokens1}
    syn2 = {DOMAIN_SYNONYMS.get(t, DOMAIN_SYNONYMS.get(_stem(t), _stem(t))) for t in tokens2}

    # Remove generic English stop words if token set is large enough
    stop_words = {"a", "an", "the", "and", "or", "of", "to", "in", "for", "with", "on", "at", "by", "from", "is", "are", "be"}
    if len(syn1) > 2:
        syn1 = syn1 - stop_words or syn1
    if len(syn2) > 2:
        syn2 = syn2 - stop_words or syn2

    intersection = syn1 & syn2
    union = syn1 | syn2
    if not union:
        return 0.0
    return len(intersection) / len(union)



def _are_types_compatible(type1: str, type2: str) -> bool:
    """Check if two data type strings belong to the same compatibility group."""
    t1 = type1.lower().strip()
    t2 = type2.lower().strip()
    if t1 == t2:
        return True
    for group in DATA_TYPE_COMPATIBILITY_GROUPS.values():
        if t1 in group and t2 in group:
            return True
    return False


class CrossSystemReconciliationEngine:
    """Deterministic Cross-System Reconciliation Engine implementing Phase 4 architecture.
    
    Operates strictly above source-system authority without modifying either source system.
    Identifies and represents correspondence candidates, factors, and conflicts with full lineage.
    """

    def __init__(self, engine_id: str = "cross_system_reconciliation_engine") -> None:
        self.engine_id = engine_id

    def reconcile(
        self,
        graph_a: Graph,
        system_a: SystemIdentity,
        graph_b: Graph,
        system_b: SystemIdentity,
        requirements_a: list[Requirement] | None = None,
        requirements_b: list[Requirement] | None = None,
        explicit_mappings: list[dict[str, Any]] | None = None,
        evidence_sources: list[Evidence] | None = None,
    ) -> CrossSystemReconciliationResult:
        """Execute deterministic cross-system reconciliation across Business, Semantic, and Requirement layers."""
        prov_id = generate_provenance_id("cross_system_reconciliation", system_a.system_id, system_b.system_id)
        evidence_all = list(evidence_sources or [])
        ev_ids_all = tuple(sorted(e.id for e in evidence_all))

        provenance = Provenance(
            id=prov_id,
            source_ids=(system_a.system_id, system_b.system_id),
            evidence_ids=ev_ids_all,
            method="deterministic_cross_system_reconciliation",
            confidence=0.90,
            assumptions=(
                "Reconciliation produces correspondence candidates without modifying source systems",
                "Similarity factors represent structured evidence, not authoritative business truth",
                "Conflicting and unresolved correspondences are preserved without silent winner selection",
            ),
        )

        candidates: list[ReconciliationCandidate] = []
        conflicts: list[Conflict] = []

        # 1. Reconcile Business Layer (Entities, Attributes, Relationships)
        bus_candidates, bus_conflicts = self._reconcile_business_layer(
            graph_a, system_a, graph_b, system_b, explicit_mappings
        )
        candidates.extend(bus_candidates)
        conflicts.extend(bus_conflicts)

        # 2. Reconcile Semantic Layer if present
        sem_candidates, sem_conflicts = self._reconcile_semantic_layer(
            graph_a, system_a, graph_b, system_b
        )
        candidates.extend(sem_candidates)
        conflicts.extend(sem_conflicts)

        # 3. Reconcile Requirements Layer if present
        if requirements_a and requirements_b:
            req_candidates, req_conflicts = self._reconcile_requirements_layer(
                requirements_a, system_a, requirements_b, system_b
            )
            candidates.extend(req_candidates)
            conflicts.extend(req_conflicts)

        # 4. Check for competing candidate mappings (preserve conflict)
        competing_conflicts = self._detect_competing_mappings(candidates, system_a, system_b)
        conflicts.extend(competing_conflicts)

        # 5. Build Governance Proposal in DRAFT status
        sorted_candidates = tuple(
            sorted(candidates, key=lambda c: (str(c.correspondence_type), c.id))
        )
        sorted_conflicts = tuple(
            sorted(conflicts, key=lambda c: (str(c.conflict_type), c.id))
        )

        proposal_id = generate_canonical_id(
            GraphLayer.BUSINESS,
            "proposal",
            "reconciliation",
            system_a.system_id,
            system_b.system_id,
        )
        proposal = ReconciliationProposal(
            id=proposal_id,
            candidate_ids=tuple(c.id for c in sorted_candidates),
            status=SemanticPublicationStatus.DRAFT,
            submitted_by=self.engine_id,
            comments=f"Automated reconciliation proposal between {system_a.system_id} and {system_b.system_id}",
            created_at="2026-09-28T00:00:00Z",
        )

        summary: dict[str, int] = {
            c_type.value: sum(1 for c in sorted_candidates if c.correspondence_type == c_type)
            for c_type in CorrespondenceType
        }
        summary["total_candidates"] = len(sorted_candidates)
        summary["conflicts_detected"] = len(sorted_conflicts)

        result_id = generate_canonical_id(
            GraphLayer.BUSINESS,
            "reconciliation_result",
            system_a.system_id,
            system_b.system_id,
        )

        return CrossSystemReconciliationResult(
            id=result_id,
            source_system=system_a,
            target_system=system_b,
            candidates=sorted_candidates,
            conflicts=sorted_conflicts,
            proposals=(proposal,),
            evidence=tuple(sorted(evidence_all, key=lambda e: e.id)),
            provenance=provenance,
            summary=summary,
            diagnostics={
                "candidate_count": len(sorted_candidates),
                "conflict_count": len(sorted_conflicts),
                "source_nodes_a": len(graph_a.nodes),
                "source_nodes_b": len(graph_b.nodes),
            },
        )

    def _reconcile_business_layer(
        self,
        graph_a: Graph,
        system_a: SystemIdentity,
        graph_b: Graph,
        system_b: SystemIdentity,
        explicit_mappings: list[dict[str, Any]] | None = None,
    ) -> tuple[list[ReconciliationCandidate], list[Conflict]]:
        candidates: list[ReconciliationCandidate] = []
        conflicts: list[Conflict] = []

        entities_a = sorted(
            [n for n in graph_a.nodes.values() if n.type == "business_entity"],
            key=lambda n: n.id,
        )
        entities_b = sorted(
            [n for n in graph_b.nodes.values() if n.type == "business_entity"],
            key=lambda n: n.id,
        )

        if not entities_a or not entities_b:
            return candidates, conflicts

        # Check for 1:N decomposition cases (e.g. System A customer vs System B customer + address + contact)
        decomposed_b = [e for e in entities_b if any(t in e.properties.get("name", "").lower() for t in ("address", "contact", "detail", "line"))]
        
        for ent_a in entities_a:
            name_a = ent_a.properties.get("name", "")
            attrs_a = set(ent_a.properties.get("attributes", []))
            matched_any = False

            # Check 1:N decomposition possibility
            if len(decomposed_b) >= 2 and any(t in name_a.lower() for t in ("customer", "order")):
                primary_b = [e for e in entities_b if e.properties.get("name", "").lower() == name_a.lower()]
                if primary_b:
                    related_group = tuple(sorted([primary_b[0].id] + [d.id for d in decomposed_b]))
                    cid = generate_multi_reconciliation_id(
                        system_a.system_id,
                        (ent_a.id,),
                        system_b.system_id,
                        related_group,
                        CorrespondenceType.RELATED,
                        GraphLayer.BUSINESS,
                    )
                    candidates.append(
                        ReconciliationCandidate(
                            id=cid,
                            source_system_id=system_a.system_id,
                            target_system_id=system_b.system_id,
                            source_object_ids=(ent_a.id,),
                            target_object_ids=related_group,
                            layer=GraphLayer.BUSINESS,
                            correspondence_type=CorrespondenceType.RELATED,
                            cardinality=Cardinality.ONE_TO_MANY,
                            status=AssertionStatus.PROPOSED,
                            confidence=0.80,
                            factors=(
                                ReconciliationFactor(
                                    factor_type=FactorType.BUSINESS_MAPPING,
                                    score=0.85,
                                    details=f"Decomposition match: {name_a} corresponds to structured composite {related_group}",
                                ),
                            ),
                            rationale=f"Structural decomposition of {name_a} across multiple entities in {system_b.system_id}",
                        )
                    )

            for ent_b in entities_b:
                name_b = ent_b.properties.get("name", "")
                attrs_b = set(ent_b.properties.get("attributes", []))

                factors: list[ReconciliationFactor] = []

                # 1. Name Similarity Factor
                name_sim = _compute_token_similarity(name_a, name_b)
                if name_sim > 0.0:
                    factors.append(
                        ReconciliationFactor(
                            factor_type=FactorType.NAME_SIMILARITY,
                            score=name_sim,
                            details=f"Token similarity between '{name_a}' and '{name_b}': {name_sim:.2f}",
                        )
                    )

                # 2. Attribute Overlap Factor
                attr_sim = 0.0
                if attrs_a and attrs_b:
                    clean_a = {_tokenize(a)[-1] if _tokenize(a) else a for a in attrs_a}
                    clean_b = {_tokenize(b)[-1] if _tokenize(b) else b for b in attrs_b}
                    overlap = clean_a & clean_b
                    union = clean_a | clean_b
                    if union:
                        attr_sim = len(overlap) / len(union)
                        factors.append(
                            ReconciliationFactor(
                                factor_type=FactorType.ATTRIBUTE_OVERLAP,
                                score=attr_sim,
                                details=f"Attribute overlap ({len(overlap)} shared): {sorted(overlap)}",
                            )
                        )

                # 3. Relationship Topology Factor
                topo_score = self._compute_topology_score(ent_a, graph_a, ent_b, graph_b)
                if topo_score > 0.0:
                    factors.append(
                        ReconciliationFactor(
                            factor_type=FactorType.RELATIONSHIP_TOPOLOGY,
                            score=topo_score,
                            details=f"Relationship topology structural alignment score: {topo_score:.2f}",
                        )
                    )

                # 4. Conflict Checking (e.g. conflicting semantics in properties)
                is_conflict, conflict_desc = self._check_business_entity_conflict(ent_a, ent_b)

                if is_conflict:
                    cand_id = generate_reconciliation_id(
                        system_a.system_id,
                        ent_a.id,
                        system_b.system_id,
                        ent_b.id,
                        CorrespondenceType.CONFLICTING,
                        GraphLayer.BUSINESS,
                    )
                    conf_id = generate_canonical_id(
                        "conflict",
                        "cross_system",
                        system_a.system_id,
                        system_b.system_id,
                        ent_a.id,
                        ent_b.id,
                    )
                    c = Conflict(
                        id=conf_id,
                        conflict_type=ConflictType.MODEL_CONFLICT,
                        status=ConflictStatus.DETECTED,
                        assertion_ids=(ent_a.id, ent_b.id),
                        source_ids=(system_a.system_id, system_b.system_id),
                        detection_method="cross_system_reconciliation_conflict_rule",
                        description=conflict_desc,
                        reconciliation_id=cand_id,
                        detected_at="2026-09-28T00:00:00Z",
                    )
                    conflicts.append(c)
                    candidates.append(
                        ReconciliationCandidate(
                            id=cand_id,
                            source_system_id=system_a.system_id,
                            target_system_id=system_b.system_id,
                            source_object_ids=(ent_a.id,),
                            target_object_ids=(ent_b.id,),
                            layer=GraphLayer.BUSINESS,
                            correspondence_type=CorrespondenceType.CONFLICTING,
                            cardinality=Cardinality.ONE_TO_ONE,
                            status=AssertionStatus.PROPOSED,
                            confidence=0.5,
                            factors=tuple(factors),
                            conflict_ids=(conf_id,),
                            rationale=conflict_desc,
                        )
                    )
                    matched_any = True
                elif name_sim >= 0.5 or (name_sim > 0.3 and attr_sim > 0.3):
                    overall_conf = max(0.1, min(0.95, (name_sim * 0.5) + (attr_sim * 0.3) + (topo_score * 0.2)))
                    cand_id = generate_reconciliation_id(
                        system_a.system_id,
                        ent_a.id,
                        system_b.system_id,
                        ent_b.id,
                        CorrespondenceType.POSSIBLE_MATCH,
                        GraphLayer.BUSINESS,
                    )
                    candidates.append(
                        ReconciliationCandidate(
                            id=cand_id,
                            source_system_id=system_a.system_id,
                            target_system_id=system_b.system_id,
                            source_object_ids=(ent_a.id,),
                            target_object_ids=(ent_b.id,),
                            layer=GraphLayer.BUSINESS,
                            correspondence_type=CorrespondenceType.POSSIBLE_MATCH,
                            cardinality=Cardinality.ONE_TO_ONE,
                            status=AssertionStatus.PROPOSED,
                            confidence=overall_conf,
                            factors=tuple(factors),
                            rationale=f"Potential business entity match between '{name_a}' and '{name_b}'",
                        )
                    )
                    matched_any = True

            # If no matches above threshold found for ent_a, represent UNRESOLVED if similar name existed or UNRELATED
            if not matched_any:
                cand_id = generate_reconciliation_id(
                    system_a.system_id,
                    ent_a.id,
                    system_b.system_id,
                    "unmatched",
                    CorrespondenceType.UNRESOLVED,
                    GraphLayer.BUSINESS,
                )
                candidates.append(
                    ReconciliationCandidate(
                        id=cand_id,
                        source_system_id=system_a.system_id,
                        target_system_id=system_b.system_id,
                        source_object_ids=(ent_a.id,),
                        target_object_ids=(f"urn:graphmodel:unresolved:{system_b.system_id}",),
                        layer=GraphLayer.BUSINESS,
                        correspondence_type=CorrespondenceType.UNRESOLVED,
                        cardinality=Cardinality.ONE_TO_ONE,
                        status=AssertionStatus.PROPOSED,
                        confidence=0.0,
                        rationale=f"No suitable correspondence found for business entity '{name_a}' in {system_b.system_id}",
                    )
                )

        return candidates, conflicts

    def _compute_topology_score(
        self, node_a: Node, graph_a: Graph, node_b: Node, graph_b: Graph
    ) -> float:
        """Compute structural relationship topology alignment score between two nodes."""
        rels_a = [r for r in graph_a.relationships.values() if r.source == node_a.id or r.target == node_a.id]
        rels_b = [r for r in graph_b.relationships.values() if r.source == node_b.id or r.target == node_b.id]

        if not rels_a or not rels_b:
            return 0.0

        types_a = {r.type.lower() for r in rels_a}
        types_b = {r.type.lower() for r in rels_b}

        overlap = types_a & types_b
        union = types_a | types_b
        return len(overlap) / len(union) if union else 0.0

    def _check_business_entity_conflict(self, ent_a: Node, ent_b: Node) -> tuple[bool, str]:
        """Detect explicit semantic/definition contradictions between two candidate business entities."""
        name_a = ent_a.properties.get("name", "").lower()
        name_b = ent_b.properties.get("name", "").lower()

        # Check explicit contradictory properties
        type_a = str(ent_a.properties.get("entity_subtype", ent_a.properties.get("definition_scope", ""))).lower()
        type_b = str(ent_b.properties.get("entity_subtype", ent_b.properties.get("definition_scope", ""))).lower()

        if (
            ("individual" in type_a and "organization" in type_b)
            or ("individual" in type_b and "organization" in type_a)
            or ("person" in type_a and "corporate" in type_b)
            or ("person" in type_b and "corporate" in type_a)
        ):
            return True, f"Contradictory entity definitions: '{name_a}' ({type_a}) vs '{name_b}' ({type_b})"

        # Check financial total contradiction (gross vs net)
        scope_a = str(ent_a.properties.get("valuation_basis", "")).lower()
        scope_b = str(ent_b.properties.get("valuation_basis", "")).lower()
        if ("gross" in scope_a and "net" in scope_b) or ("gross" in scope_b and "net" in scope_a):
            return True, f"Contradictory financial basis: '{name_a}' ({scope_a}) vs '{name_b}' ({scope_b})"

        return False, ""

    def _reconcile_semantic_layer(
        self,
        graph_a: Graph,
        system_a: SystemIdentity,
        graph_b: Graph,
        system_b: SystemIdentity,
    ) -> tuple[list[ReconciliationCandidate], list[Conflict]]:
        candidates: list[ReconciliationCandidate] = []
        conflicts: list[Conflict] = []

        sem_nodes_a = sorted(
            [n for n in graph_a.nodes.values() if n.layer == GraphLayer.SEMANTIC and n.type == "entity"],
            key=lambda n: n.id,
        )
        sem_nodes_b = sorted(
            [n for n in graph_b.nodes.values() if n.layer == GraphLayer.SEMANTIC and n.type == "entity"],
            key=lambda n: n.id,
        )

        for s_a in sem_nodes_a:
            name_a = s_a.properties.get("name", "")
            for s_b in sem_nodes_b:
                name_b = s_b.properties.get("name", "")
                sim = _compute_token_similarity(name_a, name_b)
                if sim >= 0.5:
                    cid = generate_reconciliation_id(
                        system_a.system_id,
                        s_a.id,
                        system_b.system_id,
                        s_b.id,
                        CorrespondenceType.POSSIBLE_MATCH,
                        GraphLayer.SEMANTIC,
                    )
                    candidates.append(
                        ReconciliationCandidate(
                            id=cid,
                            source_system_id=system_a.system_id,
                            target_system_id=system_b.system_id,
                            source_object_ids=(s_a.id,),
                            target_object_ids=(s_b.id,),
                            layer=GraphLayer.SEMANTIC,
                            correspondence_type=CorrespondenceType.POSSIBLE_MATCH,
                            cardinality=Cardinality.ONE_TO_ONE,
                            status=AssertionStatus.PROPOSED,
                            confidence=sim,
                            factors=(
                                ReconciliationFactor(
                                    factor_type=FactorType.NAME_SIMILARITY,
                                    score=sim,
                                    details=f"Semantic entity name similarity: {sim:.2f}",
                                ),
                            ),
                            rationale=f"Semantic correspondence between '{name_a}' and '{name_b}'",
                        )
                    )
        return candidates, conflicts

    def _reconcile_requirements_layer(
        self,
        reqs_a: list[Requirement],
        system_a: SystemIdentity,
        reqs_b: list[Requirement],
        system_b: SystemIdentity,
    ) -> tuple[list[ReconciliationCandidate], list[Conflict]]:
        candidates: list[ReconciliationCandidate] = []
        conflicts: list[Conflict] = []

        for r_a in sorted(reqs_a, key=lambda r: r.id):
            for r_b in sorted(reqs_b, key=lambda r: r.id):
                statement_sim = _compute_token_similarity(r_a.statement, r_b.statement)
                type_match = r_a.requirement_type == r_b.requirement_type

                if statement_sim >= 0.30 or (statement_sim >= 0.25 and type_match):
                    factors = [
                        ReconciliationFactor(
                            factor_type=FactorType.NAME_SIMILARITY,
                            score=statement_sim,
                            details=f"Statement token similarity: {statement_sim:.2f}",
                        )
                    ]
                    if type_match:
                        factors.append(
                            ReconciliationFactor(
                                factor_type=FactorType.EXPLICIT_CONFIGURATION,
                                score=1.0,
                                details=f"Matching requirement type: {r_a.requirement_type}",
                            )
                        )
                    conf = (statement_sim * 0.7) + (0.3 if type_match else 0.0)
                    cid = generate_reconciliation_id(
                        system_a.system_id,
                        r_a.id,
                        system_b.system_id,
                        r_b.id,
                        CorrespondenceType.POSSIBLE_MATCH,
                        GraphLayer.REQUIREMENTS,
                    )
                    candidates.append(
                        ReconciliationCandidate(
                            id=cid,
                            source_system_id=system_a.system_id,
                            target_system_id=system_b.system_id,
                            source_object_ids=(r_a.id,),
                            target_object_ids=(r_b.id,),
                            layer=GraphLayer.REQUIREMENTS,
                            correspondence_type=CorrespondenceType.POSSIBLE_MATCH,
                            cardinality=Cardinality.ONE_TO_ONE,
                            status=AssertionStatus.PROPOSED,
                            confidence=conf,
                            factors=tuple(factors),
                            rationale=f"Requirement semantic correspondence between '{r_a.statement}' and '{r_b.statement}'",
                        )
                    )
        return candidates, conflicts

    def _detect_competing_mappings(
        self,
        candidates: list[ReconciliationCandidate],
        system_a: SystemIdentity,
        system_b: SystemIdentity,
    ) -> list[Conflict]:
        """Detect when a single source object has competing candidate matches with equal high confidence."""
        conflicts: list[Conflict] = []
        src_map: dict[str, list[ReconciliationCandidate]] = {}

        for c in candidates:
            if c.correspondence_type in (CorrespondenceType.POSSIBLE_MATCH, CorrespondenceType.EQUIVALENT):
                for sid in c.source_object_ids:
                    src_map.setdefault(sid, []).append(c)

        for src_id, cands in src_map.items():
            if len(cands) > 1 and cands[0].cardinality == Cardinality.ONE_TO_ONE:
                # Multiple competing 1:1 candidates for the same source object
                conf_id = generate_canonical_id(
                    "conflict",
                    "competing_mapping",
                    system_a.system_id,
                    system_b.system_id,
                    src_id,
                )
                conf = Conflict(
                    id=conf_id,
                    conflict_type=ConflictType.MODEL_CONFLICT,
                    status=ConflictStatus.DETECTED,
                    assertion_ids=tuple(c.id for c in cands),
                    source_ids=(system_a.system_id, system_b.system_id),
                    detection_method="competing_candidate_mapping_detection",
                    description=f"Source object '{src_id}' has multiple competing candidate matches: {[c.target_object_ids for c in cands]}",
                    reconciliation_id=cands[0].id,
                    detected_at="2026-09-28T00:00:00Z",
                )
                conflicts.append(conf)

        return conflicts
