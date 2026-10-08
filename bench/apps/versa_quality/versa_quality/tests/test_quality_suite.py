import sys
import os
import unittest

# Ensure bench/apps are on python path
bench_apps = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
versa_quality_path = os.path.join(bench_apps, "versa_quality")
versa_core_path = os.path.join(bench_apps, "versa_core")
if versa_quality_path not in sys.path:
    sys.path.insert(0, versa_quality_path)
if versa_core_path not in sys.path:
    sys.path.insert(0, versa_core_path)

from versa_quality.tests.test_quality_evaluator import TestVersaQualityEvaluator
from versa_quality.tests.test_quality_spec import TestVersaQCSpec
from versa_quality.tests.test_quality_gates import TestVersaQualityGates
from versa_quality.tests.test_company_isolation import TestVersaQualityCompanyIsolation



def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestVersaQualityEvaluator))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestVersaQCSpec))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestVersaQualityGates))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestVersaQualityCompanyIsolation))
    return s


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
