# VERSA ERP TEXTILE PROCESS CONTRACT SPECIFICATION

**Document Identifier:** `CONTRACT-005`  
**Authoritative File Path:** `documents/versa/02_contracts/VERSA_TEXTILE_PROCESS_CONTRACT.md`  
**Phase:** Phase 5 — Textile Processing & Fabric Processing  
**Status:** `FROZEN FOR ARCHITECTURAL REVIEW`  
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

## 2. Normative Domain Rules

### Rule `R-TEX-001`: Process Mass-Balance Conservation
- **Rule ID:** `R-TEX-001`
- **Definition:** For every textile transformation stage $S$, the total issued input mass must exactly equal the sum of net usable output mass, recoverable scrap mass, contractual allowed process loss, and excess loss:
  $$\text{Input Mass} \equiv \text{Output Usable Mass} + \text{Recoverable Scrap Mass} + \text{Allowed Loss Mass} + \text{Excess Loss Mass}$$
- **Authority:** `VERSA_JOBWORK_CONTRACT.md`, Canonical Invariant #2 (`job_work_mass_balance`).
- **Provenance:** Tiruppur / Erode textile wet processing and knitting mass-balance standards.
- **Rationale:** Prevents physical material loss from disappearing unrecorded and enforces financial accountability for processor scrap.
- **Scope:** All internal manufacturing stages and external Job Work processing stages.
- **Counterexample (Violation):** Issuing $1000\text{ kg}$ greige fabric, receiving $920\text{ kg}$ dyed fabric with $4\%$ allowed loss ($40\text{ kg}$), and ignoring the remaining $40\text{ kg}$ deficit without recording excess loss or generating a debit note.
- **Test Expectation:** Submitting a process receipt where $\text{Output} + \text{Scrap} + \text{Loss} \ne \text{Input}$ raises a mass-balance `ValidationError`.

---

### Rule `R-TEX-002`: Fabric Physical Measurement Formulation
- **Rule ID:** `R-TEX-002`
- **Definition:** Fabric linear length and linear mass density are derived strictly from physical specimen measurements, never from static item conversion factors:
  $$\text{GLM (g/linear meter)} = \frac{\text{GSM } (g/m^2) \times \text{Cuttable Width (mm)}}{1000}$$
  $$\text{Calculated Length (meters)} = \frac{\text{Net Fabric Weight (kg)} \times 1,000,000}{\text{Measured GSM} \times \text{Cuttable Width (mm)}}$$
- **Authority:** `VERSA_QUALITY_CONTRACT.md` §3.2, ASTM D3776 / ASTM D3774.
- **Provenance:** Standard Textile Engineering Metrology.
- **Rationale:** Knitted fabric changes density during dyeing, compacting, and relaxing. Static UOM conversion factors corrupt stock valuation and cutting lay calculations.
- **Scope:** All `Versa Fabric Roll` physical dimension derivations.
- **Counterexample (Violation):** Configuring a fixed ERPNext UOM conversion rule `1 Meter = 0.25 kg` across all Single Jersey 180 GSM items regardless of actual measured GSM and width.
- **Test Expectation:** System calculates linear meters dynamically using actual inspection readings and rejects static linear overrides.

---

### Rule `R-TEX-003`: Fabric Roll Traceability & Genealogy
- **Rule ID:** `R-TEX-003`
- **Definition:** Every `Versa Fabric Roll` must possess an immutable barcode (`roll_barcode`) and link to exactly one parent `Batch` and source production transaction. When a roll is split or merged:
  - Split: Parent roll is marked `Split`; new child rolls inherit batch, shade, and quality parameters with proportionally divided weight and continuous length.
  - Merge: Input rolls are marked `Merged`; composite child roll inherits combined net weight with recalculation of aggregate defect score.
- **Authority:** Canonical Entity ENT-017 (`Versa Fabric Roll`), `VERSA_QUALITY_CONTRACT.md` §5.1.
- **Provenance:** Piece-goods roll tracking standards in garment manufacturing.
- **Rationale:** Ensures complete end-to-end auditability from raw yarn lot to finished garment cutting bundle.
- **Scope:** All knitted and woven fabric roll entities.
- **Counterexample (Violation):** Consuming a 25 kg roll partially during cutting without creating a residual roll record or tracking the consumed length.
- **Test Expectation:** Roll genealogy tree correctly traces child rolls back to original greige knitting roll and yarn lot.

---

### Rule `R-TEX-004`: Quality Gated Material Movement
- **Rule ID:** `R-TEX-004`
- **Definition:** No fabric roll or batch in `Quarantine` or `Rejected` status may be issued to a downstream production process (e.g. Cutting, Printing, Stentering) or submitted on a `Stock Entry (Material Issue)`:
  $$\text{Roll Status} \in \{\text{Quarantine}, \text{Rejected}\} \implies \text{Issue Blocked (Fail-Closed)}$$
- **Authority:** `VERSA_QUALITY_CONTRACT.md` §4, `versa_quality.gates`.
- **Provenance:** Fail-closed quality assurance governance.
- **Rationale:** Prevents defective, off-shade, or untested fabric from being cut into garments, eliminating irrecoverable production waste.
- **Scope:** All ERPNext `Stock Entry` and `Versa Job Work Order` material movements.
- **Counterexample (Violation):** Issuing a fabric roll with 4-point defect score $> 28.0$ (Grade C) to cutting without QA Head concession approval.
- **Test Expectation:** Attempting to submit a Stock Entry referencing a Quarantined or Rejected roll raises `frappe.ValidationError` / `ValueError`.

---

### Rule `R-TEX-005`: Multi-Stage Job Work Route Lineage
- **Rule ID:** `R-TEX-005`
- **Definition:** Multi-stage external processing must maintain continuous sequence integrity ($\text{Stage } N \to \text{Stage } N+1$). Material received from Stage $N$ becomes the explicit input material for Stage $N+1$, linked via delivery challans and batch genealogy without breaking the parent commercial order context.
- **Authority:** `VERSA_JOBWORK_CONTRACT.md`, Canonical Invariant #4.
- **Provenance:** Tiruppur multi-processor subcontracting model (Knitter $\to$ Dyer $\to$ Compactor $\to$ Printer).
- **Rationale:** Eliminates manual intermediate stock adjustments and guarantees processor attribution for cumulative yield losses.
- **Scope:** All multi-stage `Versa Job Work Order` executions.
- **Counterexample (Violation):** Receiving dyed fabric into a generic raw materials store and issuing it to printing under an unrelated new order without linking to the original greige batch.
- **Test Expectation:** Stage $N+1$ job work order validates that issued material originates from submitted Stage $N$ receipt.

---

## 3. Authority Boundary Specifications

| Domain Dimension | Authoritative Subsystem | Implementation Mechanism | Invariant Enforcement |
| :--- | :--- | :--- | :--- |
| **Inventory Ledger** | **ERPNext Stock** | Native `tabStock Ledger Entry` | Versa creates ZERO parallel stock balance tables. |
| **General Ledger** | **ERPNext Accounts** | Native `tabGL Entry` | Versa creates ZERO parallel financial ledgers. |
| **Physical Roll Dimensions** | **Versa Textile / Quality** | `Versa Fabric Roll`, `Versa QC Reading` | Dynamic GLM formulation from measured GSM and width. |
| **Process Quality Gates** | **Versa Quality** | `Versa QC Result`, `gates.py` | Fail-closed `before_submit` hook block on rejected/quarantined lots. |
| **Mass-Balance Governance** | **Versa Job Work** | `Versa Job Work Order` | Automated calculation of actual loss and excess loss debits. |

---

## 4. Contract Status & Epistemic Audit

- **Normative Rules:** `R-TEX-001` through `R-TEX-005` (Binding).
- **Derived Formulas:** $\text{GLM}$, $\text{Calculated Length}$, $\text{Excess Loss Mass}$.
- **Deferred Functionality:** Chemical recipe formulation (% OWF, g/L) deferred to Phase 6; IoT machine monitoring deferred to Phase 8.
- **Unresolved Questions:** Salvage scrap valuation (Open Question #11); yarn count variation compensation (Open Question #12).
