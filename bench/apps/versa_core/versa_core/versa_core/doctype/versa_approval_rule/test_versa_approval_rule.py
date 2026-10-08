"""
Unit tests for Versa Approval Rule controller (DocType ENT-039).
"""

import unittest
import sys
from pathlib import Path

# Add bench/apps to path
apps_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(apps_dir) not in sys.path:
    sys.path.insert(0, str(apps_dir))

from versa_core.versa_core.doctype.versa_approval_rule.versa_approval_rule import VersaApprovalRule


class TestVersaApprovalRule(unittest.TestCase):
    """DocType Controller Tests for Versa Approval Rule"""

    def test_valid_amount_range(self):
        """Positive: Correct min and max amounts validate cleanly."""
        rule = VersaApprovalRule({
            "name": "RULE-01",
            "document_type": "Purchase Order",
            "min_amount": 10000.0,
            "max_amount": 50000.0,
            "approver_role": "Purchase Manager",
            "is_active": 1
        })
        rule.validate_amount_range()
        self.assertEqual(rule.min_amount, 10000.0)
        self.assertEqual(rule.max_amount, 50000.0)

    def test_invalid_amount_range_raises(self):
        """Negative: max_amount < min_amount raises ValueError."""
        rule = VersaApprovalRule({
            "name": "RULE-02",
            "document_type": "Purchase Order",
            "min_amount": 50000.0,
            "max_amount": 10000.0,
            "approver_role": "Purchase Manager"
        })
        with self.assertRaises(ValueError):
            rule.validate_amount_range()

    def test_negative_min_amount_raises(self):
        """Negative: Negative min_amount raises ValueError."""
        rule = VersaApprovalRule({
            "name": "RULE-03",
            "document_type": "Purchase Order",
            "min_amount": -500.0,
            "approver_role": "Purchase Manager"
        })
        with self.assertRaises(ValueError):
            rule.validate_amount_range()

    def test_open_ended_max_amount(self):
        """Positive: Zero or None max_amount signifies open-ended threshold."""
        rule = VersaApprovalRule({
            "name": "RULE-04",
            "document_type": "Sales Order",
            "min_amount": 500000.0,
            "max_amount": 0.0,
            "approver_role": "Managing Director"
        })
        rule.validate_amount_range()
        self.assertEqual(rule.min_amount, 500000.0)

    def test_overlap_validation_detects_conflict(self):
        """Negative: Conflicting amount range raises ValueError / conflict error."""
        existing = [
            {
                "name": "RULE-PO-LOW",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "business_unit": "Spinning",
                "min_amount": 10000.0,
                "max_amount": 50000.0,
                "is_active": 1
            }
        ]
        new_conflicting_rule = VersaApprovalRule({
            "name": "RULE-PO-NEW",
            "document_type": "Purchase Order",
            "company": "Tiruppur Textiles Ltd",
            "business_unit": "Spinning",
            "min_amount": 30000.0,
            "max_amount": 80000.0,
            "is_active": 1
        })
        with self.assertRaises(ValueError):
            new_conflicting_rule.validate_no_overlap(existing_rules=existing)

    def test_overlap_validation_non_overlapping_passes(self):
        """Positive: Adjacent non-overlapping amount ranges pass validation."""
        existing = [
            {
                "name": "RULE-PO-BAND1",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "business_unit": "Spinning",
                "min_amount": 10000.0,
                "max_amount": 50000.0,
                "is_active": 1
            }
        ]
        new_valid_rule = VersaApprovalRule({
            "name": "RULE-PO-BAND2",
            "document_type": "Purchase Order",
            "company": "Tiruppur Textiles Ltd",
            "business_unit": "Spinning",
            "min_amount": 50000.01,
            "max_amount": 100000.0,
            "is_active": 1
        })
        # Should not raise
        new_valid_rule.validate_no_overlap(existing_rules=existing)

    def test_overlap_validation_inactive_rule_ignored(self):
        """Positive: Overlapping with an inactive rule does not raise conflict."""
        existing = [
            {
                "name": "RULE-PO-INACTIVE",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "business_unit": "Spinning",
                "min_amount": 10000.0,
                "max_amount": 50000.0,
                "is_active": 0  # Inactive
            }
        ]
        new_rule = VersaApprovalRule({
            "name": "RULE-PO-NEW",
            "document_type": "Purchase Order",
            "company": "Tiruppur Textiles Ltd",
            "business_unit": "Spinning",
            "min_amount": 20000.0,
            "max_amount": 40000.0,
            "is_active": 1
        })
        # Should not raise
        new_rule.validate_no_overlap(existing_rules=existing)


if __name__ == "__main__":
    unittest.main()
