from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from graphmodel.domain.models import (
    AssertionStatus,
    Conflict,
    Evidence,
    GraphLayer,
    Node,
    Provenance,
    Relationship,
    SemanticAssertion,
)
from graphmodel.graph.store import Graph


class MappingType(StrEnum):
    TABLE_TO_ENTITY = "TABLE_TO_ENTITY"
    COLUMN_TO_ATTRIBUTE = "COLUMN_TO_ATTRIBUTE"
    FK_TO_RELATIONSHIP = "FK_TO_RELATIONSHIP"
    VIEW_TO_ENTITY = "VIEW_TO_ENTITY"


@dataclass(frozen=True)
class SemanticMapping:
    """Explicit mapping record connecting a physical graph object to a semantic graph object."""
    id: str
    physical_id: str
    semantic_id: str
    mapping_type: MappingType
    status: AssertionStatus = AssertionStatus.DERIVED
    evidence_ids: tuple[str, ...] = ()
    provenance: Provenance | None = None
    confidence: float = 1.0
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "confidence": self.confidence,
            "evidence_ids": list(self.evidence_ids),
            "id": self.id,
            "mapping_type": str(self.mapping_type),
            "physical_id": self.physical_id,
            "properties": dict(sorted(self.properties.items())),
            "provenance_id": self.provenance.id if self.provenance else None,
            "semantic_id": self.semantic_id,
            "status": str(self.status),
        }


@dataclass(frozen=True)
class SemanticEntity:
    """Canonical representation of a semantic entity concept."""
    id: str
    name: str
    status: AssertionStatus = AssertionStatus.DERIVED
    layer: GraphLayer = GraphLayer.SEMANTIC
    physical_table_id: str | None = None
    attributes: tuple[str, ...] = ()
    provenance: Provenance | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    def to_node(self) -> Node:
        props = dict(self.properties)
        props.update({
            "attributes": list(self.attributes),
            "name": self.name,
            "physical_table_id": self.physical_table_id,
        })
        return Node(
            id=self.id,
            type="entity",
            layer=self.layer,
            properties=props,
            status=self.status,
            provenance=self.provenance,
        )


@dataclass(frozen=True)
class SemanticAttribute:
    """Canonical representation of a semantic entity attribute."""
    id: str
    name: str
    entity_id: str
    data_type: str
    is_identifier: bool = False
    nullable: bool = True
    physical_column_id: str | None = None
    status: AssertionStatus = AssertionStatus.DERIVED
    layer: GraphLayer = GraphLayer.SEMANTIC
    provenance: Provenance | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    def to_node(self) -> Node:
        props = dict(self.properties)
        props.update({
            "data_type": self.data_type,
            "entity_id": self.entity_id,
            "is_identifier": self.is_identifier,
            "name": self.name,
            "nullable": self.nullable,
            "physical_column_id": self.physical_column_id,
        })
        return Node(
            id=self.id,
            type="attribute",
            layer=self.layer,
            properties=props,
            status=self.status,
            provenance=self.provenance,
        )


@dataclass(frozen=True)
class SemanticRelationship:
    """Canonical representation of a semantic relationship between entities."""
    id: str
    source_entity_id: str
    type: str
    target_entity_id: str
    physical_constraint_id: str | None = None
    cardinality: str | None = None
    status: AssertionStatus = AssertionStatus.DERIVED
    layer: GraphLayer = GraphLayer.SEMANTIC
    provenance: Provenance | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    def to_relationship(self) -> Relationship:
        props = dict(self.properties)
        if self.physical_constraint_id:
            props["physical_constraint_id"] = self.physical_constraint_id
        if self.cardinality:
            props["cardinality"] = self.cardinality
        return Relationship(
            id=self.id,
            source=self.source_entity_id,
            type=self.type,
            target=self.target_entity_id,
            layer=self.layer,
            properties=props,
            status=self.status,
            provenance=self.provenance,
        )


@dataclass(frozen=True)
class SemanticGraphResult:
    """Canonical result of a semantic graph construction run."""
    graph: Graph
    entities: list[Node]
    attributes: list[Node]
    relationships: list[Relationship]
    mappings: list[SemanticMapping]
    assertions: list[SemanticAssertion]
    conflicts: list[Conflict]
    evidence: list[Evidence]
    provenance: Provenance
    diagnostics: dict[str, Any] = field(default_factory=dict)
