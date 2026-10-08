import sys
import os
import unittest

bench_apps = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
versa_quality_path = os.path.join(bench_apps, "versa_quality")
if versa_quality_path not in sys.path:
    sys.path.insert(0, versa_quality_path)

from versa_quality.versa_quality.doctype.versa_qc_spec.versa_qc_spec import VersaQCSpec



class TestVersaQCSpec(unittest.TestCase):
    """
    Tests specification validation, versioning rules, and parameter integrity.
    """

    def test_valid_qc_spec_validation(self):
        doc = VersaQCSpec({
            "spec_name": "Single Jersey 180 GSM Fabric",
            "version": "V1.0",
            "material_type": "Fabric",
            "parameters": [
                {
                    "parameter_code": "FAB_GSM_ACTUAL",
                    "parameter_name": "Measured GSM",
                    "test_method": "ASTM D3776",
                    "severity": "Critical",
                    "min_limit": 175.0,
                    "max_limit": 185.0
                }
            ]
        })
        doc.validate()  # Should complete without error

    def test_spec_invalid_version_format_rejected(self):
        doc = VersaQCSpec({
            "spec_name": "Invalid Version Spec",
            "version": "Version-Draft-2026",
            "material_type": "Yarn",
            "parameters": [
                {"parameter_code": "YRN_CSP", "severity": "Critical", "min_limit": 2800.0}
            ]
        })
        with self.assertRaises(ValueError) as ctx:
            doc.validate()
        self.assertIn("Invalid Specification Version format", str(ctx.exception))

    def test_spec_empty_parameters_rejected(self):
        doc = VersaQCSpec({
            "spec_name": "Empty Spec",
            "version": "V1.0",
            "material_type": "Fabric",
            "parameters": []
        })
        with self.assertRaises(ValueError) as ctx:
            doc.validate()
        self.assertIn("must contain at least one Quality Parameter", str(ctx.exception))

    def test_spec_inverted_limits_rejected(self):
        doc = VersaQCSpec({
            "spec_name": "Inverted Limits Spec",
            "version": "V1.0",
            "material_type": "Fabric",
            "parameters": [
                {
                    "parameter_code": "FAB_GSM_ACTUAL",
                    "min_limit": 190.0,
                    "max_limit": 170.0,  # Min > Max
                    "severity": "Critical"
                }
            ]
        })
        with self.assertRaises(ValueError) as ctx:
            doc.validate()
        self.assertIn("Min Limit (190.0) cannot be greater than Max Limit (170.0)", str(ctx.exception))

    def test_spec_duplicate_parameter_codes_rejected(self):
        doc = VersaQCSpec({
            "spec_name": "Duplicate Codes Spec",
            "version": "V1.0",
            "material_type": "Fabric",
            "parameters": [
                {"parameter_code": "FAB_GSM", "min_limit": 170.0, "max_limit": 190.0, "severity": "Critical"},
                {"parameter_code": "FAB_GSM", "min_limit": 175.0, "max_limit": 185.0, "severity": "Major"}
            ]
        })
        with self.assertRaises(ValueError) as ctx:
            doc.validate()
        self.assertIn("Duplicate Parameter Code 'FAB_GSM'", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
