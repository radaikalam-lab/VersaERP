# Prompt ID: P04-001

## Metadata
- **Phase:** Phase 4A — Textile Repository Archaeology
- **Date:** 2026-10-08
- **Title:** Open-Source Textile Repository Archaeology & Domain Evidence Extraction
- **Status:** COMPLETED
- **Provenance Classification:** ORIGINAL

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P03.6-002`
- **Supersedes:** None
- **Related Prompt(s):** `P04-002`

---

## 2. Intent & Scoping
- **Purpose:** Perform comprehensive research across 9 priority open-source textile repositories (Apparelo, ParaLogic Textile, Fabric ERP, ERPNext #41950, SME-EnergyIQ, Jacquard Designer, etc.) to discover domain knowledge relevant to Tiruppur, Erode, Salem textile processing.
- **Semantic Authority:** `documents/versa/05_validation/VERSA_TEXTILE_REPOSITORY_ARCHAEOLOGY_REPORT.md`
- **Decision Authority:** External Evidence Only
- **Input Artifacts:**
  - `documents/versa/01_domain/VERSA_DOMAIN_MODEL.md`
  - `documents/versa/02_contracts/VERSA_QUALITY_CONTRACT.md`
- **Evidence Sources:**
  - `https://github.com/aerele/apparelo`
  - `https://github.com/ParaLogicTech/textile`
  - `https://github.com/Muniyasamy107/fabric-erp`
  - `https://github.com/frappe/erpnext/issues/41950`
  - `https://github.com/imranbru99/textile-erp-nextjs`
  - `https://github.com/drmcoder/awesome-garment-erp`
  - `https://github.com/Pranavisrikala/SME-EnergyIQ`
  - `https://github.com/sujay1816/jacquard-designer`

---

## 3. Constraints & Invariants
- **CRITICAL RULE:** RESEARCH AND EVIDENCE EXTRACTION ONLY. Zero runtime code modifications, zero DocType additions, zero external package imports. External repositories are evidence only.

---

## 4. Requested Actions
1. Inspect 9 priority open-source textile repositories and regional domain workflows.
2. Build domain evidence matrix.
3. Conduct deep-dives into Job Work, Apparel Matrix, Multi-UOM, Wet Processing, and Export.
4. Author 8 authoritative research documents.

---

## 5. Expected & Resulting Outputs
- **Resulting Validation Artifacts:**
  - `documents/versa/05_validation/VERSA_TEXTILE_REPOSITORY_ARCHAEOLOGY_REPORT.md`
  - `documents/versa/05_validation/VERSA_TEXTILE_DOMAIN_EVIDENCE_MATRIX.md`
  - `documents/versa/05_validation/VERSA_JOB_WORK_SEMANTIC_GAP_ANALYSIS.md`
  - `documents/versa/05_validation/VERSA_APPAREL_MATRIX_SEMANTIC_GAP_ANALYSIS.md`
  - `documents/versa/05_validation/VERSA_TEXTILE_MEASUREMENT_EVIDENCE.md`
  - `documents/versa/05_validation/VERSA_WET_PROCESSING_EVIDENCE.md`
  - `documents/versa/05_validation/VERSA_EXPORT_DOMAIN_EVIDENCE.md`
  - `documents/versa/05_validation/VERSA_EXTERNAL_REPOSITORY_REGISTER.md`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY` (Research Only)
- **Rationale:** Design-time evidence collection with zero runtime impact.
