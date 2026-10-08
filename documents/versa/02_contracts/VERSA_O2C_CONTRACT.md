# VERSA ERP ORDER-TO-CASH (O2C) CONTRACT SPECIFICATION

## 1. Objective & Scope

This contract governs the end-to-end **Order-to-Cash (O2C)** commercial and operational lifecycle for garment exporters and domestic apparel brands, spanning customer enquiry, colour-by-size matrix ordering, style engineering, production allocation, packing, export dispatch, billing, and receivables collection.

---

## 2. End-to-End O2C Lifecycle Architecture

```text
  [ Customer Enquiry / RFQ ] (Buyer Tech Pack, Target Price, Delivery Date)
             │
             ▼
  [ Quotation & Costing Sheet ] (Versa Style Costing: Fabric, Trims, CM, Overheads, Margin)
             │
             ▼
  [ Commercial & Credit Approval ] (Versa Core: Margin & Credit Limit Check)
             │
             ▼
  [ Sales Order + Colour×Size Matrix ] (ERPNext Sales Order + Versa Order Matrix)
             │
             ▼
  [ Material Explosion & Production Plan ] (Auto-allocates Yarn, Fabric, Job Work, Batch)
             │
             ▼
  [ Garment Production Execution ] (Cutting → Printing → Stitching → Ironing)
             │
             ▼
  [ Final Quality Inspection (AQL) ] (Versa Quality: ANSI/ASQ Z1.4 / ISO 2859-1 Sampling)
             │
             ▼
  [ Packing Plan & Cartonization ] (Versa Export: Solid / Ratio Packing, Barcode Labels)
             │
             ▼
  [ Delivery Note / Shipping Bill ] (ERPNext Delivery Note + Export Container List)
             │
             ▼
  [ Sales Invoice & e-Invoicing ] (ERPNext Sales Invoice with GST / Export Benefits)
             │
             ▼
  [ Payment Collection & Aging ] (ERPNext Payment Entry + Receivables Follow-up)
```

---

## 3. Garment Order Matrix & Reconciliation Invariants

### 3.1 Matrix Architecture
Garment buyer orders are specified as a multi-dimensional matrix: $\text{Colour} \times \text{Size}$. Rather than forcing the merchandiser to enter dozens of separate SKU rows manually, Versa provides a dynamic matrix grid attached to the `Sales Order`:

```text
Style: ST-1002 (Men's Organic Crewneck T-Shirt)
+----------------+-----+-----+-----+-----+------+-------+
| Colour / Size  |  S  |  M  |  L  | XL  | XXL  | Total |
+----------------+-----+-----+-----+-----+------+-------+
| Jet Black      | 300 | 500 | 700 | 500 |  200 | 2,200 |
| Optical White  | 200 | 400 | 600 | 400 |  150 | 1,750 |
| Melange Grey   | 250 | 450 | 650 | 450 |  150 | 1,950 |
+----------------+-----+-----+-----+-----+------+-------+
| Total Pieces   | 750 |1,350|1,950|1,350|  500 | 5,900 |
+----------------+-----+-----+-----+-----+------+-------+
```

### 3.2 Full Lifecycle Quantity Reconciliation Invariants

For every cell $(c, s)$ in the order matrix:

1. **Production Quantity Invariant:**
   $$\text{Cutting Plan Qty}(c, s) = \text{Ordered Qty}(c, s) \times (1 + \text{Planned Cutting Allowance Pct})$$
2. **Packing Quantity Invariant:**
   $$\sum_{k \in \text{Cartons}} \text{CartonItem}_k(c, s).\text{qty} = \text{Packed Qty}(c, s) \le \text{Ordered Qty}(c, s) \times (1 + \text{Buyer Shipment Tolerance})$$
3. **Dispatch to Invoice Reconciliation Invariant:**
   $$\sum \text{Delivered Qty}(c, s) \equiv \sum \text{Invoiced Qty}(c, s)$$
4. **Order Completion Rule:**
   A `Sales Order` line is marked as `Fully Shipped` when:
   $$\text{Delivered Qty} \ge \text{Ordered Qty} \times (1 - \text{Short Shipment Tolerance})$$

---

## 4. Customer-Specific Governance & Commercial Controls

| Control / Check | Validation Mechanism | Exception / Escalation Path |
| :--- | :--- | :--- |
| **Credit Limit Check** | Total Outstanding + Unbilled Deliveries + Current SO $\le$ Approved Customer Credit Limit. | Hard block; requires Finance Director credit override concession. |
| **Overdue Invoices Block** | Evaluates presence of unpaid invoices past agreed payment terms (e.g. > 30 days overdue). | Blocks Sales Order submission and Delivery Note release. |
| **Minimum Order Margin** | Compares SO line price against Versa Style standard costing sheet margin threshold (e.g. $\ge 15\%$). | Triggers commercial review approval if margin drops below minimum. |
| **Buyer Tech Pack Conformance** | Mandates attached approved Tech Pack and Measurement Chart before SO release to Production. | Prevents creation of Production Work Orders in `versa_textile`. |

---

## 5. Export & Shipping Linkage

1. **Packing List Generation:** Versa Export aggregates `Versa Carton` records into container-level Packing Lists containing Gross Weight, Net Weight, Total CBM, and Piece breakdown.
2. **e-Way Bill & Shipping Bill Integration:** Connects carton weights and buyer tax/duty details with standard India Compliance / Export Documentation modules.

