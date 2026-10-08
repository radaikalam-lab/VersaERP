"""
Automated Validator for VersaERP Design-Time Semantic Workspace & Runtime Boundary.
"""

import sys
import re
from pathlib import Path

def validate_design_time_workspace(versa_root: Path):
    print("=" * 80)
    print("VERSA ERP DESIGN-TIME WORKSPACE & RUNTIME BOUNDARY VALIDATOR")
    print("=" * 80)

    # 1. Check Design-Time Workspace Existence
    dt_root = versa_root / "design-time" / "semantic-analysis"
    if not dt_root.exists():
        print(f"[FAIL] Design-time workspace missing: {dt_root}")
        return False
    print(f"[PASS] Design-time workspace verified at: {dt_root}")

    # 2. Check Toolkit Subpackages
    required_pkgs = ["semantics", "domain", "reconciliation", "requirements", "provenance"]
    for pkg in required_pkgs:
        pkg_path = dt_root / "toolkit" / pkg
        if not pkg_path.exists():
            print(f"[FAIL] Missing toolkit subpackage: {pkg}")
            return False
    print(f"[PASS] All {len(required_pkgs)} design-time toolkit subpackages verified.")

    # 3. Check README and Architectural Disclaimer
    readme_path = dt_root / "README.md"
    if not readme_path.exists() or "CRITICAL ARCHITECTURAL DISCLAIMER" not in readme_path.read_text(encoding="utf-8"):
        print(f"[FAIL] Missing or invalid README disclaimer in design-time workspace.")
        return False
    print(f"[PASS] Design-time architectural disclaimer verified.")

    # 4. Check Runtime Isolation (Zero imports from design-time or GraphModel in bench/apps)
    apps_root = versa_root / "bench" / "apps"
    forbidden_imports = ["graphmodel", "design-time", "semantic_analysis", "toolkit.semantics"]
    violations = []
    
    if apps_root.exists():
        for py_file in apps_root.rglob("*.py"):
            text = py_file.read_text(encoding="utf-8", errors="ignore")
            for line in text.splitlines():
                line_str = line.strip()
                if line_str.startswith("import ") or line_str.startswith("from "):
                    for fi in forbidden_imports:
                        if fi in line_str:
                            violations.append(f"{py_file.name}: {line_str}")

    if violations:
        print(f"[FAIL] Runtime boundary violation! Forbidden import detected in runtime apps:\n  " + "\n  ".join(violations))
        return False
    print(f"[PASS] Runtime Isolation Verified: Zero runtime dependencies on GraphModel or design-time tooling.")

    # 5. Check Authoritative Artifact Root
    docs_root = versa_root / "documents" / "versa"
    if not (docs_root / "01_domain" / "versa_domain_model.json").exists():
        print(f"[FAIL] Authoritative domain model JSON missing from {docs_root}")
        return False
    print(f"[PASS] Authoritative artifact root verified at: {docs_root}")

    print("=" * 80)
    print("DESIGN-TIME WORKSPACE: PASS")
    print("RUNTIME ISOLATION: PASS")
    print("GRAPHMODEL RUNTIME DEPENDENCY: NONE")
    print("AUTHORITATIVE ARTIFACT LOCATION: PASS")
    print("=" * 80)
    return True

if __name__ == "__main__":
    root = Path(r"E:\VersaERP")
    success = validate_design_time_workspace(root)
    sys.exit(0 if success else 1)
