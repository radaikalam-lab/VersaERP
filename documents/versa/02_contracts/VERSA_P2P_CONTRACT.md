# VERSA ERP PROCURE-TO-PAY (P2P) CONTRACT SPECIFICATION

## 1. Objective & Scope

This contract defines the end-to-end **Procure-to-Pay (P2P)** lifecycle for raw material purchasing (Yarn, Greige Fabric, Dyes, Chemicals, Trims, Accessories, Packing Materials) and subcontracted services in the Tiruppur manufacturing ecosystem.

---

## 2. End-to-End P2P Lifecycle Architecture

```text
  [ Material Requirement ] (Auto-generated from Sales Order BOM / Reorder Level)
             │
             ▼
  [ Material Request / Purchase Requisition ] (ERPNext standard)
             │
             ▼
  [ RFQ & Supplier Quotation Comparison ] (Versa P2P Extension: Comparison Grid & Approval)
             │
             ▼
  [ Purchase Order ] (ERPNext PO + Versa Specs & Approval Matrix)
             │
             ▼
  [ Purchase Receipt ] (ERPNext standard + Physical Lot/Roll Creation)
             │
             ▼
  [ Incoming Quality Inspection ] (Versa Quality: Multi-parameter Test & Grade)
             │
     ┌───────┴────────────────────────┬────────────────────────┐
     ▼                                ▼                        ▼
[ Accepted ]                   [ Quarantine ]             [ Rejected ]
     │                                │                        │
     ▼                                ▼                        ▼
[ Stock Warehouse ]            [ Concession Review ]      [ Purchase Return ]
     │                                │                        │
     ├────────────────────────────────┘                        │
     ▼                                                         ▼
[ Purchase Invoice (3-Way Match) ] (ERPNext)           [ Debit Note ]
     │
     ▼
[ Payment Entry & Settlement ] (ERPNext)
```

---

## 3. Stage Responsibility & Functional Boundaries

| Stage / Artifact | System Responsibility | Core Functionality & Business Rules |
| :--- | :--- | :--- |
| **Material Requirement** | `ERPNext + Versa Textile` | Explodes `Versa Style` BOM against confirmed `Sales Order` or production reorder levels. |
| **Material Request (PR)** | `ERPNext Core` | Standard requisition document specifying Item, Quantity, Required Date, Warehouse. |
| **Supplier Selection & RFQ**| `Versa P2P Extension` | Quotation comparison matrix evaluating Supplier Rate, Payment Terms, Lead Time, Historical Quality Rating. |
| **Purchase Order (PO)** | `ERPNext + Versa Core` | Attaches `Versa Material Spec` (Yarn Count, Mill, Composition, Fabric GSM, Width). Subject to `Versa Approval Rule`. |
| **Purchase Receipt (GRN)** | `ERPNext + Versa Textile` | Generates `Versa Material Lot` and individual `Versa Fabric Roll` records with initial `Quarantine` grade. |
| **Incoming QC** | `Versa Quality` | Executes `Versa QC Result` tests (GSM, Count, CSP, Shrinkage, Chemical purity). Dispositions to Accepted, Concession, or Rejected. |
| **Stock Ledger Update** | `ERPNext Core` | Moves accepted inventory to Active Warehouse. Quarantined stock remains non-issueable. |
| **Purchase Invoice** | `ERPNext Core` | Standard 3-way matching (PO Price, Receipt Qty, Invoice Amount) with GST/e-Invoicing integration. |
| **Payment Entry** | `ERPNext Core` | Bank / Cash disbursements respecting agreed supplier credit terms and debit notes. |

---

## 4. Subcontracted Job Work Procurement Sub-Process

In textile manufacturing, substantial procurement occurs as **services (Job Work)** rather than raw goods purchase:

```text
  [ Job Work Requirement ] (Knitting, Dyeing, Printing, Washing)
             │
             ▼
  [ Job Work Order (VJWO) ] (Versa Job Work: Process, Worker, Rate, Loss %)
             │
             ▼
  [ Material Issue ] (ERPNext Stock Entry: Raw Store → Job Worker Warehouse)
             │
             ▼
  [ External Processing ] (Job Worker execution at external plant)
             │
             ▼
  [ Job Work Receipt ] (ERPNext Stock Entry: Job Worker Warehouse → Processed Store)
             │
             ▼
  [ Mass Balance & QC ] (Versa Job Work Result: Output + Loss + Scrap Reconciliation)
             │
             ▼
  [ Subcontractor Invoice ] (ERPNext Purchase Invoice for Service Charges ± Scrap Debits)
             │
             ▼
  [ Payment Settlement ] (ERPNext Payment Entry)
```

---

## 5. P2P Business Controls & Invariants

1. **Approval Matrix Invariant:**
   A `Purchase Order` cannot be submitted (`docstatus = 1`) without satisfying the `Versa Approval Rule` matching `(company, cost_center, total_amount)`.
2. **Quality Gate Invariant:**
   A `Purchase Receipt` for quality-mandatory items (`is_qc_required = 1`) cannot update the active stock warehouse until a corresponding `Versa QC Result` is approved with status `Accepted` or `Accepted with Concession`.
3. **Three-Way Matching Invariant:**
   $$\text{Invoice Qty} \le \text{Accepted Receipt Qty} \quad \land \quad \text{Invoice Rate} \le \text{PO Rate} \times (1 + \text{Price Tolerance})$$
4. **Supplier Performance Scoring Invariant:**
   Every completed `Purchase Receipt` and `Versa QC Result` updates the supplier's running performance indices:
   - **Quality Score:** $\frac{\text{Accepted Qty}}{\text{Total Received Qty}} \times 100$
   - **On-Time Delivery Score:** $\frac{\text{On-Time Deliveries}}{\text{Total Deliveries}} \times 100$
   - **Price Variance Score:** $\frac{\text{Agreed PO Amount}}{\text{Invoiced Amount}} \times 100$

