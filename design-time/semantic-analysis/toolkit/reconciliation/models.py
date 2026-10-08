import unicodedata
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from graphmodel.domain.models import (
    AssertionStatus,
    Conflict,
    Evidence,
    GraphLayer,
    Provenance,
    SemanticPublicationStatus,
    generate_canonical_id,
    normalize_component,
)


class CorrespondenceType(StrEnum):
    """Canonical classification of cross-system correspondence."""
    EQUIVALENT = "EQUIVALENT"
    RELATED = "RELATED"
    POSSIBLE_MATCH = "POSSIBLE_MATCH"
    CONFLICTING = "CONFLICTING"
    UNRELATED = "UNRELATED"
    UNRESOLVED = "UNRESOLVED"


class Cardinality(StrEnum):
    """Mapping cardinality between source and target structures."""
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_ONE = "MANY_TO_ONE"
    MANY_TO_MANY = "MANY_TO_MANY"


class FactorType(StrEnum):
    """Deterministic evidence factor categories supporting reconciliation."""
    NAME_SIMILARITY = "NAME_SIMILARITY"
    ATTRIBUTE_OVERLAP = "ATTRIBUTE_OVERLAP"
    IDENTIFIER_ROLE = "IDENTIFIER_ROLE"
    DATA_TYPE_COMPATIBILITY = "DATA_TYPE_COMPATIBILITY"
    RELATIONSHIP_TOPOLOGY = "RELATIONSHIP_TOPOLOGY"
    SEMANTIC_MAPPING = "SEMANTIC_MAPPING"
    BUSINESS_MAPPING = "BUSINESS_MAPPING"
    SOURCE_DOCUMENT = "SOURCE_DOCUMENT"
    HUMAN_ASSERTION = "HUMAN_ASSERTION"
    EXPLICIT_CONFIGURATION = "EXPLICIT_CONFIGURATION"


@dataclass(frozen=True)
class SystemIdentity:
    """Explicit source system identity abstraction."""
    system_id: str
    system_type: str = "postgresql"
    environment: str | None = None
    instance_id: str | None = None
    description: str = ""
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.system_id or not str(self.system_id).strip():
            raise ValueError("SystemIdentity.system_id is mandatory and cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "description": self.description,
            "environment": self.environment,
            "instance_id": self.instance_id,
            "properties": dict(sorted(self.properties.items())),
            "system_id": self.system_id,
            "system_type": self.system_type,
        }


@dataclass(frozen=True)
class ReconciliationFactor:
    """Deterministic factor supporting a reconciliation candidate."""
    factor_type: FactorType
    score: float
    weight: float = 1.0
    details: str = ""
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (0.0 <= self.score <= 1.0):
            raise ValueError(f"ReconciliationFactor.score must be in [0.0, 1.0], got {self.score}")
        if self.weight < 0.0:
            raise ValueError(f"ReconciliationFactor.weight must be non-negative, got {self.weight}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "details": self.details,
            "evidence_ids": list(self.evidence_ids),
            "factor_type": str(self.factor_type),
            "score": round(self.score, 4),
            "weight": round(self.weight, 4),
        }


def generate_reconciliation_id(
    source_sys: str,
    source_obj: str,
    target_sys: str,
    target_obj: str,
    correspondence_type: CorrespondenceType | str,
    layer: GraphLayer | str = GraphLayer.BUSINESS,
    is_symmetric: bool = True,
) -> str:
    """Generate a deterministic, canonical URI for a cross-system reconciliation candidate.
    
    If symmetric (e.g. EQUIVALENT, POSSIBLE_MATCH, CONFLICTING, UNRELATED, UNRESOLVED),
    orders the pair lexicographically so candidate(A, B) == candidate(B, A).
    """
    nfc_src_sys = unicodedata.normalize("NFC", str(source_sys).strip()).lower()
    nfc_src_obj = unicodedata.normalize("NFC", str(source_obj).strip()).lower()
    nfc_tgt_sys = unicodedata.normalize("NFC", str(target_sys).strip()).lower()
    nfc_tgt_obj = unicodedata.normalize("NFC", str(target_obj).strip()).lower()

    if is_symmetric:
        pair1 = (nfc_src_sys, nfc_src_obj)
        pair2 = (nfc_tgt_sys, nfc_tgt_obj)
        if pair1 > pair2:
            pair1, pair2 = pair2, pair1
        return generate_canonical_id(
            layer,
            "reconciliation",
            str(correspondence_type),
            pair1[0],
            pair1[1],
            pair2[0],
            pair2[1],
        )
    return generate_canonical_id(
        layer,
        "reconciliation",
        str(correspondence_type),
        nfc_src_sys,
        nfc_src_obj,
        nfc_tgt_sys,
        nfc_tgt_obj,
    )


def generate_multi_reconciliation_id(
    source_sys: str,
    source_objs: tuple[str, ...],
    target_sys: str,
    target_objs: tuple[str, ...],
    correspondence_type: CorrespondenceType | str,
    layer: GraphLayer | str = GraphLayer.BUSINESS,
) -> str:
    """Generate a deterministic canonical URI for 1:N or N:M reconciliation candidates."""
    norm_src_objs = ":".join(normalize_component(o) for o in sorted(source_objs))
    norm_tgt_objs = ":".join(normalize_component(o) for o in sorted(target_objs))
    return generate_canonical_id(
        layer,
        "reconciliation_multi",
        str(correspondence_type),
        source_sys,
        norm_src_objs,
        target_sys,
        norm_tgt_objs,
    )


@dataclass(frozen=True)
class ReconciliationCandidate:
    """First-class cross-system reconciliation correspondence candidate."""
    id: str
    source_system_id: str
    target_system_id: str
    source_object_ids: tuple[str, ...]
    target_object_ids: tuple[str, ...]
    layer: GraphLayer = GraphLayer.BUSINESS
    correspondence_type: CorrespondenceType = CorrespondenceType.POSSIBLE_MATCH
    cardinality: Cardinality = Cardinality.ONE_TO_ONE
    status: AssertionStatus = AssertionStatus.PROPOSED
    confidence: float = 0.5
    factors: tuple[ReconciliationFactor, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    conflict_ids: tuple[str, ...] = ()
    rationale: str = ""
    provenance: Provenance | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not str(self.id).strip():
            raise ValueError("ReconciliationCandidate.id is mandatory")
        if not self.source_object_ids:
            raise ValueError("ReconciliationCandidate.source_object_ids cannot be empty")
        if not self.target_object_ids:
            raise ValueError("ReconciliationCandidate.target_object_ids cannot be empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"ReconciliationCandidate.confidence must be in [0.0, 1.0], got {self.confidence}")

    @property
    def source_object_id(self) -> str:
        """Convenience property for 1:1 or 1:N primary source object."""
        return self.source_object_ids[0]

    @property
    def target_object_id(self) -> str:
        """Convenience property for 1:1 or N:1 primary target object."""
        return self.target_object_ids[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "cardinality": str(self.cardinality),
            "confidence": round(self.confidence, 4),
            "conflict_ids": sorted(self.conflict_ids),
            "correspondence_type": str(self.correspondence_type),
            "evidence_ids": sorted(self.evidence_ids),
            "factors": [f.to_dict() for f in self.factors],
            "id": self.id,
            "layer": str(self.layer),
            "properties": dict(sorted(self.properties.items())),
            "provenance_id": self.provenance.id if self.provenance else None,
            "rationale": self.rationale,
            "source_object_ids": sorted(self.source_object_ids),
            "source_system_id": self.source_system_id,
            "status": str(self.status),
            "target_object_ids": sorted(self.target_object_ids),
            "target_system_id": self.target_system_id,
        }


@dataclass(frozen=True)
class ReconciliationProposal:
    """Formal governance proposal for review and approval of reconciliation candidates."""
    id: str
    candidate_ids: tuple[str, ...]
    status: SemanticPublicationStatus = SemanticPublicationStatus.DRAFT
    submitted_by: str = "reconciliation_engine"
    reviewed_by: str | None = None
    comments: str = ""
    created_at: str | None = None
    reviewed_at: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_ids": sorted(self.candidate_ids),
            "comments": self.comments,
            "created_at": self.created_at,
            "id": self.id,
            "properties": dict(sorted(self.properties.items())),
            "reviewed_at": self.reviewed_at,
            "reviewed_by": self.reviewed_by,
            "status": str(self.status),
            "submitted_by": self.submitted_by,
        }


@dataclass(frozen=True)
class CrossSystemReconciliationResult:
    """Canonical deterministic result of a cross-system reconciliation operation."""
    id: str
    source_system: SystemIdentity
    target_system: SystemIdentity
    candidates: tuple[ReconciliationCandidate, ...]
    conflicts: tuple[Conflict, ...]
    proposals: tuple[ReconciliationProposal, ...]
    evidence: tuple[Evidence, ...]
    provenance: Provenance
    summary: dict[str, int] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidates": [c.to_dict() for c in self.candidates],
            "conflicts": [c.id for c in self.conflicts],
            "diagnostics": dict(sorted(self.diagnostics.items())),
            "evidence": [e.id for e in self.evidence],
            "id": self.id,
            "proposals": [p.to_dict() for p in self.proposals],
            "provenance_id": self.provenance.id,
            "source_system": self.source_system.to_dict(),
            "summary": dict(sorted(self.summary.items())),
            "target_system": self.target_system.to_dict(),
        }
