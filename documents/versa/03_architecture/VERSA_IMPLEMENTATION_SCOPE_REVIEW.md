# VERSA ERP — IMPLEMENTATION SCOPE & MVP REVIEW

## 1. Executive Summary & Objective

This document performs a critical scoping review of the Versa ERP implementation specification to distinguish between the **Minimum Viable Implementation (Phase 1 Essential Foundation)** and deferred capabilities, ensuring the coding phase focuses on high-impact core operations without implementing ungrounded abstractions or premature complexities.

---

## 2. Four-Tier Scope Categorization Framework

```text
================================================================================
                    IMPLEMENTATION SCOPE CLASSIFICATION
================================================================================
1. MUST HAVE (Phase 1 — Core Operational Engine):
   Essential DocTypes, invariants, and hooks required for basic P2P, O2C,
   Job Work, Quality Gate, and Fabric Roll traceability.

2. SHOULD HAVE (Phase 2 — Advanced Operational Features):
   Ratio packing optimization, multi-level approval matrices, containerization,
   and dynamic batch yield recalculation.

3. DEFER (Phase 3 / Customer Validation Required):
   Destructive fabric roll lab sampling intervals, normalized blend composition
   child tables, and multi-tenant inter-company subcontract tax routing.

4. DO NOT IMPLEMENT YET (Out of Scope):
   Generic LIMS laboratory workflow engine, custom stock ledger tables,
   parallel general ledgers, and standalone machine IoT integrations.
================================================================================
```

---

## 3. Detailed Component-by-Component Scope Breakdown

### 3.1 MUST HAVE (Phase 1 Essential Foundation)

| Canonical Entity / Feature | App / Platform | Scope Rationale | Invariants Enforced |
| :--- | :--- | :--- | :--- |
| **`Company`, `Cost Center`, `Warehouse`** | `erpnext` | Legal boundary, tenant isolation, storage locations | `multi_company_isolation` |
| **`Item`, `Batch`** | `erpnext` | Inventory catalog and dye lot tracking | Stock Ledger authority |
| **`Customer`, `Supplier`** | `erpnext` | Commercial buyer and vendor/job worker masters | Vendor AVL check |
| **`Sales Order` + `Versa Order Matrix`** | `erpnext` + `versa_textile` | Multi-dimensional matrix order entry and validation | `order_matrix_conservation` |
| **`Purchase Order`, `Purchase Receipt`** | `erpnext` | Procurement execution and incoming stock gate | `quality_gate_enforcement` |
| **`Stock Entry`** | `erpnext` | Authoritative stock movements for raw materials and job work | Single Stock Ledger |
| **`Purchase Invoice`, `Sales Invoice`** | `erpnext` | Authoritative financial AP/AR billing | `three_way_matching`, `dispatch_invoice_reconciliation` |
| **`Versa Style` + Child Tables** | `versa_textile` | Garment tech pack sheet, BOM consumption, colourways, sizes | Style BOM explosion |
| **`Versa Fabric Roll`** | `versa_textile` | Physical barcode serialization, length, actual GSM, width | `fabric_roll_dual_uom_conservation` |
| **`Versa Job Worker` + `Process`** | `versa_jobwork` | Subcontractor profile, machine capability, compliance | AVL check |
| **`Versa Job Work Order` + Tables** | `versa_jobwork` | Subcontracting execution, stock issue/receipt, mass balance | `job_work_mass_balance`, `job_work_excess_loss_penalty` |
| **`Versa QC Spec` & `Versa QC Result`** | `versa_quality` | Lab test methods, multi-point readings, pass/reject gate | `quality_gate_enforcement`, `astm_d5430_4point_defect_scoring` |
| **`Versa Approval Rule`** | `versa_core` | Basic threshold approvals for SO, PO, and Job Work Orders | Approval enforcement |

---

### 3.2 SHOULD HAVE (Phase 2 Operational Features)

| Feature / DocType | App | Purpose |
| :--- | :--- | :--- |
| **`Versa Packing Plan` & `Versa Carton`** | `versa_export` | Ratio/solid cartonization, net/gross weights, carton barcodes (`carton_packing_conservation`). |
| **Supplier OTIF Analytics** | `versa_core` | Background scoring job updating on-time in-full delivery performance indices. |
| **Barcode Scan REST API** | `versa_textile` | Mobile floor scanning endpoint for rapid roll receipt and issue. |
| **Mass Balance Auto-Reconcile API** | `versa_jobwork` | Subcontractor batch closure API calculating yield and material debit adjustments. |
| **Concession Dual Sign-Off** | `versa_quality` | Workflow requiring Quality Head + Merchandiser sign-off on out-of-spec goods. |

---

### 3.3 DEFER (Phase 3 / Customer Validation Required)

| Deferred Item | Identifier | Reason for Deferral | Customer Validation Action |
| :--- | :--- | :--- | :--- |
| **Fabric Roll Physical Sampling Protocol** | `ASM-002 / OPEN` | Destructive/non-destructive sample cut intervals across roll lengths vary by buyer standard (e.g. M&S vs Next). | Validate in customer discovery workshop during bench commissioning. |
| **Weighing Scale Tolerance Threshold** | `ASM-001` | Whether $\le 0.1\%$ is global or configurable per chemical/wet process. | Set as configurable parameter in `Company` settings. |
| **Normalized Material Composition Child Table** | `ASM-011` | Text composition (e.g. "95% Cotton 5% Elastane") is sufficient for Phase 1/2; normalized multi-fiber table only needed for advanced analytics. | Revisit in Phase 4. |
| **Inter-Company Subcontracting Tax Routing** | `ASM-012` | GST e-invoicing for intra-group jobs vs internal Cost Center allocation depends on legal group structure. | Configure per client setup. |

---

### 3.4 DO NOT IMPLEMENT YET (Strictly Out of Scope)

```text
================================================================================
STRICTLY PROHIBITED IMPLEMENTATION ANTI-PATTERNS & PREMATURE SCOPE:
================================================================================
1. Parallel Stock Ledger / Inventory Balance Tables:
   Under no circumstances may Versa create custom tables tracking inventory
   quantities or valuation balances. ERPNext Stock Ledger Entry is the sole authority.

2. Parallel General Ledger / Accounts Payable Tables:
   No custom journal or GL tables. All debits/credits must post through ERPNext GL Entry.

3. Generic LIMS (Laboratory Information Management System):
   Versa Quality must focus strictly on textile parameters (GSM, Count, CSP, Fastness,
   Shrinkage, Spirality, 4-Point Grading). Do not build generic lab sample tracking.

4. Direct Machine IoT / OPC-UA / Modbus Hardware Integration:
   Hardware integrations for knitting counters and stenter temperature loggers are
   Phase 5 roadmap items. Phase 1/2 use manual / barcode scan data capture.

5. Direct Runtime GraphModel Linkage:
   Zero GraphModel Python code, packages, or database schemas inside Frappe.
================================================================================
```
