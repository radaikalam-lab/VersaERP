import sys
import os
import unittest
from types import SimpleNamespace

bench_apps = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
versa_quality_path = os.path.join(bench_apps, "versa_quality")
if versa_quality_path not in sys.path:
    sys.path.insert(0, versa_quality_path)

from versa_quality.gates import check_purchase_receipt_qc_gate, check_stock_entry_qc_gate



class TestVersaQualityGates(unittest.TestCase):
    """
    Tests fail-closed quality gate enforcement.
    """

    def test_pr_gate_passes_when_qc_not_required(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00001",
            is_qc_required=0,
            items=[]
        )
        self.assertTrue(check_purchase_receipt_qc_gate(doc))

    def test_pr_gate_blocks_uninspected_material(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00002",
            is_qc_required=1,
            versa_qc_status="Pending QC",
            versa_qc_result=None,
            items=[]
        )
        with self.assertRaises(ValueError) as ctx:
            check_purchase_receipt_qc_gate(doc)
        self.assertIn("Quality Gate Block", str(ctx.exception))
        self.assertIn("Pending QC", str(ctx.exception))

    def test_pr_gate_passes_when_status_qc_passed(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00003",
            is_qc_required=1,
            versa_qc_status="QC Passed",
            versa_qc_result="VQR-2026-00001",
            items=[]
        )
        self.assertTrue(check_purchase_receipt_qc_gate(doc))

    def test_pr_gate_passes_when_status_concession(self):
        doc = SimpleNamespace(
            name="MAT-PRE-2026-00004",
            is_qc_required=1,
            versa_qc_status="Accepted with Concession",
            versa_qc_result="VQR-2026-00002",
            items=[]
        )
        self.assertTrue(check_purchase_receipt_qc_gate(doc))

    def test_stock_entry_receipt_bypasses_quarantine_check(self):
        doc = SimpleNamespace(
            name="MAT-STE-2026-00001",
            purpose="Material Receipt",
            items=[]
        )
        self.assertTrue(check_stock_entry_qc_gate(doc))


if __name__ == "__main__":
    unittest.main()
