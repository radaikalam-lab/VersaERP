"""
Universal Agent Assurance Domain & Epistemic Integration Fabric (GM-ASSURE-001).

Core Invariants:
1. Agent Claims != Assurance Evidence
2. Assurance Evidence != Truth
3. Assurance Result != Authorization
4. Authorization != Execution
5. Execution != Verification
6. Capability != Authority
7. Evidence != Authority
8. Confidence != Authority
9. Recommendation != Decision
10. Decision != Authorization
11. Understanding != Ownership

Zero execution or governance authority in the assurance substrate.
"""

from __future__ import annotations

import hashlib
import importlib
import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from graphmodel.domain.evidence_integrity import (
    EvidenceIntegrityPackage,
    create_integrity_package,
)
from graphmodel.domain.models import Evidence


class ObservationEpistemicType(StrEnum):
    """Epistemic certainty classification for runtime observations."""

    CLAIMED = "CLAIMED"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"


class ObservationEventType(StrEnum):
    """Runtime event classification."""

    AGENT_PROMPT = "AGENT_PROMPT"
    AGENT_RESPONSE = "AGENT_RESPONSE"
    MODEL_INVOCATION = "MODEL_INVOCATION"
    MODEL_OUTPUT = "MODEL_OUTPUT"
    TOOL_INVOCATION = "TOOL_INVOCATION"
    TOOL_RESULT = "TOOL_RESULT"
    AUTHORIZATION_CHECK = "AUTHORIZATION_CHECK"
    EXECUTION_ATTEMPT = "EXECUTION_ATTEMPT"
    EXECUTION_RESULT = "EXECUTION_RESULT"
    STATE_INSPECTION = "STATE_INSPECTION"
    SYSTEM_VERIFICATION = "SYSTEM_VERIFICATION"


class AssertionType(StrEnum):
    """Deterministic assurance assertion categories."""

    CAPABILITY_COMPLIANCE = "CAPABILITY_COMPLIANCE"
    POLICY_COMPLIANCE = "POLICY_COMPLIANCE"
    WORKFLOW_COMPLIANCE = "WORKFLOW_COMPLIANCE"
    TOOL_COMPLIANCE = "TOOL_COMPLIANCE"
    AUTHORIZATION_COMPLIANCE = "AUTHORIZATION_COMPLIANCE"
    PRECONDITION_COMPLIANCE = "PRECONDITION_COMPLIANCE"
    POSTCONDITION_COMPLIANCE = "POSTCONDITION_COMPLIANCE"
    OUTCOME_COMPLIANCE = "OUTCOME_COMPLIANCE"
    EVIDENCE_COMPLETENESS = "EVIDENCE_COMPLETENESS"
    SCOPE_COMPLIANCE = "SCOPE_COMPLIANCE"


class FindingType(StrEnum):
    """Discrete assurance finding categories."""

    VIOLATION = "VIOLATION"
    WARNING = "WARNING"
    INCONCLUSIVE = "INCONCLUSIVE"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    UNEXPECTED_OPERATION = "UNEXPECTED_OPERATION"
    UNEXPECTED_TOOL = "UNEXPECTED_TOOL"
    UNAUTHORIZED_OPERATION = "UNAUTHORIZED_OPERATION"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    WORKFLOW_DEVIATION = "WORKFLOW_DEVIATION"
    PRECONDITION_FAILURE = "PRECONDITION_FAILURE"
    POSTCONDITION_FAILURE = "POSTCONDITION_FAILURE"
    OUTCOME_NOT_VERIFIED = "OUTCOME_NOT_VERIFIED"


class FindingSeverity(StrEnum):
    """Severity classification for assurance findings."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AssuranceStatus(StrEnum):
    """Aggregated deterministic assurance evaluation status."""

    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass(frozen=True)
class AssuranceContract:
    """Declared behavioral, capability, and authorization boundaries for an agent."""

    contract_id: str
    contract_version: str
    agent_identity: str
    agent_version: str
    accountable_owner: str
    capability_declarations: tuple[str, ...] = field(default_factory=tuple)
    allowed_operations: tuple[str, ...] = field(default_factory=tuple)
    forbidden_operations: tuple[str, ...] = field(default_factory=tuple)
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    forbidden_tools: tuple[str, ...] = field(default_factory=tuple)
    allowed_scopes: tuple[str, ...] = field(default_factory=tuple)
    forbidden_scopes: tuple[str, ...] = field(default_factory=tuple)
    required_approvals: tuple[str, ...] = field(default_factory=tuple)
    required_evidence: tuple[str, ...] = field(default_factory=tuple)
    expected_workflow: tuple[str, ...] = field(default_factory=tuple)
    preconditions: dict[str, Any] = field(default_factory=dict)
    postconditions: dict[str, Any] = field(default_factory=dict)
    policy_references: tuple[str, ...] = field(default_factory=tuple)
    governance_references: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "agent_identity": self.agent_identity,
            "agent_version": self.agent_version,
            "accountable_owner": self.accountable_owner,
            "capability_declarations": list(self.capability_declarations),
            "allowed_operations": list(self.allowed_operations),
            "forbidden_operations": list(self.forbidden_operations),
            "allowed_tools": list(self.allowed_tools),
            "forbidden_tools": list(self.forbidden_tools),
            "allowed_scopes": list(self.allowed_scopes),
            "forbidden_scopes": list(self.forbidden_scopes),
            "required_approvals": list(self.required_approvals),
            "required_evidence": list(self.required_evidence),
            "expected_workflow": list(self.expected_workflow),
            "preconditions": dict(self.preconditions),
            "postconditions": dict(self.postconditions),
            "policy_references": list(self.policy_references),
            "governance_references": list(self.governance_references),
        }


@dataclass(frozen=True)
class AssuranceObservation:
    """Immutable, timestamped observation categorized by epistemic certainty."""

    observation_id: str
    correlation_id: str
    agent_identity: str
    agent_version: str
    observation_type: ObservationEpistemicType
    event_type: ObservationEventType
    payload: dict[str, Any]
    sequence_number: int
    timestamp: str
    provenance_id: str | None = None
    evidence_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "correlation_id": self.correlation_id,
            "agent_identity": self.agent_identity,
            "agent_version": self.agent_version,
            "observation_type": str(self.observation_type),
            "event_type": str(self.event_type),
            "payload": dict(self.payload),
            "sequence_number": self.sequence_number,
            "timestamp": self.timestamp,
            "provenance_id": self.provenance_id,
            "evidence_id": self.evidence_id,
        }


@dataclass(frozen=True)
class AssuranceFinding:
    """Discrete evidence-backed evaluation finding."""

    finding_id: str
    assertion_type: AssertionType
    finding_type: FindingType
    description: str
    observation_references: tuple[str, ...] = field(default_factory=tuple)
    evidence_references: tuple[str, ...] = field(default_factory=tuple)
    severity: FindingSeverity = FindingSeverity.MEDIUM

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "assertion_type": str(self.assertion_type),
            "finding_type": str(self.finding_type),
            "description": self.description,
            "observation_references": list(self.observation_references),
            "evidence_references": list(self.evidence_references),
            "severity": str(self.severity),
        }


@dataclass(frozen=True)
class AssuranceEvaluation:
    """Aggregated deterministic assurance evaluation."""

    evaluation_id: str
    contract_id: str
    contract_version: str
    agent_identity: str
    correlation_id: str
    status: AssuranceStatus
    assertions_evaluated: tuple[str, ...]
    findings: tuple[AssuranceFinding, ...]
    evaluated_at: str
    commitment_digest: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "agent_identity": self.agent_identity,
            "correlation_id": self.correlation_id,
            "status": str(self.status),
            "assertions_evaluated": list(self.assertions_evaluated),
            "findings": [f.to_dict() for f in self.findings],
            "evaluated_at": self.evaluated_at,
            "commitment_digest": self.commitment_digest,
        }


@dataclass(frozen=True)
class AssuranceEpistemicInterpretation:
    """GraphModel semantic interpretation of an assurance evaluation."""

    interpretation_id: str
    evaluation_id: str
    contract_id: str
    agent_identity: str
    correlation_id: str
    assurance_status: AssuranceStatus
    business_impact_summary: str
    epistemic_confidence: float
    governance_recommendation: str
    interpreted_at: str


def interpret_assurance_evaluation(
    evaluation: AssuranceEvaluation,
    interpretation_id: str,
    interpreted_at: str = "2026-09-30T12:00:00Z",
) -> AssuranceEpistemicInterpretation:
    """Interpret assurance findings semantically within GraphModel epistemic control plane."""
    if evaluation.status == AssuranceStatus.PASS:
        impact = "Agent adhered strictly to declared capabilities, tools, authorizations, and verified outcomes."
        recommendation = "PROCEED_TO_GOVERNANCE_REVIEW"
        confidence = 1.0
    elif evaluation.status == AssuranceStatus.FAIL:
        reasons = [f.description for f in evaluation.findings if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.HIGH)]
        impact = f"Agent violated declared boundaries: {'; '.join(reasons)}"
        recommendation = "REJECT_DUE_TO_VIOLATION"
        confidence = 1.0
    elif evaluation.status == AssuranceStatus.INCONCLUSIVE:
        missing = [f.description for f in evaluation.findings if f.finding_type in (FindingType.OUTCOME_NOT_VERIFIED, FindingType.MISSING_EVIDENCE)]
        impact = f"Evidence or verification is incomplete: {'; '.join(missing)}"
        recommendation = "REQUIRE_ADDITIONAL_EVIDENCE"
        confidence = 0.5
    else:
        impact = "Evaluation was not conducted or skipped."
        recommendation = "HOLD_FOR_MANUAL_AUDIT"
        confidence = 0.0

    return AssuranceEpistemicInterpretation(
        interpretation_id=interpretation_id,
        evaluation_id=evaluation.evaluation_id,
        contract_id=evaluation.contract_id,
        agent_identity=evaluation.agent_identity,
        correlation_id=evaluation.correlation_id,
        assurance_status=evaluation.status,
        business_impact_summary=impact,
        epistemic_confidence=confidence,
        governance_recommendation=recommendation,
        interpreted_at=interpreted_at,
    )


def build_assurance_evidence_package(
    evaluation: AssuranceEvaluation,
    observations: list[AssuranceObservation],
    package_id: str | None = None,
    created_at: str = "2026-09-30T12:00:00Z",
) -> EvidenceIntegrityPackage:
    """Package an assurance evaluation and observations into a tamper-evident EvidenceIntegrityPackage."""
    evidence_items: list[Evidence] = []

    # Main evaluation evidence
    eval_evidence = Evidence(
        id=f"evi:{evaluation.evaluation_id}",
        source_id=evaluation.contract_id,
        source_type="assurance_evaluation",
        source_version=evaluation.contract_version,
        locator=f"correlation/{evaluation.correlation_id}",
        excerpt=f"Assurance status: {evaluation.status.value}",
        confidence=1.0 if evaluation.status == AssuranceStatus.PASS else 0.5,
        properties={
            "agent_identity": evaluation.agent_identity,
            "status": evaluation.status.value,
            "findings_count": len(evaluation.findings),
            "commitment_digest": evaluation.commitment_digest or "",
        },
    )
    evidence_items.append(eval_evidence)

    # Observation evidence items
    for obs in observations:
        obs_evidence = Evidence(
            id=f"evi:{obs.observation_id}",
            source_id=obs.agent_identity,
            source_type=f"assurance_observation:{obs.event_type.value}",
            source_version=obs.agent_version,
            locator=f"seq/{obs.sequence_number}",
            excerpt=f"Observed {obs.event_type.value} ({obs.observation_type.value})",
            confidence=1.0 if obs.observation_type == ObservationEpistemicType.VERIFIED else 0.8,
            properties={
                "observation_type": obs.observation_type.value,
                "event_type": obs.event_type.value,
                "correlation_id": obs.correlation_id,
            },
        )
        evidence_items.append(obs_evidence)

    pkg_id = package_id or f"urn:graphmodel:assurance_package:{evaluation.correlation_id}"
    return create_integrity_package(evidence_items, package_id=pkg_id, created_at=created_at)


def evaluate_assurance_trace(
    contract: AssuranceContract,
    observations: list[AssuranceObservation],
    correlation_id: str,
    evaluation_timestamp: str = "2026-09-30T12:00:00Z",
) -> AssuranceEvaluation:
    """Evaluate an assurance trace, delegating dynamically to Cognitia if available."""
    try:
        cgn_assurance = importlib.import_module("cognitia.assurance")
        cgn_engine_cls = getattr(cgn_assurance, "AssuranceEngine")
        cgn_obs_cls = getattr(cgn_assurance, "AssuranceObservation")
        cgn_contract_cls = getattr(cgn_assurance, "AssuranceContract")
        cgn_epistemic_cls = getattr(cgn_assurance, "ObservationEpistemicType")
        cgn_event_cls = getattr(cgn_assurance, "ObservationEventType")

        cgn_contract = cgn_contract_cls(
            contract_id=contract.contract_id,
            contract_version=contract.contract_version,
            agent_identity=contract.agent_identity,
            agent_version=contract.agent_version,
            accountable_owner=contract.accountable_owner,
            capability_declarations=list(contract.capability_declarations),
            allowed_operations=list(contract.allowed_operations),
            forbidden_operations=list(contract.forbidden_operations),
            allowed_tools=list(contract.allowed_tools),
            forbidden_tools=list(contract.forbidden_tools),
            allowed_scopes=list(contract.allowed_scopes),
            forbidden_scopes=list(contract.forbidden_scopes),
            required_approvals=list(contract.required_approvals),
            required_evidence=list(contract.required_evidence),
            expected_workflow=list(contract.expected_workflow),
            preconditions=dict(contract.preconditions),
            postconditions=dict(contract.postconditions),
            policy_references=list(contract.policy_references),
            governance_references=list(contract.governance_references),
        )

        cgn_obs_list = []
        for o in observations:
            cgn_obs = cgn_obs_cls(
                observation_id=o.observation_id,
                correlation_id=o.correlation_id,
                agent_identity=o.agent_identity,
                agent_version=o.agent_version,
                observation_type=getattr(cgn_epistemic_cls, o.observation_type.value),
                event_type=getattr(cgn_event_cls, o.event_type.value),
                payload=dict(o.payload),
                sequence_number=o.sequence_number,
                timestamp=o.timestamp,
                provenance_id=o.provenance_id,
                evidence_id=o.evidence_id,
            )
            cgn_obs_list.append(cgn_obs)

        engine = cgn_engine_cls()
        cgn_eval = engine.evaluate_trace(cgn_contract, cgn_obs_list, correlation_id, evaluation_timestamp)

        findings = []
        for f in cgn_eval.findings:
            findings.append(
                AssuranceFinding(
                    finding_id=f.finding_id,
                    assertion_type=AssertionType(f.assertion_type.value),
                    finding_type=FindingType(f.finding_type.value),
                    description=f.description,
                    observation_references=tuple(f.observation_references),
                    evidence_references=tuple(f.evidence_references),
                    severity=FindingSeverity(f.severity.value),
                )
            )

        return AssuranceEvaluation(
            evaluation_id=cgn_eval.evaluation_id,
            contract_id=cgn_eval.contract_id,
            contract_version=cgn_eval.contract_version,
            agent_identity=cgn_eval.agent_identity,
            correlation_id=cgn_eval.correlation_id,
            status=AssuranceStatus(cgn_eval.status.value),
            assertions_evaluated=tuple(cgn_eval.assertions_evaluated),
            findings=tuple(findings),
            evaluated_at=cgn_eval.evaluated_at,
            commitment_digest=cgn_eval.commitment_digest,
        )
    except (ImportError, AttributeError):
        # Deterministic fallback evaluation within GraphModel
        return _fallback_evaluate_trace(contract, observations, correlation_id, evaluation_timestamp)


def _fallback_evaluate_trace(
    contract: AssuranceContract,
    observations: list[AssuranceObservation],
    correlation_id: str,
    evaluation_timestamp: str,
) -> AssuranceEvaluation:
    """GraphModel deterministic standalone fallback evaluation."""
    sorted_obs = sorted(observations, key=lambda o: (o.sequence_number, o.timestamp))
    findings: list[AssuranceFinding] = []
    assertions_evaluated: list[str] = []

    # 1. TOOL_COMPLIANCE
    assertions_evaluated.append(AssertionType.TOOL_COMPLIANCE.value)
    for obs in sorted_obs:
        if obs.event_type == ObservationEventType.TOOL_INVOCATION:
            tool_name = obs.payload.get("tool_name", "")
            if contract.forbidden_tools and tool_name in contract.forbidden_tools:
                findings.append(
                    AssuranceFinding(
                        finding_id=f"finding:tool:forbidden:{obs.observation_id}",
                        assertion_type=AssertionType.TOOL_COMPLIANCE,
                        finding_type=FindingType.UNEXPECTED_TOOL,
                        description=f"Forbidden tool '{tool_name}' invoked by agent '{obs.agent_identity}'",
                        observation_references=(obs.observation_id,),
                        severity=FindingSeverity.CRITICAL,
                    )
                )
            elif contract.allowed_tools and tool_name not in contract.allowed_tools:
                findings.append(
                    AssuranceFinding(
                        finding_id=f"finding:tool:unallowed:{obs.observation_id}",
                        assertion_type=AssertionType.TOOL_COMPLIANCE,
                        finding_type=FindingType.UNEXPECTED_TOOL,
                        description=f"Tool '{tool_name}' is not in allowed_tools list",
                        observation_references=(obs.observation_id,),
                        severity=FindingSeverity.HIGH,
                    )
                )

    # 2. POLICY_COMPLIANCE
    assertions_evaluated.append(AssertionType.POLICY_COMPLIANCE.value)
    for obs in sorted_obs:
        op_name = obs.payload.get("operation_name") or obs.payload.get("action")
        if op_name:
            if contract.forbidden_operations and op_name in contract.forbidden_operations:
                findings.append(
                    AssuranceFinding(
                        finding_id=f"finding:op:forbidden:{obs.observation_id}",
                        assertion_type=AssertionType.POLICY_COMPLIANCE,
                        finding_type=FindingType.POLICY_VIOLATION,
                        description=f"Forbidden operation '{op_name}' executed",
                        observation_references=(obs.observation_id,),
                        severity=FindingSeverity.CRITICAL,
                    )
                )
            elif contract.allowed_operations and op_name not in contract.allowed_operations:
                findings.append(
                    AssuranceFinding(
                        finding_id=f"finding:op:unallowed:{obs.observation_id}",
                        assertion_type=AssertionType.POLICY_COMPLIANCE,
                        finding_type=FindingType.UNEXPECTED_OPERATION,
                        description=f"Operation '{op_name}' is not in declared allowed_operations",
                        observation_references=(obs.observation_id,),
                        severity=FindingSeverity.HIGH,
                    )
                )

    # 3. SCOPE_COMPLIANCE
    assertions_evaluated.append(AssertionType.SCOPE_COMPLIANCE.value)
    for obs in sorted_obs:
        scope = (
            obs.payload.get("target_scope")
            or obs.payload.get("scope")
            or obs.payload.get("resource_scope")
            or obs.payload.get("target_resource")
        )
        if scope:
            if contract.forbidden_scopes and scope in contract.forbidden_scopes:
                findings.append(
                    AssuranceFinding(
                        finding_id=f"finding:scope:forbidden:{obs.observation_id}",
                        assertion_type=AssertionType.SCOPE_COMPLIANCE,
                        finding_type=FindingType.VIOLATION,
                        description=f"Target scope '{scope}' is explicitly forbidden",
                        observation_references=(obs.observation_id,),
                        severity=FindingSeverity.CRITICAL,
                    )
                )
            elif contract.allowed_scopes and scope not in contract.allowed_scopes:
                findings.append(
                    AssuranceFinding(
                        finding_id=f"finding:scope:unallowed:{obs.observation_id}",
                        assertion_type=AssertionType.SCOPE_COMPLIANCE,
                        finding_type=FindingType.VIOLATION,
                        description=f"Target scope '{scope}' is not within declared allowed_scopes",
                        observation_references=(obs.observation_id,),
                        severity=FindingSeverity.HIGH,
                    )
                )

    # 4. AUTHORIZATION_COMPLIANCE
    assertions_evaluated.append(AssertionType.AUTHORIZATION_COMPLIANCE.value)
    authorized_contexts = set()
    for obs in sorted_obs:
        if obs.event_type == ObservationEventType.AUTHORIZATION_CHECK:
            auth_id = obs.payload.get("authorization_id")
            if auth_id and obs.payload.get("authorized", False):
                authorized_contexts.add(auth_id)
        elif obs.event_type in (ObservationEventType.EXECUTION_ATTEMPT, ObservationEventType.EXECUTION_RESULT):
            if obs.payload.get("is_mutating", True):
                auth_ref = obs.payload.get("authorization_id") or obs.payload.get("authorization_ref")
                if not auth_ref:
                    findings.append(
                        AssuranceFinding(
                            finding_id=f"finding:auth:missing:{obs.observation_id}",
                            assertion_type=AssertionType.AUTHORIZATION_COMPLIANCE,
                            finding_type=FindingType.UNAUTHORIZED_OPERATION,
                            description="Mutating execution attempted without authorization reference",
                            observation_references=(obs.observation_id,),
                            severity=FindingSeverity.CRITICAL,
                        )
                    )
                elif auth_ref not in authorized_contexts and not obs.payload.get("authorization_valid", False):
                    findings.append(
                        AssuranceFinding(
                            finding_id=f"finding:auth:unverified:{obs.observation_id}",
                            assertion_type=AssertionType.AUTHORIZATION_COMPLIANCE,
                            finding_type=FindingType.UNAUTHORIZED_OPERATION,
                            description=f"Mutating execution referenced unverified authorization '{auth_ref}'",
                            observation_references=(obs.observation_id,),
                            severity=FindingSeverity.CRITICAL,
                        )
                    )

    # 5. POSTCONDITION & OUTCOME COMPLIANCE
    if contract.postconditions:
        assertions_evaluated.append(AssertionType.POSTCONDITION_COMPLIANCE.value)
        verifications = [
            obs for obs in sorted_obs
            if obs.observation_type == ObservationEpistemicType.VERIFIED
            or obs.event_type == ObservationEventType.SYSTEM_VERIFICATION
        ]
        if not verifications:
            findings.append(
                AssuranceFinding(
                    finding_id="finding:postcond:no_verification",
                    assertion_type=AssertionType.POSTCONDITION_COMPLIANCE,
                    finding_type=FindingType.OUTCOME_NOT_VERIFIED,
                    description="No independent VERIFIED observation found to validate postconditions",
                    severity=FindingSeverity.HIGH,
                )
            )
        else:
            verified_state: dict[str, Any] = {}
            for v in verifications:
                verified_state.update(v.payload.get("verified_state", {}))
                verified_state.update(v.payload.get("state", {}))

            for k, expected_v in contract.postconditions.items():
                if k not in verified_state:
                    findings.append(
                        AssuranceFinding(
                            finding_id=f"finding:postcond:unverified:{k}",
                            assertion_type=AssertionType.POSTCONDITION_COMPLIANCE,
                            finding_type=FindingType.OUTCOME_NOT_VERIFIED,
                            description=f"Declared postcondition '{k}' was not independently verified",
                            severity=FindingSeverity.HIGH,
                        )
                    )
                elif verified_state[k] != expected_v:
                    findings.append(
                        AssuranceFinding(
                            finding_id=f"finding:postcond:failed:{k}",
                            assertion_type=AssertionType.POSTCONDITION_COMPLIANCE,
                            finding_type=FindingType.POSTCONDITION_FAILURE,
                            description=f"Postcondition '{k}' verification failed: expected {expected_v}, actual {verified_state[k]}",
                            severity=FindingSeverity.CRITICAL,
                        )
                    )

    # Status resolution
    fail_types = {
        FindingType.VIOLATION,
        FindingType.UNAUTHORIZED_OPERATION,
        FindingType.UNEXPECTED_TOOL,
        FindingType.POLICY_VIOLATION,
        FindingType.WORKFLOW_DEVIATION,
        FindingType.PRECONDITION_FAILURE,
        FindingType.POSTCONDITION_FAILURE,
    }
    inconclusive_types = {
        FindingType.INCONCLUSIVE,
        FindingType.MISSING_EVIDENCE,
        FindingType.OUTCOME_NOT_VERIFIED,
    }

    status = AssuranceStatus.PASS
    for f in findings:
        if f.finding_type in fail_types:
            status = AssuranceStatus.FAIL
            break
        elif f.finding_type in inconclusive_types:
            status = AssuranceStatus.INCONCLUSIVE

    # Deterministic evaluation identity derived from canonicalized semantic inputs
    identity_dict = {
        "contract_id": contract.contract_id,
        "contract_version": contract.contract_version,
        "agent_identity": contract.agent_identity,
        "correlation_id": correlation_id,
        "observations": [o.to_dict() for o in sorted_obs],
    }
    identity_bytes = json.dumps(identity_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")
    identity_digest = hashlib.sha256(identity_bytes).hexdigest()
    eval_id = f"eval:{contract.contract_id}:{correlation_id}:{identity_digest[:16]}"

    preliminary_dict = {
        "evaluation_id": eval_id,
        "contract_id": contract.contract_id,
        "contract_version": contract.contract_version,
        "agent_identity": contract.agent_identity,
        "correlation_id": correlation_id,
        "status": str(status),
        "assertions_evaluated": list(assertions_evaluated),
        "findings": [f.to_dict() for f in findings],
        "evaluated_at": evaluation_timestamp,
    }
    eval_bytes = json.dumps(preliminary_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")
    commitment_digest = hashlib.sha256(eval_bytes).hexdigest()

    return AssuranceEvaluation(
        evaluation_id=eval_id,
        contract_id=contract.contract_id,
        contract_version=contract.contract_version,
        agent_identity=contract.agent_identity,
        correlation_id=correlation_id,
        status=status,
        assertions_evaluated=tuple(assertions_evaluated),
        findings=tuple(findings),
        evaluated_at=evaluation_timestamp,
        commitment_digest=commitment_digest,
    )
