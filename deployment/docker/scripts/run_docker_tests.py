#!/usr/bin/env python3
"""
VersaERP Canonical Test Runner for Docker Runtime.
Runs all test suites inside the Docker container and outputs structured classification.
"""

import sys
import unittest
from pathlib import Path

def run_tests():
    print("=" * 75)
    print("VERSA ERP DOCKER CANONICAL RUNTIME TEST SUITE")
    print("=" * 75)
    
    # Locate bench directory
    bench_dir = Path("/home/frappe/frappe-bench")
    if not bench_dir.exists():
        bench_dir = Path(__file__).resolve().parent.parent.parent / "bench"
        
    core_tests_dir = bench_dir / "apps" / "versa_core" / "versa_core" / "tests"
    quality_tests_dir = bench_dir / "apps" / "versa_quality" / "versa_quality" / "tests"
    docker_scripts_dir = bench_dir / "deployment" / "docker" / "scripts"
    if not docker_scripts_dir.exists():
        docker_scripts_dir = Path(__file__).resolve().parent
        
    sys.path.insert(0, str(bench_dir / "apps" / "frappe"))
    sys.path.insert(0, str(bench_dir / "apps" / "erpnext"))
    sys.path.insert(0, str(bench_dir / "apps" / "versa_core"))
    sys.path.insert(0, str(bench_dir / "apps" / "versa_quality"))
    sys.path.insert(0, str(docker_scripts_dir))
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if core_tests_dir.exists():
        suite.addTests(loader.discover(start_dir=str(core_tests_dir), pattern="test_*.py"))
    if quality_tests_dir.exists():
        suite.addTests(loader.discover(start_dir=str(quality_tests_dir), pattern="test_*.py"))
    if docker_scripts_dir.exists():
        suite.addTests(loader.discover(start_dir=str(docker_scripts_dir), pattern="test_*.py"))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 75)
    print("DOCKER RUNTIME TEST SUMMARY")
    print("=" * 75)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Passed:          {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed:          {len(result.failures)}")
    print(f"Errors:          {len(result.errors)}")
    print(f"Skipped:         {len(result.skipped)}")
    print("=" * 75)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

