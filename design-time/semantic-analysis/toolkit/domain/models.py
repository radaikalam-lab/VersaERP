import math
import unicodedata
import urllib.parse
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class GraphLayer(StrEnum):
    BUSINESS = "business"
    PHYSICAL = "physical"
    REQUIREMENTS = "requirements"
    SEMANTIC = "semantic"


class AssertionStatus(StrEnum):
    OBSERVED = "observed"
    DERIVED = "derived"
    INFERRED = "inferred"
    PROPOSED = "proposed"
    VALIDATED = "validated"
    PUBLISHED = "published"
    REJECTED = "rejected"
    RETIRED = "retired"


NodeStatus = AssertionStatus
RelationshipStatus = AssertionStatus


class SemanticPublicationStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    VALIDATED = "validated"
    PUBLISHED = "published"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ExecutionProposalStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    AUTHORIZED = "authorized"
    READY = "ready"
    EXECUTING = "executing"
    EXECUTED = "executed"
    VERIFIED = "verified"
    REJECTED = "rejected"
    FAILED = "failed"
    PARTIALLY_EXECUTED = "partially_executed"
    VERIFICATION_FAILED = "verification_failed"
    CANCELLED = "cancelled"


# Backward compatibility alias
ProposalStatus = SemanticPublicationStatus


class ConflictType(StrEnum):
    ATTRIBUTE_CONFLICT = "attribute_conflict"
    CARDINALITY_CONFLICT = "cardinality_conflict"
    IDENTITY_CONFLICT = "identity_conflict"
    MODEL_CONFLICT = "model_conflict"
    REQUIREMENT_CONFLICT = "requirement_conflict"
    SEMANTIC_CONFLICT = "semantic_conflict"
    SOURCE_CONFLICT = "source_conflict"
    TEMPORAL_CONFLICT = "temporal_conflict"


class ConflictStatus(StrEnum):
    DETECTED = "detected"
    OPEN = "open"
    RESOLVED = "resolved"
    ACCEPTED_AS_AMBIGUOUS = "accepted_as_ambiguous"


class IdentityOperation(StrEnum):
    CREATE = "create"
    ALIAS = "alias"
    MAP = "map"
    MERGE = "merge"
    SPLIT = "split"
    REDIRECT = "redirect"
    RETIRE = "retire"
    REACTIVATE = "reactivate"


def normalize_component(comp: Any) -> str:
    """Normalize and safely percent-encode a URI component."""
    if comp is None:
        return ""
    nfc_str = unicodedata.normalize("NFC", str(comp).strip())
    lowered = nfc_str.lower()
    return urllib.parse.quote(lowered, safe="-_.~")


def generate_canonical_id(layer: GraphLayer | str, entity_type: str, *components: str) -> str:
    """Generate a deterministic, collision-resistant canonical URI."""
    norm_layer = normalize_component(layer)
    norm_type = normalize_component(entity_type)
    encoded = [normalize_component(c) for c in components if c is not None and str(c).strip()]
    if encoded:
        return f"urn:graphmodel:{norm_layer}:{norm_type}:{':'.join(encoded)}"
    return f"urn:graphmodel:{norm_layer}:{norm_type}"


@dataclass(frozen=True)
class Confidence:
    value: float

    def __post_init__(self) -> None:
        if math.isnan(self.value) or math.isinf(self.value):
            raise ValueError(f"Confidence value cannot be NaN or Infinity, got {self.value}")
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"Confidence value must be between 0.0 and 1.0, got {self.value}")

    def __float__(self) -> float:
        return float(self.value)


@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: str
    source_type: str
    source_version: str | None = None
    locator: str | None = None
    excerpt: str | None = None
    confidence: float | None = None
    collected_at: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)


def generate_provenance_id(method: str, *components: str) -> str:
    """Generate a deterministic canonical URI for a Provenance record."""
    return generate_canonical_id("provenance", "record", method, *components)


@dataclass(frozen=True)
class Provenance:
    id: str
    source_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    method: str = "unknown"
    confidence: float | None = None
    assumptions: tuple[str, ...] = ()
    transformations: tuple[str, ...] = ()
    created_at: str | None = None
    operator_id: str | None = None

    def __post_init__(self) -> None:
        if not self.id or not str(self.id).strip():
            raise ValueError("Provenance.id is mandatory and must not be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source_ids": list(self.source_ids),
            "evidence_ids": list(self.evidence_ids),
            "method": self.method,
            "confidence": self.confidence,
            "assumptions": list(self.assumptions),
            "transformations": list(self.transformations),
            "created_at": self.created_at,
            "operator_id": self.operator_id,
        }


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    layer: GraphLayer = GraphLayer.PHYSICAL
    properties: dict[str, Any] = field(default_factory=dict)
    status: AssertionStatus = AssertionStatus.OBSERVED
    provenance: Provenance | None = None


@dataclass(frozen=True)
class Relationship:
    id: str
    source: str
    type: str
    target: str
    layer: GraphLayer = GraphLayer.PHYSICAL
    properties: dict[str, Any] = field(default_factory=dict)
    status: AssertionStatus = AssertionStatus.OBSERVED
    provenance: Provenance | None = None
    allow_self_reference: bool = False


Edge = Relationship


@dataclass(frozen=True)
class SemanticAssertion:
    id: str
    candidate_concept: str
    target_id: str | None = None
    layer: GraphLayer = GraphLayer.SEMANTIC
    evidence: tuple[Evidence, ...] = ()
    provenance: Provenance | None = None
    method: str = "unknown"
    confidence: float | None = None
    assumptions: tuple[str, ...] = ()
    status: AssertionStatus = AssertionStatus.INFERRED
    properties: dict[str, Any] = field(default_factory=dict)


Assertion = SemanticAssertion


@dataclass(frozen=True)
class Conflict:
    id: str
    conflict_type: ConflictType
    status: ConflictStatus = ConflictStatus.DETECTED
    assertion_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    detection_method: str = "reconciliation"
    description: str = ""
    resolution: str | None = None
    resolution_evidence_id: str | None = None
    resolver_id: str | None = None
    resolver_role: str | None = None
    reconciliation_id: str | None = None
    detected_at: str | None = None
    resolved_at: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Approval:
    id: str
    proposal_id: str
    approver_id: str
    role: str
    decision: str = "APPROVED"
    comments: str = ""
    timestamp: str | None = None


@dataclass(frozen=True)
class AuditRecord:
    id: str
    timestamp: str
    actor_id: str
    action: str
    resource_id: str
    authority_used: str
    provenance_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PolicyDecision:
    id: str
    actor_id: str
    action: str
    resource: str
    granted_authorities: tuple[str, ...] = ()
    decision: str = "ALLOW"
    reason: str = ""
    evaluated_at: str | None = None


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    source_type: str
    version: str = "1.0.0"
    declared_capabilities: tuple[str, ...] = ()
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DirectionalSpecification:
    id: str
    objective: str
    current_context: dict[str, Any] = field(default_factory=dict)
    desired_state: dict[str, Any] = field(default_factory=dict)
    constraints: tuple[str, ...] = ()
    allowed_capabilities: tuple[str, ...] = ()
    prohibited_capabilities: tuple[str, ...] = ()
    success_conditions: tuple[str, ...] = ()
    acceptance_conditions: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    provenance: Provenance | None = None
    version: str = "v0.1.0"


@dataclass(frozen=True)
class SemanticPublicationProposal:
    id: str
    title: str
    description: str = ""
    proposed_by: str = "system"
    status: SemanticPublicationStatus = SemanticPublicationStatus.DRAFT
    assertions: list[SemanticAssertion] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    provenance: Provenance | None = None
    created_at: str | None = None
    version: str = "v0.1.0"


@dataclass(frozen=True)
class ExecutionStep:
    id: str
    step_number: int
    operation: str
    target: str
    parameters: dict[str, Any] = field(default_factory=dict)
    expected_preconditions: tuple[str, ...] = ()
    expected_postconditions: tuple[str, ...] = ()
    rollback_operation: str | None = None
    idempotency_key: str | None = None
    reversibility: bool = True
    verification_method: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "expected_postconditions": sorted(self.expected_postconditions),
            "expected_preconditions": sorted(self.expected_preconditions),
            "id": self.id,
            "idempotency_key": self.idempotency_key,
            "operation": self.operation,
            "parameters": dict(sorted(self.parameters.items())),
            "reversibility": self.reversibility,
            "rollback_operation": self.rollback_operation,
            "step_number": self.step_number,
            "target": self.target,
            "verification_method": self.verification_method,
        }


@dataclass(frozen=True)
class ExecutionPlan:
    id: str
    proposal_id: str
    target_source_id: str
    steps: list[ExecutionStep] = field(default_factory=list)
    status: str = "draft"
    created_at: str | None = None
    approved_by: str | None = None
    provenance_id: str | None = None
    is_dry_run: bool = False
    verification_strategy: str = ""
    version: str = "v0.1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "approved_by": self.approved_by,
            "created_at": self.created_at,
            "id": self.id,
            "is_dry_run": self.is_dry_run,
            "plan_id": self.id,
            "proposal_id": self.proposal_id,
            "provenance_id": self.provenance_id,
            "status": self.status,
            "steps": [s.to_dict() for s in self.steps],
            "target_source_id": self.target_source_id,
            "verification_strategy": self.verification_strategy,
        }


@dataclass(frozen=True)
class ExecutionProposal:
    id: str
    title: str
    target_source_id: str
    description: str = ""
    proposed_by: str = "system"
    status: ExecutionProposalStatus = ExecutionProposalStatus.DRAFT
    plan_id: str | None = None
    modifications: dict[str, Any] = field(default_factory=dict)
    provenance: Provenance | None = None
    created_at: str | None = None
    governance_decision_id: str | None = None
    recommendation_id: str | None = None
    decision_context_id: str | None = None
    target_object_ids: tuple[str, ...] = ()
    proposed_operation: str = ""
    risk_classification: str = "moderate"
    reversibility: bool = True
    authorization_requirements: tuple[str, ...] = ()
    idempotency_key: str | None = None
    correlation_id: str | None = None
    rationale: str = ""
    affected_entities: tuple[str, ...] = ()
    version: str = "v0.1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "affected_entities": sorted(self.affected_entities),
            "authorization_requirements": sorted(self.authorization_requirements),
            "correlation_id": self.correlation_id,
            "created_at": self.created_at,
            "decision_context_id": self.decision_context_id,
            "description": self.description,
            "governance_decision_id": self.governance_decision_id,
            "id": self.id,
            "idempotency_key": self.idempotency_key,
            "modifications": dict(sorted(self.modifications.items())),
            "plan_id": self.plan_id,
            "proposed_by": self.proposed_by,
            "proposed_operation": self.proposed_operation,
            "provenance_id": self.provenance.id if self.provenance else None,
            "rationale": self.rationale,
            "recommendation_id": self.recommendation_id,
            "reversibility": self.reversibility,
            "risk_classification": self.risk_classification,
            "status": str(self.status),
            "target_object_ids": sorted(self.target_object_ids),
            "target_source_id": self.target_source_id,
            "title": self.title,
        }


Proposal = SemanticPublicationProposal


@dataclass(frozen=True)
class IdentityRecord:
    id: str
    canonical_id: str
    source_id: str
    aliases: tuple[str, ...] = ()
    status: str = "ACTIVE"
    provenance: Provenance | None = None
    properties: dict[str, Any] = field(default_factory=dict)
