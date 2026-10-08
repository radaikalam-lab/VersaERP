from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from graphmodel.domain.models import AssertionStatus, GraphLayer, Provenance


class RequirementType(StrEnum):
    FUNCTIONAL = "FUNCTIONAL"
    NON_FUNCTIONAL = "NON_FUNCTIONAL"
    DATA = "DATA"
    INTEGRATION = "INTEGRATION"
    SECURITY = "SECURITY"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"


class EvidenceCategory(StrEnum):
    SYSTEM_DERIVED = "SYSTEM_DERIVED"
    DOCUMENT_DERIVED = "DOCUMENT_DERIVED"
    HUMAN_ASSERTED = "HUMAN_ASSERTED"
    EXPLICIT_REQUIREMENT = "EXPLICIT_REQUIREMENT"


@dataclass(frozen=True)
class Actor:
    id: str
    name: str
    role_type: str = "user"
    description: str = ""
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BusinessRule:
    id: str
    name: str
    statement: str
    expression: str | None = None
    enforcing_entity: str | None = None
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Process:
    id: str
    name: str
    description: str = ""
    steps: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Event:
    id: str
    name: str
    payload_schema: dict[str, Any] = field(default_factory=dict)
    triggered_by: str | None = None
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Constraint:
    id: str
    name: str
    constraint_type: str = "general"
    target: str | None = None
    expression: str | None = None
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Capability:
    id: str
    name: str
    description: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RequirementRelationship:
    id: str
    source_id: str
    type: str
    target_id: str
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Requirement:
    id: str
    statement: str
    requirement_type: RequirementType = RequirementType.FUNCTIONAL
    entities: tuple[str, ...] = ()
    actors: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    processes: tuple[str, ...] = ()
    events: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    layer: GraphLayer = GraphLayer.REQUIREMENTS
    status: AssertionStatus = AssertionStatus.OBSERVED
    provenance: Provenance | None = None
    properties: dict[str, Any] = field(default_factory=dict)
