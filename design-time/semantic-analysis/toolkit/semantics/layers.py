"""Canonical Three-Layer Semantic Architecture (GM-SEM-001).

Establishes the normative Three-Layer Semantic stratification:
- Layer 1: Technology & Language Semantics (e.g. COBOL syntax, CICS verbs, binary storage formats)
- Layer 2: Enterprise System & Implementation Mechanics (e.g. business logic flow, system state transitions, error handling)
- Layer 3: Domain & Business Invariants (e.g. general ledger double-entry, separation of duties, regulatory constraints)

Core Epistemic Invariants:
- L1 != L2 != L3
- L2 Implementation Semantics != L3 Domain Semantics
- Domain Knowledge != Implementation Knowledge
- Technical mechanics cannot be promoted to domain truth without explicit corroborated evidence.
"""

from __future__ import annotations

from enum import Enum


class SemanticLayer(str, Enum):
    """Canonical Three-Layer Semantic Architecture stratification (GM-SEM-001)."""

    LAYER_1_TECHNOLOGY = "LAYER_1_TECHNOLOGY"
    LAYER_2_ENTERPRISE_SYSTEM = "LAYER_2_ENTERPRISE_SYSTEM"
    LAYER_3_DOMAIN_BUSINESS = "LAYER_3_DOMAIN_BUSINESS"

    # Conventional Shorthand Aliases for Domain Knowledge Modules (Same Enum Members)
    L1_TECHNOLOGY = "LAYER_1_TECHNOLOGY"
    L2_ENTERPRISE_IMPLEMENTATION = "LAYER_2_ENTERPRISE_SYSTEM"
    L3_DOMAIN_BUSINESS = "LAYER_3_DOMAIN_BUSINESS"

    @classmethod
    def from_str(cls, value: str) -> SemanticLayer:
        """Parse string flexibly into canonical semantic layer."""
        normalized = value.strip().upper()
        if normalized in ("LAYER_1_TECHNOLOGY", "L1_TECHNOLOGY", "L1", "1", "TECHNOLOGY"):
            return cls.LAYER_1_TECHNOLOGY
        if normalized in (
            "LAYER_2_ENTERPRISE_SYSTEM",
            "L2_ENTERPRISE_IMPLEMENTATION",
            "L2",
            "2",
            "ENTERPRISE_SYSTEM",
            "ENTERPRISE_IMPLEMENTATION",
        ):
            return cls.LAYER_2_ENTERPRISE_SYSTEM
        if normalized in ("LAYER_3_DOMAIN_BUSINESS", "L3_DOMAIN_BUSINESS", "L3", "3", "DOMAIN_BUSINESS", "BUSINESS"):
            return cls.LAYER_3_DOMAIN_BUSINESS
        raise ValueError(f"Unknown semantic layer value: '{value}'")

    @property
    def is_technology(self) -> bool:
        """Whether this layer represents Layer 1 Technology/Format mechanics."""
        return self in (SemanticLayer.LAYER_1_TECHNOLOGY, SemanticLayer.L1_TECHNOLOGY)

    @property
    def is_implementation(self) -> bool:
        """Whether this layer represents Layer 2 Enterprise Implementation mechanics."""
        return self in (SemanticLayer.LAYER_2_ENTERPRISE_SYSTEM, SemanticLayer.L2_ENTERPRISE_IMPLEMENTATION)

    @property
    def is_domain(self) -> bool:
        """Whether this layer represents Layer 3 Universal Domain/Business invariants."""
        return self in (SemanticLayer.LAYER_3_DOMAIN_BUSINESS, SemanticLayer.L3_DOMAIN_BUSINESS)
