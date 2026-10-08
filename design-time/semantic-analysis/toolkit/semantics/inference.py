from abc import ABC, abstractmethod
from collections.abc import Iterable

from graphmodel.domain.models import (
    AssertionStatus,
    Evidence,
    GraphLayer,
    Provenance,
    SemanticAssertion,
    SemanticPublicationStatus,
    generate_canonical_id,
    generate_provenance_id,
)
from graphmodel.graph.store import Graph
from graphmodel.semantics.draft import SemanticDraft


class SemanticInferenceEngine(ABC):
    """Protocol for semantic inference. Inference produces drafts and has no authority to mutate truth."""

    @abstractmethod
    def infer(
        self,
        source_graph: Graph,
        evidence_sources: Iterable[Evidence] | None = None,
    ) -> SemanticDraft:
        """Infer semantic concepts from a source graph without mutating the source."""
        raise NotImplementedError


class FixtureSemanticInferencer(SemanticInferenceEngine):
    """Deterministic rule-based inference engine for Phase 0 testing and fixtures."""

    def __init__(self, draft_id: str = "draft-001") -> None:
        self.draft_id = draft_id

    def _to_pascal_case(self, name: str) -> str:
        parts = name.replace("-", "_").split("_")
        return "".join(p.capitalize() for p in parts if p)

    def infer(
        self,
        source_graph: Graph,
        evidence_sources: Iterable[Evidence] | None = None,
    ) -> SemanticDraft:
        draft = SemanticDraft(id=self.draft_id, status=SemanticPublicationStatus.DRAFT)
        evidence_list = tuple(evidence_sources) if evidence_sources else ()

        for node in sorted(source_graph.nodes.values(), key=lambda n: n.id):
            if node.type == "table":
                raw_name = node.properties.get("name", node.id)
                inferred_concept = self._to_pascal_case(raw_name)
                canonical_sem_id = generate_canonical_id(GraphLayer.SEMANTIC, "entity", inferred_concept)

                prov = Provenance(
                    id=generate_provenance_id("naming_convention_heuristic", node.id),
                    source_ids=(node.id,),
                    evidence_ids=tuple(e.id for e in evidence_list if e.source_id == node.id),
                    method="naming_convention_heuristic",
                    confidence=0.85,
                    assumptions=("Table name represents domain entity",),
                )
                assertion = SemanticAssertion(
                    id=canonical_sem_id,
                    candidate_concept=inferred_concept,
                    target_id=node.id,
                    layer=GraphLayer.SEMANTIC,
                    evidence=tuple(e for e in evidence_list if e.source_id == node.id),
                    provenance=prov,
                    method="naming_convention_heuristic",
                    confidence=0.85,
                    assumptions=("Table name represents domain entity",),
                    status=AssertionStatus.INFERRED,
                    properties={"physical_table": node.id},
                )
                draft.add_assertion(assertion)

        return draft
