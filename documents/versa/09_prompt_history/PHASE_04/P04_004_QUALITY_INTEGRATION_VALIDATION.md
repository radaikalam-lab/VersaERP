# Prompt ID: P04-004

## Metadata
- **Phase:** Phase 4D — Quality Integration Validation
- **Date:** 2026-10-08
- **Title:** Live Document Lifecycle, Quality Gate & Docker Stack Integration Validation
- **Status:** COMPLETED
- **Provenance Classification:** ORIGINAL

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P04-003`
- **Supersedes:** None
- **Related Prompt(s):** `P04-005`

---

## 2. Intent & Scoping
- **Purpose:** Validate `versa_quality` through the actual Frappe/ERPNext document lifecycle, test Purchase Receipt and Stock Entry quality gates, multi-company and multi-tenant isolation, idempotency, and transactional consistency in Docker.
- **Semantic Authority:** `documents/versa/02_contracts/VERSA_QUALITY_CONTRACT.md`
- **Decision Authority:** Integration Validation Gate

---

## 3. Constraints & Invariants
- Use canonical Docker runtime.
- Enforce fail-closed quality gates on uninspected, quarantined, or rejected materials.

---

## 4. Requested Actions
1. Author comprehensive runtime integration test suite `deployment/docker/scripts/test_quality_runtime.py`.
2. Execute tests for Spec lifecycle, Result lifecycle, PR gate, SE gate, Company isolation, Tenant isolation, ASTM D5430, and Idempotency.
3. Harden `gates.py` and `versa_qc_result.py` against fail-closed defect exposures.
4. Author `VERSA_QUALITY_INTEGRATION_VALIDATION_REPORT.md`.

---

## 5. Expected & Resulting Outputs
- **Resulting Implementation:**
  - `bench/apps/versa_quality/versa_quality/gates.py` (Hardened)
  - `bench/apps/versa_quality/versa_quality/versa_quality/doctype/versa_qc_result/versa_qc_result.py` (Hardened)
- **Resulting Tests:** `deployment/docker/scripts/test_quality_runtime.py` (29/29 PASS)
- **Resulting Validation Artifacts:**
  - `documents/versa/05_validation/VERSA_QUALITY_INTEGRATION_VALIDATION_REPORT.md`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY`
- **Rationale:** Runtime bug fixes and comprehensive lifecycle tests.
