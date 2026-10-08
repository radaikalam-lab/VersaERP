import re
from typing import Any


class SemanticMappingRules:
    """Deterministic, conservative rules for mapping physical database structures to semantic graph concepts."""

    @staticmethod
    def to_pascal_case(name: str) -> str:
        """Convert snake_case, kebab-case, or spaced strings to PascalCase."""
        if not name or not name.strip():
            return "UnknownEntity"
        # Split on non-alphanumeric boundaries while preserving Unicode letters
        tokens = re.split(r"[^a-zA-Z0-9\u0080-\uffff]+", name.strip())
        pascal = "".join(token.capitalize() for token in tokens if token)
        return pascal or "UnknownEntity"

    @staticmethod
    def to_attribute_name(column_name: str) -> str:
        """Normalize physical column name to canonical semantic attribute name."""
        cleaned = column_name.strip().lower()
        # Replace non-alphanumeric characters with underscores
        normalized = re.sub(r"[^a-z0-9\u0080-\uffff]+", "_", cleaned)
        return normalized.strip("_") or "attribute"

    @classmethod
    def infer_relationship_type(
        cls,
        source_table: str,
        target_table: str,
        fk_columns: tuple[str, ...] = (),
        target_columns: tuple[str, ...] = (),
        fk_properties: dict[str, Any] | None = None,
    ) -> str:
        """Derive a conservative semantic relationship type between two entities based on FK structure."""
        src = source_table.lower()
        tgt = target_table.lower()

        # Check for typical composition / line item patterns
        if src.startswith(tgt) and (src.endswith("_item") or src.endswith("_line") or src.endswith("_detail")):
            return "CONTAINS"
        if tgt.startswith(src) and (tgt.endswith("_item") or tgt.endswith("_line") or tgt.endswith("_detail")):
            return "PART_OF"

        # Check for common semantic verbs based on conservative matching
        if "customer" in tgt and "order" in src:
            return "PLACED_BY"
        if "product" in tgt and ("item" in src or "order" in src):
            return "REFERENCES_PRODUCT"

        # Default conservative association
        return "ASSOCIATED_WITH"
