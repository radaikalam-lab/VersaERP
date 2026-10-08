"""
Unit test suite for versa_core platform modules (Permissions, Approvals, Analytics).
Covers both positive and fail-closed negative security paths.
"""

import unittest
import sys
from pathlib import Path

# Add bench/apps to path
apps_dir = Path(__file__).resolve().parent.parent.parent
if str(apps_dir) not in sys.path:
    sys.path.insert(0, str(apps_dir))

import frappe
import frappe.defaults
from versa_core.permissions import get_permission_query_conditions_company, check_company_isolation
from versa_core.approvals import get_matching_approval_rule, check_approval_permission
from versa_core.analytics import update_supplier_otif


def setup_frappe_env(user="test_merchandiser@example.com", company="Tiruppur Textiles Ltd"):
    frappe.local.flags = frappe._dict(mute_messages=True, print_messages=False, in_test=True)
    frappe.local.message_log = []
    frappe.session = frappe._dict(user=user)
    frappe.local.session = frappe.session
    frappe.local.db = None
    frappe._user_defaults = {"Company": company} if company else {}
    frappe.defaults.get_user_default = lambda key, user=None: frappe._user_defaults.get(key)


class TestVersaCoreMultiCompany(unittest.TestCase):
    """Multi-Company Tenant Isolation Security Tests (CANONICAL_INVARIANT: multi_company_isolation)"""

    def setUp(self):
        setup_frappe_env(user="test_merchandiser@example.com", company="Tiruppur Textiles Ltd")

    def tearDown(self):
        frappe._mock_approval_rules = None

    def test_permission_query_conditions_standard_user(self):
        """Positive: Standard user receives SQL restriction matching authorized company."""
        cond = get_permission_query_conditions_company("test_merchandiser@example.com")
        self.assertEqual(cond, "(`company` = 'Tiruppur Textiles Ltd')")

    def test_permission_query_conditions_administrator(self):
        """Positive: Administrator receives unrestricted empty condition."""
        cond = get_permission_query_conditions_company("Administrator")
        self.assertEqual(cond, "")

    def test_permission_query_conditions_no_company_fails_closed(self):
        """Negative / Fail-Closed: User with no company gets '1 = 0' restriction (NOT 'Test Company')."""
        frappe._user_defaults = {}
        cond = get_permission_query_conditions_company("unassigned_user@example.com")
        self.assertEqual(cond, "1 = 0")
        self.assertNotIn("Test Company", cond)

    def test_check_company_isolation_same_company_succeeds(self):
        """Positive: User accessing own company document succeeds."""
        doc = frappe._dict(doctype="Sales Order", company="Tiruppur Textiles Ltd")
        self.assertTrue(check_company_isolation(doc))

    def test_check_company_isolation_admin_bypasses(self):
        """Positive: Administrator is exempt from company restriction."""
        frappe.session.user = "Administrator"
        doc = frappe._dict(doctype="Sales Order", company="Other Mill Ltd")
        self.assertTrue(check_company_isolation(doc))

    def test_check_company_isolation_cross_company_fails(self):
        """Negative / Security: Accessing cross-company document raises PermissionError."""
        doc = frappe._dict(doctype="Sales Order", company="Coimbatore Spinning Mills")
        with self.assertRaises(frappe.PermissionError):
            check_company_isolation(doc)

    def test_check_company_isolation_missing_doc_company_fails(self):
        """Negative / Security: Document with missing company raises ValidationError."""
        doc = frappe._dict(doctype="Purchase Order", company="")
        with self.assertRaises(frappe.ValidationError):
            check_company_isolation(doc)

    def test_check_company_isolation_missing_user_company_fails(self):
        """Negative / Security: User with no active company context raises PermissionError."""
        frappe._user_defaults = {}
        doc = frappe._dict(doctype="Sales Order", company="Tiruppur Textiles Ltd")
        with self.assertRaises(frappe.PermissionError):
            check_company_isolation(doc)

    def test_check_company_isolation_none_doc_fails(self):
        """Negative / Security: None doc parameter raises ValidationError."""
        with self.assertRaises(frappe.ValidationError):
            check_company_isolation(None)


class TestVersaCoreApprovalEngine(unittest.TestCase):
    """Dynamic Multi-Level Approval Engine Tests (ENT-039 / P2P & O2C Governance)"""

    def setUp(self):
        setup_frappe_env(user="purchase_user@example.com", company="Tiruppur Textiles Ltd")
        frappe.get_roles = lambda user=None: ["Purchase User", "Employee"]
        # Register mock approval rules in test environment
        frappe._mock_approval_rules = [
            {
                "name": "VAR-PO-001",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "business_unit": "Spinning Mill",
                "min_amount": 50000.0,
                "max_amount": 500000.0,
                "approver_role": "Purchase Manager",
                "approver_user": None,
                "is_active": 1
            },
            {
                "name": "VAR-PO-002",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "business_unit": "Spinning Mill",
                "min_amount": 500000.01,
                "max_amount": 0.0,  # Open-ended
                "approver_role": "Managing Director",
                "approver_user": "md@versaerp.com",
                "is_active": 1
            },
            {
                "name": "VAR-PO-INACTIVE",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "min_amount": 10000.0,
                "max_amount": 49999.0,
                "approver_role": "Purchase Supervisor",
                "is_active": 0
            }
        ]

    def tearDown(self):
        frappe._mock_approval_rules = None

    def test_approval_rule_matching_valid_band(self):
        """Positive: Amount within band matches correct rule."""
        rule = get_matching_approval_rule("Purchase Order", 150000.0, company="Tiruppur Textiles Ltd", cost_center="Spinning Mill")
        self.assertIsNotNone(rule)
        self.assertEqual(rule.get("name"), "VAR-PO-001")
        self.assertEqual(rule.get("approver_role"), "Purchase Manager")

    def test_approval_rule_matching_open_ended_max(self):
        """Positive: Amount exceeding high threshold matches open-ended rule."""
        rule = get_matching_approval_rule("Purchase Order", 2500000.0, company="Tiruppur Textiles Ltd", cost_center="Spinning Mill")
        self.assertIsNotNone(rule)
        self.assertEqual(rule.get("name"), "VAR-PO-002")
        self.assertEqual(rule.get("approver_role"), "Managing Director")

    def test_approval_rule_matching_below_min_amount(self):
        """Positive: Amount below minimum threshold returns None (auto-approved / no rule needed)."""
        rule = get_matching_approval_rule("Purchase Order", 25000.0, company="Tiruppur Textiles Ltd", cost_center="Spinning Mill")
        self.assertIsNone(rule)

    def test_approval_rule_cross_company_filtered_out(self):
        """Negative: Rule configured for Company A does not match Company B."""
        rule = get_matching_approval_rule("Purchase Order", 150000.0, company="Other Company Ltd", cost_center="Spinning Mill")
        self.assertIsNone(rule)

    def test_approval_rule_inactive_ignored(self):
        """Negative: Inactive rule is ignored."""
        rule = get_matching_approval_rule("Purchase Order", 30000.0, company="Tiruppur Textiles Ltd", cost_center="Spinning Mill")
        self.assertIsNone(rule)

    def test_approval_rule_db_unavailable_fails_closed(self):
        """Negative / Fail-Closed: When DB/mock is completely unavailable, throws ValidationError."""
        frappe._mock_approval_rules = None
        frappe.local.db = None
        with self.assertRaises(frappe.ValidationError):
            get_matching_approval_rule("Purchase Order", 150000.0)

    def test_check_approval_permission_valid_role_succeeds(self):
        """Positive: User having required role passes approval check."""
        frappe.get_roles = lambda user=None: ["Purchase Manager", "Employee"]
        doc = frappe._dict(
            doctype="Purchase Order",
            company="Tiruppur Textiles Ltd",
            cost_center="Spinning Mill",
            grand_total=150000.0
        )
        self.assertTrue(check_approval_permission(doc))
        self.assertEqual(doc.get("versa_approval_rule"), "VAR-PO-001")

    def test_check_approval_permission_insufficient_role_fails(self):
        """Negative / Security: User lacking required role raises PermissionError."""
        frappe.get_roles = lambda user=None: ["Purchase User"]  # Lacks Purchase Manager
        doc = frappe._dict(
            doctype="Purchase Order",
            company="Tiruppur Textiles Ltd",
            cost_center="Spinning Mill",
            grand_total=150000.0
        )
        with self.assertRaises(frappe.PermissionError):
            check_approval_permission(doc)

    def test_check_approval_permission_specific_user_mismatch_fails(self):
        """Negative / Security: User matching role but not designated approver user raises PermissionError."""
        frappe.get_roles = lambda user=None: ["Managing Director"]
        frappe.session.user = "different_user@versaerp.com"  # Rule requires md@versaerp.com
        doc = frappe._dict(
            doctype="Purchase Order",
            company="Tiruppur Textiles Ltd",
            cost_center="Spinning Mill",
            grand_total=1000000.0
        )
        with self.assertRaises(frappe.PermissionError):
            check_approval_permission(doc)

    def test_check_approval_permission_admin_bypasses(self):
        """Positive: Administrator is exempt from approval matrix role requirements."""
        frappe.session.user = "Administrator"
        frappe.get_roles = lambda user=None: ["System Manager"]
        doc = frappe._dict(
            doctype="Purchase Order",
            company="Tiruppur Textiles Ltd",
            cost_center="Spinning Mill",
            grand_total=1000000.0
        )
        self.assertTrue(check_approval_permission(doc))

    def test_check_approval_permission_none_doc_fails(self):
        """Negative / Security: None doc raises ValidationError."""
        with self.assertRaises(frappe.ValidationError):
            check_approval_permission(None)


class TestVersaCoreAnalytics(unittest.TestCase):
    """Supplier Performance & OTIF Analytics Tests (DERIVED_METRIC: supplier_otif_scoring)"""

    def setUp(self):
        setup_frappe_env()

    def test_supplier_otif_deferred_does_not_return_fake_score(self):
        """Integrity: update_supplier_otif returns None (deferred per DEC-007) and does NOT return fabricated 100%."""
        doc = frappe._dict(doctype="Purchase Receipt", supplier="SUP-001")
        result = update_supplier_otif(doc)
        self.assertIsNone(result)
        self.assertNotEqual(result, 100.0)
        self.assertNotEqual(result, 98.5)

    def test_supplier_otif_missing_supplier_safe_handling(self):
        """Integrity: update_supplier_otif handles missing supplier safely without exception."""
        doc = frappe._dict(doctype="Purchase Receipt", supplier=None)
        result = update_supplier_otif(doc)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
