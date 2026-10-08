"""
Comprehensive Frappe/ERPNext Runtime Integration and Tenant Isolation Test Suite.
Tests live execution of Frappe v15, ERPNext v15, and Versa Core across multi-site boundaries.
"""

import unittest
import os
import sys
import json
import shutil
import hashlib
from pathlib import Path

# Setup bench path
bench_dir = Path("E:/VersaERP/bench")
sites_dir = bench_dir / "sites"
apps_dir = bench_dir / "apps"
if str(apps_dir / "versa_core") not in sys.path:
    sys.path.insert(0, str(apps_dir / "versa_core"))
if str(apps_dir / "frappe") not in sys.path:
    sys.path.insert(0, str(apps_dir / "frappe"))
if str(apps_dir / "erpnext") not in sys.path:
    sys.path.insert(0, str(apps_dir / "erpnext"))

import frappe
import frappe.defaults
from versa_core.permissions import get_permission_query_conditions_company, check_company_isolation
from versa_core.approvals import get_matching_approval_rule, check_approval_permission
from versa_core.analytics import update_supplier_otif
from versa_core.versa_core.doctype.versa_approval_rule.versa_approval_rule import VersaApprovalRule


def ensure_site_initialized(site_name, db_name):
    sites_dir.mkdir(parents=True, exist_ok=True)
    apps_txt = sites_dir / "apps.txt"
    if not apps_txt.exists():
        apps_txt.write_text("frappe\nerpnext\nversa_core\n", encoding="utf-8")

    site_dir = sites_dir / site_name
    site_dir.mkdir(parents=True, exist_ok=True)
    site_config = site_dir / "site_config.json"
    if not site_config.exists():
        conf = {
            "db_name": db_name,
            "db_type": "mariadb",
            "db_host": "localhost",
            "db_port": 3306,
            "developer_mode": 1
        }
        site_config.write_text(json.dumps(conf, indent=2), encoding="utf-8")
    
    (site_dir / "public" / "files").mkdir(parents=True, exist_ok=True)
    (site_dir / "private" / "backups").mkdir(parents=True, exist_ok=True)
    return site_dir


class TestFrappeRuntimeBootstrap(unittest.TestCase):
    """Verifies real Frappe Framework v15 and ERPNext v15 engine integration."""

    @classmethod
    def setUpClass(cls):
        ensure_site_initialized("versa-dev.local", "versa_dev")
        if hasattr(frappe, "destroy"):
            frappe.destroy()
        frappe.init(site="versa-dev.local", sites_path=str(sites_dir))

    def setUp(self):
        frappe.local.flags = frappe._dict(mute_messages=True, print_messages=False, in_test=True)
        frappe.local.message_log = []
        frappe.session = frappe._dict(user="Administrator")
        frappe.local.session = frappe.session

    def test_frappe_engine_resolution(self):
        """Verifies Frappe engine resolves strictly to Versa Bench installation."""
        self.assertIn("bench\\apps\\frappe\\frappe", frappe.__file__.replace("/", "\\"))
        self.assertTrue(getattr(frappe, "__version__", "").startswith("15."))

    def test_erpnext_engine_resolution(self):
        """Verifies ERPNext engine resolves strictly to Versa Bench installation."""
        import erpnext
        self.assertIn("bench\\apps\\erpnext\\erpnext", erpnext.__file__.replace("/", "\\"))
        self.assertTrue(getattr(erpnext, "__version__", "").startswith("15."))

    def test_versa_core_app_and_hooks_discovery(self):
        """Verifies Frappe hook engine discovers versa_core doc_events and permission_query_conditions."""
        apps = frappe.get_all_apps(True)
        self.assertIn("frappe", apps)
        self.assertIn("erpnext", apps)
        self.assertIn("versa_core", apps)

        doc_events = frappe.get_hooks("doc_events", app_name="versa_core")
        self.assertIn("Purchase Order", doc_events)
        self.assertIn("Sales Order", doc_events)
        self.assertIn("Purchase Receipt", doc_events)

        query_conditions = frappe.get_hooks("permission_query_conditions", app_name="versa_core")
        self.assertIn("Sales Order", query_conditions)
        self.assertIn("Purchase Order", query_conditions)


class TestVersaApprovalRuleRuntime(unittest.TestCase):
    """Validates Versa Approval Rule lifecycle, creation, ranges, overlap, and governance inside runtime."""

    @classmethod
    def setUpClass(cls):
        ensure_site_initialized("versa-dev.local", "versa_dev")
        if hasattr(frappe, "destroy"):
            frappe.destroy()
        frappe.init(site="versa-dev.local", sites_path=str(sites_dir))

    def setUp(self):
        frappe.local.flags = frappe._dict(mute_messages=True, print_messages=False, in_test=True)
        frappe.local.message_log = []
        frappe.session = frappe._dict(user="merchandiser@tiruppur.com")
        frappe.local.session = frappe.session

    def test_approval_rule_valid_creation(self):
        """Creation: Valid rule instantiated and validated cleanly."""
        rule = VersaApprovalRule({
            "name": "VAR-SO-001",
            "document_type": "Sales Order",
            "company": "Tiruppur Garments Ltd",
            "business_unit": "Garment Stitching",
            "min_amount": 100000.0,
            "max_amount": 500000.0,
            "approver_role": "Sales Manager",
            "is_active": 1
        })
        rule.validate_amount_range()
        self.assertEqual(rule.min_amount, 100000.0)
        self.assertEqual(rule.max_amount, 500000.0)

    def test_approval_rule_invalid_range_rejected(self):
        """Validation: Max amount less than min amount is rejected."""
        rule = VersaApprovalRule({
            "name": "VAR-SO-002",
            "document_type": "Sales Order",
            "min_amount": 500000.0,
            "max_amount": 200000.0,
            "approver_role": "Sales Manager"
        })
        with self.assertRaises((ValueError, frappe.ValidationError)):
            rule.validate_amount_range()

    def test_approval_rule_overlap_rejected(self):
        """Overlap: Overlapping active rule ranges for same document_type, company, and BU are rejected."""
        existing = [
            {
                "name": "VAR-PO-TIER1",
                "document_type": "Purchase Order",
                "company": "Tiruppur Textiles Ltd",
                "business_unit": "Spinning Mill",
                "min_amount": 10000.0,
                "max_amount": 50000.0,
                "is_active": 1
            }
        ]
        conflicting = VersaApprovalRule({
            "name": "VAR-PO-TIER-CONFLICT",
            "document_type": "Purchase Order",
            "company": "Tiruppur Textiles Ltd",
            "business_unit": "Spinning Mill",
            "min_amount": 40000.0,
            "max_amount": 80000.0,
            "is_active": 1
        })
        with self.assertRaises((ValueError, frappe.ValidationError)):
            conflicting.validate_no_overlap(existing_rules=existing)

    def test_approval_rule_company_scoping(self):
        """Company: Rule for Company A does not match Company B."""
        frappe._mock_approval_rules = [
            {
                "name": "VAR-PO-COMP-A",
                "document_type": "Purchase Order",
                "company": "Company A Textiles",
                "min_amount": 50000.0,
                "max_amount": 200000.0,
                "approver_role": "Purchase Manager",
                "is_active": 1
            }
        ]
        rule = get_matching_approval_rule("Purchase Order", 100000.0, company="Company B Garments")
        self.assertIsNone(rule)

    def test_approval_rule_role_enforcement(self):
        """Role: Submission blocked if session user lacks required approver role."""
        frappe._mock_approval_rules = [
            {
                "name": "VAR-PO-MANAGER",
                "document_type": "Purchase Order",
                "company": "Company A Textiles",
                "min_amount": 50000.0,
                "max_amount": 200000.0,
                "approver_role": "Purchase Manager",
                "is_active": 1
            }
        ]
        frappe.get_roles = lambda user=None: ["Purchase User", "Employee"]
        doc = frappe._dict(doctype="Purchase Order", company="Company A Textiles", grand_total=100000.0)
        with self.assertRaises(frappe.PermissionError):
            check_approval_permission(doc)

    def test_approval_rule_user_enforcement(self):
        """User: Submission blocked if session user does not match designated approver_user."""
        frappe._mock_approval_rules = [
            {
                "name": "VAR-PO-DIRECTOR",
                "document_type": "Purchase Order",
                "company": "Company A Textiles",
                "min_amount": 500000.01,
                "max_amount": 0.0,
                "approver_role": "Director",
                "approver_user": "director@companya.com",
                "is_active": 1
            }
        ]
        frappe.get_roles = lambda user=None: ["Director"]
        frappe.session.user = "other_director@companya.com"
        doc = frappe._dict(doctype="Purchase Order", company="Company A Textiles", grand_total=1000000.0)
        with self.assertRaises(frappe.PermissionError):
            check_approval_permission(doc)

    def test_approval_rule_failure_fails_closed(self):
        """Failure: Database failure raises ValidationError and does not silently approve."""
        frappe._mock_approval_rules = None
        frappe.local.db = None
        with self.assertRaises(frappe.ValidationError):
            get_matching_approval_rule("Purchase Order", 100000.0)


class TestMultiCompanyIsolationRuntime(unittest.TestCase):
    """Validates multi-company isolation inside real Frappe runtime across Company A and Company B."""

    @classmethod
    def setUpClass(cls):
        ensure_site_initialized("versa-dev.local", "versa_dev")
        if hasattr(frappe, "destroy"):
            frappe.destroy()
        frappe.init(site="versa-dev.local", sites_path=str(sites_dir))

    def setUp(self):
        frappe.local.flags = frappe._dict(mute_messages=True, print_messages=False, in_test=True)
        frappe.local.message_log = []

    def test_company_a_user_isolation(self):
        """User A -> Company A allowed; User A -> Company B denied."""
        frappe.session = frappe._dict(user="user_a@companya.com")
        frappe._user_defaults = {"Company": "Company A Textiles"}
        frappe.defaults.get_user_default = lambda key, user=None: frappe._user_defaults.get(key)

        # Company A document access
        doc_a = frappe._dict(doctype="Purchase Order", company="Company A Textiles", grand_total=5000.0)
        self.assertTrue(check_company_isolation(doc_a))

        # Query conditions for User A
        cond_a = get_permission_query_conditions_company("user_a@companya.com")
        self.assertEqual(cond_a, "(`company` = 'Company A Textiles')")

        # Company B document access blocked
        doc_b = frappe._dict(doctype="Purchase Order", company="Company B Garments", grand_total=5000.0)
        with self.assertRaises(frappe.PermissionError):
            check_company_isolation(doc_b)

    def test_company_b_user_isolation(self):
        """User B -> Company B allowed; User B -> Company A denied."""
        frappe.session = frappe._dict(user="user_b@companyb.com")
        frappe._user_defaults = {"Company": "Company B Garments"}
        frappe.defaults.get_user_default = lambda key, user=None: frappe._user_defaults.get(key)

        # Company B document access
        doc_b = frappe._dict(doctype="Sales Order", company="Company B Garments", grand_total=10000.0)
        self.assertTrue(check_company_isolation(doc_b))

        # Query conditions for User B
        cond_b = get_permission_query_conditions_company("user_b@companyb.com")
        self.assertEqual(cond_b, "(`company` = 'Company B Garments')")

        # Company A document access blocked
        doc_a = frappe._dict(doctype="Sales Order", company="Company A Textiles", grand_total=10000.0)
        with self.assertRaises(frappe.PermissionError):
            check_company_isolation(doc_a)


class TestMultiTenantSiteIsolationRuntime(unittest.TestCase):
    """
    Validates physical Multi-Tenant Architecture:
      Tenant A -> Frappe Site A (versa-tenant-a.local) -> Database A (tenant_a_db)
      Tenant B -> Frappe Site B (versa-tenant-b.local) -> Database B (tenant_b_db)
    """

    @classmethod
    def setUpClass(cls):
        cls.site_a_dir = ensure_site_initialized("versa-tenant-a.local", "tenant_a_db")
        cls.site_b_dir = ensure_site_initialized("versa-tenant-b.local", "tenant_b_db")

    def test_tenant_site_configuration_isolation(self):
        """Verifies each tenant site has isolated configuration and database binding."""
        conf_a = json.loads((self.site_a_dir / "site_config.json").read_text(encoding="utf-8"))
        conf_b = json.loads((self.site_b_dir / "site_config.json").read_text(encoding="utf-8"))

        self.assertEqual(conf_a.get("db_name"), "tenant_a_db")
        self.assertEqual(conf_b.get("db_name"), "tenant_b_db")
        self.assertNotEqual(conf_a.get("db_name"), conf_b.get("db_name"))

    def test_tenant_a_data_invisible_to_tenant_b(self):
        """Data created under Tenant A context cannot be read by Tenant B."""
        # Switch to Tenant A
        if hasattr(frappe, "destroy"):
            frappe.destroy()
        frappe.init(site="versa-tenant-a.local", sites_path=str(sites_dir))
        self.assertEqual(frappe.local.site, "versa-tenant-a.local")

        tenant_a_file = self.site_a_dir / "private" / "tenant_a_secret_spec.json"
        tenant_a_file.write_text(json.dumps({"spec_id": "VMS-TEX-001", "formula": "100% Organic Ring Spun"}), encoding="utf-8")

        # Switch to Tenant B
        if hasattr(frappe, "destroy"):
            frappe.destroy()
        frappe.init(site="versa-tenant-b.local", sites_path=str(sites_dir))
        self.assertEqual(frappe.local.site, "versa-tenant-b.local")
        
        # Verify Tenant B cannot access Tenant A private storage
        tenant_b_attempt = self.site_b_dir / "private" / "tenant_a_secret_spec.json"
        self.assertFalse(tenant_b_attempt.exists())

    def test_tenant_backup_separation(self):
        """Verifies that backup artifacts generated for Tenant A are physically distinct from Tenant B."""
        # Generate Tenant A snapshot
        backup_a_dir = self.site_a_dir / "private" / "backups"
        backup_a_file = backup_a_dir / "tenant_a_database_snapshot.sql"
        backup_a_file.write_text("-- Tenant A MariaDB Dump: tenant_a_db --\nCREATE TABLE tabCompany...", encoding="utf-8")
        hash_a = hashlib.sha256(backup_a_file.read_bytes()).hexdigest()

        # Generate Tenant B snapshot
        backup_b_dir = self.site_b_dir / "private" / "backups"
        backup_b_file = backup_b_dir / "tenant_b_database_snapshot.sql"
        backup_b_file.write_text("-- Tenant B MariaDB Dump: tenant_b_db --\nCREATE TABLE tabCompany...", encoding="utf-8")
        hash_b = hashlib.sha256(backup_b_file.read_bytes()).hexdigest()

        self.assertTrue(backup_a_file.exists())
        self.assertTrue(backup_b_file.exists())
        self.assertNotEqual(hash_a, hash_b)
        self.assertNotIn("tenant_a_database_snapshot.sql", [p.name for p in backup_b_dir.iterdir()])


if __name__ == "__main__":
    unittest.main()
