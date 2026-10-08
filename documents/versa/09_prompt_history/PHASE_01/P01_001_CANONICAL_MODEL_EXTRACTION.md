# Prompt ID: P01-001

## Metadata
- **Phase:** Phase 1 — Canonical Domain Modeling & Semantic Extraction
- **Date:** 2026-09-22
- **Title:** Extraction of Canonical 39 Entities, 28 Relationships, and Invariants
- **Status:** COMPLETED
- **Provenance Classification:** RECONSTRUCTED

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P00-001`
- **Supersedes:** None
- **Related Prompt(s):** `P02-001`

---

## 2. Intent & Scoping
- **Purpose:** Formalize canonical domain model: 39 entities, 28 relationships, 6 invariants, 3 business rules, 2 workflow rules, and 2 derived metrics.
- **Semantic Authority:** `documents/versa/01_domain/VERSA_DOMAIN_MODEL.md`
- **Decision Authority:** `DEC-002`
- **Input Artifacts:**
  - `documents/versa/00_source/Versa_ERP_Platform_Strategy_Tiruppur.docx`
- **Evidence Sources:**
  - `documents/versa/01_domain/versa_domain_model.json`

---

## 3. Constraints & Invariants
- Enforce strict identity, uniqueness, and relational integrity.
- Formalize canonical invariants: `multi_company_isolation`, `job_work_mass_balance`, `order_matrix_conservation`, `fail_closed_approval_governance`.

---

## 4. Requested Actions
1. Author canonical domain model specifications.
2. Build relational RDBMS schema projection.
3. Formulate data ownership rules.
4. Establish automated schema validator `validate_versa_domain_model.py`.

---

## 5. Expected & Resulting Outputs
- **Resulting Decisions:** `documents/versa/06_decisions/VERSA_DESIGN_TIME_SEMANTIC_ANALYSIS.md`
- **Resulting Contracts:** `documents/versa/01_domain/VERSA_DATA_OWNERSHIP.md`
- **Resulting Validation Artifacts:**
  - `documents/versa/01_domain/VERSA_DOMAIN_MODEL.md`
  - `documents/versa/01_domain/VERSA_RDBMS_MODEL.md`
  - `documents/versa/01_domain/versa_domain_model.json`
  - `documents/versa/05_validation/validate_versa_domain_model.py`

---

## 6. Change Impact Classification
- **Classification:** `SEMANTIC_CHANGE`
- **Rationale:** Established canonical domain baseline.
