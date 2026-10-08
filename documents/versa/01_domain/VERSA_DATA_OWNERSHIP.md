# VERSA ERP DATA OWNERSHIP & SYSTEM OF RECORD (SoR) BOUNDARY

## 1. Objective and Authority Principles

To prevent data duplication, split-brain accounting, and synchronization drift, this document defines the **Authoritative System of Record (SoR)** for every business object across the **GraphModel (Design-time)**, **ERPNext Core**, and **Versa Extensions** landscape.

### Core Authority Laws:
1. **Financial & Accounting Authority:** ERPNext General Ledger (`tabGL Entry`) is the sole system of record for monetary values, payable/receivable balances, tax calculations (GST), and asset valuation. Versa modules never create standalone financial ledgers.
2. **Stock Valuation & Legal Inventory Authority:** ERPNext Stock Ledger (`tabStock Ledger Entry`) is the authoritative source for warehouse on-hand quantities, FIFO/moving-average valuation, and legal stock movements. Versa Fabric Roll and Carton models act as physical tracking overlays referencing ERPNext stock batches and warehouses.
3. **Product Engineering & Domain Authority:** Versa applications are the authoritative SoR for textile engineering specifications (Yarn, Fabric, GSM, Shrinkage), Garment Styles (BOM, Routing, Colourways, Sizes), Subcontracting Mass Balances, and Multi-parameter Quality Evidence.

---

## 2. Authoritative System of Record (SoR) Matrix

| Business Data / Entity | Authoritative SoR | Secondary / Consumer Systems | Synchronization & Integration Pattern |
| :--- | :--- | :--- | :--- |
| **Legal Company & Currency** | `ERPNext Core` | Versa Core, Versa Textile | Linked via `company` foreign key on all Versa documents. |
| **Chart of Accounts & GL** | `ERPNext Core` | Versa Reporting | Read-only analytics; transactions post via ERPNext standard invoices. |
| **Customer Master** | `ERPNext Core` | Versa Style, Versa O2C | Linked via `customer` Link field; extended with buyer brand attributes. |
| **Supplier Master** | `ERPNext Core` | Versa Job Work, Versa P2P | Linked via `supplier` Link field. |
| **Base Item Master** | `ERPNext Core` | Versa Material Spec | Base SKU defines valuation and tax; Versa attaches technical specifications. |
| **Warehouse & Bin Quantities**| `ERPNext Core` | Versa Fabric Roll | Fabric rolls sum to match ERPNext `Bin.actual_qty` in Kg/Meters. |
| **Textile Material Spec** | `Versa Textile` | ERPNext Item, Work Orders | Versa owns composition, spinning count, fabric construction, GSM. |
| **Colour & Shade Masters** | `Versa Textile` | Style Colourways, Job Work | Standardized colour codes referenced across styles and lab dips. |
| **Fabric Roll Traceability** | `Versa Textile` | ERPNext Stock Ledger | Roll barcode tracks piece length, weight, GSM, defect score; links to ERPNext Batch. |
| **Garment Style (Tech Pack)** | `Versa Textile` | ERPNext BOM / Work Order | Style holds canonical master; generates standard ERPNext BOM on production release. |
| **Order Matrix (Colour×Size)**| `Versa Textile` | ERPNext Sales Order | Matrix grid on Sales Order generates/reconciles standard `Sales Order Item` lines. |
| **Job Worker Capability Profile**| `Versa Job Work` | ERPNext Supplier | Captures machine gauge, capacity, loss tolerances; links to `Supplier`. |
| **Job Work Subcontract Order**| `Versa Job Work` | ERPNext Stock Entry | Versa tracks process parameters & yields; posts ERPNext `Stock Entry` for material issue/receipt. |
| **Mass Balance & Process Loss**| `Versa Job Work` | ERPNext Purchase Invoice | Calculates scrap/loss debits applied to Job Worker settlement invoices. |
| **QC Specifications & Limits** | `Versa Quality` | Inspection Engine | Versioned technical parameters, test methods, tolerances. |
| **QC Physical Measurements** | `Versa Quality` | ERPNext Quality Inspection| Captures multi-point physical readings; pushes pass/fail disposition to ERPNext receipt. |
| **Cartonization & Packing Plan**| `Versa Export` | ERPNext Delivery Note | Versa allocates pieces to cartons; generates packing list for Delivery Note. |

---

## 3. Product Layer Classification

To maximize multi-customer platform reusability and prevent custom code contamination, all functionality is strictly classified into 4 layers:

```text
+-------------------------------------------------------------------+
| 4. CUSTOMER CUSTOMIZATION (One-off reports, bespoke legacy imports)|
+-------------------------------------------------------------------+
| 3. CUSTOMER CONFIGURATION (Workflows, print formats, approval bands)|
+-------------------------------------------------------------------+
| 2. VERSA INDUSTRY (Tiruppur Textile, Dyeing, Job Work, Packing)   |
+-------------------------------------------------------------------+
| 1. VERSA CORE (Approval matrix, credit policy, portal, multi-BU)  |
+-------------------------------------------------------------------+
| 0. ERPNext / Frappe (Accounting, Stock, Purchasing, Sales, HR)     |
+-------------------------------------------------------------------+
```

### 3.1 Layer Breakdown

1. **VERSA CORE (Cross-Industry Foundation):**
   - Multi-tier dynamic approval matrices (amount, cost center, item group).
   - Unified credit policy, credit limit evaluation, overdue invoice hold engines.
   - Branch / Business Unit scoping and user permission templates.
   - Reusable notification, exception escalation, and audit logging utilities.
2. **VERSA INDUSTRY (Tiruppur Textile & Garment Pack):**
   - Yarn & Fabric specifications and dual-UOM calculators.
   - Physical Fabric Roll barcode tracking and ASTM 4-point defect grading.
   - Garment Style master, BOM/Routing formulations, and colour-by-size order matrix.
   - Distributed Job Work subcontracting orders with mass-balance reconciliation.
   - Multi-parameter textile QC testing (GSM, shrinkage %, spirality %, fastness).
   - Cartonization, ratio packing plans, and export container packing lists.
3. **CUSTOMER CONFIGURATION (Zero-Code Customization):**
   - Company-specific approval hierarchies (configured via `Versa Approval Rule`).
   - Buyer-specific AQL sampling levels and measurement tolerance bands.
   - Custom print formats, barcode labels, and email notification triggers.
   - Custom dashboard KPIs and saved report views.
4. **CUSTOMER CUSTOMIZATION (Isolated Bespoke Extensions):**
   - Legacy data migration scripts.
   - Proprietary third-party hardware integrations (e.g. legacy circular knitting machine counters).
   - Specific buyer electronic data interchange (EDI) format adapters.

---

## 4. Multi-Company & Multi-Tenant Isolation Strategy

1. **Company Scoping Invariant:** Every Versa master and transactional DocType includes a mandatory, indexed `company` field linked to `tabCompany`.
2. **Permission Query Governance:** Frappe permission queries (`permission_query_conditions`) automatically inject `company IN (user_permitted_companies)` to enforce strict multi-company data segregation.
3. **Master Data Sharing:** Standard industry taxonomies (e.g., `Versa Colour`, `Versa QC Spec`) can be flagged as `is_global` or scoped to a specific `company` depending on tenant configuration.

