# Prompt ID: P02-001

## Metadata
- **Phase:** Phase 2 — Frappe Implementation Specification
- **Date:** 2026-09-28
- **Title:** Mapping Canonical Entities to Frappe DocTypes & Non-Invasive Hooks
- **Status:** COMPLETED
- **Provenance Classification:** RECONSTRUCTED

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P01-001`
- **Supersedes:** None
- **Related Prompt(s):** `P02-002`, `P02-003`

---

## 2. Intent & Scoping
- **Purpose:** Map canonical entities (ENT-001 to ENT-039) to Frappe framework primitives, custom DocTypes, child tables, doc_events, and permission query conditions.
- **Semantic Authority:** `documents/versa/04_implementation_spec/VERSA_FRAPPE_MODEL.md`
- **Decision Authority:** `DEC-003`
- **Input Artifacts:**
  - `documents/versa/01_domain/VERSA_DOMAIN_MODEL.md`
  - `documents/versa/01_domain/VERSA_RDBMS_MODEL.md`

---

## 3. Constraints & Invariants
- Zero core forks of Frappe or ERPNext. Non-invasive modular app overlay only.

---

## 4. Requested Actions
1. Author Frappe implementation specification.
2. Build bidirectional traceability between canonical entities and Frappe schemas.
3. Validate schema mappings via `validate_frappe_specification.py`.

---

## 5. Expected & Resulting Outputs
- **Resulting Decisions:** `documents/versa/06_decisions/VERSA_FRAPPE_IMPLEMENTATION_DECISIONS.md`
- **Resulting Contracts:** `documents/versa/04_implementation_spec/VERSA_FRAPPE_IMPLEMENTATION_SPECIFICATION.md`
- **Resulting Validation Artifacts:**
  - `documents/versa/04_implementation_spec/VERSA_FRAPPE_MODEL.md`
  - `documents/versa/04_implementation_spec/VERSA_FRAPPE_IMPLEMENTATION_TRACEABILITY.md`
  - `documents/versa/05_validation/validate_frappe_specification.py`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY`
- **Rationale:** Frappe framework mapping without altering canonical semantics.
