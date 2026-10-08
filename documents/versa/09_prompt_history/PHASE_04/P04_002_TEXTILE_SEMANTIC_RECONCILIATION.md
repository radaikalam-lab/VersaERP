# Prompt ID: P04-002

## Metadata
- **Phase:** Phase 4B — Textile Semantic Reconciliation
- **Date:** 2026-10-08
- **Title:** Semantic Reconciliation & Epistemic Recalibration of Textile Evidence
- **Status:** COMPLETED
- **Provenance Classification:** ORIGINAL

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P04-001`
- **Supersedes:** None
- **Related Prompt(s):** `P04-003`

---

## 2. Intent & Scoping
- **Purpose:** Perform final semantic reconciliation pass over the completed archaeology; classify observations into strict categories (`EXTERNAL_OBSERVATION`, `CANDIDATE_SEMANTIC`, `VERSA_CONFIRMED`, `VERSA_CONFLICT`, `NOT_RELEVANT`, `DEFERRED`); eliminate unverified overclaims.
- **Semantic Authority:** `documents/versa/05_validation/VERSA_TEXTILE_SEMANTIC_RECONCILIATION_REPORT.md`
- **Decision Authority:** Architectural Governance Gate

---

## 3. Constraints & Invariants
- DO NOT convert external observations into normative Versa rules without explicit Versa decision.
- Zero runtime code changes, zero DocType modifications, zero domain contract changes.

---

## 4. Requested Actions
1. Reconcile evidence classification across tolerances, UOMs, and wet processing parameters.
2. Eliminate overclaims and recalibrate language.
3. Compare provisional `versa_quality` against `VERSA_QUALITY_CONTRACT.md`.
4. Reconcile Job Work, Order Matrix, Multi-UOM, Wet Processing, and Export.
5. Author `VERSA_TEXTILE_SEMANTIC_RECONCILIATION_REPORT.md`.

---

## 5. Expected & Resulting Outputs
- **Resulting Validation Artifacts:**
  - `documents/versa/05_validation/VERSA_TEXTILE_SEMANTIC_RECONCILIATION_REPORT.md`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY` (Audit & Reconciliation)
- **Rationale:** Strict epistemic governance without contract mutation.
