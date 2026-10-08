# VERSA ERP DOMAIN ASSUMPTION & PROVENANCE REGISTER

## 1. Objective & Scope

This register documents all material assumptions, inferences, and technical defaults introduced during the domain extraction and semantic analysis of `Source/Versa_ERP_Platform_Strategy_Tiruppur.docx`. 

To prevent unverified technical assumptions from becoming rigid implementation constraints, each entry isolates the evidence, operational risk, required business decision, and current governance status.

---

## 2. Provenance Taxonomy Definition

- **`SOURCE`:** Explicitly stated or required by the source document (`Versa_ERP_Platform_Strategy_Tiruppur.docx`).
- **`INFERRED`:** Logically deduced from standard Tiruppur textile operations and ERPNext architectural conventions.
- **`ASSUMED`:** Introduced by engineering to make schemas and validation concrete; requires customer validation during Phase 0.
- **`DERIVED`:** Computationally derived from transactional or master data.
- **`OPEN`:** Architectural trade-off requiring executive or stakeholder decision.

---

## 3. Comprehensive Assumption Register

| ID | Assumption Description | Provenance & Evidence | Operational Risk | Decision Required | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ASM-001** | **Mass Balance Unaccounted Tolerance:** Default tolerance is assumed to be $\le 0.1\%$ of issued batch weight to accommodate weighing scale calibration variance. | `ASSUMED` — Inferred from physical scale tolerances in wet processing. | Setting too tight a tolerance causes false theft flags; too loose causes unmonitored shrinkage. | Confirm whether tolerance should be global ($0.1\%$) or configurable per process/material in `Versa Process Loss Tolerance Setting`. | **PROPOSED (CONFIGURABLE)** |
| **ASM-002** | **Fabric Stock Valuation UOM:** ERPNext inventory valuation is maintained strictly in Weight ($kg$), while Length ($m$) is tracked dynamically as a physical roll attribute. | `INFERRED` — Strategy doc Section 6.2 highlights dual tracking; ERPNext valuation is single-currency/UOM. | Valuation discrepancies if fabric stretch/shrinkage changes linear meter weight. | Confirm that commercial costing and stock ledger use $kg$, while cutting room lay-plans consume rolls by meters. | **VALIDATED DESIGN** |
| **ASM-003** | **Job Work Transaction Engine:** `Versa Job Work Order` orchestrates operations and posts standard ERPNext `Stock Entry` (Material Transfer) and `Purchase Invoice` (Service Charges), bypassing ERPNext's rigid Subcontracting Order. | `INFERRED` — Strategy doc Appendix A.5 models distinct Job Work tables with mass-balance reconciliation. | Parallel workflow if ERPNext standard subcontracting is simultaneously enabled. | Authorize `versa_jobwork` as the primary subcontracting engine for textile operations. | **ACCEPTED FOR PHASE 1** |
| **ASM-004** | **Yarn CSP Threshold (`csp_min`):** Assumed default threshold of $\ge 2800$ for combed cotton yarn count strength product. | `ASSUMED` — Standard industry spinning benchmark (SITRA). Not in source text. | Rejecting yarn lots that meet commercial requirements but fail hardcoded benchmark. | Make `csp_min` an optional baseline on `Versa Yarn Spec` overridden by buyer Tech Pack / QC Spec. | **PROPOSED (SPEC-DRIVEN)** |
| **ASM-005** | **Garment SAM Field (`target_sam_minutes`):** Style master includes Standard Allowed Minutes (SAM) for operation cost calculation. | `INFERRED` — Inferred from standard piece-rate costing in Tiruppur garmenting. | Discrepancy with industrial engineering (IE) time studies if treated as fixed. | Use as indicative costing reference; actual line efficiency tracked in production batch. | **ACCEPTED** |
| **ASM-006** | **Job Worker Daily Capacity (`daily_capacity_kg`):** Profile records rated machine capacity in $kg/\text{day}$. | `ASSUMED` — Introduced for load scheduling in Section 10. | Static capacity does not account for machine downtime or yarn count changes. | Clarify whether capacity is an indicative profile attribute or an active scheduling constraint. | **INFORMATIONAL (PHASE 1)** |
| **ASM-007** | **ASTM / ISO / AATCC Quality Standards:** Specific test methods (ASTM D3776 for GSM, ASTM D5430 for 4-point fabric grading, ISO 105 for fastness, AATCC 135 for shrinkage) are pre-populated. | `INFERRED` — Strategy doc Section 12 lists GSM, shrinkage, fastness, spirality; specific standard numbers are industry best-practice. | Buyer-specific testing methods (e.g. Marks & Spencer, Next, Decathlon proprietary methods) differing from defaults. | Pre-load standards as editable master records in `Versa QC Spec` rather than hardcoded rules. | **ACCEPTED (MASTER DATA)** |
| **ASM-008** | **Garment Final AQL Sampling Levels:** Final garment inspection assumes ANSI/ASQ Z1.4 (ISO 2859-1) Normal Single Sampling Level II with AQL 1.5/2.5. | `INFERRED` — Strategy doc Section 12 mentions "Sampling/AQL, critical/major/minor defects". | Incompatible sampling sizes for small-batch domestic retail orders. | Store AQL tables as configuration (`Versa AQL Sampling Table`) selectable per buyer. | **ACCEPTED (CONFIGURABLE)** |
| **ASM-009** | **Order Matrix Persistence Model:** `Versa Order Matrix` is stored as an embedded Child Table on `Sales Order`, synchronizing bidirectional quantities with `Sales Order Item` lines via `validate` hooks. | `INFERRED` — Strategy doc Section 9 & Appendix A.4. | Data desynchronization if client-side grid fails to sync with line items. | Enforce server-side authoritative sum validation on `before_save`. | **ACCEPTED DESIGN** |
| **ASM-010** | **Multi-Company Scoping:** Core masters (`Item`, `Versa Colour`, `Versa QC Spec`) can be shared globally across group companies, while transactional objects (`Versa Job Work Order`, `Versa Fabric Roll`, `Versa Style`) are strictly scoped by `Company`. | `INFERRED` — Strategy doc Appendix A.15. | Unintended cross-company visibility in multi-tenant conglomerate setups. | Add `is_global` check on shared taxonomies and mandatory `company` foreign key on transactions. | **ACCEPTED DESIGN** |
| **ASM-011** | **Composition Free-Text Representation:** Material composition is captured as structured text (e.g. "95% Cotton 5% Elastane") in Phase 1 rather than a normalized composition child table. | `ASSUMED` — Appendix A.3 defines `composition VARCHAR(255)`. | Cannot query dynamically by exact blend % without regex parsing. | Retain structured string for Phase 1; plan normalized blend table for Phase 4 advanced analytics if needed. | **ACCEPTED (PHASE 1)** |
| **ASM-012** | **Inter-Company Subcontracting Flow:** Job work performed between group companies is treated as an internal transfer via Cost Centers rather than generating GST tax invoices. | `INFERRED` — Strategy doc Section 14 (Business units). | GST e-invoicing compliance violations if legal entities differ. | Add `is_internal_subcontract` toggle; route to legal Inter-Company PO if separate GSTINs exist. | **PROPOSED (CONFIGURABLE)** |

---

## 4. Governance & Review Policy

1. All **`ASSUMED`** items must be explicitly confirmed with Versa stakeholders during Phase 0 customer discovery workshops.
2. No assumed field value may act as a hard-blocking transaction validator without a supervisor concession override path.

