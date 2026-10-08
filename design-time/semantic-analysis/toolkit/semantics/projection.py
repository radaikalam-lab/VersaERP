"""Outbound Semantic Projection Foundation — Phase 13.

This module implements the outbound semantic projection boundary connecting
governed Business Graph intent down to Target Projections and Execution Proposals.

Path:
    Business Intent / Operation
          ↓
    Semantic Projection Engine
          ↓
    Target System Projection
          ↓
    Execution Intent / Plan
          ↓
    ExecutionProposal (Governed)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from graphmodel.domain.models import (
    ExecutionPlan,
    ExecutionProposal,
    ExecutionProposalStatus,
    ExecutionStep,
    Provenance,
    generate_canonical_id,
    generate_provenance_id,
)
from graphmodel.execution.models import ExecutionOperation
from graphmodel.graph.store import Graph


class ProjectionStrategy(StrEnum):
    """Strategy for semantic-to-target projection."""

    DIRECT = "direct"
    TRANSFORMED = "transformed"
    COMPOSITE = "composite"
    CONDITIONAL = "conditional"


@dataclass(frozen=True)
class FieldProjection:
    """Mapping specification for projecting a single business attribute to a target field."""

    source_attribute_id: str
    target_field_name: str
    data_type: str = "string"
    transformation_rule: str | None = None
    default_value: Any = None
    is_required: bool = False
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "default_value": self.default_value,
            "data_type": self.data_type,
            "is_required": self.is_required,
            "properties": dict(sorted(self.properties.items())),
            "source_attribute_id": self.source_attribute_id,
            "target_field_name": self.target_field_name,
            "transformation_rule": self.transformation_rule,
        }


@dataclass(frozen=True)
class TargetProjection:
    """Specification of target system structure for an outbound projection."""

    projection_id: str
    target_system: str
    target_object_name: str
    field_projections: tuple[FieldProjection, ...] = ()
    strategy: ProjectionStrategy = ProjectionStrategy.DIRECT
    version: str = "v1"
    properties: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.projection_id or not str(self.projection_id).strip():
            raise ValueError("TargetProjection.projection_id is mandatory")
        if not self.target_system or not str(self.target_system).strip():
            raise ValueError("TargetProjection.target_system is mandatory")
        if not self.target_object_name or not str(self.target_object_name).strip():
            raise ValueError("TargetProjection.target_object_name is mandatory")

    def to_dict(self) -> dict[str, Any]:
        return {
            "field_projections": [fp.to_dict() for fp in self.field_projections],
            "projection_id": self.projection_id,
            "properties": dict(sorted(self.properties.items())),
            "strategy": str(self.strategy),
            "target_object_name": self.target_object_name,
            "target_system": self.target_system,
            "version": self.version,
        }


@dataclass(frozen=True)
class OutboundProjectionResult:
    """Result of evaluating a semantic projection from business graph to target proposal."""

    projection_id: str
    business_entity_id: str
    target_system: str
    target_object_name: str
    projected_payload: dict[str, Any]
    operation: ExecutionOperation
    proposal: ExecutionProposal
    provenance: Provenance
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "business_entity_id": self.business_entity_id,
            "diagnostics": dict(sorted(self.diagnostics.items())),
            "operation": str(self.operation),
            "projected_payload": dict(sorted(self.projected_payload.items())),
            "projection_id": self.projection_id,
            "proposal_id": self.proposal.id,
            "provenance_id": self.provenance.id,
            "target_object_name": self.target_object_name,
            "target_system": self.target_system,
        }


class SemanticProjectionEngine:
    """Engine for projecting Business Graph intent into Target Projections and Execution Proposals."""

    def __init__(self, engine_id: str = "semantic_projection_engine_01") -> None:
        self.engine_id = engine_id

    def project_entity(
        self,
        business_entity_id: str,
        graph: Graph,
        target_projection: TargetProjection,
        operation: ExecutionOperation = ExecutionOperation.CREATE,
        proposed_by: str = "system",
        entity_values: dict[str, Any] | None = None,
    ) -> OutboundProjectionResult:
        """Project a single Business Entity node to a target system ExecutionProposal."""
        b_node = graph.get_node(business_entity_id)
        if not b_node:
            raise ValueError(f"Business entity node '{business_entity_id}' not found in graph")

        prov = Provenance(
            id=generate_provenance_id("semantic_projection", self.engine_id, business_entity_id),
            source_ids=(business_entity_id,),
            method="outbound_semantic_projection",
            confidence=0.95,
            assumptions=("Business entity intent projects deterministically to target schema",),
        )

        values = entity_values or b_node.properties
        projected_payload: dict[str, Any] = {}

        for field_proj in target_projection.field_projections:
            val = values.get(field_proj.source_attribute_id)
            if val is None:
                val = values.get(field_proj.target_field_name)
            if val is None and field_proj.default_value is not None:
                val = field_proj.default_value
            projected_payload[field_proj.target_field_name] = val

        proj_id = generate_canonical_id(
            "projection", target_projection.target_system, business_entity_id
        )

        proposal_id = generate_canonical_id(
            "proposal", "execution", target_projection.target_system, business_entity_id
        )

        step = ExecutionStep(
            id=generate_canonical_id("step", proposal_id, "0"),
            step_number=0,
            operation=operation.value if hasattr(operation, "value") else str(operation),
            target=f"{target_projection.target_system}:{target_projection.target_object_name}",
            parameters={"payload": projected_payload},
        )

        plan = ExecutionPlan(
            id=generate_canonical_id("plan", proposal_id),
            proposal_id=proposal_id,
            target_source_id=target_projection.target_system,
            steps=[step],
        )

        proposal = ExecutionProposal(
            id=proposal_id,
            title=f"Outbound Projection for {b_node.properties.get('name', business_entity_id)}",
            description=f"Projected from business entity {business_entity_id} to {target_projection.target_system}",
            proposed_by=proposed_by,
            target_source_id=target_projection.target_system,
            status=ExecutionProposalStatus.DRAFT,
            plan_id=plan.id,
            provenance=prov,
        )

        diagnostics = {
            "field_count": len(projected_payload),
            "strategy": str(target_projection.strategy),
            "version": target_projection.version,
        }

        return OutboundProjectionResult(
            projection_id=proj_id,
            business_entity_id=business_entity_id,
            target_system=target_projection.target_system,
            target_object_name=target_projection.target_object_name,
            projected_payload=projected_payload,
            operation=operation,
            proposal=proposal,
            provenance=prov,
            diagnostics=diagnostics,
        )
