# Prompt ID: P03-001

## Metadata
- **Phase:** Phase 3 — Core Implementation Bootstrap
- **Date:** 2026-10-05
- **Title:** Bootstrap of `versa_core` Application & Approval Rule Engine
- **Status:** COMPLETED
- **Provenance Classification:** RECONSTRUCTED

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P02-003`
- **Supersedes:** None
- **Related Prompt(s):** `P03-002`

---

## 2. Intent & Scoping
- **Purpose:** Implement `versa_core` Frappe app containing dynamic approval matrices (`Versa Approval Rule`), multi-company isolation query conditions, and supplier analytics stubs.
- **Semantic Authority:** `documents/versa/04_implementation_spec/VERSA_FRAPPE_IMPLEMENTATION_SPECIFICATION.md`
- **Decision Authority:** `DEC-006`

---

## 3. Constraints & Invariants
- Fail-closed multi-company query filtering.
- Dynamic approval rules governing Purchase Order grand total thresholds.

---

## 4. Requested Actions
1. Create `bench/apps/versa_core` app package.
2. Implement `Versa Approval Rule` DocType.
3. Wire document events and permission query conditions.

---

## 5. Expected & Resulting Outputs
- **Resulting Decisions:** `documents/versa/06_decisions/VERSA_QUALITY_IMPLEMENTATION_DECISIONS.md`
- **Resulting Implementation:** `bench/apps/versa_core/`
- **Resulting Tests:** `bench/apps/versa_core/versa_core/tests/test_core_suite.py`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY`
- **Rationale:** Initial core platform package implementation.
