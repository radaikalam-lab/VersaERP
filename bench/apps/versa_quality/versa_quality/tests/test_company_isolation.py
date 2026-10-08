import sys
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

bench_apps = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
versa_quality_path = os.path.join(bench_apps, "versa_quality")
if versa_quality_path not in sys.path:
    sys.path.insert(0, versa_quality_path)

from versa_quality.permissions import (
    get_permission_query_conditions_quality_result,
    get_permission_query_conditions_quality_spec,
    check_quality_company_isolation
)



class TestVersaQualityCompanyIsolation(unittest.TestCase):
    """
    Tests fail-closed multi-company isolation on quality objects.
    """

    def test_query_conditions_administrator(self):
        cond = get_permission_query_conditions_quality_result("Administrator")
        self.assertEqual(cond, "")

    @patch("versa_quality.permissions.get_user_active_company", return_value="Test Company A")
    def test_query_conditions_user_with_company(self, mock_comp):
        cond = get_permission_query_conditions_quality_result("user_a@versaerp.com")
        self.assertEqual(cond, "(`tabVersa QC Result`.`company` = 'Test Company A')")

    @patch("versa_quality.permissions.get_user_active_company", return_value=None)
    def test_query_conditions_no_company_fails_closed(self, mock_comp):
        cond = get_permission_query_conditions_quality_result("user_unassigned@versaerp.com")
        self.assertEqual(cond, "1 = 0")

    @patch("versa_quality.permissions.get_user_active_company", return_value="Test Company A")
    def test_spec_query_conditions_user_with_company(self, mock_comp):
        cond = get_permission_query_conditions_quality_spec("user_a@versaerp.com")
        self.assertIn("`company` = 'Test Company A'", cond)
        self.assertIn("`company` IS NULL", cond)

    @patch("versa_quality.permissions.get_user_active_company", return_value=None)
    def test_spec_query_conditions_no_company_returns_global_only(self, mock_comp):
        cond = get_permission_query_conditions_quality_spec("user_unassigned@versaerp.com")
        self.assertIn("`company` IS NULL", cond)

    @patch("versa_quality.permissions.get_user_active_company", return_value="Test Company A")
    def test_check_company_isolation_same_company_succeeds(self, mock_comp):
        doc = SimpleNamespace(name="VQR-2026-00001", company="Test Company A", doctype="Versa QC Result")
        self.assertTrue(check_quality_company_isolation(doc))

    @patch("versa_quality.permissions.get_user_active_company", return_value="Test Company A")
    def test_check_company_isolation_cross_company_fails(self, mock_comp):
        doc = SimpleNamespace(name="VQR-2026-00002", company="Test Company B", doctype="Versa QC Result")
        with self.assertRaises(PermissionError) as ctx:
            check_quality_company_isolation(doc)
        self.assertIn("Cross-Company Violation", str(ctx.exception))

    def test_check_company_isolation_none_doc_fails(self):
        with self.assertRaises(ValueError):
            check_quality_company_isolation(None)

    def test_check_company_isolation_missing_doc_company_fails(self):
        doc = SimpleNamespace(name="VQR-2026-00003", company=None, doctype="Versa QC Result")
        with self.assertRaises(ValueError):
            check_quality_company_isolation(doc)


if __name__ == "__main__":
    unittest.main()
