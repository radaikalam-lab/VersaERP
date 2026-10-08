# Prompt ID: P03.6-001

## Metadata
- **Phase:** Phase 3.6 — Docker Canonical Runtime
- **Date:** 2026-10-07
- **Title:** Establishment of Canonical Containerized Multi-Tenant Stack
- **Status:** COMPLETED
- **Provenance Classification:** RECONSTRUCTED

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P03.5-001`
- **Supersedes:** None
- **Related Prompt(s):** `P03.6-002`

---

## 2. Intent & Scoping
- **Purpose:** Establish Docker as the canonical VersaERP runtime and deployment environment with MariaDB 10.6, Redis Cache, Redis Queue, and Frappe backend.
- **Semantic Authority:** `documents/versa/03_architecture/VERSA_DOCKER_RUNTIME_ARCHITECTURE.md`
- **Decision Authority:** `DEC-009`

---

## 3. Constraints & Invariants
- Docker containerization is canonical; Windows-native environment is reference only.
- Strict healthchecks on all services.

---

## 4. Requested Actions
1. Author `deployment/docker/Dockerfile` and `docker-compose.yml`.
2. Build canonical runner `run_docker_tests.py`.
3. Validate container health and site bootstrap.

---

## 5. Expected & Resulting Outputs
- **Resulting Decisions:** `documents/versa/03_architecture/VERSA_DOCKER_RUNTIME_ARCHITECTURE.md`
- **Resulting Implementation:** `deployment/docker/`
- **Resulting Tests:** `deployment/docker/scripts/run_docker_tests.py` (37/37 PASS)
- **Resulting Validation Artifacts:** `documents/versa/05_validation/VERSA_PHASE_3_6_DOCKER_RUNTIME_REPORT.md`

---

## 6. Change Impact Classification
- **Classification:** `ARCHITECTURAL_CHANGE`
- **Rationale:** Standardized canonical deployment stack.
