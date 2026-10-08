from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from graphmodel.domain.models import (
    Conflict,
    ConflictStatus,
    ConflictType,
    GraphLayer,
    generate_canonical_id,
)
from graphmodel.graph.store import Graph


class ReconciliationStatus(StrEnum):
    ADDED = "added"
    AMBIGUOUS = "ambiguous"
    CONFLICT = "conflict"
    DRIFT = "drift"
    MATCH = "match"
    MISSING = "missing"
    MODIFIED = "modified"


@dataclass(frozen=True)
class ReconciliationDelta:
    element_id: str
    status: ReconciliationStatus
    source_element: dict[str, Any] | None = None
    target_element: dict[str, Any] | None = None
    difference_details: str = ""
    conflict_id: str | None = None


@dataclass(frozen=True)
class ReconciliationResult:
    id: str
    source_layer: GraphLayer | None
    target_layer: GraphLayer | None
    deltas: tuple[ReconciliationDelta, ...] = ()
    conflicts: tuple[Conflict, ...] = ()
    summary: dict[str, int] = field(default_factory=dict)
    computed_at: str | None = None


class ReconciliationEngine:
    """Deterministic graph comparison engine implementing Reconciliation Contract v0.1.0."""

    @staticmethod
    def compare(
        source_graph: Graph,
        target_graph: Graph,
        result_id: str = "rec_result_01",
        detect_conflicts: bool = True,
    ) -> ReconciliationResult:
        deltas: list[ReconciliationDelta] = []
        created_conflicts: list[Conflict] = []
        summary: dict[str, int] = {s.value: 0 for s in ReconciliationStatus}

        all_node_ids = sorted(set(source_graph.nodes.keys()) | set(target_graph.nodes.keys()))

        for nid in all_node_ids:
            src_node = source_graph.get_node(nid)
            tgt_node = target_graph.get_node(nid)

            if src_node and tgt_node:
                if src_node.type == tgt_node.type and src_node.properties == tgt_node.properties:
                    status = ReconciliationStatus.MATCH
                    diff = "Nodes match identically"
                    conflict_id = None
                else:
                    # Incompatible types or conflicting properties
                    if src_node.type != tgt_node.type:
                        status = ReconciliationStatus.CONFLICT
                        diff = f"Model conflict: source type '{src_node.type}' contradicts target type '{tgt_node.type}'"
                        conflict_id = generate_canonical_id(
                            GraphLayer.BUSINESS if target_graph.layer == GraphLayer.BUSINESS else GraphLayer.SEMANTIC,
                            "conflict",
                            "model",
                            result_id,
                            nid,
                        )
                        if detect_conflicts:
                            c = Conflict(
                                id=conflict_id,
                                conflict_type=ConflictType.MODEL_CONFLICT,
                                status=ConflictStatus.DETECTED,
                                assertion_ids=(nid,),
                                source_ids=(src_node.id, tgt_node.id),
                                detection_method="reconciliation_engine",
                                description=diff,
                                reconciliation_id=result_id,
                                detected_at="2026-09-28T00:00:00Z",
                            )
                            created_conflicts.append(c)
                    else:
                        status = ReconciliationStatus.MODIFIED
                        diff = f"Property discrepancy on {nid}: src({src_node.properties}) vs tgt({tgt_node.properties})"
                        conflict_id = None

                deltas.append(
                    ReconciliationDelta(
                        element_id=nid,
                        status=status,
                        source_element={"type": src_node.type, "properties": src_node.properties},
                        target_element={"type": tgt_node.type, "properties": tgt_node.properties},
                        difference_details=diff,
                        conflict_id=conflict_id,
                    )
                )
                summary[status.value] += 1
            elif src_node and not tgt_node:
                status = ReconciliationStatus.ADDED
                deltas.append(
                    ReconciliationDelta(
                        element_id=nid,
                        status=status,
                        source_element={"type": src_node.type, "properties": src_node.properties},
                        target_element=None,
                        difference_details="Element present in source but missing in target",
                    )
                )
                summary[status.value] += 1
            elif tgt_node and not src_node:
                status = ReconciliationStatus.MISSING
                deltas.append(
                    ReconciliationDelta(
                        element_id=nid,
                        status=status,
                        source_element=None,
                        target_element={"type": tgt_node.type, "properties": tgt_node.properties},
                        difference_details="Element declared in target but missing in source",
                    )
                )
                summary[status.value] += 1

        sorted_deltas = tuple(sorted(deltas, key=lambda d: (str(d.status), d.element_id)))
        sorted_conflicts = tuple(sorted(created_conflicts, key=lambda c: (str(c.conflict_type), c.id)))

        return ReconciliationResult(
            id=result_id,
            source_layer=source_graph.layer,
            target_layer=target_graph.layer,
            deltas=sorted_deltas,
            conflicts=sorted_conflicts,
            summary=summary,
        )
