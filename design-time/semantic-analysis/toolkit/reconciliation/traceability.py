from dataclasses import dataclass, field
from typing import Any

from graphmodel.graph.store import Graph
from graphmodel.reconciliation.models import CorrespondenceType, ReconciliationCandidate


@dataclass(frozen=True)
class CrossSystemLineageRecord:
    """Lineage branch for a single system participating in a reconciliation correspondence."""
    system_id: str
    object_id: str
    business_entity_id: str | None = None
    semantic_entity_id: str | None = None
    physical_table_id: str | None = None
    evidence_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "business_entity_id": self.business_entity_id,
            "evidence_ids": list(self.evidence_ids),
            "object_id": self.object_id,
            "physical_table_id": self.physical_table_id,
            "semantic_entity_id": self.semantic_entity_id,
            "system_id": self.system_id,
        }


@dataclass(frozen=True)
class ReconciliationTraceabilityChain:
    """Full cross-system multi-layer traceability record for a Reconciliation Candidate.
    
    Candidate -> Source System Lineage (Bus -> Sem -> Phys -> Evidence)
              -> Target System Lineage (Bus -> Sem -> Phys -> Evidence)
    """
    candidate_id: str
    correspondence_type: CorrespondenceType
    source_system_id: str
    target_system_id: str
    source_lineage: tuple[CrossSystemLineageRecord, ...] = field(default_factory=tuple)
    target_lineage: tuple[CrossSystemLineageRecord, ...] = field(default_factory=tuple)
    combined_evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "combined_evidence_ids": list(self.combined_evidence_ids),
            "correspondence_type": str(self.correspondence_type),
            "source_lineage": [r.to_dict() for r in self.source_lineage],
            "source_system_id": self.source_system_id,
            "target_lineage": [r.to_dict() for r in self.target_lineage],
            "target_system_id": self.target_system_id,
        }


class CrossSystemTraceabilityEngine:
    """Reconstructs cross-system traceability lineage for reconciliation candidates."""

    @staticmethod
    def _trace_object_in_graph(obj_id: str, graph: Graph, system_id: str) -> CrossSystemLineageRecord:
        node = graph.get_node(obj_id)
        if not node:
            return CrossSystemLineageRecord(
                system_id=system_id,
                object_id=obj_id,
            )

        bus_id: str | None = None
        sem_id: str | None = None
        phys_id: str | None = None
        ev_ids: list[str] = []

        if node.provenance:
            ev_ids.extend(node.provenance.evidence_ids)

        if node.type == "business_entity":
            bus_id = node.id
            sem_id = node.properties.get("semantic_entity_id")
            if sem_id:
                sem_node = graph.get_node(sem_id)
                if sem_node:
                    if sem_node.provenance:
                        ev_ids.extend(sem_node.provenance.evidence_ids)
                    phys_id = sem_node.properties.get("physical_table_id")
                    if phys_id:
                        phys_node = graph.get_node(phys_id)
                        if phys_node and phys_node.provenance:
                            ev_ids.extend(phys_node.provenance.evidence_ids)
        elif node.type == "entity" and node.layer.value == "semantic":
            sem_id = node.id
            phys_id = node.properties.get("physical_table_id")
            if phys_id:
                phys_node = graph.get_node(phys_id)
                if phys_node and phys_node.provenance:
                    ev_ids.extend(phys_node.provenance.evidence_ids)
        elif node.type == "table" and node.layer.value == "physical":
            phys_id = node.id

        return CrossSystemLineageRecord(
            system_id=system_id,
            object_id=obj_id,
            business_entity_id=bus_id,
            semantic_entity_id=sem_id,
            physical_table_id=phys_id,
            evidence_ids=tuple(sorted(set(ev_ids))),
        )

    @classmethod
    def trace_candidate(
        cls,
        candidate: ReconciliationCandidate,
        graph_a: Graph,
        graph_b: Graph,
    ) -> ReconciliationTraceabilityChain:
        """Trace both source and target objects of a candidate through their respective graphs."""
        src_lineages = [
            cls._trace_object_in_graph(sid, graph_a, candidate.source_system_id)
            for sid in candidate.source_object_ids
        ]
        tgt_lineages = [
            cls._trace_object_in_graph(tid, graph_b, candidate.target_system_id)
            for tid in candidate.target_object_ids
        ]

        all_ev = set(candidate.evidence_ids)
        for sl in src_lineages:
            all_ev.update(sl.evidence_ids)
        for tl in tgt_lineages:
            all_ev.update(tl.evidence_ids)

        return ReconciliationTraceabilityChain(
            candidate_id=candidate.id,
            correspondence_type=candidate.correspondence_type,
            source_system_id=candidate.source_system_id,
            target_system_id=candidate.target_system_id,
            source_lineage=tuple(src_lineages),
            target_lineage=tuple(tgt_lineages),
            combined_evidence_ids=tuple(sorted(all_ev)),
        )
