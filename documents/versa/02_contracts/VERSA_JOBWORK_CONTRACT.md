# VERSA ERP JOB WORK & SUBCONTRACTING CONTRACT SPECIFICATION

## 1. Objective & Ecosystem Context

In the Tiruppur textile cluster, over 65% of specialized manufacturing operations (Circular Knitting, Yarn Dyeing, Fabric Dyeing, Compacting, All-Over Rotary Printing, Chest Screen Printing, Computerized Embroidery, Washing / Bio-Polishing, and Garment Stitching) are executed via **external Job Workers (Subcontractors)**.

This contract defines the authoritative operational lifecycle, mass-balance conservation laws, scrap/loss accounting rules, and financial settlement mechanisms for Job Work.

---

## 2. Job Work Operational Lifecycle

```text
  [ Job Work Requirement ] (Generated from Sales Order or Production Schedule)
             │
             ▼
  [ Job Work Order (VJWO) ] (Process, Job Worker, Agreed Rate, Loss Tolerance %)
             │
             ▼
  [ Material Issue ] (ERPNext Stock Entry: Material Transfer to Subcontractor Warehouse)
             │  (Tracks specific Yarn Lots or Fabric Roll Barcodes)
             ▼
  [ Subcontractor Processing ] (Knitting / Dyeing / Printing / Stitching)
             │
             ▼
  [ Material Receipt ] (ERPNext Stock Entry: Subcontractor Warehouse to Transit/Store)
             │
             ▼
  [ Quality Inspection ] (Versa Quality: Multi-parameter inspection on received goods)
             │
             ▼
  [ Mass Balance & Reconciliation ] (Calculates Net Yield, Process Loss, Scrap, Rework)
             │
             ▼
  [ Job Work Settlement Invoice ] (ERPNext Purchase Invoice for Processing Charges)
             │  (Applies automated debit adjustments if process loss exceeds tolerance)
             ▼
  [ Payment Settlement ] (ERPNext Payment Entry)
```

---

## 3. Mass Balance Conservation Law & Reconciliation Invariants

### 3.1 The Fundamental Mass Balance Invariant

For every `Versa Job Work Order` and issued lot/batch, total issued material mass must be fully conserved and reconciled:

$$\text{Issued Quantity} \equiv \text{Converted Output Quantity} + \text{Process Loss} + \text{Wastage / Scrap} + \text{Returned Unprocessed} + \text{Unaccounted Quantity}$$

Where:
- **$\text{Issued Quantity}$:** Physical weight ($kg$) or length ($m$) of raw material issued (e.g. Yarn cones, Greige fabric rolls).
- **$\text{Converted Output Quantity}$:** Physical weight of finished/processed goods received (normalized by process expansion/shrinkage ratio if applicable).
- **$\text{Process Loss}$:** Normal invisible loss resulting from process dynamics (e.g. fly/lint in knitting, moisture evaporation/sizing wash-off in dyeing).
- **$\text{Wastage / Scrap}$:** Physical defective scrap generated (e.g. fabric cuttings, end-bits, dirty yarn) returned by the job worker.
- **$\text{Returned Unprocessed}$:** Intact raw materials returned unused by the job worker.
- **$\text{Unaccounted Quantity}$:** Missing mass unaccounted for by physical measurements.

### 3.2 Unaccounted Quantity Governance Law

```text
================================================================================
GOVERNANCE RULE:
Unaccounted Quantity is STRICTLY NOT PERMITTED (Tolerance = 0.00 kg).
Allowable scale calibration tolerance is capped at <= 0.1% of issued batch mass.
Any Unaccounted Quantity > 0.1% is classified as MATERIAL THEFT / LOSS,
blocking Job Work Order closure and automatically generating a Material Debit Note
against the Job Worker's pending service ledger.
================================================================================
```

---

## 4. Process-Specific Loss Tolerances & Billing Formulas

| Process | Typical Standard Loss % | Wastage / Scrap % | Billing Basis | Settlement Formula |
| :--- | :--- | :--- | :--- | :--- |
| **Circular Knitting** | $2.5\% - 3.5\%$ | $0.5\% - 1.0\%$ (Lint/Cuts) | Per Kg Output | $\text{Gross Payable} = \text{Output Kg} \times \text{Rate/Kg}$ |
| **Yarn Dyeing** | $3.0\% - 4.5\%$ | $0.5\%$ | Per Kg Output | $\text{Gross Payable} = \text{Dyed Output Kg} \times \text{Rate/Kg}$ |
| **Fabric Dyeing / Finishing**| $4.0\% - 6.0\%$ | $1.0\%$ (End-bits) | Per Kg Output | $\text{Gross Payable} = \text{Finished Kg} \times \text{Rate/Kg}$ |
| **Chest Screen Printing** | $0.0\%$ (Count-based) | $\le 1.5\%$ (Rejection) | Per Piece | $\text{Gross Payable} = \text{Passed Pcs} \times \text{Rate/Pc}$ |
| **All-Over Rotary Printing**| $3.0\% - 5.0\%$ | $1.5\%$ | Per Meter / Kg | $\text{Gross Payable} = \text{Printed Mtr} \times \text{Rate/Mtr}$ |
| **Garment Stitching** | $0.0\%$ (Count-based) | $\le 1.0\%$ (Alteration) | Per Piece (SAM) | $\text{Gross Payable} = \text{Passed Pcs} \times \text{Rate/Pc}$ |

---

## 5. Excess Loss Penalty & Debit Invariant

If the actual process loss exceeds the contractually allowed tolerance:

$$\text{Excess Loss} = \max\left(0, \text{Actual Process Loss} - (\text{Issued Quantity} \times \text{Allowed Loss Pct})\right)$$

$$\text{Material Debit Amount} = \text{Excess Loss} \times \text{Standard Material Cost per Kg}$$

$$\text{Net Settlement Payable} = \text{Job Work Service Invoice Amount} - \text{Material Debit Amount}$$

---

## 6. Job Worker Capability & Quality Integration

1. **Approved Vendor List (AVL):** A Job Work Order can only be raised for a Job Worker whose `compliance_status == 'Compliant'` and whose `Versa Job Worker Process` profile lists the required process and machine specifications (e.g. 24GG / 30" Dia Knitting Machine).
2. **Quality Rating Feedback:** Every receipt inspection updates the job worker's running quality rating. If the rating drops below $3.5 / 5.0$, new Job Work Orders require Managing Director sign-off.

