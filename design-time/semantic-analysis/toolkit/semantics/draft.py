from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from graphmodel.domain.models import (
    AssertionStatus,
    Evidence,
    GraphLayer,
    Node,
    Provenance,
    SemanticAssertion,
    SemanticPublicationStatus,
)
from graphmodel.governance.policy import Authority, require_authority
from graphmodel.graph.store import Graph


@dataclass(frozen=True)
class SemanticCandidate:
    physical_id: str
    semantic_type: str
    evidence: tuple[Evidence, ...] = ()
    provenance: Provenance | None = None
    status: AssertionStatus = AssertionStatus.INFERRED
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticDraft:
    id: str
    title: str = ""
    description: str = ""
    assertions: list[SemanticAssertion] = field(default_factory=list)
    candidates: list[SemanticCandidate] = field(default_factory=list)
    status: SemanticPublicationStatus = SemanticPublicationStatus.DRAFT
    evidence_ids: list[str] = field(default_factory=list)
    provenance: Provenance | None = None
    assumptions: list[str] = field(default_factory=list)
    confidence: float = 0.85
    created_at: str | None = None

    def add_assertion(self, assertion: SemanticAssertion) -> None:
        if assertion.status not in {
            AssertionStatus.INFERRED,
            AssertionStatus.PROPOSED,
            AssertionStatus.VALIDATED,
            AssertionStatus.PUBLISHED,
            AssertionStatus.REJECTED,
        }:
            raise ValueError(f"Invalid semantic assertion status: {assertion.status}")
        self.assertions.append(assertion)
        for ev in assertion.evidence:
            if ev.id not in self.evidence_ids:
                self.evidence_ids.append(ev.id)

    def add(self, candidate: SemanticCandidate | SemanticAssertion) -> None:
        if isinstance(candidate, SemanticAssertion):
            self.add_assertion(candidate)
            return

        if candidate.status not in {
            AssertionStatus.INFERRED,
            AssertionStatus.PROPOSED,
            AssertionStatus.VALIDATED,
            AssertionStatus.PUBLISHED,
            AssertionStatus.REJECTED,
        }:
            raise ValueError(f"Invalid semantic candidate status: {candidate.status}")
        self.candidates.append(candidate)

    def validate(self, granted_authorities: Iterable[Authority | str]) -> Graph:
        """Promote draft assertions into a validated Business Graph.

        Requires explicit Authority.VALIDATE.
        """
        require_authority(granted_authorities, Authority.VALIDATE)

        business_graph = Graph(layer=GraphLayer.BUSINESS)

        for assertion in self.assertions:
            if assertion.status != AssertionStatus.REJECTED:
                node = Node(
                    id=assertion.id,
                    type=assertion.candidate_concept,
                    layer=GraphLayer.BUSINESS,
                    properties=assertion.properties,
                    status=AssertionStatus.VALIDATED,
                    provenance=assertion.provenance,
                )
                business_graph.add_node(node)

        for candidate in self.candidates:
            if candidate.status != AssertionStatus.REJECTED:
                node = Node(
                    id=candidate.physical_id,
                    type=candidate.semantic_type,
                    layer=GraphLayer.BUSINESS,
                    properties=candidate.properties,
                    status=AssertionStatus.VALIDATED,
                    provenance=candidate.provenance,
                )
                business_graph.add_node(node)

        self.status = SemanticPublicationStatus.VALIDATED
        return business_graph
