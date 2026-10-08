# VERSA ERP — ARTIFACT MIGRATION & PROVENANCE REPORT

## 1. Executive Summary

This report documents the physical migration of all 26 canonical Versa artifacts from their initial design-time extraction locations under `E:\GraphModel` to the authoritative repository under `E:\VersaERP\documents\versa`.

---

## 2. Before vs After Migration Audit

| Artifact | Original Location (`E:\GraphModel`) | Authoritative Location (`E:\VersaERP\documents\versa`) | Status | SHA-256 Hash |
| :--- | :--- | :--- | :--- | :--- |
| `Versa_ERP_Platform_Strategy_Tiruppur.docx` | `.../Versa_ERP_Platform_Strategy_Tiruppur.docx` | `00_source/Versa_ERP_Platform_Strategy_Tiruppur.docx` | `AUTHORITATIVE` | `6f6217df9f0f0134...` |
| `VERSA_DOMAIN_MODEL.md` | `.../VERSA_DOMAIN_MODEL.md` | `01_domain/VERSA_DOMAIN_MODEL.md` | `AUTHORITATIVE` | `0f482f737965f7ca...` |
| `VERSA_RDBMS_MODEL.md` | `.../VERSA_RDBMS_MODEL.md` | `01_domain/VERSA_RDBMS_MODEL.md` | `AUTHORITATIVE` | `532d48f5a678fec9...` |
| `VERSA_DATA_OWNERSHIP.md` | `.../VERSA_DATA_OWNERSHIP.md` | `01_domain/VERSA_DATA_OWNERSHIP.md` | `AUTHORITATIVE` | `82121c2d99e27aff...` |
| `versa_domain_model.json` | `.../versa_domain_model.json` | `01_domain/versa_domain_model.json` | `AUTHORITATIVE` | `96dfa1c3e229fcdd...` |
| `VERSA_P2P_CONTRACT.md` | `.../VERSA_P2P_CONTRACT.md` | `02_contracts/VERSA_P2P_CONTRACT.md` | `AUTHORITATIVE` | `0738a896d37b7668...` |
| `VERSA_O2C_CONTRACT.md` | `.../VERSA_O2C_CONTRACT.md` | `02_contracts/VERSA_O2C_CONTRACT.md` | `AUTHORITATIVE` | `cc8dc1d3208bb178...` |
| `VERSA_JOBWORK_CONTRACT.md` | `.../VERSA_JOBWORK_CONTRACT.md` | `02_contracts/VERSA_JOBWORK_CONTRACT.md` | `AUTHORITATIVE` | `f672c9a50b730d49...` |
| `VERSA_QUALITY_CONTRACT.md` | `.../VERSA_QUALITY_CONTRACT.md` | `02_contracts/VERSA_QUALITY_CONTRACT.md` | `AUTHORITATIVE` | `6eaef3fdadf62500...` |
| `VERSA_MODEL_RECONCILIATION.md` | `.../VERSA_MODEL_RECONCILIATION.md` | `03_architecture/VERSA_MODEL_RECONCILIATION.md` | `AUTHORITATIVE` | `cc8b66927628b214...` |
| `VERSA_FINAL_CANONICAL_AUDIT.md` | `.../VERSA_FINAL_CANONICAL_AUDIT.md` | `03_architecture/VERSA_FINAL_CANONICAL_AUDIT.md` | `AUTHORITATIVE` | `44a11d52bff0f0e3...` |
| `VERSA_IMPLEMENTATION_GATE.md` | `.../VERSA_IMPLEMENTATION_GATE.md` | `03_architecture/VERSA_IMPLEMENTATION_GATE.md` | `AUTHORITATIVE` | `dc26685b40d453b9...` |
| `VERSA_APP_BOUNDARY_ANALYSIS.md` | `.../VERSA_APP_BOUNDARY_ANALYSIS.md` | `03_architecture/VERSA_APP_BOUNDARY_ANALYSIS.md` | `AUTHORITATIVE` | `a774e5bb9014f137...` |
| `VERSA_PHASE_2_1_ARCHITECTURE_CHALLENGE.md` | `.../VERSA_PHASE_2_1_ARCHITECTURE_CHALLENGE.md` | `03_architecture/VERSA_PHASE_2_1_ARCHITECTURE_CHALLENGE.md` | `AUTHORITATIVE` | `e04b7096714f5c9e...` |
| `VERSA_PHASE_2_IMPLEMENTATION_SPEC_REPORT.md` | `.../VERSA_PHASE_2_IMPLEMENTATION_SPEC_REPORT.md` | `03_architecture/VERSA_PHASE_2_IMPLEMENTATION_SPEC_REPORT.md` | `AUTHORITATIVE` | `e30d7b3f4d8eaed2...` |
| `VERSA_IMPLEMENTATION_SCOPE_REVIEW.md` | `.../VERSA_IMPLEMENTATION_SCOPE_REVIEW.md` | `03_architecture/VERSA_IMPLEMENTATION_SCOPE_REVIEW.md` | `AUTHORITATIVE` | `91b9efe0a1d0e09e...` |
| `VERSA_FRAPPE_MODEL.md` | `.../VERSA_FRAPPE_MODEL.md` | `04_implementation_spec/VERSA_FRAPPE_MODEL.md` | `AUTHORITATIVE` | `644ed7bdffcecb9e...` |
| `VERSA_FRAPPE_IMPLEMENTATION_SPECIFICATION.md` | `.../VERSA_FRAPPE_IMPLEMENTATION_SPECIFICATION.md` | `04_implementation_spec/VERSA_FRAPPE_IMPLEMENTATION_SPECIFICATION.md` | `AUTHORITATIVE` | `05971d7f906a538d...` |
| `VERSA_FRAPPE_IMPLEMENTATION_TRACEABILITY.md` | `.../VERSA_FRAPPE_IMPLEMENTATION_TRACEABILITY.md` | `04_implementation_spec/VERSA_FRAPPE_IMPLEMENTATION_TRACEABILITY.md` | `AUTHORITATIVE` | `09c0933c3e2c0e0c...` |
| `validate_versa_domain_model.py` | `.../validate_versa_domain_model.py` | `05_validation/validate_versa_domain_model.py` | `AUTHORITATIVE` | `d244fc400d9f21b7...` |
| `validate_frappe_specification.py` | `.../validate_frappe_specification.py` | `05_validation/validate_frappe_specification.py` | `AUTHORITATIVE` | `65a62501f5dde898...` |
| `validate_phase_2_1_architecture.py` | `.../validate_phase_2_1_architecture.py` | `05_validation/validate_phase_2_1_architecture.py` | `AUTHORITATIVE` | `6973af17d1ad8fb4...` |
| `validate_versa_artifacts.py` | `.../validate_versa_artifacts.py` | `05_validation/validate_versa_artifacts.py` | `AUTHORITATIVE` | `feb137c294bc828d...` |
| `VERSA_FRAPPE_IMPLEMENTATION_DECISIONS.md` | `.../VERSA_FRAPPE_IMPLEMENTATION_DECISIONS.md` | `06_decisions/VERSA_FRAPPE_IMPLEMENTATION_DECISIONS.md` | `AUTHORITATIVE` | `acb24004e2cf09f8...` |
| `VERSA_PHASE_2_1_DECISIONS.md` | `.../VERSA_PHASE_2_1_DECISIONS.md` | `06_decisions/VERSA_PHASE_2_1_DECISIONS.md` | `AUTHORITATIVE` | `17a4c68fa38a714e...` |
| `VERSA_OPEN_QUESTIONS.md` | `.../VERSA_OPEN_QUESTIONS.md` | `07_open_questions/VERSA_OPEN_QUESTIONS.md` | `AUTHORITATIVE` | `d6da0c98b0439860...` |
| `VERSA_ASSUMPTION_REGISTER.md` | `.../VERSA_ASSUMPTION_REGISTER.md` | `07_open_questions/VERSA_ASSUMPTION_REGISTER.md` | `AUTHORITATIVE` | `897f035a1a8cbc09...` |

---

## 3. Verification & Integrity

- **Total Artifacts Migrated:** 26 baseline files + Manifest + Governance Policies
- **Hash Matching:** 100% Cryptographic Match against source files
- **GraphModel Cleanliness:** Verified zero runtime code inside `E:\GraphModel`
- **Status:** `MIGRATION COMPLETE — REPOSITORY AUTHORITATIVE`