# VERSA ERP — TEXTILE REPOSITORY ARCHAEOLOGY & SEMANTIC GAP ANALYSIS REPORT

## 1. Executive Summary & Purpose

Before proceeding with runtime implementation across Phase 4 (`versa_quality`) and subsequent textile verticals (Phase 5 Matrix & Production, Phase 6 Job Work, Phase 7 Export), a comprehensive **Textile Repository Archaeology and Semantic Gap Analysis** was conducted across open-source implementations, community research discussions, and regional Tamil Nadu (Tiruppur, Erode, Salem) textile manufacturing systems.

### Strict Governance Boundary:
- **Research & Semantic Analysis Only:** Zero runtime code or semantic contracts were modified during this phase.
- **Clean-Room Boundary:** External repositories serve solely as evidence sources. No external code, packages, or forks are imported into Versa.
- **Authority Preservation:** ERPNext retains absolute authority over the Stock Ledger and General Ledger.

---

## 2. Executive Synthesis

### A. What already exists?
- **Apparelo (Aerele Technologies):** A legacy open-source Frappe application developed in Tiruppur that pioneered the Order Matrix concept and Style master in earlier Frappe versions (v11/v12). Now deprecated/archived, but confirms the exact industrial need for multi-dimensional size/colour order entry.
- **ParaLogic Textile:** A specialized digital fabric printing and roll-tracking workspace. However, it requires a hard fork of Frappe/ERPNext, creating an unacceptable dependency and upgrade hazard.
- **Fabric ERP (KAK Textile):** A full-stack Spring Boot / React ERP demonstrating complete vertical integration across yarn procurement, warping, weaving, dyeing, stentering, 4-point QC, roll packing, and GST wholesale dispatch in Tamil Nadu mills.
- **Scan ERP / Awesome Garment Toolkit:** Open-source Python/Node toolkits providing standard algorithms for SMV calculation, ISO 2859-1 AQL sampling tables, and QR-based bundle tracking.

### B. What can Versa learn?
1. **Apparel Matrix is non-negotiable:** Representing every size $\times$ colour combination as a discrete Item master and BOM causes system failure at scale. The aggregate Style + Order Matrix model is the industry-proven solution.
2. **Strict mass-balance is essential in Job Work:** Process loss in dyeing, bleaching, and knitting must be actively reconciled with dynamic tolerance limits, with automatic excess loss financial debit integration.
3. **Dual-UOM is fundamentally physical:** Conversions between Weight (kg) and Length (meters) must be anchored in verified roll-level GSM and width measurements, rather than static multiplication constants.
4. **Never fork Frappe/ERPNext:** Monolithic forks (like ParaLogic) create technical debt that prevents adopting upstream security updates, multi-tenancy enhancements, and official ecosystem extensions.

### C. What does ERPNext already provide?
- Rock-solid General Ledger and Double-Entry Accounting.
- Authoritative Stock Ledger with FIFO/Moving Average valuation.
- Standard Procurement and Sales pipelines (`Purchase Order`, `Purchase Receipt`, `Sales Order`, `Delivery Note`, `Sales Invoice`).
- Robust Role-Based Access Control (RBAC), DocType metadata extensibility, event hooks, and multi-currency transactions.

### D. Where is ERPNext insufficient?
- **High-SKU Variant Proliferation (Issue #41950):** Native Item Variants create explosive document bloat for apparel.
- **Single-Stage Rigid Subcontracting:** Standard ERPNext subcontracting assumes a simple single-stage PO $\to$ GRN flow and lacks native multi-stage process routing without creating phantom intermediate Item codes.
- **Absence of Dual-UOM Mass Conservation:** Standard ERPNext handles UOM conversion factors as linear constants, ignoring non-linear wet processing shrinkage and GSM variations.
- **Lack of Physical Roll Barcode Overlay:** Standard ERPNext stops at the Batch level and does not track individual continuous fabric rolls with gross/net weight and 4-point defect grading.

### E. What is unique about Versa?
- **Fail-Closed Multi-Company Governance:** Cryptographically secure tenant isolation combined with fail-closed multi-company transaction scoping (`1 = 0` if unassigned).
- **Physical Fabric Roll Overlay without Ledger Duplication:** Roll-level traceability, weight-length dual-UOM validation, and ASTM D5430 4-point defect scoring directly on top of standard ERPNext stock batches.
- **Automated Job Work Mass-Balance & Financial Settlement:** Invariant-enforced mass conservation with automated calculation of excess loss debits on vendor processing bills.
- **Integrated Order Matrix without Item Proliferation:** A unified Style sheet and matrix child table that handles sizing and colourways without polluting the database with 50+ phantom items.

### F. What should NOT be built?
- Do **not** build a duplicate inventory ledger or custom stock valuation engine.
- Do **not** build a duplicate general ledger or accounting transaction store.
- Do **not** build an in-app CAD drawing/pattern software (weave design belongs in external CAD tools).
- Do **not** build a generic Laboratory Information Management System (LIMS).

### G. What should be deferred?
- **Shop-Floor Intelligence & SCADA IoT:** Real-time machine vibration telemetry, boiler steam SCADA monitoring, and Time-of-Day (ToD) tariff optimization (modeled in SME-EnergyIQ) are deferred to future post-ERP phases.
- **Advanced Digital Print Repeat Calculator:** Specialized repeat nesting algorithms deferred to future extensions.

---

## 3. Critical Final Comparison Matrix

| Capability | ERPNext Native | Existing Open Source | Tiruppur / Erode Evidence | Versa Canonical Model | Versa Gap Status | Final Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Multi-Stage Job Work** | Partial (requires separate PO per stage) | Fabric ERP (stage transitions) | Multi-vendor outsourced wet processing | `Versa Job Work Order` (ENT-023) | **PARTIAL_MATCH** | Enhance with sequential chaining in Phase 6. |
| **Delivery Challan** | Delivery Note / India Compliance | Standard Section 143 Challan | Mandatory GST transport document | ERPNext `Delivery Note` + Versa extension | **MATCH** | Use native ERPNext / India Compliance for GST. |
| **Yield & Process Loss** | Static BOM scrap % | Dynamic loss % in Fabric ERP | 3–5% Knitting/Dyeing loss tolerance | Invariant `job_work_mass_balance` | **MATCH** | Enforce fail-closed mass balance in Phase 6. |
| **Dual-UOM (kg vs m)** | Fixed conversion factor | Formula calculation in Fabric ERP | Non-linear GSM/width weight-length relation | `Versa Fabric Roll` (ENT-018) | **MATCH** | Maintain Python dual-UOM validator ($\pm 5\%$). |
| **Fabric GSM Validation** | None | Manual QC recording | Target GSM $\pm 3.0\%$ tolerance | `Versa Fabric Spec` (ENT-017) | **MATCH** | Implemented in `versa_quality` evaluator. |
| **Roll Tracking** | Batch only (no roll entity) | ParaLogic `Fabric Roll` (forked) | Individual roll barcode tags (18–24 kg) | `Versa Fabric Roll` (ENT-018) | **MATCH** | Maintain physical overlay without ledger fork. |
| **Order Matrix** | Flat line items (Issue #41950) | Apparelo Matrix Popover | Matrix ordering by Size $\times$ Colour | `Versa Order Matrix` (ENT-030) | **MATCH** | Implement UI grid popover in Phase 5. |
| **Apparel Variants** | 1 Item per variant (Bloat) | Style Master + Variant Child | Single Tech Pack per Style | `Versa Style` (ENT-019) | **MATCH** | Avoid phantom Item variant generation. |
| **Wet Processing** | Generic Work Order | Fabric ERP / ParaLogic recipes | Softflow dyeing, Stenter, Compactor | `Versa Job Work Order` (`process`) | **PARTIAL_MATCH** | Add chemical recipe child table in Phase 6. |
| **Quality & 4-Point Lab** | Inspection Criteria (Pass/Fail) | ASTM D5430 formula in Fabric ERP | 4-point defect scoring & AQL tables | `Versa QC Result` (ENT-024) | **MATCH** | Implemented in `versa_quality`. |
| **Carton Ratio Packing** | Basic packing list | Scan ERP Ratio packing | Solid / Ratio packing with barcode scans | `Versa Packing Plan` (ENT-025) | **MATCH** | Implement in `versa_export` (Phase 7). |
| **Export Documentation** | Delivery Note & Sales Invoice | Fabric ERP Export Contracts | Commercial Invoice, Packing List, Ports | `Versa Packing Plan` + ERPNext Invoice | **MATCH** | Leverage ERPNext transaction root with Versa overlay. |
| **B2B Integration** | Standard APIs | Custom client portals | Customer portal for approval & dispatch | Standard Frappe REST API / Portal | **MATCH** | Utilize native Frappe web portal endpoints. |
| **Shop-Floor Intelligence**| None | SME-EnergyIQ (MILP / IoT) | Energy ToD tariffs, stenter temperature | Explicitly deferred to Future Phase | **NOT_RELEVANT** (Future) | Retain in research archive; do not include in MVP. |

---

## 4. No Implementation Gate Verification

In strict accordance with the project directives:
- **Zero runtime code changes were made.**
- **Zero DocTypes were modified or created.**
- **Zero external packages or dependencies were imported.**
- **Zero canonical invariants or domain contracts were altered.**

---

## 5. Final Classification

```text
============================================================
TEXTILE REPOSITORY ARCHAEOLOGY COMPLETE
============================================================

No runtime implementation changes made.
No semantic contracts modified.
No external code imported.

Ready for Versa Semantic Reconciliation Review.
============================================================
```
