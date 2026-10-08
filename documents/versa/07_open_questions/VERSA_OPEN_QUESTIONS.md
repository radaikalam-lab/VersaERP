# VERSA ERP OPEN ARCHITECTURAL QUESTIONS & VALIDATION LOG

## 1. Context & Purpose

This document catalogs open architectural and operational questions extracted from the analysis of `Source/Versa_ERP_Platform_Strategy_Tiruppur.docx` and standard Tiruppur manufacturing workflows. These questions highlight areas requiring customer validation during Phase 0 discovery before freezing implementation schemas.

---

## 2. Structured Open Questions Matrix

### Question 1: Item Variant Explosion vs. Specification Decoupling
- **Source / Context:** Strategy Document Section 6.2, 8.1, Appendix A.1.
- **Affected Entities:** `Item`, `Versa Material Spec`, `Versa Yarn Spec`, `Versa Fabric Spec`.
- **Affected Workflows:** Master Data creation, Sales Order entry, Stock Ledger valuation.
- **Why It Matters:** Generating ERPNext Item Variants for every permutation of (Fibre $\times$ Count $\times$ Mill $\times$ Structure $\times$ GSM $\times$ Width $\times$ Finish $\times$ Colour $\times$ Shade) can easily produce $>50,000$ Item master records, degrading UI search performance and database index caches.
- **Possible Interpretations:**
  - *Option A (ERPNext Standard Variants):* Create explicit Item Variants for every colour/shade/GSM combination.
  - *Option B (Decoupled Spec + Batch/Roll Attributes):* Maintain generic Item masters (e.g. "Cotton Greige Fabric 30s Single Jersey") and store specific GSM, shade, and width attributes on `Versa Fabric Spec`, `Batch`, and `Versa Fabric Roll`.
- **Recommended Decision:** **Adopt Option B.** Maintain standard Item SKUs at the generic construction level and attach `Versa Material Spec` and lot/roll-level attributes. This preserves ERPNext database performance while maintaining complete technical detail.

---

### Question 2: Fabric Roll Dual-UOM Stock Ledger Integration
- **Source / Context:** Strategy Document Section 6.2, Appendix A.3.
- **Affected Entities:** `Versa Fabric Roll`, `Stock Ledger Entry`, `Bin`.
- **Affected Workflows:** Purchase Receipt, Stock Entry (Material Issue to Cutting), Inventory Valuation.
- **Why It Matters:** Fabric in Tiruppur is purchased and costed by Weight ($kg$) but consumed and laid in cutting tables by Length ($m$). Standard ERPNext tracks valuation on a single primary UOM with fixed secondary UOM conversion factors, but fabric roll density varies dynamically by sample GSM and moisture.
- **Possible Interpretations:**
  - *Option A (ERPNext Primary UOM = Kg):* Use $kg$ as the stock valuation UOM in ERPNext; track meters as a dynamic physical attribute on `Versa Fabric Roll`.
  - *Option B (ERPNext Secondary UOM with strict conversion):* Force ERPNext dual-UOM on every stock transaction.
- **Recommended Decision:** **Adopt Option A.** ERPNext stock ledger and inventory valuation are maintained strictly in $kg$. Physical cutting issuance, roll allocation, and meter calculations are managed in `versa_textile` through `Versa Fabric Roll` records referencing the stock batch.

---

### Question 3: Subcontracting Architecture (ERPNext Subcontracting PO vs. Dedicated Versa Job Work Order)
- **Source / Context:** Strategy Document Section 10, Appendix A.5.
- **Affected Entities:** `Purchase Order` (Subcontracting), `Subcontracting Receipt`, `Versa Job Work Order`.
- **Affected Workflows:** Job Work Issue, Process Loss calculation, Scrap Debit note generation.
- **Why It Matters:** ERPNext v14+ introduced a dedicated Subcontracting Module (`Subcontracting Order`, `Subcontracting Receipt`). However, ERPNext standard subcontracting assumes discrete item conversion rather than textile multi-step mass-balance (e.g. Yarn $\to$ Greige $\to$ Dyed $\to$ Compacted) with dynamic moisture/loss percentages and scrap accounting.
- **Possible Interpretations:**
  - *Option A (Pure Versa Job Work Order):* Build a purpose-built `Versa Job Work Order` that manages operational issue/receipt via standard `Stock Entry` and generates a standard `Purchase Invoice` for service charges.
  - *Option B (Extend ERPNext Subcontracting Order):* Inject custom fields into ERPNext's `Subcontracting Order`.
- **Recommended Decision:** **Adopt Option A.** `Versa Job Work Order` provides full mass-balance conservation, multi-stage yield tracking, and scrap debit automation without being constrained by ERPNext's rigid subcontracting BOM assumptions.

---

### Question 4: Colour × Size Matrix Persistence Architecture
- **Source / Context:** Strategy Document Section 9, Appendix A.4.
- **Affected Entities:** `Sales Order`, `Sales Order Item`, `Versa Order Matrix`.
- **Affected Workflows:** Order Booking, Production Planning, Packing, Invoicing.
- **Why It Matters:** Garment buyers order via a 2D grid ($\text{Colour} \times \text{Size}$). Standard ERPNext transactions require flat `Sales Order Item` lines for tax, pricing, and fulfillment tracking.
- **Possible Interpretations:**
  - *Option A (Pure UI Grid with auto-generated Item rows):* The matrix is an interactive Frappe client-side UI that populates standard `Sales Order Item` child table rows behind the scenes.
  - *Option B (Dual Child Tables):* Maintain `Versa Order Matrix` as an independent child table on `Sales Order` and synchronize with `Sales Order Item` via server-side `before_save` hooks.
- **Recommended Decision:** **Adopt Option B.** Storing both the matrix grid and the line items ensures seamless reporting in standard ERPNext accounting while giving garment merchandisers native matrix editing and status tracking.

---

### Question 5: Multi-Company and Inter-Company Job Work Scoping
- **Source / Context:** Strategy Document Section 14, 21, Appendix A.15.
- **Affected Entities:** `Versa Job Work Order`, `Company`, `Supplier`.
- **Affected Workflows:** Sister-concern subcontracting (e.g. spinning mill, knitting unit, and garment exporter under the same group).
- **Why It Matters:** In many Tiruppur conglomerates, knitting and dyeing are executed by sister companies. Transactions can be internal stock transfers or formal legal inter-company purchases.
- **Possible Interpretations:**
  - *Case 1 (External Job Worker):* Standard Subcontracting workflow with vendor service invoice.
  - *Case 2 (Sister Concern / Internal BU):* Internal Stock Transfer between Cost Centers / Companies without service GST invoice.
- **Recommended Decision:** Support both modes via a `is_internal_subcontract` flag on `Versa Job Work Order`. If internal, post Inter-Company Stock Transfers; if external, post standard Job Work Receipts and Supplier Service Invoices.

---

### Question 6: Supplier OTIF On-Time and In-Full Formal Reconciliation Rules
- **Source / Context:** Strategy Document Section 8.3, `VERSA_P2P_CONTRACT.md` Section 5.4, `versa_domain_model.json` DERIVED_METRIC `supplier_otif_scoring`.
- **Affected Entities:** `Supplier`, `Purchase Order`, `Purchase Receipt`, `Purchase Order Item`.
- **Affected Workflows:** GRN Submission, Supplier Performance Dashboard, Vendor Rating.
- **Why It Matters:** The high-level formula $\text{OTIF} = (\text{On-Time In-Full Receipts} / \text{Total Receipts}) \times 100$ leaves operational reconciliation rules unspecified:
  1. *On-Time Definition:* Is the comparison date `Purchase Receipt.posting_date` against `Purchase Order.schedule_date` at header or line item? What grace period or tolerance days apply?
  2. *In-Full Definition:* How are split shipments evaluated? Is a partial delivery penalized as not-in-full, or evaluated cumulatively against PO line quantities with standard yarn/fabric weight tolerances ($\pm 3\%$)?
  3. *Zero History / Cancellation Handling:* How are newly onboarded vendors or canceled receipts scored without distorting analytics?
- **Possible Interpretations:**
  - *Option A (Line-Level Cumulative Matching):* Background job compares accumulated receipt quantities per PO line against line-level schedule dates and tolerance bands.
  - *Option B (Header-Level Binary Evaluation):* Each GRN is scored based on whether `posting_date <= required_date` and `per_received == 100`.
- **Recommended Decision:** **Adopt Option A as target design during Phase 0 Discovery.** Defer runtime calculation in `versa_core` (per DEC-007) until the exact line matching tolerance rules are finalized in customer workshops.


