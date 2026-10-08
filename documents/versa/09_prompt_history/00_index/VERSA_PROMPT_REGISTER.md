# VERSA ERP PROMPT REGISTER

**Document Path:** `documents/versa/09_prompt_history/00_index/VERSA_PROMPT_REGISTER.md`  
**System Status:** Authoritative Prompt Catalog  
**Classification Standard:** `ORIGINAL`, `RECONSTRUCTED`, `REFERENCED`, `DERIVED`  

---

## Master Prompt Register

| Prompt ID | Phase | Classification | Purpose | Primary Artifact | Decision | Contract Impact | Implementation Impact | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`P00-001`** | Phase 0 | `RECONSTRUCTED` | Initial platform strategy & Tiruppur textile requirements | `00_source/Versa_ERP_Platform_Strategy_Tiruppur.docx` | `DEC-001` | Initial Baseline Scoping | Strategy Formation | `COMPLETED` |
| **`P01-001`** | Phase 1 | `RECONSTRUCTED` | Canonical 39 entities, 28 relationships, and invariants | `01_domain/VERSA_DOMAIN_MODEL.md` | `DEC-002` | Canonical Model Extraction | Schema Models & JSON | `COMPLETED` |
| **`P02-001`** | Phase 2 | `RECONSTRUCTED` | Frappe implementation specification & schema mapping | `04_implementation_spec/VERSA_FRAPPE_MODEL.md` | `DEC-003` | None (Frappe Projection) | DocType Spec Schemas | `COMPLETED` |
| **`P02-002`** | Phase 2.1 | `RECONSTRUCTED` | Adversarial challenge of multi-company & approval boundaries | `03_architecture/VERSA_PHASE_2_1_ARCHITECTURE_CHALLENGE.md` | `DEC-004` | None (Hardened Invariants) | Fail-closed Security Logic | `COMPLETED` |
| **`P02-003`** | Phase 2.2 | `RECONSTRUCTED` | Artifact manifest & SHA-256 workspace governance | `ARTIFACT_MANIFEST.md` | `DEC-005` | Boundary Governance | Validation Scripts | `COMPLETED` |
| **`P03-001`** | Phase 3 | `RECONSTRUCTED` | Bootstrap `versa_core` application & approval rules | `bench/apps/versa_core/` | `DEC-006` | None | Core DocTypes & Hooks | `COMPLETED` |
| **`P03-002`** | Phase 3 | `RECONSTRUCTED` | Strict hardening gate, fail-closed isolation, OTIF deferral | `05_validation/VERSA_PHASE_3_HARDENING_REPORT.md` | `DEC-007` | None | Hardened Permissions & Analytics | `COMPLETED` |
| **`P03.5-001`** | Phase 3.5 | `RECONSTRUCTED` | Real Frappe/ERPNext v15 runtime bench bootstrap | `05_validation/VERSA_PHASE_3_5_FRAPPE_RUNTIME_REPORT.md` | `DEC-008` | None | Site Bootstrap & DB Binding | `COMPLETED` |
| **`P03.6-001`** | Phase 3.6 | `RECONSTRUCTED` | Canonical Docker runtime containerization | `03_architecture/VERSA_DOCKER_RUNTIME_ARCHITECTURE.md` | `DEC-009` | None | Docker Compose & Stack | `COMPLETED` |
| **`P03.6-002`** | Phase 3.6 | `RECONSTRUCTED` | Docker MariaDB 10.6 LTS alignment & persistence hardening | `05_validation/VERSA_PHASE_3_6_DOCKER_RUNTIME_REPORT.md` | `DEC-010` | None | MariaDB 10.6 & Test Runner | `COMPLETED` |
| **`P04-001`** | Phase 4A | `ORIGINAL` | Textile repository archaeology across 9 open-source projects | `05_validation/VERSA_TEXTILE_REPOSITORY_ARCHAEOLOGY_REPORT.md` | None | Evidence Collection Only | Research & Archeology Docs | `COMPLETED` |
| **`P04-002`** | Phase 4B | `ORIGINAL` | Semantic reconciliation & overclaim elimination | `05_validation/VERSA_TEXTILE_SEMANTIC_RECONCILIATION_REPORT.md` | None | Classification Only | Epistemic Recalibration | `COMPLETED` |
| **`P04-003`** | Phase 4C | `ORIGINAL` | Quality contract-to-code traceability review | `05_validation/VERSA_QUALITY_IMPLEMENTATION_REVIEW.md` | None | None (100% Conformance) | Traceability Matrix | `COMPLETED` |
| **`P04-004`** | Phase 4D | `ORIGINAL` | Quality document lifecycle & Docker integration validation | `05_validation/VERSA_QUALITY_INTEGRATION_VALIDATION_REPORT.md` | None | None | Hardened gates.py & tests | `COMPLETED` |
| **`P04-005`** | Phase 4E | `ORIGINAL` | Final evidence audit, ASTM D5430 provenance & Phase 4 closure | `06_decisions/VERSA_PHASE_4_CLOSURE_DECISION.md` | `DEC-011` | None | Phase 4 Formally Closed | `COMPLETED` |
| **`P05-001`** | Phase 5 | `RESERVED` | Textile processing & domain workflows initiation | `09_prompt_history/PHASE_05/README.md` | TBD | Phase 5 Scoping | Phase 5 Bootstrap | `PENDING` |
| **`P05-002`** | Phase 5 | `ORIGINAL` | Textile processing & fabric processing semantic model definition & gate | `09_prompt_history/PHASE_05/P05_002_TEXTILE_PROCESS_SEMANTIC_DEFINITION.md` | `DEC-012` | `CONTRACT-005` | None (Specification Gate Only) | `COMPLETED` |
| **`P05-003`** | Phase 5 | `ORIGINAL` | Adversarial textile contract review of CONTRACT-005 & decision candidates | `09_prompt_history/PHASE_05/P05_003_ADVERSARIAL_TEXTILE_CONTRACT_REVIEW.md` | `DEC-013` (Cand.) | `CONTRACT-005` (Clarifications) | None (Review Gate Only) | `COMPLETED` |

---

## Classification Summary

- **Total Material Prompts Cataloged:** 18
- **`ORIGINAL` Prompts:** 7 (`P04-001`, `P04-002`, `P04-003`, `P04-004`, `P04-005`, `P05-002`, `P05-003`)
- **`RECONSTRUCTED` Prompts:** 10 (`P00-001` through `P03.6-002`)
- **`REFERENCED` / `RESERVED` Prompts:** 1 (`P05-001`)
- **`DERIVED` Records:** 0


