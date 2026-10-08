# Prompt ID: P03.6-002

## Metadata
- **Phase:** Phase 3.6 Hardening & Closure
- **Date:** 2026-10-08
- **Title:** Docker MariaDB 10.6 LTS Realignment & Pre-Phase 4 Gate Hardening
- **Status:** COMPLETED
- **Provenance Classification:** RECONSTRUCTED

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P03.6-001`
- **Supersedes:** None
- **Related Prompt(s):** `P04-001`

---

## 2. Intent & Scoping
- **Purpose:** Audit and harden Docker stack against unvalidated MariaDB versions; align with MariaDB 10.6 LTS for Frappe v15 compliance; verify restart persistence and tenant isolation.
- **Semantic Authority:** `documents/versa/03_architecture/VERSA_DOCKER_RUNTIME_ARCHITECTURE.md`
- **Decision Authority:** `DEC-010`

---

## 3. Constraints & Invariants
- Enforce strict database compatibility with Frappe v15 engine.
- Preserve 35 / 35 artifact manifest verification.

---

## 4. Requested Actions
1. Realign MariaDB container image to `mariadb:10.6`.
2. Execute full regression suite inside Docker container (37 / 37 pass).
3. Validate persistence across container restarts.

---

## 5. Expected & Resulting Outputs
- **Resulting Decisions:** `documents/versa/03_architecture/VERSA_DOCKER_RUNTIME_ARCHITECTURE.md`
- **Resulting Implementation:** `deployment/docker/`
- **Resulting Tests:** `deployment/docker/scripts/run_docker_tests.py` (37/37 PASS)
- **Resulting Validation Artifacts:** `documents/versa/05_validation/VERSA_PHASE_3_6_DOCKER_RUNTIME_REPORT.md`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY`
- **Rationale:** Container environment hardening.
