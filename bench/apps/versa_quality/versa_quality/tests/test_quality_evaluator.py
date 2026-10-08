import sys
import os
import unittest

bench_apps = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
versa_quality_path = os.path.join(bench_apps, "versa_quality")
if versa_quality_path not in sys.path:
    sys.path.insert(0, versa_quality_path)

from versa_quality.evaluator import (

    calculate_readings_statistics,
    evaluate_parameter_measurement,
    calculate_4point_defect_score,
    evaluate_overall_disposition
)


class TestVersaQualityEvaluator(unittest.TestCase):
    """
    Tests mathematical and logical determinism of the quality evaluator.
    """

    def test_readings_statistics_empty(self):
        stats = calculate_readings_statistics([])
        self.assertEqual(stats["count"], 0)
        self.assertIsNone(stats["mean"])
        self.assertIsNone(stats["min"])
        self.assertIsNone(stats["max"])
        self.assertIsNone(stats["std_dev"])

    def test_readings_statistics_multi_point(self):
        # 5 readings of GSM across fabric width (Left, Center-Left, Center, Center-Right, Right)
        readings = [180.5, 181.2, 179.8, 180.0, 182.0]
        stats = calculate_readings_statistics(readings)
        self.assertEqual(stats["count"], 5)
        self.assertEqual(stats["mean"], 180.7)
        self.assertEqual(stats["min"], 179.8)
        self.assertEqual(stats["max"], 182.0)
        self.assertAlmostEqual(stats["std_dev"], 0.9055, places=3)


    def test_evaluate_parameter_range_pass(self):
        # Target GSM: 180 +/- 5 (175 - 185)
        readings = [179.0, 181.0, 180.0]
        res = evaluate_parameter_measurement(
            parameter_code="FAB_GSM_ACTUAL",
            severity="Critical",
            min_limit=175.0,
            max_limit=185.0,
            target_value="180",
            tolerance_type="Range",
            readings=readings
        )
        self.assertEqual(res["status"], "Pass")
        self.assertEqual(res["stats"]["count"], 3)
        self.assertEqual(res["stats"]["mean"], 180.0)

    def test_evaluate_parameter_range_fail_high(self):
        # Target GSM: 180 +/- 5 (175 - 185), Observed: 188.0
        readings = [187.0, 189.0, 188.0]
        res = evaluate_parameter_measurement(
            parameter_code="FAB_GSM_ACTUAL",
            severity="Critical",
            min_limit=175.0,
            max_limit=185.0,
            target_value="180",
            tolerance_type="Range",
            readings=readings
        )
        self.assertEqual(res["status"], "Fail")
        self.assertEqual(res["stats"]["mean"], 188.0)
        self.assertIn("exceeds maximum limit", res["reason"])

    def test_evaluate_parameter_range_fail_low(self):
        # Target GSM: 180 +/- 5 (175 - 185), Observed: 172.0
        readings = [171.0, 173.0, 172.0]
        res = evaluate_parameter_measurement(
            parameter_code="FAB_GSM_ACTUAL",
            severity="Critical",
            min_limit=175.0,
            max_limit=185.0,
            target_value="180",
            tolerance_type="Range",
            readings=readings
        )
        self.assertEqual(res["status"], "Fail")
        self.assertIn("below minimum limit", res["reason"])

    def test_evaluate_parameter_minimum_only(self):
        # Yarn CSP minimum >= 2800
        res_pass = evaluate_parameter_measurement(
            parameter_code="YRN_CSP",
            severity="Major",
            min_limit=2800.0,
            max_limit=None,
            target_value=">=2800",
            tolerance_type="Minimum",
            readings=[2950.0, 3010.0, 2890.0]
        )
        self.assertEqual(res_pass["status"], "Pass")

        res_fail = evaluate_parameter_measurement(
            parameter_code="YRN_CSP",
            severity="Major",
            min_limit=2800.0,
            max_limit=None,
            target_value=">=2800",
            tolerance_type="Minimum",
            readings=[2650.0, 2700.0, 2750.0]
        )
        self.assertEqual(res_fail["status"], "Fail")

    def test_evaluate_parameter_visual_pass_fail(self):
        # Critical defect check (1.0 = Pass/No defects, 0.0 = Defect found)
        res_pass = evaluate_parameter_measurement(
            parameter_code="GAR_CRITICAL_DEFECT",
            severity="Critical",
            min_limit=None,
            max_limit=None,
            target_value="No Sharp Needles",
            tolerance_type="Visual/Pass-Fail",
            readings=[1.0, 1.0, 1.0]
        )
        self.assertEqual(res_pass["status"], "Pass")

        res_fail = evaluate_parameter_measurement(
            parameter_code="GAR_CRITICAL_DEFECT",
            severity="Critical",
            min_limit=None,
            max_limit=None,
            target_value="No Sharp Needles",
            tolerance_type="Visual/Pass-Fail",
            readings=[1.0, 0.0, 1.0]
        )
        self.assertEqual(res_fail["status"], "Fail")

    def test_evaluate_parameter_missing_readings_inconclusive(self):
        res = evaluate_parameter_measurement(
            parameter_code="FAB_GSM_ACTUAL",
            severity="Critical",
            min_limit=175.0,
            max_limit=185.0,
            target_value="180",
            tolerance_type="Range",
            readings=[]
        )
        self.assertEqual(res["status"], "Inconclusive")
        self.assertIn("Missing measurement readings", res["reason"])

    def test_4point_defect_score_astm_d5430(self):
        # Grade A: 10 defect points across 100 yds of 60-inch fabric -> (10 * 3600)/(100 * 60) = 6.0
        score_a, grade_a = calculate_4point_defect_score(10.0, 100.0, 60.0)
        self.assertEqual(score_a, 6.0)
        self.assertEqual(grade_a, "Grade A")

        # Grade B (Concession): 40 defect points -> (40 * 3600)/(100 * 60) = 24.0
        score_b, grade_b = calculate_4point_defect_score(40.0, 100.0, 60.0)
        self.assertEqual(score_b, 24.0)
        self.assertEqual(grade_b, "Grade B")

        # Grade C (Reject): 60 defect points -> (60 * 3600)/(100 * 60) = 36.0
        score_c, grade_c = calculate_4point_defect_score(60.0, 100.0, 60.0)
        self.assertEqual(score_c, 36.0)
        self.assertEqual(grade_c, "Grade C")

    def test_overall_disposition_all_pass(self):
        measurements = [
            {"parameter_code": "FAB_GSM", "severity": "Critical", "status": "Pass"},
            {"parameter_code": "FAB_WIDTH", "severity": "Critical", "status": "Pass"},
            {"parameter_code": "DYE_WASH", "severity": "Major", "status": "Pass"}
        ]
        disp = evaluate_overall_disposition(measurements, defect_score=5.0)
        self.assertEqual(disp["overall_status"], "Accepted")
        self.assertEqual(disp["critical_fails"], 0)
        self.assertEqual(disp["major_fails"], 0)

    def test_overall_disposition_critical_fail_rejects(self):
        measurements = [
            {"parameter_code": "FAB_GSM", "severity": "Critical", "status": "Fail"},
            {"parameter_code": "FAB_WIDTH", "severity": "Critical", "status": "Pass"}
        ]
        disp = evaluate_overall_disposition(measurements)
        self.assertEqual(disp["overall_status"], "Rejected")
        self.assertEqual(disp["critical_fails"], 1)

    def test_overall_disposition_major_fail_without_concession_rejects(self):
        measurements = [
            {"parameter_code": "FAB_GSM", "severity": "Critical", "status": "Pass"},
            {"parameter_code": "DYE_RUB_WET", "severity": "Major", "status": "Fail"}
        ]
        disp = evaluate_overall_disposition(measurements)
        self.assertEqual(disp["overall_status"], "Rejected")

    def test_overall_disposition_major_fail_with_concession_accepts(self):
        measurements = [
            {"parameter_code": "FAB_GSM", "severity": "Critical", "status": "Pass"},
            {"parameter_code": "DYE_RUB_WET", "severity": "Major", "status": "Fail"}
        ]
        disp = evaluate_overall_disposition(
            measurements,
            concession_reason="Buyer approved slight wet rubbing variance for garment wash style.",
            concession_approved_by="qa_head@versaerp.com"
        )
        self.assertEqual(disp["overall_status"], "Accepted with Concession")


if __name__ == "__main__":
    unittest.main()
