"""
Evidence Integrity & Cryptographic Commitment Fabric (GM-EVI-001).

Core Invariants:
1. Evidence != Authority
2. Commitment = Integrity of Committed Evidence != Factual Truth of Claim
3. Attestation != Truth != Authority
4. Commitment Verification != Governance Approval != Execution Authorization
5. Execution != Verification
"""

from __future__ import annotations

import hashlib
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from graphmodel.domain.models import Evidence


class CommitmentAlgorithm(StrEnum):
    """Canonical cryptographic commitment algorithms."""

    SHA256 = "sha256"
    SHA256_MERKLE = "sha256_merkle"


class CommitmentVersion(StrEnum):
    """Version of cryptographic commitment rules."""

    V1_0 = "v1.0.0"


class CanonicalizationVersion(StrEnum):
    """Version of deterministic evidence canonicalization rules."""

    V1_0 = "v1.0.0"


class EvidenceVerificationStatus(StrEnum):
    """Outcome status of cryptographic evidence integrity verification."""

    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    INCONCLUSIVE = "INCONCLUSIVE"


SENSITIVE_FIELD_NAMES = {
    "password",
    "pwd",
    "secret",
    "token",
    "api_key",
    "private_key",
    "credential",
    "authorization_bearer",
}

CREDENTIAL_PATTERN = re.compile(r"[a-zA-Z0-9_]+/[^@\s]+@[a-zA-Z0-9_.:/]+", re.IGNORECASE)


def _sanitize_properties(props: dict[str, Any]) -> dict[str, Any]:
    """Scrub sensitive credentials and embedded connection strings before canonicalization."""
    sanitized: dict[str, Any] = {}
    for k in sorted(props.keys()):
        k_lower = str(k).lower()
        if any(s in k_lower for s in SENSITIVE_FIELD_NAMES):
            continue  # Exclude credential keys entirely

        v = props[k]
        if isinstance(v, str) and CREDENTIAL_PATTERN.search(v):
            sanitized[k] = "[REDACTED: credential removed]"
        elif isinstance(v, dict):
            sanitized[k] = _sanitize_properties(v)
        else:
            sanitized[k] = v
    return sanitized


def canonicalize_evidence(
    evidence: Evidence,
    version: CanonicalizationVersion = CanonicalizationVersion.V1_0,
) -> bytes:
    """Produce deterministic, versioned, credential-scrubbed UTF-8 bytes for an Evidence object.

    Architectural Boundary:
    1. Evidence Normalization Policy (GraphModel owned):
       - Scrub sensitive credentials and embedded URI passwords.
       - Filter ephemeral execution/generation timestamps.
       - Project canonical Evidence attributes.
    2. Deterministic Canonicalization V1 (Computational formatting):
       - Ascending lexicographical key sorting.
       - Compact delimiter formatting (no extra whitespace).
       - UTF-8 byte serialization.
    """
    if version != CanonicalizationVersion.V1_0:
        raise ValueError(f"Unsupported canonicalization version: {version}")

    sanitized_props = _sanitize_properties(evidence.properties or {})

    canonical_dict = {
        "confidence": round(float(evidence.confidence), 6) if evidence.confidence is not None else None,
        "excerpt": evidence.excerpt,
        "id": evidence.id,
        "locator": evidence.locator,
        "properties": sanitized_props,
        "source_id": evidence.source_id,
        "source_type": evidence.source_type,
        "source_version": evidence.source_version,
    }

    # Deterministic Canonicalization V1 formatting
    json_str = json.dumps(canonical_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return json_str.encode("utf-8")


# =========================================================================
# GraphModel Compatibility Fallback Computational Substrate
# Normative Implementation: Cognitia Computational Substrate (cognitia.computational / rust/cognitia-computational)
# Fallback Role: Standalone / in-process resilience adhering to the identical contract
# =========================================================================


def _compute_sha256(data: bytes) -> str:
    """Compute standard SHA-256 hexadecimal digest (fallback substrate)."""
    return hashlib.sha256(data).hexdigest()


def compute_leaf_hash(data: bytes) -> str:
    """Compute SHA-256 leaf hash with domain separator 0x00.

    Domain separation establishes distinct hash domains for leaf and interior
    nodes and prevents ambiguity between those node types.
    """
    hasher = hashlib.sha256()
    hasher.update(b"\x00")
    hasher.update(data)
    return hasher.hexdigest()


def compute_interior_hash(left_hex: str, right_hex: str) -> str:
    """Compute SHA-256 interior node hash with domain separator 0x01.

    Domain separation establishes distinct hash domains for leaf and interior
    nodes and prevents ambiguity between those node types.
    """
    left_bytes = bytes.fromhex(left_hex)
    right_bytes = bytes.fromhex(right_hex)
    hasher = hashlib.sha256()
    hasher.update(b"\x01")
    hasher.update(left_bytes)
    hasher.update(right_bytes)
    return hasher.hexdigest()


def _verify_merkle_proof_computation(proof: MerkleProof, expected_root_hex: str) -> bool:
    """Pure computational Merkle audit proof verification (fallback substrate)."""
    if proof.root_hash.lower() != expected_root_hex.lower():
        return False
    try:
        curr_hash = proof.leaf_hash
        for step in proof.steps:
            if step.position == "left":
                curr_hash = compute_interior_hash(step.hash, curr_hash)
            elif step.position == "right":
                curr_hash = compute_interior_hash(curr_hash, step.hash)
            else:
                return False
        return curr_hash.lower() == expected_root_hex.lower()
    except Exception:
        return False


@dataclass(frozen=True)
class MerkleProofStep:
    """A single step along the Merkle audit path."""

    hash: str
    position: str  # "left" | "right"


@dataclass(frozen=True)
class MerkleProof:
    """Merkle audit proof establishing membership in an evidence root."""

    leaf_id: str
    leaf_hash: str
    root_hash: str
    steps: tuple[MerkleProofStep, ...]
    algorithm: str = "sha256_merkle"

    def to_dict(self) -> dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "leaf_hash": self.leaf_hash,
            "leaf_id": self.leaf_id,
            "root_hash": self.root_hash,
            "steps": [{"hash": s.hash, "position": s.position} for s in self.steps],
        }


@dataclass(frozen=True)
class EvidenceLeaf:
    """A canonical evidence leaf in a Merkle tree."""

    evidence_id: str
    canonical_bytes: bytes
    leaf_hash: str
    index: int


@dataclass(frozen=True)
class EvidenceCommitment:
    """Cryptographic commitment for a single evidence item or Merkle root."""

    commitment_id: str
    evidence_id: str
    algorithm: CommitmentAlgorithm | str
    algorithm_version: CommitmentVersion | str
    canonicalization_version: CanonicalizationVersion | str
    digest: str
    created_at: str
    provenance_id: str | None = None
    merkle_root: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "algorithm": self.algorithm.value if isinstance(self.algorithm, CommitmentAlgorithm) else str(self.algorithm),
            "algorithm_version": self.algorithm_version.value if isinstance(self.algorithm_version, CommitmentVersion) else str(self.algorithm_version),
            "canonicalization_version": self.canonicalization_version.value if isinstance(self.canonicalization_version, CanonicalizationVersion) else str(self.canonicalization_version),
            "commitment_id": self.commitment_id,
            "created_at": self.created_at,
            "digest": self.digest,
            "evidence_id": self.evidence_id,
            "merkle_root": self.merkle_root,
            "provenance_id": self.provenance_id,
        }



@dataclass(frozen=True)
class EvidenceIntegrityPackage:
    """A package of evidence items with individual and Merkle commitments."""

    package_id: str
    evidence_items: tuple[Evidence, ...]
    commitments: tuple[EvidenceCommitment, ...]
    merkle_root: str | None = None
    canonicalization_version: CanonicalizationVersion = CanonicalizationVersion.V1_0
    created_at: str = "2026-09-30T00:00:00Z"

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonicalization_version": self.canonicalization_version.value,
            "commitments": [c.to_dict() for c in self.commitments],
            "created_at": self.created_at,
            "evidence_count": len(self.evidence_items),
            "evidence_ids": [e.id for e in self.evidence_items],
            "merkle_root": self.merkle_root,
            "package_id": self.package_id,
        }


@dataclass(frozen=True)
class EvidenceAttestation:
    """Attestation that a commitment was verified, with explicit non-truth disclaimer."""

    attestation_id: str
    commitment_id: str
    attester_id: str
    status: EvidenceVerificationStatus
    attested_at: str
    disclaimer: str = "Attestation verifies cryptographic commitment integrity only, not factual or business claim truth."

    def to_dict(self) -> dict[str, Any]:
        return {
            "attestation_id": self.attestation_id,
            "attested_at": self.attested_at,
            "attester_id": self.attester_id,
            "commitment_id": self.commitment_id,
            "disclaimer": self.disclaimer,
            "status": self.status.value,
        }


def commit_evidence(
    evidence: Evidence,
    algorithm: CommitmentAlgorithm = CommitmentAlgorithm.SHA256,
    version: CommitmentVersion = CommitmentVersion.V1_0,
    canonicalization_version: CanonicalizationVersion = CanonicalizationVersion.V1_0,
    provenance_id: str | None = None,
    created_at: str | None = None,
) -> EvidenceCommitment:
    """Create a deterministic cryptographic commitment for an individual Evidence item."""
    canonical_bytes = canonicalize_evidence(evidence, canonicalization_version)
    digest = hashlib.sha256(canonical_bytes).hexdigest()
    ts = created_at or "2026-09-30T00:00:00Z"

    commitment_id = f"urn:graphmodel:commitment:sha256:{evidence.id}:{digest[:16]}"
    return EvidenceCommitment(
        commitment_id=commitment_id,
        evidence_id=evidence.id,
        algorithm=algorithm,
        algorithm_version=version,
        canonicalization_version=canonicalization_version,
        digest=digest,
        created_at=ts,
        provenance_id=provenance_id,
        merkle_root=None,
    )


def build_evidence_merkle_tree(
    evidence_list: list[Evidence],
) -> tuple[str, list[EvidenceLeaf], dict[str, MerkleProof]]:
    """Build a deterministic Merkle tree over a collection of Evidence items."""
    if not evidence_list:
        empty_root = _compute_sha256(b"")
        return empty_root, [], {}

    # 1. Canonical deduplication and deterministic sorting by evidence.id
    unique_map: dict[str, Evidence] = {e.id: e for e in evidence_list}
    sorted_evidence = [unique_map[k] for k in sorted(unique_map.keys())]

    # 2. Build leaves
    leaves: list[EvidenceLeaf] = []
    leaf_hashes: list[str] = []
    for idx, evi in enumerate(sorted_evidence):
        c_bytes = canonicalize_evidence(evi)
        l_hash = compute_leaf_hash(c_bytes)
        leaves.append(EvidenceLeaf(evidence_id=evi.id, canonical_bytes=c_bytes, leaf_hash=l_hash, index=idx))
        leaf_hashes.append(l_hash)

    # 3. Build tree layers
    layers: list[list[str]] = [leaf_hashes]
    current_layer = leaf_hashes[:]
    while len(current_layer) > 1:
        next_layer: list[str] = []
        for i in range(0, len(current_layer), 2):
            if i + 1 < len(current_layer):
                next_layer.append(compute_interior_hash(current_layer[i], current_layer[i + 1]))
            else:
                # Duplicate odd node
                next_layer.append(compute_interior_hash(current_layer[i], current_layer[i]))
        layers.append(next_layer)
        current_layer = next_layer

    root_hash = layers[-1][0]

    # 4. Generate Merkle proofs
    proofs: dict[str, MerkleProof] = {}
    for idx, leaf in enumerate(leaves):
        steps: list[MerkleProofStep] = []
        curr_idx = idx
        for layer in layers[:-1]:
            is_right = (curr_idx % 2 == 1)
            if is_right:
                sib_idx = curr_idx - 1
            elif curr_idx + 1 < len(layer):
                sib_idx = curr_idx + 1
            else:
                sib_idx = curr_idx  # Odd node duplicated

            steps.append(MerkleProofStep(
                hash=layer[sib_idx],
                position="left" if is_right else "right",
            ))
            curr_idx //= 2

        proofs[leaf.evidence_id] = MerkleProof(
            leaf_id=leaf.evidence_id,
            leaf_hash=leaf.leaf_hash,
            root_hash=root_hash,
            steps=tuple(steps),
        )

    return root_hash, leaves, proofs


def create_integrity_package(
    evidence_list: list[Evidence],
    package_id: str | None = None,
    created_at: str = "2026-09-30T00:00:00Z",
) -> EvidenceIntegrityPackage:
    """Construct an EvidenceIntegrityPackage with single commitments and Merkle root."""
    root_hash, _, _ = build_evidence_merkle_tree(evidence_list)
    commitments: list[EvidenceCommitment] = []
    for evi in evidence_list:
        c = commit_evidence(evi, created_at=created_at)
        commitments.append(EvidenceCommitment(
            commitment_id=c.commitment_id,
            evidence_id=c.evidence_id,
            algorithm=CommitmentAlgorithm.SHA256_MERKLE,
            algorithm_version=CommitmentVersion.V1_0,
            canonicalization_version=CanonicalizationVersion.V1_0,
            digest=c.digest,
            created_at=c.created_at,
            provenance_id=c.provenance_id,
            merkle_root=root_hash,
        ))

    pkg_id = package_id or f"urn:graphmodel:evidence_package:{root_hash[:16]}"
    return EvidenceIntegrityPackage(
        package_id=pkg_id,
        evidence_items=tuple(evidence_list),
        commitments=tuple(commitments),
        merkle_root=root_hash,
        canonicalization_version=CanonicalizationVersion.V1_0,
        created_at=created_at,
    )


def verify_evidence_integrity(
    evidence: Evidence,
    commitment: EvidenceCommitment,
) -> EvidenceVerificationStatus:
    """Independently verify an evidence item against a commitment."""
    if commitment.canonicalization_version != CanonicalizationVersion.V1_0:
        return EvidenceVerificationStatus.INCONCLUSIVE

    if commitment.algorithm_version != CommitmentVersion.V1_0:
        return EvidenceVerificationStatus.INCONCLUSIVE

    try:
        canonical_bytes = canonicalize_evidence(evidence, commitment.canonicalization_version)
        recomputed_digest = _compute_sha256(canonical_bytes)

        if recomputed_digest == commitment.digest:
            return EvidenceVerificationStatus.VERIFIED
        return EvidenceVerificationStatus.FAILED
    except Exception:
        return EvidenceVerificationStatus.INCONCLUSIVE


def verify_merkle_proof(
    leaf_hash: str,
    proof: MerkleProof,
    expected_root: str,
) -> EvidenceVerificationStatus:
    """Verify a Merkle audit proof against an expected root hash."""
    if leaf_hash.lower() != proof.leaf_hash.lower():
        return EvidenceVerificationStatus.FAILED

    is_valid = _verify_merkle_proof_computation(proof, expected_root)
    return EvidenceVerificationStatus.VERIFIED if is_valid else EvidenceVerificationStatus.FAILED


class CommitmentAnchorProvider(ABC):
    """Abstract interface for optional external commitment anchoring."""

    @abstractmethod
    def anchor_commitment(self, root_hash: str, metadata: dict[str, Any]) -> dict[str, Any]:
        """Anchor a Merkle root hash into an external ledger/log."""
        raise NotImplementedError

    @abstractmethod
    def verify_anchor(self, root_hash: str, anchor_record: dict[str, Any]) -> bool:
        """Verify that an anchor record matches the root hash."""
        raise NotImplementedError


class OfflineCommitmentAnchorProvider(CommitmentAnchorProvider):
    """Default offline in-memory anchor provider operating with zero network dependencies."""

    def __init__(self) -> None:
        self._anchors: dict[str, dict[str, Any]] = {}

    def anchor_commitment(self, root_hash: str, metadata: dict[str, Any]) -> dict[str, Any]:
        record = {
            "anchor_id": f"anchor_{root_hash[:16]}",
            "root_hash": root_hash,
            "anchored_at": "2026-09-30T00:00:00Z",
            "metadata": metadata,
            "provider": "offline_in_memory",
        }
        self._anchors[root_hash] = record
        return record

    def verify_anchor(self, root_hash: str, anchor_record: dict[str, Any]) -> bool:
        stored = self._anchors.get(root_hash)
        if not stored:
            return False
        return stored.get("root_hash") == root_hash == anchor_record.get("root_hash")
