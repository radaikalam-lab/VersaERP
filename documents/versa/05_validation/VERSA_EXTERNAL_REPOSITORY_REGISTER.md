# VERSA ERP — EXTERNAL TEXTILE REPOSITORY REGISTER

## 1. Executive Summary & Governance Standard

This register documents the external open-source repositories, community research artifacts, and software projects inspected during the **Phase 4 Pre-Implementation Textile Repository Archaeology & Semantic Gap Analysis**.

### Strict Architectural Boundaries:
- **Evidence Sources Only:** External repositories serve solely as domain evidence and reference points.
- **Zero Runtime Dependencies:** No external repositories, packages, forks, or copy-pasted code are imported into the VersaERP runtime.
- **License Hygiene:** Every repository is classified with respect to copyright, license terms, and reuse risk.

---

## 2. External Repository Inventory

| Ref ID | Project / Repository Name | Owner / Maintainer | Repository URL | Primary Tech Stack | License | Activity / Status | Geographic Relevance | Industry Relevance | Frappe / ERPNext Relevance | Reuse Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `EXT-REP-001` | **Apparelo** | Aerele Technologies | `https://github.com/aerele/apparelo` | Python, Frappe Framework, JS | MIT License | Deprecated / Archived (Frappe v11/v12) | **DIRECT** (Tiruppur, TN) | Garment Manufacturing, CMT | Direct Frappe App | **DOMAIN PATTERN WORTH EXTRACTING** |
| `EXT-REP-002` | **ParaLogic Textile** | ParaLogic Technologies | `https://github.com/ParaLogicTech/textile` | Python, Frappe Fork, JS | GPL-3.0 / Proprietary Fork | Active / Pre-release | **INDIRECT** (India / Surat / Global) | Digital Fabric Printing, Pre-treatment | Forked Frappe/ERPNext | **REFERENCE ONLY** (Fork Dependency Hazard) |
| `EXT-REP-003` | **Fabric ERP (KAK Textile)** | Muniyasamy | `https://github.com/Muniyasamy107/fabric-erp` | Spring Boot 3.3 (Java 17), React 19, MySQL 8 | License Unspecified (Open Repo) | Active (2025–2026) | **DIRECT** (Tamil Nadu Weaving/Dyeing) | Weaving, Sizing, Dyeing, Stenter, ETP | Standalone ERP Stack | **DOMAIN PATTERN WORTH EXTRACTING** |
| `EXT-REP-004` | **ERPNext Manufacturing Variants (Issue #41950)** | Frappe Technologies | `https://github.com/frappe/erpnext/issues/41950` | Python, Frappe Framework | GPL-3.0 (ERPNext Core) | Active Feature Discussion (2024–2026) | **GENERAL** (Apparel / Footwear Industry) | High-SKU Variant BOM Proliferation | Upstream Core ERPNext Issue | **DOMAIN PATTERN WORTH EXTRACTING** |
| `EXT-REP-005` | **ERPNext Subcontracting & India Compliance** | Frappe / Resilient Tech | `https://github.com/resilient-tech/india-compliance` | Python, Frappe Framework | GPL-3.0 | Active Production Release | **INDIRECT** (All-India GST / Job Work) | Subcontracting Challan, ITC-04, e-Way | Direct Frappe Extension App | **REFERENCE ONLY** (Compliance Overlay) |
| `EXT-REP-006` | **Textile ERP Next.js** | Imran Ahmed (imranbru99) | `https://github.com/imranbru99/textile-erp-nextjs` | Next.js 16, TypeScript, Prisma, MySQL | MIT License | Active (2025–2026) | **GENERAL** (South Asia Textile Mills) | Spinning, Weaving, QC, B2B Dispatch | Standalone Web App | **REFERENCE ONLY** |
| `EXT-REP-007` | **Awesome Garment ERP / Scan ERP** | Santosh Rijal (drmcoder) | `https://github.com/drmcoder/awesome-garment-erp` | Markdown Index, Node.js / Python Utilities | MIT License | Active (2024–2026) | **INDIRECT** (South Asian Garment CMT) | SMV, AQL Tables, QR Bundle Tracking | Toolkit & Ecosystem Index | **REFERENCE ONLY** |
| `EXT-REP-008` | **SME-EnergyIQ** | Pranavi Srikala | `https://github.com/Pranavisrikala/SME-EnergyIQ` | Python, Streamlit, PuLP (MILP), Scikit-Learn | MIT License | Active Hackathon Project (2026) | **DIRECT** (Tirupur / Coimbatore / Surat) | Textile Mill Energy Telemetry, ToD Tariff | Standalone Python / IoT Sandbox | **REFERENCE ONLY** (Future Intelligence Baseline) |
| `EXT-REP-009` | **Jacquard Designer** | Sujay | `https://github.com/sujay1816/jacquard-designer` | JavaScript, HTML5 Canvas | MIT License | Active | **INDIRECT** (Surat / Handloom & Powerloom) | Weave Patterns, 1-bit BMP Loom Drive | Standalone CAD Utility | **REFERENCE ONLY** (Future Design Integration) |

---

## 3. Geographic Relevance Definitions

- **DIRECT:** Specifically designed for or deployed within the Tamil Nadu textile cluster (Tiruppur, Erode, Salem, Coimbatore, Karur). Reflects exact local operational practices (e.g. stage-wise Job Work challans, dual-UOM kg/meters mass conservation, yarn count Ne systems, stenter loss tolerances).
- **INDIRECT:** Addresses Indian apparel/textile manufacturing workflows (GST, e-Way bills, Job Work ITC-04, CMT contracting) but without exclusive Tamil Nadu cluster specialization.
- **GENERAL:** International or generic textile/apparel manufacturing systems without Indian regulatory or cluster-specific mechanics.

---

## 4. Reuse & Licensing Classifications

1. **DO NOT REUSE:** Repositories with proprietary, conflicting, or contaminated copyleft licenses that cannot be safely combined with Versa's modular architecture, or repositories that introduce dangerous monolithic platform forks (e.g., ParaLogic's hard Frappe/ERPNext fork).
2. **REFERENCE ONLY:** Repositories providing valuable domain taxonomy, workflow patterns, or mathematical formulas (e.g. ASTM D5430, AQL ISO 2859-1, SMV calculation) which inform Versa design but require zero code borrowing.
3. **DOMAIN PATTERN WORTH EXTRACTING:** Repositories demonstrating mature business conceptual models (e.g. Apparelo's Order Matrix concept, Fabric ERP's multi-stage weaving/stenter routing, Issue #41950's matrix-level BOM solution) that should be modeled natively inside Versa DocTypes.
4. **POTENTIAL CODE REUSE — REQUIRES LICENSE REVIEW:** Non-existent in Phase 4. All Versa code is written clean-room against canonical contracts.
