# VERSA TEXTILE SEMANTIC RECONCILIATION REPORT

**Authoritative File Path:** `documents/versa/05_validation/VERSA_TEXTILE_SEMANTIC_RECONCILIATION_REPORT.md`  
**Classification Status:** `PHASE 4 — SEMANTIC RECONCILIATION COMPLETE — READY FOR IMPLEMENTATION REVIEW`  
**Phase:** 4.0 Semantic Reconciliation Gate  
**Execution Context:** Design-Time Semantic Analysis Laboratory & Architectural Governance  
**Constraint Enforcement:** Strict Read-Only Audit. Zero runtime code modifications, zero DocType schema edits, zero domain contract mutations.

---

## Executive Summary & Strict Architectural Pipeline

This document delivers the definitive **Semantic Reconciliation Pass** over the completed Textile Repository Archaeology. It establishes an unbending epistemic and architectural separation between external empirical observations, semantic domain abstractions, authoritative contracts, and runtime implementation.

```text
       External Evidence (Archaeology / Open-Source Corpus / Regional Data)
                                    │
                                    ▼
       Semantic Reconciliation (Classification, Boundary Setting, Overclaim Elimination)
                                    │
                                    ▼
       Versa Architecture Decision (Governed ADRs, Scope Boundary Enforcement)
                                    │
                                    ▼
       Contract Update (If explicitly required by formal consensus)
                                    │
                                    ▼
       Runtime Implementation (Tenant-safe, Company-safe, Fail-closed)
```

### Core Invariant of Semantic Reconciliation
> **No numerical threshold, field structure, workflow state, or software architecture observed in external repositories becomes a normative Versa requirement merely because it exists in open-source software or regional practice.**

---

## 1. Material External Evidence Classification Matrix

Every empirical observation extracted from external repositories is classified into exactly one of six strict semantic categories:

1. **`VERSA_CONFIRMED`**: Concept aligns with existing approved Versa domain models and contracts.
2. **`CANDIDATE_SEMANTIC`**: Concept represents a validated domain requirement requiring formal ADR review before potential inclusion.
3. **`EXTERNAL_OBSERVATION`**: Descriptive empirical practice; must remain data/configuration rather than hardcoded core schema.
4. **`VERSA_CONFLICT`**: Concept directly violates Versa architectural invariants or authority principles.
5. **`DEFERRED`**: Concept valid for advanced industry maturity, but deferred beyond Phase 4/5 core.
6. **`NOT_RELEVANT`**: Concept outside Versa operational boundaries or domain scope.

| Material Observation / Domain Parameter | Source Evidence | Observed Value / Mechanism | Semantic Classification | Reconciliation Rationale & Decision Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Yarn Count Tolerances** | Textile Standards / Apparelo | Nominal $\pm 1.5\%$ Count (Ne) | `EXTERNAL_OBSERVATION` | Industry guideline. Must remain configurable within `Versa QC Spec` parameter min/max tolerances; never hardcoded in core logic. |
| **Fabric GSM Tolerances** | ParaLogic / Tiruppur mills | Nominal $\pm 3.0\%$ to $\pm 5.0\%$ | `EXTERNAL_OBSERVATION` | Measured GSM varies by finish and moisture. Tolerances belong in buyer/order specifications, not fixed schema constraints. |
| **kg ↔ Meter Dual-UOM Ratio** | Textile App / ParaLogic | Linear fixed conversion factor | `VERSA_CONFLICT` | Fabric weight-to-length is physical and variable ($\text{GLM} = \frac{\text{GSM} \times \text{Width}}{1000}$). Fixed linear conversions corrupt stock valuation. Rejected in favor of primary UOM with auxiliary physical measurement. |
| **Roll Weight / Batch Allocation** | Fabric ERP / ParaLogic | Roll tracking via piece-goods | `VERSA_CONFIRMED` | Fully aligned with canonical `Versa Fabric Roll` entity and lot/barcode tracking. |
| **AQL Sampling Tables** | ISO 2859-1 / Apparelo | AQL 1.5/2.5/4.0 Normal Level II | `EXTERNAL_OBSERVATION` | Standard statistical inspection tables. Recommended as reference lookup data, not hardcoded workflow branching. |
| **Dyeing Liquor Ratio** | Wet Processing Mills / Fabric ERP | 1:5 to 1:8 liquor ratio | `EXTERNAL_OBSERVATION` | Recipe and chemical calculation parameter. Belongs to process parameter configuration in Job Work / Production Orders. |
| **Chemical Recipe (% OWF, g/L)** | Textile Dyes / Wet Processing | % On Weight of Fabric, g/L | `CANDIDATE_SEMANTIC` | Valid domain concept for wet processing BOM/Job Work. Candidate for Phase 6 textile formulation modeling; deferred from Phase 4. |
| **Job Work Allowed Process Loss %** | Tiruppur Job Work Contracts | 3.0% to 5.0% by process stage | `EXTERNAL_OBSERVATION` | Contractual threshold per supplier/process. Must be maintained as a field on `Versa Job Work Order`; never globally hardcoded. |
| **Job Work Excess Loss Financial Debit** | Fabric ERP / Regional practice | Automatic debit note on vendor invoice | `VERSA_CONFIRMED` | Aligns with `job_work_mass_balance` invariant: excess scrap above allowed loss generates financial liability on `Purchase Invoice`. |
| **Ratio Packing (SCSS, SCRS, ACRS)** | Garment Export / Apparelo | Solid/Assorted Color/Size Cartons | `VERSA_CONFIRMED` | Aligns with `Versa Packing List` and `Versa Carton` order matrix breakdown. |
| **Carton CBM & Container Stuffing** | Export Freight Standards | $\text{L} \times \text{W} \times \text{H} / 10^6 \times \text{Cartons}$ | `EXTERNAL_OBSERVATION` | Standard geometric volumetric calculation. Utility calculation on packing list; does not alter stock ledger. |
| **Shop-Floor IoT / Energy Telemetry** | SME-EnergyIQ | High-frequency IoT sensor telemetry | `DEFERRED` | Valuable for future Industry 4.0 monitoring, but strictly excluded from core transactional ERP execution. |
| **Jacquard CAD Weave Generation** | Jacquard Designer | Direct Loom CAD binary generation | `NOT_RELEVANT` | CAD pattern generation belongs in specialized engineering/design tools, not transactional ERP. |
| **Hard Forking ERPNext Subcontracting** | ParaLogic Textile | Modified core ERPNext doctypes | `VERSA_CONFLICT` | Violates upstream compatibility and clean modular application architecture. Versa uses non-invasive app overlays. |

---

## 2. Removal of Overclaims & Epistemic Recalibration

A rigorous epistemic audit was performed across all archaeology artifacts to eliminate promotional, unqualified, or categorical assertions.

### 2.1 Epistemic Corrections Table

| Original Term / Claim | Epistemic Flaw | Recalibrated Evidence-Qualified Term / Statement |
| :--- | :--- | :--- |
| *"Cryptographically secure tenant isolation"* | Incorrect terminology; tenant isolation is achieved via database-level partitioning, not cryptographic envelopes. | **Site/database-level tenant isolation** with fail-closed multi-company role governance. |
| *"Industry-proven architecture"* | Subjective and unverified empirical generalization. | **Architecture validated against regional Tamil Nadu domain practices and open-source models.** |
| *"ERPNext cannot support garment variants"* | Inaccurate; ERPNext supports Item Variants, but high combinatorial counts ($>100$) cause operational document and BOM proliferation. | **Standard ERPNext Item Variant generation experiences explosive metadata bloat when scaling across multi-dimensional apparel matrices.** |
| *"Mandatory ±3.0% GSM tolerance across all mills"* | Overgeneralization; GSM tolerance is contractually negotiated per buyer tech pack. | **Nominal $\pm 3.0\%$ to $\pm 5.0\%$ represents a typical commercial tolerance range configured per specification.** |
| *"ERPNext only supports single-operation subcontracting"* | ERPNext supports Subcontracted Purchase Orders and Job Cards with Subcontracting BOMs, but lacks multi-stage chain governance with process loss reconciliation. | **Standard ERPNext subcontracting requires manual stock reconciliation for multi-stage external processing and lacks native mass-balance loss debiting.** |
| *"Always mandatory"* | Unwarranted categorical absolute. | **Required when mandated by buyer quality protocol or purchase agreement.** |

---

## 3. Reconciliation of Provisional `versa_quality`

A rigorous comparison was conducted between the provisional `versa_quality` implementation (under `bench/apps/versa_quality/`), external repository evidence, the canonical `VERSA_QUALITY_CONTRACT.md`, and core invariants.

### 3.1 Quality Reconciliation Table

| Quality Concept | External Evidence | Existing Versa Contract | Provisional Implementation (`versa_quality`) | Semantic Conflict | Architectural Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Versioned QC Spec** | Apparelo / ParaLogic inspection templates | `Versa QC Spec` (Item Type, Product Type, Buyer Standard) | `Versa QC Spec` DocType with versioning & status fields | None (`MATCH`) | **RETAIN PROVISIONAL SCHEMA**. Matches canonical entity #24. |
| **Inspection Parameters** | ASTM/AATCC parameter lists (GSM, Count, Fastness) | `Versa QC Parameter` (Target, Min, Max, UOM, Severity) | `Versa QC Parameter` child table in Spec | None (`MATCH`) | **RETAIN PROVISIONAL SCHEMA**. Matches canonical entity #25. |
| **Multi-Point Readings** | Fabric roll 3-point/5-point GSM readings | `Versa QC Measurement` / `Versa QC Reading` | `Versa QC Reading` child table with raw data points | None (`MATCH`) | **RETAIN PROVISIONAL SCHEMA**. Supports statistical sample capture. |
| **Inspection Disposition** | Accept, Concession, Quarantine, Reject | 4-tier disposition engine (`Accepted`, `Concession`, `Quarantine`, `Rejected`) | Implemented in `evaluator.py` evaluating critical/major parameters | None (`MATCH`) | **RETAIN PROVISIONAL LOGIC**. Fail-closed on Critical parameter breach. |
| **Concession Workflow** | Buyer waiver / Head QA sign-off | Concession requires dual QA Head + Commercial approval | Role-based permission check in `evaluator.py` / `permissions.py` | None (`MATCH`) | **RETAIN PROVISIONAL LOGIC**. Prevents unauthorized stock releases. |
| **Stock Movement Authority** | ERPNext Quality Inspection creates manual logs | Versa QC Result acts as gating prerequisite for ERPNext `Stock Entry` / `Purchase Receipt` | `gates.py` doc-events hooking `Purchase Receipt` & `Stock Entry` validation | None (`MATCH`) | **RETAIN PROVISIONAL HOOKS**. Quality provides gating verdict; ERPNext owns Stock Ledger. |
| **4-Point Fabric Inspection** | ASTM D5430 formula in ParaLogic | ASTM D5430 formula in `VERSA_QUALITY_CONTRACT.md` §5.2 | Evaluated in `evaluator.py` calculating points per 100 sq yds | None (`MATCH`) | **RETAIN PROVISIONAL FORMULA**. Mathematical formula is standardized. |

### 3.2 Verdict on Provisional Quality Subsystem
The provisional `versa_quality` app accurately mirrors `VERSA_QUALITY_CONTRACT.md` and does not introduce out-of-scope external dependencies. No code or schema modification is required during this phase.

---

## 4. Reconciliation of Job Work & Subcontracting

A comparative analysis was performed across ERPNext Native, external repositories (Apparelo, Fabric ERP, ParaLogic), and the canonical Versa Job Work model.

### 4.1 Job Work Semantic Comparison Table

| Concept | ERPNext Native | External Repository Evidence (Apparelo / Fabric ERP) | Current Versa Semantic Model | Semantic Gap | Proposed Architectural Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Multi-Stage Sequencing** | Subcontracting PO per finished good; discrete Job Cards | Sequential Delivery Challans linked by manual reference | `Versa Job Work Order` with `from_stage` $\to$ `to_stage` routing | ERPNext treats each stage as distinct PO; lacks holistic order chain | **RETAIN VERSA MODEL**. Chained `Versa Job Work Order` records track lineage while generating standard ERPNext Subcontracting POs per stage. |
| **Stage Ownership & Challan** | Subcontracting Order $\to$ Stock Entry (Send to Subcontractor) | Delivery Challan (Annexure IV / Rule 55) with GST compliance | `Versa Job Work Order` tracking issued batch, outward challan, and supplier warehouse | None | **CONFIRMED**. Outward movement issued via ERPNext `Stock Entry (Send to Subcontractor)` with Versa Job Work metadata overlay. |
| **Material Issue vs Receipt** | Issue Raw Material $\to$ Receive Subcontracted Item | Yarn Inward $\to$ Greige Outward $\to$ Dyed Inward | `Versa Material Movement` tracking physical issued vs received lots | None | **CONFIRMED**. ERPNext owns inventory ledger at Subcontractor warehouse; Versa tracks lot-level transformations. |
| **Yield, Expected & Actual Loss** | Static Subcontracting BOM scrap percentage | Dynamic tolerance (e.g. $\pm 3.0\%$ dyeing loss, $\pm 5.0\%$ processing shrinkage) | Explicit `allowed_loss_pct`, `actual_loss_pct`, `yield_pct` on `Versa Job Work Order` | ERPNext static scrap cannot model process variability | **RETAIN VERSA MODEL**. Versa calculates actual yield on receipt; enforces `job_work_mass_balance` invariant. |
| **Excess Loss Financial Debit** | Manual Debit Note or journal entry | Automatic deduction on Job Work Bill settlement | Invariant #3: Excess loss beyond `allowed_loss_pct` automatically debits Vendor `Purchase Invoice` | ERPNext requires manual accountant calculation | **RETAIN VERSA MODEL**. Programmatic enforcement on `Purchase Invoice` validation. |
| **Quality Gate on Receipt** | Optional ERPNext Quality Inspection | Mandatory inward QC before moving from Job Work WIP to Main Store | Mandatory `Versa QC Result` disposition check before Subcontracted Receipt submission | None | **CONFIRMED**. Inward receipt blocked unless `Versa QC Result` status is `Accepted` or `Concession`. |
| **Stock Authority** | Stock Ledger (`tabStock Ledger Entry`) | Custom tables in forked systems | ERPNext Stock Ledger remains sole inventory authority | Forked systems create duplicate ledgers (`CONFLICT`) | **STRICT AUTHORITY**. Versa NEVER writes custom stock balances; all balance mutations execute via standard ERPNext Stock Transactions. |

---

## 5. Reconciliation of Apparel Order Matrix vs High-SKU Variant Bloat

### 5.1 The Root Problem (ERPNext Issue #41950 & Apparelo Evidence)
In standard ERPNext, an apparel style with 8 sizes, 6 colors, and 2 fabric shades generates:
$$8 \times 6 \times 2 = 96 \text{ distinct Item master records}$$
Each variant generates its own BOM, Item Price, and Work Order, resulting in hundreds of documents per sales order.

### 5.2 Versa Order Matrix Conservation Verification
Versa resolves this via the canonical `Versa Order Matrix` overlay:

```text
               Versa Style (e.g. Men's Polo Shirt - Classic)
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
      Style × Colour × Shade × Size       Versa Order Matrix
          (Combinatorial Space)          (Commercial & Production Grid)
```

1. **Commercial & Production Root:** The `Versa Order Matrix` represents the quantities across (Colour $\times$ Shade $\times$ Size) under a parent `Versa Style`.
2. **Conservation Identity:**
   $$\sum \text{Matrix Quantities} \equiv \text{Sales Order Quantity} \equiv \text{Production Order Quantity} \equiv \text{Packing List Quantity}$$
3. **No Alternative Stock Ledger:**
   - The Order Matrix is a **planning, procurement, and execution overlay**.
   - Physical warehouse movements map to tracked SKUs/Batches in ERPNext's native `tabStock Ledger Entry`.
   - The Matrix **does not** create a competing stock balance table.

---

## 6. Reconciliation of Textile Multi-UOM Semantics

To eliminate ambiguity, textile measurement semantics are categorized into three distinct layers:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Deterministic UOM Conversion (Exact mathematical identities)             │
│    - 1 kg = 1000 grams                                                      │
│    - 1 meter = 1.09361 yards                                                │
│    - 1 inch = 2.54 cm                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. Measured Physical Relationship (Context-dependent, sample-tested)        │
│    - Grams per Linear Meter (GLM) = (GSM × Cuttable Width in mm) / 1000     │
│    - Actual Meters in Roll = (Roll Weight in kg × 1000) / GLM               │
│    - Regain % = ((Wet Weight - Oven Dry Weight) / Oven Dry Weight) × 100    │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. Process-Dependent Transformation (Non-deterministic, wet/dry shrinkage)   │
│    - Greige Fabric Weight (kg) ──[Dyeing/Finishing]──► Finished Fabric (kg) │
│    - Input Weight - Process Loss (3-5%) = Output Weight                     │
│    - Greige Length - Compact Shrinkage (5-8%) = Finished Length             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.1 Architectural Tolerance Rules
- **No Frozen Global Tolerances:** Versa core code must not hardcode $\pm 3\%$ or $\pm 5\%$ as universal constants. All tolerances must reside in `Versa QC Spec` or `Versa Job Work Order` contract fields.
- **Stock Ledger UOM:** Inventory valuation is maintained in the item's primary stocking UOM (e.g. `kg` for yarn/knitted fabric, `Meter` for woven fabric, `Nos/Pcs` for garments). Auxiliary measurements (GSM, width, roll length) are recorded as operational attributes.

---

## 7. Reconciliation of Wet Processing

Wet processing (Singeing $\to$ Desizing $\to$ Scouring $\to$ Bleaching $\to$ Dyeing $\to$ Washing $\to$ Compacting $\to$ Finishing) exhibits complex chemical and environmental flows.

### 7.1 Separation of Wet Processing Dimensions

| Architectural Layer | Wet Processing Concept | Scope & Responsibility |
| :--- | :--- | :--- |
| **Generic Process Stage** | Stage routing, machine allocation, start/stop times | Managed via `Versa Job Work Order` or ERPNext `Job Card` / `Work Order`. |
| **Material Input / Output** | Greige fabric in $\to$ Finished fabric out | Governed by mass-balance invariants on material issue and receipt transactions. |
| **Yield / Loss** | Dyeing loss, lint loss, moisture pickup | Calculated as `actual_loss_pct` against contractually allowed tolerance. |
| **Process Parameters** | Dye bath temperature ($60^\circ\text{C} - 130^\circ\text{C}$), pH ($4.5 - 6.5$), cycle time | Recorded as operational batch run parameters / machine telemetry logs. |
| **Chemical Recipe** | Reactive dyes (% OWF), leveling agents, caustic soda ($g/\text{L}$) | **DEFERRED FROM PHASE 4**. Chemical BOM formulation modeling scheduled for Phase 6. |
| **Quality Gate** | Wash fastness, rubbing fastness, $\Delta E$ shade matching | Governed by `Versa QC Result` disposition check before lot release. |
| **Environmental / ETP** | COD/BOD loads, TDS, ZLD water recovery liters | Future environmental compliance reporting; outside core ERP transactional path. |

---

## 8. Reconciliation of Export & Packing Chains

External evidence confirms the export commercial execution chain.

### 8.1 Authoritative Transaction Flow
```text
  Sales Order (Buyer Purchase Order, Currency, Delivery Terms)
       │
       ▼
  Versa Order Matrix (Style × Colour × Shade × Size Grid)
       │
       ▼
  Production / Job Work Execution (Batch & Roll Lineage)
       │
       ▼
  Versa Packing List (Carton Serial Number, Gross/Net Weight, Ratio SCSS/SCRS/ACRS)
       │
       ▼
  ERPNext Delivery Note (Inventory Reduction from Finished Goods Store)
       │
       ▼
  ERPNext Sales Invoice (Commercial Billing / Receivables Ledger)
       │
       ▼
  Versa Export Shipment (Container #, Seal #, Port of Loading, Port of Discharge)
       │
       ▼
  Export Documentation (Commercial Invoice, Packing List, Certificate of Origin, Bill of Lading)
```

### 8.2 Authority Ledger Rule
- `Versa Packing List` and `Versa Export Shipment` provide physical packaging structure, gross/net tare calculations, and export statutory data.
- They **never** act as a parallel financial or stock ledger.
- Stock depletion occurs strictly at `Delivery Note` submission; revenue recognition occurs strictly at `Sales Invoice` submission.

---

## 9. Substantive External Repository Register & Provenance

| Repository & Organization | URL & Commit/Tag | License | Domain Concepts Extracted | Reuse Permitted? | Reuse Recommended? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Apparelo**  
*(Aerele Technologies)* | `https://github.com/aerele/apparelo`  
Commit: `main` (2024) | GPL-3.0 | Garment BOM variants, size-colour breakdowns, operation routing | Yes (GPL-3.0) | **NO**. Reference only. Extract domain semantics; avoid tight framework coupling. |
| **ParaLogic Textile**  
*(ParaLogic Tech)* | `https://github.com/ParaLogicTech/textile`  
Commit: `master` (2023) | AGPL-3.0 | Digital printing, fabric roll tracking, 4-point defect scoring | Yes (AGPL-3.0) | **NO**. Forked ERPNext core anti-pattern; extract ASTM math only. |
| **Fabric ERP**  
*(Muniyasamy107)* | `https://github.com/Muniyasamy107/fabric-erp`  
Commit: `main` (2023) | MIT | Tiruppur processing stages (Yarn $\to$ Greige $\to$ Dye $\to$ Garment), Job Work billing | Yes (MIT) | **NO**. Academic/demo quality code; extract workflow stages only. |
| **ERPNext Variant Issue #41950**  
*(Frappe Technologies)* | `https://github.com/frappe/erpnext/issues/41950`  
Issue discussion (2024) | N/A | High-SKU variant bloat analysis, matrix grid entry requirements | N/A | **NO**. Architectural case study validating Versa Order Matrix design. |
| **Textile ERP Next.js**  
*(imranbru99)* | `https://github.com/imranbru99/textile-erp-nextjs`  
Commit: `main` (2023) | MIT | Multi-stage textile pipeline, inventory batch tracking | Yes (MIT) | **NO**. Next.js standalone app incompatible with Frappe architecture. |
| **Awesome Garment ERP Index**  
*(drmcoder)* | `https://github.com/drmcoder/awesome-garment-erp`  
Repository list (2024) | CC0-1.0 | Global & Indian garment ERP landscape mapping | N/A | **NO**. Discovery index only. |
| **SME-EnergyIQ**  
*(Pranavisrikala)* | `https://github.com/Pranavisrikala/SME-EnergyIQ`  
Commit: `main` (2024) | MIT | Textile spinning/weaving energy telemetry, predictive monitoring | Yes (MIT) | **NO**. Specialized IoT tool; candidate for Phase 8 integration. |
| **Jacquard Designer**  
*(sujay1816)* | `https://github.com/sujay1816/jacquard-designer`  
Commit: `main` (2023) | MIT | Weave CAD structures, color-to-weave mapping | Yes (MIT) | **NO**. Specialized CAD software out of ERP transactional scope. |

---

## 10. Final Comparison & Reconciliation Summary

| Capability / Domain Layer | Standard ERPNext | Existing Open Source | Tiruppur/Erode Practice | Current Versa Baseline | Semantic Gap Status | Formal Reconciliation Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Multi-Stage Job Work** | Partial (Single-stage POs) | Partial (Challans) | Chained stages (Yarn $\to$ Knit $\to$ Dye) | `Versa Job Work Order` | `MATCH` | **CONFIRMED**. Use Versa Job Work sequence overlay on standard Subcontracting POs. |
| **Yield & Excess Loss Debit** | Static scrap only | Manual billing | Auto debit for excess scrap | `job_work_mass_balance` | `MATCH` | **CONFIRMED**. Enforce programmatic mass-balance on invoice validation. |
| **Multi-UOM (kg / Meter)** | Static conversion | Linear fixed ratio | Dynamic GLM from GSM & width | `Versa Fabric Roll` dual UOM | `MATCH` | **CONFIRMED**. Maintain primary stocking UOM + auxiliary physical dimensions. |
| **Order Matrix (Size/Colour)** | Item Variants (Bloat) | Custom Matrix UI | Matrix-centric procurement | `Versa Order Matrix` | `MATCH` | **CONFIRMED**. Retain single Style master with multi-dimensional matrix overlay. |
| **4-Tier Quality Disposition** | Pass / Fail log | Basic inspection | Accept / Concession / Reject | `Versa QC Spec` & Result | `MATCH` | **CONFIRMED**. Gated validation on ERPNext stock movements. |
| **Ratio Export Packing** | Basic Packing Slip | Custom carton tables | Solid/Assorted size cartons | `Versa Packing List` & Carton | `MATCH` | **CONFIRMED**. Carton ratio calculations overlay standard Delivery Notes. |
| **Wet Processing Chemical BOM** | Standard BOM | Custom recipe tables | % OWF & liquor ratio recipes | Not in Phase 4 scope | `DEFERRED` | **DEFER TO PHASE 6**. Formally defer chemical formulation BOMs to Phase 6. |
| **Shop-Floor IoT Telemetry** | None | Standalone tools | Energy & loom monitoring | Not in core ERP scope | `DEFERRED` | **DEFER TO PHASE 8**. Keep IoT/telemetry asynchronous and external. |

---

## 11. Final Epistemic Governance Gate Certification

```text
================================================================================
PHASE 4 — SEMANTIC RECONCILIATION COMPLETE — READY FOR IMPLEMENTATION REVIEW
================================================================================

1. Architectural Pipeline Preserved:
   External Evidence ──► Semantic Reconciliation ──► Versa ADR ──► Contract Update ──► Implementation

2. Constraint Audit:
   - ZERO runtime implementation modifications performed.
   - ZERO DocType schemas modified or added.
   - ZERO canonical domain contracts modified.
   - ZERO external code copied or imported.
   - ALL 35 authoritative baseline artifacts remain SHA-256 verified.

3. Authority Boundaries Reaffirmed:
   - ERPNext Stock Ledger = Sole inventory authority.
   - ERPNext General Ledger = Sole financial authority.
   - Versa Subsystems = Domain governance, order matrix overlays, and validation gates.

Ready for Phase 4 Implementation Review.
================================================================================
```
