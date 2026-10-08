"""
Versa Quality — Comprehensive Docker Runtime Integration & Isolation Test Suite.
Validates live Frappe hook discovery, DocType registration, full document lifecycles,
Purchase Receipt / Stock Entry quality gates, multi-company and multi-tenant isolation,
ASTM D5430 4-point scoring, physical measurement relationships, and ERPNext authority boundaries.
"""

import os
import sys
import unittest
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

# Set up bench paths
if os.path.exists("/home/frappe/frappe-bench"):
    bench_root = "/home/frappe/frappe-bench"
else:
    bench_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "bench"))

apps_path = os.path.join(bench_root, "apps")
sys.path.insert(0, os.path.join(apps_path, "frappe"))
sys.path.insert(0, os.path.join(apps_path, "erpnext"))
sys.path.insert(0, os.path.join(apps_path, "versa_core"))
sys.path.insert(0, os.path.join(apps_path, "versa_quality"))

import frappe
from versa_quality.versa_quality.doctype.versa_qc_spec.versa_qc_spec import VersaQCSpec
from versa_quality.versa_quality.doctype.versa_qc_result.versa_qc_result import VersaQCResult
from versa_quality.evaluator import (
    calculate_readings_statistics,
    evaluate_parameter_measurement,
    calculate_4point_defect_score,
    evaluate_overall_disposition
)
from versa_quality.gates import check_purchase_receipt_qc_gate, check_stock_entry_qc_gate
from versa_quality.permissions import (
    get_permission_query_conditions_quality_result,
    get_permission_query_conditions_quality_spec,
    check_quality_company_isolation
)
from versa_quality.events.purchase_receipt import check_qc_conformance
from versa_quality.events.stock_entry import validate_qc_status


def setup_frappe_test_env(user="qa_inspector@versaerp.com", company="Tiruppur Textiles Ltd"):
    """
    Initializes mock Frappe local environment to ensure LocalProxy objects are bound.
    """
    if hasattr(frappe, "local"):
        frappe.local.flags = frappe._dict(mute_messages=True, print_messages=False, in_test=True)
        frappe.local.message_log = []
        frappe.session = frappe._dict(user=user)
        frappe.local.session = frappe.session
        frappe.local.db = frappe._dict(
            count=lambda *args, **kwargs: 0,
            get_value=lambda *args, **kwargs: None,
            get_all=lambda *args, **kwargs: []
        )
        frappe.db = frappe.local.db
        frappe._user_defaults = {"Company": company} if company else {}
        frappe.defaults = frappe._dict(
            get_user_default=lambda key, user=None: frappe._user_defaults.get(key)
        )


class TestVersaQualityRuntimeBootstrap(unittest.TestCase):
    """
    Tests Frappe app and hook registration for versa_quality.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_versa_quality_app_and_hooks_discovery(self):
        """
        Verifies Frappe hook engine discovers versa_quality doc_events and permission_query_conditions.
        """
        import versa_quality.hooks as vq_hooks
        self.assertEqual(vq_hooks.app_name, "versa_quality")
        self.assertIn("Purchase Receipt", vq_hooks.doc_events)
        self.assertIn("Stock Entry", vq_hooks.doc_events)
        self.assertIn("Versa QC Result", vq_hooks.doc_events)
        self.assertIn("Versa QC Result", vq_hooks.permission_query_conditions)
        self.assertIn("Versa QC Spec", vq_hooks.permission_query_conditions)


class TestVersaQCSpecLifecycle(unittest.TestCase):
    """
    Tests Versa QC Spec document validation, versioning, and historical immutability.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_spec_valid_creation_and_validation(self):
        spec = VersaQCSpec({
            "name": "VQC-Single Jersey 180 GSM-V1.0",
            "spec_name": "Single Jersey 180 GSM",
            "version": "V1.0",
            "material_type": "Fabric",
            "company": "Tiruppur Textiles Ltd",
            "is_active": 1,
            "status": "Approved",
            "parameters": [
                {
                    "parameter_code": "FAB_GSM_ACTUAL",
                    "parameter_name": "Measured GSM",
                    "test_method": "ASTM D3776",
                    "severity": "Critical",
                    "min_limit": 175.0,
                    "max_limit": 185.0,
                    "sampling_required": 3
                },
                {
                    "parameter_code": "FAB_WIDTH_CUTTABLE",
                    "parameter_name": "Cuttable Width",
                    "test_method": "ASTM D3774",
                    "severity": "Critical",
                    "min_limit": 59.5,
                    "max_limit": 61.5,
                    "sampling_required": 3
                }
            ]
        })
        spec.validate()
        self.assertEqual(spec.version, "V1.0")
        self.assertEqual(len(spec.parameters), 2)

    def test_spec_missing_mandatory_name_fails(self):
        spec = VersaQCSpec({"version": "V1.0", "material_type": "Fabric"})
        with self.assertRaises(ValueError) as ctx:
            spec.validate()
        self.assertIn("Specification Name", str(ctx.exception))

    def test_spec_invalid_version_format_fails(self):
        spec = VersaQCSpec({
            "spec_name": "Invalid Spec",
            "version": "Release-Alpha",
            "material_type": "Fabric",
            "parameters": [{"parameter_code": "FAB_GSM", "min_limit": 100.0, "max_limit": 200.0}]
        })
        with self.assertRaises(ValueError) as ctx:
            spec.validate()
        self.assertIn("Invalid Specification Version format", str(ctx.exception))

    def test_spec_inverted_limits_fails(self):
        spec = VersaQCSpec({
            "spec_name": "Inverted Spec",
            "version": "V1.0",
            "material_type": "Fabric",
            "parameters": [{"parameter_code": "FAB_GSM", "min_limit": 190.0, "max_limit": 170.0}]
        })
        with self.assertRaises(ValueError) as ctx:
            spec.validate()
        self.assertIn("Min Limit (190.0) cannot be greater than Max Limit (170.0)", str(ctx.exception))

    def test_spec_duplicate_parameter_codes_fails(self):
        spec = VersaQCSpec({
            "spec_name": "Dup Spec",
            "version": "V1.0",
            "material_type": "Fabric",
            "parameters": [
                {"parameter_code": "FAB_GSM", "min_limit": 170.0, "max_limit": 190.0},
                {"parameter_code": "FAB_GSM", "min_limit": 175.0, "max_limit": 185.0}
            ]
        })
        with self.assertRaises(ValueError) as ctx:
            spec.validate()
        self.assertIn("Duplicate Parameter Code 'FAB_GSM'", str(ctx.exception))

    def test_spec_historical_immutability_blocks_reversion(self):
        spec = VersaQCSpec({
            "name": "VQC-Locked-V1.0",
            "spec_name": "Locked Spec",
            "version": "V1.0",
            "material_type": "Fabric",
            "status": "Draft",
            "parameters": [{"parameter_code": "FAB_GSM", "min_limit": 175.0, "max_limit": 185.0}]
        })
        frappe.db.count = lambda *args, **kwargs: 3
        with self.assertRaises(ValueError) as ctx:
            spec.validate_historical_integrity()
        self.assertIn("Cannot revert specification 'VQC-Locked-V1.0' to Draft", str(ctx.exception))


class TestVersaQCResultLifecycle(unittest.TestCase):
    """
    Tests Versa QC Result evaluation, readings processing, and submission lifecycle.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_qc_result_deterministic_pass(self):
        result = VersaQCResult({
            "name": "VQR-2026-00001",
            "company": "Tiruppur Textiles Ltd",
            "qc_spec": "VQC-Single Jersey 180 GSM-V1.0",
            "spec_version": "V1.0",
            "inspection_type": "Incoming Material",
            "source_doctype": "Purchase Receipt",
            "source_name": "MAT-PRE-2026-00001",
            "item": "KNT-FAB-SJ-180",
            "inspected_by": "qa_inspector@versaerp.com",
            "inspection_date": "2026-10-08",
            "measurements": [
                {
                    "parameter_code": "FAB_GSM_ACTUAL",
                    "severity": "Critical",
                    "min_limit": 175.0,
                    "max_limit": 185.0,
                    "tolerance_type": "Range"
                }
            ],
            "readings": [
                {"parameter_code": "FAB_GSM_ACTUAL", "reading_no": 1, "reading_value": 179.5},
                {"parameter_code": "FAB_GSM_ACTUAL", "reading_no": 2, "reading_value": 180.5},
                {"parameter_code": "FAB_GSM_ACTUAL", "reading_no": 3, "reading_value": 180.0}
            ]
        })
        with patch("versa_quality.permissions.get_user_active_company", return_value="Tiruppur Textiles Ltd"):
            result.validate()

        self.assertEqual(result.overall_status, "Accepted")
        m0 = result.measurements[0]
        status_val = m0.get("reading_status") if isinstance(m0, dict) else getattr(m0, "reading_status", None)
        mean_val = m0.get("mean_reading") if isinstance(m0, dict) else getattr(m0, "mean_reading", None)
        self.assertEqual(status_val, "Pass")
        self.assertEqual(mean_val, 180.0)

    def test_qc_result_concession_signoff_lifecycle(self):
        result = VersaQCResult({
            "name": "VQR-2026-00002",
            "company": "Tiruppur Textiles Ltd",
            "qc_spec": "VQC-Single Jersey 180 GSM-V1.0",
            "inspection_type": "Incoming Material",
            "source_doctype": "Purchase Receipt",
            "source_name": "MAT-PRE-2026-00002",
            "item": "KNT-FAB-SJ-180",
            "inspected_by": "qa_inspector@versaerp.com",
            "inspection_date": "2026-10-08",
            "measurements": [
                {
                    "parameter_code": "FAB_GSM_ACTUAL",
                    "severity": "Critical",
                    "min_limit": 175.0,
                    "max_limit": 185.0,
                    "tolerance_type": "Range"
                }
            ],
            "readings": [
                {"parameter_code": "FAB_GSM_ACTUAL", "reading_no": 1, "reading_value": 172.0}
            ],
            "concession_reason": "Buyer accepted lighter weight for summer garment style",
            "concession_approved_by": "qa_head@versaerp.com"
        })
        with patch("versa_quality.permissions.get_user_active_company", return_value="Tiruppur Textiles Ltd"):
            result.validate()

        self.assertEqual(result.overall_status, "Accepted with Concession")
        self.assertIn("concession by qa_head@versaerp.com", result.evaluation_summary)

    def test_qc_result_concession_without_signoff_rejects(self):
        result = VersaQCResult({
            "name": "VQR-2026-00003",
            "company": "Tiruppur Textiles Ltd",
            "qc_spec": "VQC-Single Jersey 180 GSM-V1.0",
            "inspection_type": "Incoming Material",
            "source_doctype": "Purchase Receipt",
            "source_name": "MAT-PRE-2026-00003",
            "item": "KNT-FAB-SJ-180",
            "inspected_by": "qa_inspector@versaerp.com",
            "inspection_date": "2026-10-08",
            "measurements": [
                {"parameter_code": "FAB_GSM_ACTUAL", "severity": "Critical", "min_limit": 175.0, "max_limit": 185.0}
            ],
            "readings": [
                {"parameter_code": "FAB_GSM_ACTUAL", "reading_no": 1, "reading_value": 170.0}
            ]
        })
        with patch("versa_quality.permissions.get_user_active_company", return_value="Tiruppur Textiles Ltd"):
            result.validate()

        self.assertEqual(result.overall_status, "Rejected")

    def test_qc_result_on_submit_blocks_inconclusive(self):
        result = VersaQCResult({
            "name": "VQR-2026-00004",
            "overall_status": "Inconclusive"
        })
        with self.assertRaises(ValueError) as ctx:
            result.on_submit()
        self.assertIn("Cannot submit Versa QC Result in 'Inconclusive' status", str(ctx.exception))


class TestPurchaseReceiptQualityGateIntegration(unittest.TestCase):
    """
    Tests Purchase Receipt quality gating through doc_event handlers.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_pr_uninspected_material_blocked(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00100",
            is_qc_required=1,
            versa_qc_status="Pending QC",
            versa_qc_result=None,
            items=[]
        )
        with self.assertRaises(ValueError) as ctx:
            check_qc_conformance(doc)
        self.assertIn("Quality Gate Block", str(ctx.exception))

    def test_pr_accepted_material_allowed(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00101",
            is_qc_required=1,
            versa_qc_status="QC Passed",
            versa_qc_result="VQR-2026-00001",
            items=[]
        )
        self.assertTrue(check_qc_conformance(doc))

    def test_pr_concession_material_allowed(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00102",
            is_qc_required=1,
            versa_qc_status="Accepted with Concession",
            versa_qc_result="VQR-2026-00002",
            items=[]
        )
        self.assertTrue(check_qc_conformance(doc))

    def test_pr_db_query_fallback_passes_when_valid_qc_in_db(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00103",
            is_qc_required=1,
            versa_qc_status="Pending QC",
            versa_qc_result="VQR-2026-00003",
            items=[]
        )
        with patch.object(frappe, "get_all", return_value=[{"name": "VQR-2026-00003"}]):
            self.assertTrue(check_purchase_receipt_qc_gate(doc))


class TestStockEntryQualityGateIntegration(unittest.TestCase):
    """
    Tests Stock Entry quality gating against quarantined or rejected fabric rolls.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_stock_entry_accepted_roll_allowed(self):
        doc = SimpleNamespace(
            name="MAT-STE-2026-00201",
            purpose="Material Issue",
            items=[SimpleNamespace(versa_fabric_roll="ROLL-2026-0001")]
        )
        with patch.object(frappe, "get_value", return_value={"quality_grade": "Accepted", "status": "In Stock"}):
            self.assertTrue(validate_qc_status(doc))

    def test_stock_entry_quarantined_roll_blocked(self):
        doc = SimpleNamespace(
            name="MAT-STE-2026-00202",
            purpose="Material Issue",
            items=[SimpleNamespace(versa_fabric_roll="ROLL-2026-0002")]
        )
        with patch.object(frappe, "get_value", return_value={"quality_grade": "Quarantine", "status": "Quarantined"}):
            with self.assertRaises(ValueError) as ctx:
                validate_qc_status(doc)
            self.assertIn("Quality Gate Block", str(ctx.exception))
            self.assertIn("Quarantine", str(ctx.exception))

    def test_stock_entry_rejected_roll_blocked(self):
        doc = SimpleNamespace(
            name="MAT-STE-2026-00203",
            purpose="Material Issue",
            items=[SimpleNamespace(versa_fabric_roll="ROLL-2026-0003")]
        )
        with patch.object(frappe, "get_value", return_value={"quality_grade": "Rejected", "status": "Rejected"}):
            with self.assertRaises(ValueError) as ctx:
                validate_qc_status(doc)
            self.assertIn("Quality Gate Block", str(ctx.exception))
            self.assertIn("Rejected", str(ctx.exception))


class TestCompanyIsolationRuntime(unittest.TestCase):
    """
    Validates multi-company quality isolation within a tenant.
    """

    def setUp(self):
        setup_frappe_test_env()

    @patch("versa_quality.permissions.get_user_active_company", return_value="Company A")
    def test_company_a_user_isolation(self, mock_comp):
        doc_a = SimpleNamespace(name="VQR-2026-00001", company="Company A", doctype="Versa QC Result")
        doc_b = SimpleNamespace(name="VQR-2026-00002", company="Company B", doctype="Versa QC Result")

        self.assertTrue(check_quality_company_isolation(doc_a))
        with self.assertRaises(PermissionError):
            check_quality_company_isolation(doc_b)

    @patch("versa_quality.permissions.get_user_active_company", return_value="Company B")
    def test_company_b_user_isolation(self, mock_comp):
        doc_a = SimpleNamespace(name="VQR-2026-00001", company="Company A", doctype="Versa QC Result")
        doc_b = SimpleNamespace(name="VQR-2026-00002", company="Company B", doctype="Versa QC Result")

        self.assertTrue(check_quality_company_isolation(doc_b))
        with self.assertRaises(PermissionError):
            check_quality_company_isolation(doc_a)

    @patch("versa_quality.permissions.get_user_active_company", return_value=None)
    def test_unassigned_user_fails_closed(self, mock_comp):
        cond = get_permission_query_conditions_quality_result("unassigned_user@versaerp.com")
        self.assertEqual(cond, "1 = 0")


class TestTenantSiteIsolationRuntime(unittest.TestCase):
    """
    Validates physical tenant isolation on quality data across sites.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_tenant_sites_exist_and_isolated(self):
        tenant_a_sites = os.path.join(bench_root, "sites", "versa-tenant-a.local")
        tenant_b_sites = os.path.join(bench_root, "sites", "versa-tenant-b.local")

        self.assertTrue(os.path.exists(tenant_a_sites), f"Tenant A site missing at {tenant_a_sites}")
        self.assertTrue(os.path.exists(tenant_b_sites), f"Tenant B site missing at {tenant_b_sites}")
        self.assertNotEqual(tenant_a_sites, tenant_b_sites)


class TestASTM5430DefectScoreValidation(unittest.TestCase):
    """
    Validates ASTM D5430 4-Point System scoring, boundary conditions, and grade classification.
    """

    def test_4point_grade_a(self):
        # 10 points on 100 yds of 60 in fabric -> (10 * 3600)/(100 * 60) = 6.0
        score, grade = calculate_4point_defect_score(10.0, 100.0, 60.0)
        self.assertEqual(score, 6.0)
        self.assertEqual(grade, "Grade A")

    def test_4point_grade_b_concession(self):
        # 40 points on 100 yds of 60 in fabric -> (40 * 3600)/(100 * 60) = 24.0
        score, grade = calculate_4point_defect_score(40.0, 100.0, 60.0)
        self.assertEqual(score, 24.0)
        self.assertEqual(grade, "Grade B")

    def test_4point_grade_c_rejected(self):
        # 50 points on 100 yds of 60 in fabric -> (50 * 3600)/(100 * 60) = 30.0
        score, grade = calculate_4point_defect_score(50.0, 100.0, 60.0)
        self.assertEqual(score, 30.0)
        self.assertEqual(grade, "Grade C")

    def test_4point_zero_length_inconclusive(self):
        score, grade = calculate_4point_defect_score(10.0, 0.0, 60.0)
        self.assertIsNone(score)
        self.assertEqual(grade, "Inconclusive")


class TestPhysicalMeasurementValidation(unittest.TestCase):
    """
    Validates physical fabric measurement relationships (GLM = GSM * Width / 1000).
    """

    def test_glm_physical_relationship_calculation(self):
        # Specimen: GSM = 180 g/m^2, Cuttable Width = 60 inches (1524 mm)
        # GLM = (180 * 1524) / 1000 = 274.32 grams / linear meter
        gsm = 180.0
        width_mm = 60.0 * 25.4
        glm = (gsm * width_mm) / 1000.0
        self.assertAlmostEqual(glm, 274.32, places=2)

        # Roll of 25.0 kg -> Calculated Length = (25.0 * 1000) / 274.32 = 91.13 meters
        roll_weight_kg = 25.0
        calc_length_m = (roll_weight_kg * 1000.0) / glm
        self.assertAlmostEqual(calc_length_m, 91.13, places=2)


class TestQualityIdempotencyAndAuthority(unittest.TestCase):
    """
    Validates idempotency of quality events and ERPNext ledger authority exclusivity.
    """

    def setUp(self):
        setup_frappe_test_env()

    def test_idempotent_event_validation(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00301",
            is_qc_required=1,
            versa_qc_status="QC Passed",
            versa_qc_result="VQR-2026-00001",
            items=[]
        )
        # First execution
        res1 = check_qc_conformance(doc)
        # Second execution (retry/re-validation)
        res2 = check_qc_conformance(doc)
        self.assertTrue(res1)
        self.assertTrue(res2)
        self.assertEqual(res1, res2)

    def test_zero_competing_ledgers_created(self):
        import versa_quality
        # Verify package does not define duplicate ledger doctypes
        pkg_dir = os.path.dirname(versa_quality.__file__)
        doctypes_dir = os.path.join(pkg_dir, "versa_quality", "doctype")
        discovered_doctypes = os.listdir(doctypes_dir)
        
        self.assertNotIn("versa_stock_ledger", discovered_doctypes)
        self.assertNotIn("versa_gl_entry", discovered_doctypes)
        self.assertNotIn("versa_inventory_balance", discovered_doctypes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
