# VERSA ERP TEXTILE PROCESS CONTRACT SPECIFICATION

**Document Identifier:** `CONTRACT-005`  
**Contract Version:** `v1.1`  
**Authoritative File Path:** `documents/versa/02_contracts/VERSA_TEXTILE_PROCESS_CONTRACT.md`  
**Phase:** Phase 5 — Textile Processing & Fabric Processing  
**Status:** `FROZEN FOR IMPLEMENTATION SPECIFICATION`  
**Governing Decisions:** [`DEC-012`](file:///e:/VersaERP/documents/versa/06_decisions/VERSA_PHASE_5_SEMANTIC_DECISIONS.md), [`DEC-013`](file:///e:/VersaERP/documents/versa/06_decisions/VERSA_PHASE_5_DECISION_RESOLUTION.md)  
**Governing Domain Model:** [`VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md`](file:///e:/VersaERP/documents/versa/01_domain/VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md)  

---

## 1. Scope & Epistemic Boundaries

This contract defines the normative rules, state transitions, mass-balance conservation laws, physical measurement relationships, and authority boundaries governing textile manufacturing operations in VersaERP.

```text
       [ Upstream Yarn Lot / PO ]
                   │
                   ▼ (Knitting / Weaving)
       [ Greige Fabric Batch (kg / Rolls) ]
                   │
                   ▼ (Dyeing / Finishing Job Work)
       [ Finished Fabric Batch ] ──► [ Quality Gate: Versa QC Result ]
                                                  │
                                                  ▼
                                     [ Approved Active Stock ]
```

---

## 2. Version Change Record (`v1.0` $\to$ `v1.1`)

| Target Rule | Prior Version (`v1.0`) | Amended Frozen Version (`v1.1`) | Authorizing Decision |
| :--- | :--- | :--- | :--- |
| **`R-TEX-001`** | Conflated Expected/Allowed loss; implied automated debit note posting. | Formalized 4 loss terms; bounded excess loss to generating `Debit Candidate` only; added 4 Stage Conservation Models. | `DEC-013.1`, `DEC-013.2`, `DEC-013.4` |
| **`R-TEX-002`** | Implicit linear metrology lifecycle. | Decoupled into 3-Dimensional Metrology Model (Origin, Verification, Disposition). | `DEC-013.5` |
| **`R-TEX-003`** | Constrained roll to "exactly one parent batch". | Established `Material Transformation Lineage` supporting $1 \to 1, 1 \to N, N \to 1, N \to N$. | `DEC-013.3` |
| **`R-TEX-004`** | Quality gate interlock rule. | Re-affirmed fail-closed gate linking 3D metrology disposition to Stock Entry block. | `DEC-011`, `DEC-013.5` |
| **`R-TEX-005`** | Multi-stage job work route sequence. | Clarified commercial lineage context across sequential processing stages. | `DEC-012`, `DEC-013.3` |

---

## 3. Normative Domain Rules

### Rule `R-TEX-001`: Process Mass-Balance & Loss Conservation
- **Rule ID:** `R-TEX-001`
- **Definition:** For every textile transformation stage $S$, the total issued input mass must exactly equal the sum of net usable output mass, recoverable scrap mass, contractual allowed process loss, and excess loss:
  $$\text{Input Mass } (M_{\text{in}}) \equiv M_{\text{out\_usable}} + M_{\text{recoverable\_scrap}} + L_{\text{allowed}} + L_{\text{excess}}$$
  where:
  - $\text{Actual Loss } (L_{\text{actual}}) = M_{\text{in}} - (M_{\text{out\_usable}} + M_{\text{recoverable\_scrap}})$
  - $\text{Expected Loss Allowance } (L_{\text{expected}}) = M_{\text{in}} \times \text{Tolerance}\%$
  - $\text{Allowed Loss } (L_{\text{allowed}}) = \min(L_{\text{actual}}, L_{\text{expected}})$
  - $\text{Excess Loss } (L_{\text{excess}}) = \max(0, L_{\text{actual}} - L_{\text{expected}})$
- **Tolerance Precedence:** Tolerance percentage is resolved strictly via commercial hierarchy:
  $$\text{Job Work Order Agreement} \longrightarrow \text{Vendor Master Subcontracting Agreement} \longrightarrow \text{Zero Tolerance (0.0\%) Strict Default}$$
- **Settlement Authority:** Excess loss ($L_{\text{excess}} > 0$) generates a **Debit Candidate / Settlement Deduction**. VersaERP shall NOT autonomously create or submit `GL Entry` or `Debit Note` transactions; all financial postings remain strictly within ERPNext Accounts approval workflows.
- **Stage Conservation Taxonomy:** Transformation stages must execute under one of 4 normative models:
  1. `MASS_CONSERVATION_DRY` (Knitting, Winding)
  2. `MASS_CONSERVATION_ADJUSTED` (Bleaching, Dyeing, Printing)
  3. `DIMENSIONAL_TRANSFORMATION` (Stentering, Compacting)
  4. `PIECE_COUNT_MASS_CONSERVATION` (Garment Cutting)
- **Authority:** `VERSA_JOBWORK_CONTRACT.md`, Canonical Invariant #2, `DEC-013.1`, `DEC-013.2`, `DEC-013.4`.
- **Provenance:** Tiruppur / Erode textile wet processing and knitting mass-balance standards.
- **Scope:** All internal manufacturing stages and external Job Work processing stages.
- **Counterexample (Violation):** Issuing 1000 kg greige fabric, receiving 920 kg dyed fabric with 4% allowed loss (40 kg), and ignoring the remaining 40 kg deficit without creating a Debit Candidate or obtaining an authorized concession.
- **Test Expectation:** Submitting a process receipt where $M_{\text{out}} + M_{\text{scrap}} + L_{\text{allowed}} + L_{\text{excess}} \ne M_{\text{in}}$ raises a mass-balance `ValidationError`.

---

### Rule `R-TEX-002`: Fabric Physical Measurement & Metrology Epistemics
- **Rule ID:** `R-TEX-002`
- **Definition:** Fabric linear length and linear mass density are derived strictly from physical specimen measurements, never from static item conversion factors:
  $$\text{GLM (g/linear meter)} = \frac{\text{Measured GSM } (g/m^2) \times \text{Cuttable Width (mm)}}{1000}$$
  $$\text{Calculated Length (meters)} = \frac{\text{Net Fabric Weight (kg)} \times 1,000,000}{\text{Measured GSM} \times \text{Cuttable Width (mm)}}$$
- **3-Dimensional Metrology Model:** Every physical property reading is decoupled into:
  1. *Value Origin:* `DECLARED` (vendor invoice), `MEASURED` (calibrated scale/instrument), `CALCULATED` (derived via formula).
  2. *Verification State:* `UNVERIFIED` vs `VERIFIED` (inspected within instrument tolerance).
  3. *Commercial Disposition:* `PENDING`, `ACCEPTED` (ingested to stock), `CONCESSION`, `REJECTED`.
- **Authority:** `VERSA_QUALITY_CONTRACT.md` §3.2, ASTM D3776 / ASTM D3774, `DEC-013.5`.
- **Provenance:** Standard Textile Engineering Metrology.
- **Rationale:** Knitted fabric changes density during dyeing and compacting. Static UOM conversion factors corrupt stock valuation and cutting lay calculations.
- **Scope:** All `Versa Fabric Roll` physical dimension derivations.
- **Counterexample (Violation):** Configuring a fixed ERPNext UOM conversion rule `1 Meter = 0.25 kg` across all Single Jersey 180 GSM items regardless of actual measured GSM and width.
- **Test Expectation:** System calculates linear meters dynamically using actual inspection readings and rejects static linear overrides.

---

### Rule `R-TEX-003`: Material Transformation Lineage & Roll Genealogy
- **Rule ID:** `R-TEX-003`
- **Definition:** Every `Versa Fabric Roll` possesses an immutable unique barcode (`roll_barcode`) and maintains full material lineage across `Material Transformation Events`. Supports all physical transformation topologies:
  - **$1 \to 1$:** Single roll finishing or re-inspection.
  - **$1 \to N$ (Split):** Parent roll is marked `Split`; child rolls inherit lot, shade, and quality parameters with proportionally divided weight and continuous length.
  - **$N \to 1$ (Merge):** Input rolls marked `Merged`; composite child roll inherits combined net weight with recalculation of aggregate defect score.
  - **$N \to N$:** Multi-roll batch processing across stenter / compacting lines.
  - **$1 \to \text{Pieces} + \text{Scrap}$:** Cutting lay panel creation with end-bits and Chindi remnants.
- **Authority:** Canonical Entity ENT-017 (`Versa Fabric Roll`), `VERSA_QUALITY_CONTRACT.md` §5.1, `DEC-013.3`.
- **Provenance:** Piece-goods roll tracking standards in garment manufacturing.
- **Rationale:** Ensures complete end-to-end auditability from raw yarn lot to finished garment cutting bundle.
- **Scope:** All knitted and woven fabric roll entities.
- **Counterexample (Violation):** Consuming a 25 kg roll partially during cutting without creating a residual roll record or tracking the consumed length.
- **Test Expectation:** Roll genealogy tree correctly traces child rolls back to original greige knitting rolls and yarn lots.

---

### Rule `R-TEX-004`: Quality Gated Material Movement
- **Rule ID:** `R-TEX-004`
- **Definition:** No fabric roll or batch in `Quarantine` or `Rejected` disposition status may be issued to a downstream production process (e.g. Cutting, Printing, Stentering) or submitted on a `Stock Entry (Material Issue)`:
  $$\text{Roll Status} \in \{\text{Quarantine}, \text{Rejected}\} \implies \text{Issue Blocked (Fail-Closed)}$$
- **Authority:** `VERSA_QUALITY_CONTRACT.md` §4, `versa_quality.gates`, `DEC-011`, `DEC-013.5`.
- **Provenance:** Fail-closed quality assurance governance.
- **Rationale:** Prevents defective, off-shade, or untested fabric from being cut into garments, eliminating irrecoverable production waste.
- **Scope:** All ERPNext `Stock Entry` and `Versa Job Work Order` material movements.
- **Counterexample (Violation):** Issuing a fabric roll with 4-point defect score $> 28.0$ (Grade C) to cutting without QA Head concession approval.
- **Test Expectation:** Attempting to submit a Stock Entry referencing a Quarantined or Rejected roll raises `frappe.ValidationError` / `ValueError`.

---

### Rule `R-TEX-005`: Multi-Stage Job Work Route Lineage
- **Rule ID:** `R-TEX-005`
- **Definition:** Multi-stage external processing must maintain continuous sequence integrity ($\text{Stage } N \to \text{Stage } N+1$). Material received from Stage $N$ becomes the explicit input material for Stage $N+1$, linked via delivery challans and transformation lineage without breaking the parent commercial order context.
- **Authority:** `VERSA_JOBWORK_CONTRACT.md`, Canonical Invariant #4, `DEC-012`, `DEC-013.3`.
- **Provenance:** Tiruppur multi-processor subcontracting model (Knitter $\to$ Dyer $\to$ Compactor $\to$ Printer).
- **Rationale:** Eliminates manual intermediate stock adjustments and guarantees processor attribution for cumulative yield losses.
- **Scope:** All multi-stage `Versa Job Work Order` executions.
- **Counterexample (Violation):** Receiving dyed fabric into a generic raw materials store and issuing it to printing under an unrelated new order without linking to the original greige batch.
- **Test Expectation:** Stage $N+1$ job work order validates that issued material originates from submitted Stage $N$ receipt.

---

## 4. Authority Boundary Specifications

| Domain Dimension | Authoritative Subsystem | Implementation Mechanism | Invariant Enforcement |
| :--- | :--- | :--- | :--- |
| **Inventory Ledger** | **ERPNext Stock** | Native `tabStock Ledger Entry` | Versa creates ZERO parallel stock balance tables. |
| **General Ledger** | **ERPNext Accounts** | Native `tabGL Entry` | Versa creates ZERO parallel financial ledgers. |
| **Physical Roll Dimensions** | **Versa Textile / Quality** | `Versa Fabric Roll`, `Versa QC Reading` | Dynamic GLM formulation from measured GSM and cuttable width. |
| **Process Quality Gates** | **Versa Quality** | `Versa QC Result`, `gates.py` | Fail-closed `before_submit` hook block on rejected/quarantined lots. |
| **Mass-Balance & Settlement** | **Versa Job Work** | `Versa Job Work Order` | Calculates Debit Candidates; ERPNext Accounts reviews and posts Debit Notes. |

---

## 5. Contract Status & Epistemic Certification

- **Normative Rules:** `R-TEX-001` through `R-TEX-005` (Binding & Authoritative).
- **Contract Status:** **`FROZEN FOR IMPLEMENTATION SPECIFICATION`**.
- **Deferred Functionality:** Chemical recipe formulation (% OWF, g/L) deferred to Phase 6; IoT machine monitoring deferred to Phase 8.
- **Tracked Open Questions:** `OQ-011` through `OQ-018` actively tracked in `VERSA_PHASE_5_OPEN_QUESTIONS.md` and `VERSA_PHASE_5_CONTRACT_REVIEW_OPEN_QUESTIONS.md`.
