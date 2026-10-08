# VERSA ERP — JOB WORK SEMANTIC GAP ANALYSIS

## 1. Executive Summary

Subcontracting ("Job Work") is the primary production architecture of the Tiruppur, Erode, and Salem textile clusters. Over 70% of wet processing (dyeing, bleaching, printing) and mechanical conversion (knitting, compacting, embroidery, washing) is outsourced to specialized third-party job workers.

This analysis evaluates **Native ERPNext Subcontracting**, **Aerele Apparelo**, **Fabric ERP**, and **ParaLogic Textile** against the **Versa Job Work Model**.

---

## 2. Comparative Matrix: Job Work Paradigms

| Feature / Domain Concept | ERPNext Native Subcontracting | Aerele Apparelo | Fabric ERP (KAK Textile) | ParaLogic Textile | Versa Job Work Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Operational Model** | Purchase Order with `is_subcontracted=1` + BOM consumption on Purchase Receipt. | Custom Job Work extension over Frappe Work Order & Job Cards. | Multi-stage process routing (Yarn $\to$ Greige $\to$ Dyed $\to$ Finished). | Roll-to-roll print job tracking with customized forked ledger. | **Versa Job Work Order (`VJWO`)**: Dedicated subcontracting orchestration document. |
| **Material Outward / Challan** | `Stock Entry (Send to Subcontractor)` to Supplier Warehouse. | `Stock Entry` linked to Work Order / Operation. | Outward Delivery Challan with gross/tare weight recording. | Outward print batch allocation. | Invariant-enforced `Stock Entry` auto-created on `VJWO` submit; GST Delivery Challan support. |
| **Vendor Qualification (AVL)** | Basic Supplier master; no mandatory capability or compliance gating. | Supplier rating field; manual review. | Vendor-process master mapping (e.g. Sizing Mill, Dyeing Unit). | Machine-specific printer profile. | **Approved Vendor List (AVL)**: Job Worker must have `status = 'Compliant'` and possess certified process capability in `Versa Job Worker Process`. |
| **Sequential Multi-Stage Routing** | Requires separate discrete Purchase Orders and separate intermediate item codes for every stage. | Linked Job Cards on single Work Order; cumbersome cross-vendor transport. | Multi-stage batch transitions across mill departments and external processors. | Specialized single-operation focus (Digital Print). | Direct stage-to-stage WIP handoff (`source_sales_order` / `previous_job_work_order`) without creating artificial intermediary item masters. |
| **Process Loss & Wastage** | Static scrap percentage in BOM; cannot adjust per batch easily. | Work Order scrap reporting. | Process loss % tracking with tolerance limits per fabric type. | Fixed ink/fabric wastage margin. | **Dynamic Allowed Loss %** (e.g. 3.0% for Knitting, 4.5% for Dyeing) with server-side threshold validation. |
| **Mass Balance Conservation** | No built-in physical mass conservation check between supplied mass and returned mass. | Basic quantity check against ordered pieces. | Physical mass conservation balance: Input $\equiv$ Output + Loss + Scrap. | Fabric meterage reconciliation. | **Strict Mass Balance Invariant (`job_work_mass_balance`)**: $\text{Issued Mass} \equiv \text{Output} + \text{Loss} + \text{Scrap} + \text{Returned} + \text{Unaccounted}$ ($\text{Unaccounted} \le 0.1\%$). |
| **Excess Loss Financial Settlement** | Manual manual debit note creation; no automatic link to job work bill. | Manual invoice deduction. | Automatic debit of excess yarn/fabric loss against job worker processing charges. | Manual settlement. | **Automated Excess Loss Debit**: Auto-populates `versa_excess_loss_debit` on `Purchase Invoice` to deduct unrecovered raw material cost from vendor processing bill. |
| **Partial & Staggered Receipts** | Handled via multiple Purchase Receipts against one PO. | Handled via partial Job Card completion. | Supported via lot-wise delivery logs. | Supported via roll batching. | **Child Table `results_received`**: Multi-delivery logging with cumulative yield tracking and progressive mass reconciliation. |
| **Stock Ledger Authority** | ERPNext Stock Ledger is authoritative. | ERPNext Stock Ledger is authoritative. | Custom SQL table updates in Spring Boot. | Custom forked ledger (non-standard). | **ERPNext Stock Ledger is sole authoritative inventory source**; Versa provides mass balance and yield governance. |

---

## 3. Deep Dive: Key Industry Gaps & Versa Solutions

### Gap 1: Intermediate Item Code Proliferation in Multi-Stage Job Work
- **The Problem:** In native ERPNext, passing 10,000 kg of Yarn through Knitting $\to$ Dyeing $\to$ Compacting $\to$ Printing requires creating 4 distinct Item Codes (`YARN-30S`, `FAB-GREIGE-30S`, `FAB-DYED-RED-30S`, `FAB-PRINTED-RED-30S`) and 4 separate BOMs. This creates master data explosion for seasonal fashion items.
- **Versa Solution:** `Versa Job Work Order` tracks the **Stage Output** (`received_item`, `process`) against the commercial root (`source_sales_order` or `Versa Style`), allowing material to progress across processes without forcing redundant master SKU proliferation.

### Gap 2: Fail-Open Process Loss & Financial Leakage
- **The Problem:** In standard ERP systems, if a job worker receives 1,000 kg of combed yarn and returns 920 kg of knitted fabric with no explanation for the remaining 80 kg, the invoice is often approved because standard tolerance checks only compare price and order quantity.
- **Versa Solution:** Versa enforces the **Mass Balance Invariant**. If process loss exceeds `allowed_loss_pct` (e.g. 30 kg allowed, 80 kg actual $\implies$ 50 kg excess loss), submission of the completion record is blocked until either:
  1. Returned unprocessed yarn / scrap is formally logged, or
  2. An **Excess Loss Debit** is automatically calculated ($50\text{ kg} \times \text{Yarn Valuation Rate}$) and deducted from the Job Worker's `Purchase Invoice`.

### Gap 3: Job Worker Capability & Compliance Gating
- **The Problem:** Unqualified or non-compliant subcontractors (e.g. dyeing units lacking Zero Liquid Discharge / ETP compliance or without the requisite machine gauge) are assigned work orders, causing quality rejections or legal liabilities.
- **Versa Solution:** `before_submit` hook on `Versa Job Work Order` validates that the vendor is in `Versa Job Worker` with `compliance_status == 'Compliant'` and has verified capability for the specific `process` in `Versa Job Worker Process`.

---

## 4. Recommended Phase 6 Implementation Blueprint

1. Retain ERPNext `Purchase Order` / `Purchase Receipt` / `Stock Entry` as the underlying inventory/accounting transaction layer.
2. Position `Versa Job Work Order` as the high-level operational controller that validates mass balance, computes yields, enforces AVL gating, and injects excess loss debits into `Purchase Invoice`.
3. Add sequential stage chaining fields (`previous_job_work_order`, `next_process`) in Phase 6 without modifying core schemas now.
