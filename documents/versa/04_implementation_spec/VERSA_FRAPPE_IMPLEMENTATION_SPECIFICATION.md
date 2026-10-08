# VERSA ERP — FRAPPE / ERPNext IMPLEMENTATION SPECIFICATION

## 1. Authoritative Architecture & Runtime Boundaries

This document defines the authoritative, frozen implementation specification for the Versa ERP platform on Frappe Framework v15 and ERPNext v15.

```text
================================================================================
                    ARCHITECTURAL RUNTIME BOUNDARY
================================================================================
  [ E:\GraphModel ] (Design-Time Semantic Analysis Environment)
         │
         │  * Canonical Domain Extraction
         │  * Invariant Formalization & Audit
         │  * Contract Reconciliation
         │  * Design-Time Specification Generation
         │
         ▼  (ZERO RUNTIME LINKAGE / NO CODE IMPORT)
  [ E:\VersaERP\bench ] (Frappe / ERPNext Runtime Platform)
         │
         ├── frappe (v15 Engine)
         ├── erpnext (v15 Transactional & Accounting Core)
         ├── india_compliance (GST, e-Way Bill, e-Invoicing)
         │
         ├── versa_core (App: Governance, Approvals & Common Utilities)
         ├── versa_textile (App: Textile Masters, Specs, Fabric Rolls, Styles)
         ├── versa_jobwork (App: Subcontracting, Mass Balance & Yield)
         ├── versa_quality (App: Multi-Tier QC Specs & Lab Measurements)
         └── versa_export (App: Ratio Packing, Cartonization & Containerization)
================================================================================
```

### 1.1 Non-Negotiable Architectural Rules
1. **GraphModel is Design-Time Only:** GraphModel must never become a Python runtime dependency, git submodule, package requirement, or runtime service of Versa ERP.
2. **Single Source of Truth:** ERPNext `Stock Ledger Entry` and `GL Entry` are the sole and absolute authorities for inventory valuation, warehouse quantities, accounts payable, accounts receivable, and general ledger postings. Versa custom DocTypes orchestrate domain-specific lifecycles and push transactional movements into standard ERPNext documents. No parallel stock or accounting ledger is permitted.
3. **Canonical Semantic Preservation:** All 39 canonical entities, 28 relationships, and 13 invariants/rules formalized in `versa_domain_model.json` are fully mapped into Frappe metadata without dropping domain constraints.

---

## 2. Frappe Application Structure & Modular Organization

The Versa ERP suite is organized into 5 modular Frappe applications located under `E:\VersaERP\bench\apps\`:

```text
E:\VersaERP\bench\apps\
├── versa_core/                  # Governance, Approval Matrices, Multi-Company Query Conditions
├── versa_textile/               # Yarn/Fabric Specs, Fabric Roll Traceability, Styles, Order Matrix
├── versa_jobwork/               # Job Workers, Job Work Orders, Mass Balance & Yield Reconciliation
├── versa_quality/               # Versioned QC Specs, Lab Measurements, Quality Gates & Dispositions
└── versa_export/                # Ratio Packing Plans, Carton Barcode Serialization, Packing Lists
```

### App Dependencies Hierarchy
```text
erpnext
  └── versa_core
        ├── versa_textile
        │     ├── versa_jobwork
        │     └── versa_export
        └── versa_quality (cross-cutting QC gates for P2P, Job Work, and Textile)
```

---

## 3. Canonical DocType Specifications (All 39 Entities)

### 3.1 ERPNext Reused & Extended Standard DocTypes (14 Entities)

These entities represent standard ERPNext DocTypes that are extended via custom fields (`fixtures/custom_field.json`), custom child tables, and controller event hooks (`hooks.py`). Standard ERPNext core files remain 100% untouched.

```
Entity Breakdown:
1. Company (SHARED_MASTER)
2. Cost Center (COMPANY_OWNED)
3. Customer (SHARED_MASTER)
4. Supplier (SHARED_MASTER)
5. Item (SHARED_MASTER)
6. Warehouse (COMPANY_OWNED)
7. Batch (SHARED_MASTER)
8. Sales Order (COMPANY_SCOPED_TRANSACTION)
9. Purchase Order (COMPANY_SCOPED_TRANSACTION)
10. Purchase Receipt (COMPANY_SCOPED_TRANSACTION)
11. Delivery Note (COMPANY_SCOPED_TRANSACTION)
12. Purchase Invoice (COMPANY_SCOPED_TRANSACTION)
13. Sales Invoice (COMPANY_SCOPED_TRANSACTION)
14. Stock Entry (COMPANY_SCOPED_TRANSACTION)
```

#### 1. Company
- **Frappe DocType:** `Company` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `Prompt` / Field `company_name`
- **Business Purpose:** Legal entity boundary, chart of accounts root, and statutory GST entity.
- **Versa Extension:** Standard ERPNext authority. Custom fields: `versa_default_jobwork_loss_tolerance` (Float, Default: 3.0), `versa_enable_fabric_roll_quarantine` (Check, Default: 1).
- **Provenance:** `SOURCE`

#### 2. Cost Center
- **Frappe DocType:** `Cost Center` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `COMPANY_OWNED` | **Autoname:** `Prompt` / Field `cost_center_name`
- **Business Purpose:** Operational department / mill division cost accounting.
- **Versa Extension:** Custom field `versa_business_unit_type` (Select: `Spinning Mill`, `Knitting Unit`, `Dyeing House`, `Printing Unit`, `Garment Stitching`, `Finishing & Packing`, `Corporate`).
- **Provenance:** `SOURCE`

#### 3. Customer
- **Frappe DocType:** `Customer` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `Prompt` / Field `customer_name`
- **Business Purpose:** Buyer entity for garment export orders and domestic retail accounts.
- **Versa Extension:** Custom fields: `versa_buyer_code` (Data, Unique), `versa_default_aql_level` (Select: `Level I`, `Level II`, `Level III`, Default: `Level II`), `versa_shipment_tolerance_pct` (Float, Default: 5.0).
- **Provenance:** `SOURCE`

#### 4. Supplier
- **Frappe DocType:** `Supplier` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `Prompt` / Field `supplier_name`
- **Business Purpose:** Raw material vendor (yarn mill, dye supplier) and job work subcontractor.
- **Versa Extension:** Links 1-to-1 to `Versa Job Worker` if `supplier_type == 'Job Worker'`. Custom fields: `versa_otif_score` (Float, Read-only), `versa_quality_rating` (Float, Read-only).
- **Provenance:** `SOURCE`

#### 5. Item
- **Frappe DocType:** `Item` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `Prompt` / Field `item_code`
- **Business Purpose:** Inventory SKU master for raw materials, trims, fabric, and finished garments.
- **Versa Extension:** Custom fields: `versa_item_category` (Select: `Yarn`, `Greige Fabric`, `Finished Fabric`, `Dye/Chemical`, `Trim/Accessory`, `Garment SKU`, `Packing Material`), `versa_material_spec` (Link: `Versa Material Spec`), `is_fabric_roll_tracked` (Check, Default: 0), `is_qc_required` (Check, Default: 1).
- **Provenance:** `SOURCE`

#### 6. Warehouse
- **Frappe DocType:** `Warehouse` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `COMPANY_OWNED` | **Autoname:** `Prompt` / Field `warehouse_name`
- **Business Purpose:** Physical storage location for raw materials, in-process goods, job work transit, and finished stock.
- **Versa Extension:** Custom fields: `versa_warehouse_type` (Select: `Raw Material Store`, `Job Worker Subcontract Store`, `Quarantine Inspection Store`, `Active Floor Store`, `Export Finished Goods Store`), `versa_job_worker` (Link: `Versa Job Worker`, depends_on: `eval:doc.versa_warehouse_type=='Job Worker Subcontract Store'`).
- **Provenance:** `SOURCE`

#### 7. Batch
- **Frappe DocType:** `Batch` | **App:** `erpnext` | **Type:** Master (Standard)
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `Prompt` / `BATCH-.YYYY.-.#####.`
- **Business Purpose:** Lot tracking unit for yarn dye lots, fabric dye batches, and chemical lots.
- **Versa Extension:** Custom fields: `versa_dye_lot_no` (Data), `versa_shade` (Link: `Versa Shade`), `versa_qc_status` (Select: `Quarantine`, `QC Passed`, `Concession`, `Rejected`, Default: `Quarantine`).
- **Provenance:** `SOURCE`

#### 8. Sales Order
- **Frappe DocType:** `Sales Order` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `SO-.YYYY.-.#####.`
- **Business Purpose:** Commercial commitment from garment buyer.
- **Versa Extension:**
  - Embedded Child Table: `versa_order_matrix` (Table: `Versa Order Matrix`).
  - Custom fields: `versa_style` (Link: `Versa Style`), `versa_season` (Data), `versa_packing_status` (Select: `Unplanned`, `Partially Packed`, `Fully Packed`, Default: `Unplanned`), `versa_approval_rule` (Link: `Versa Approval Rule`).
  - Validation Hook: `before_save` synchronizes `Versa Order Matrix` totals with `Sales Order Item` lines.
- **Provenance:** `SOURCE`

#### 9. Purchase Order
- **Frappe DocType:** `Purchase Order` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `PO-.YYYY.-.#####.`
- **Business Purpose:** Procurement order for raw materials, yarn, accessories, or dyes.
- **Versa Extension:** Custom fields: `versa_material_spec` (Link: `Versa Material Spec`), `versa_approval_rule` (Link: `Versa Approval Rule`), `versa_tolerance_pct` (Float, Default: 3.0).
- **Provenance:** `SOURCE`

#### 10. Purchase Receipt
- **Frappe DocType:** `Purchase Receipt` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `MAT-PRE-.YYYY.-.#####.`
- **Business Purpose:** Physical goods receipt note (GRN).
- **Versa Extension:**
  - Custom fields: `versa_qc_result` (Link: `Versa QC Result`), `versa_qc_status` (Select: `Pending QC`, `QC Passed`, `Concession`, `Rejected`, Default: `Pending QC`).
  - Event Hooks: `before_submit` enforces QC gate (hard block if `is_qc_required == 1` and `versa_qc_status != 'QC Passed'`). `on_submit` auto-generates `Versa Fabric Roll` records for fabric items.
- **Provenance:** `SOURCE`

#### 11. Delivery Note
- **Frappe DocType:** `Delivery Note` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `MAT-DN-.YYYY.-.#####.`
- **Business Purpose:** Dispatch and shipping note for export container shipment or domestic delivery.
- **Versa Extension:** Custom fields: `versa_packing_plan` (Link: `Versa Packing Plan`), `versa_total_cartons` (Int, Read-only), `versa_net_weight_kg` (Float, Read-only), `versa_gross_weight_kg` (Float, Read-only).
- **Provenance:** `SOURCE`

#### 12. Purchase Invoice
- **Frappe DocType:** `Purchase Invoice` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `ACC-PINV-.YYYY.-.#####.`
- **Business Purpose:** Financial vendor bill and Job Worker processing charge settlement.
- **Versa Extension:** Custom fields: `versa_job_work_order` (Link: `Versa Job Work Order`), `versa_excess_loss_debit` (Currency, Default: 0.0), `versa_3way_matched` (Check, Read-only).
- **Provenance:** `SOURCE`

#### 13. Sales Invoice
- **Frappe DocType:** `Sales Invoice` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `ACC-SINV-.YYYY.-.#####.`
- **Business Purpose:** Financial billing document for shipped garments with GST/e-Invoicing integration.
- **Versa Extension:** Custom fields: `versa_style` (Link: `Versa Style`), `versa_order_matrix_reconciled` (Check, Default: 1).
- **Provenance:** `SOURCE`

#### 14. Stock Entry
- **Frappe DocType:** `Stock Entry` | **App:** `erpnext` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `MAT-STE-.YYYY.-.#####.`
- **Business Purpose:** Authoritative inventory movement ledger for raw material issue, job work transfer, and cutting issue.
- **Versa Extension:**
  - Custom fields: `versa_job_work_order` (Link: `Versa Job Work Order`), `versa_fabric_roll` (Link: `Versa Fabric Roll`).
  - Event Hook: `on_submit` updates physical `Versa Fabric Roll` status (`Issued to Cutting`, `Issued to Job Work`, `Consumed`).
- **Provenance:** `SOURCE`

---

### 3.2 Versa Custom Masters & Extensions (8 Entities)

#### 15. Versa Material Spec
- **Frappe DocType:** `Versa Material Spec` | **App:** `versa_textile` | **Type:** Master
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `VMS-.item.-.version.`
- **Business Purpose:** Master technical specification sheet for yarns, fabrics, dyes, and trims.
- **Fields:**
  - `item` (Link: `Item` [Mandatory, Immutable])
  - `specification_version` (Data [Mandatory, Default: 'V1.0', Immutable])
  - `material_type` (Select: `Yarn`, `Fabric`, `Dye/Chemical`, `Trim/Accessory`, `Packing Material` [Mandatory])
  - `composition` (Data: e.g. "100% Combed Cotton" [Mandatory])
  - `is_active` (Check: Default 1)
  - `approval_status` (Select: `Draft`, `Approved`, `Obsolete` [Default: 'Draft'])
- **Indexes:** Unique index on `(item, specification_version)`.
- **Provenance:** `SOURCE`

#### 16. Versa Yarn Spec
- **Frappe DocType:** `Versa Yarn Spec` | **App:** `versa_textile` | **Type:** Master Extension
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `VYS-.material_spec.`
- **Business Purpose:** Specialized spinning and physical yarn parameters.
- **Fields:**
  - `material_spec` (Link: `Versa Material Spec` [Mandatory, Unique, Immutable])
  - `yarn_count` (Data [Mandatory, e.g. "30s", "34s", "40s"])
  - `count_system` (Select: `Ne`, `Nm`, `Denier`, `Tex` [Mandatory, Default: 'Ne'])
  - `ply` (Int [Mandatory, Default: 1])
  - `spinning_process` (Select: `Combed`, `Carded`, `Compact`, `Open End`, `Air Jet` [Mandatory])
  - `blend_ratio` (Data [Mandatory, e.g. "100% Cotton", "60/40 CVC"])
  - `csp_min` (Float [Default: 2800.0])
  - `twist_direction` (Select: `Z`, `S` [Default: 'Z'])
  - `origin_mill` (Data)
- **Provenance:** `SOURCE`

#### 17. Versa Fabric Spec
- **Frappe DocType:** `Versa Fabric Spec` | **App:** `versa_textile` | **Type:** Master Extension
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `VFS-.material_spec.`
- **Business Purpose:** Specialized knitting/weaving structure and finishing parameters.
- **Fields:**
  - `material_spec` (Link: `Versa Material Spec` [Mandatory, Unique, Immutable])
  - `fabric_structure` (Select: `Single Jersey`, `1x1 Rib`, `2x2 Rib`, `Interlock`, `Fleece`, `Pique`, `Waffle`, `Terry` [Mandatory])
  - `target_gsm` (Float [Mandatory])
  - `cuttable_width_inches` (Float [Mandatory])
  - `finish_type` (Select: `Greige`, `Bleached`, `Dyed`, `Mercerized`, `Bio-Polished`, `Brushed` [Mandatory])
  - `shrinkage_length_pct_max` (Float [Default: -5.0])
  - `shrinkage_width_pct_max` (Float [Default: -5.0])
  - `spirality_pct_max` (Float [Default: 4.0])
  - `gauge_recommended` (Data: e.g. "24GG", "28GG")
  - `diameter_recommended` (Data: e.g. "30 Inch", "34 Inch")
- **Provenance:** `SOURCE`

#### 18. Versa Fabric Roll
- **Frappe DocType:** `Versa Fabric Roll` | **App:** `versa_textile` | **Type:** Master / Traceability Unit
- **Company Authority:** `COMPANY_OWNED` | **Autoname:** `field:roll_barcode` (Series: `ROLL-.YYYY.-.#####.`)
- **Business Purpose:** Physical roll-level traceability unit linking weight, length, GSM, width, defect points, and warehouse location.
- **Fields:**
  - `roll_barcode` (Data [Mandatory, Unique, Immutable])
  - `company` (Link: `Company` [Mandatory, Immutable])
  - `item` (Link: `Item` [Mandatory, Immutable])
  - `batch` (Link: `Batch` [Mandatory, Immutable])
  - `warehouse` (Link: `Warehouse` [Mandatory])
  - `shade` (Link: `Versa Shade` [Mandatory])
  - `roll_no` (Int [Mandatory])
  - `net_weight_kg` (Float [Mandatory])
  - `gross_weight_kg` (Float [Mandatory])
  - `length_meters` (Float [Mandatory])
  - `actual_gsm` (Float)
  - `actual_width_inches` (Float)
  - `quality_grade` (Select: `Grade A`, `Grade B`, `Grade C`, `Quarantine`, `Rejected` [Default: 'Quarantine'])
  - `defect_points_4point` (Float [Default: 0.0])
  - `status` (Select: `In Stock`, `Issued to Cutting`, `Issued to Job Work`, `Consumed`, `Scrapped` [Default: 'In Stock'])
  - `source_purchase_receipt` (Link: `Purchase Receipt`)
- **Validation:** Server-side dual-UOM mass conservation validation:
  $$\text{Expected Weight} = \frac{\text{Length}(m) \times (\text{Width}(\text{in}) \times 0.0254) \times \text{GSM}}{1000} \pm 5.0\%$$
- **Provenance:** `SOURCE`

#### 19. Versa Style
- **Frappe DocType:** `Versa Style` | **App:** `versa_textile` | **Type:** Master / Tech Pack Sheet
- **Company Authority:** `COMPANY_OWNED` | **Autoname:** `field:style_no`
- **Business Purpose:** Core product engineering sheet holding bill of materials, operations, colourways, and size ranges.
- **Fields:**
  - `style_no` (Data [Mandatory, Unique])
  - `company` (Link: `Company` [Mandatory, Immutable])
  - `buyer_customer` (Link: `Customer` [Mandatory])
  - `brand` (Data)
  - `season` (Data [Mandatory])
  - `garment_type` (Select: `T-Shirt`, `Polo Shirt`, `Hoodie`, `Joggers`, `Pajama`, `Dress`, `Babywear` [Mandatory])
  - `base_fabric_item` (Link: `Item` [Mandatory])
  - `target_sam_minutes` (Float [Default: 0.0])
  - `status` (Select: `Development`, `Sampling`, `Costed`, `Approved for Production`, `Archived` [Default: 'Development'])
  - `tech_pack_attachment` (Attach)
  - Child Tables: `materials` (Table: `Versa Style Material`), `operations` (Table: `Versa Style Operation`), `colourways` (Table: `Versa Style Colourway`), `size_range` (Table: `Versa Style Size`).
- **Provenance:** `SOURCE`

#### 20. Versa Job Worker
- **Frappe DocType:** `Versa Job Worker` | **App:** `versa_jobwork` | **Type:** Master Extension
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `VJW-.supplier.`
- **Business Purpose:** Subcontractor capability profile, machine specifications, and capacity.
- **Fields:**
  - `supplier` (Link: `Supplier` [Mandatory, Unique, Immutable])
  - `daily_capacity_kg` (Float [Default: 0.0])
  - `standard_loss_tolerance_pct` (Float [Default: 3.0])
  - `quality_rating` (Float [Default: 5.0, Read-only])
  - `compliance_status` (Select: `Compliant`, `Under Review`, `Blacklisted` [Default: 'Compliant'])
  - `gstin` (Data)
  - `process_capabilities` (Table: `Versa Job Worker Process`)
- **Provenance:** `SOURCE`

#### 21. Versa QC Spec
- **Frappe DocType:** `Versa QC Spec` | **App:** `versa_quality` | **Type:** Master
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `VQC-.spec_name.-.version.`
- **Business Purpose:** Versioned quality specification defining lab test methods, tolerances, and parameter limits.
- **Fields:**
  - `spec_name` (Data [Mandatory])
  - `version` (Data [Mandatory, Default: 'V1.0'])
  - `material_type` (Select: `Yarn`, `Fabric`, `Dye/Chemical`, `Trim`, `Garment Final AQL` [Mandatory])
  - `buyer_customer` (Link: `Customer`)
  - `is_active` (Check: Default 1)
  - `parameters` (Table: `Versa QC Parameter` [Mandatory])
- **Indexes:** Unique index on `(spec_name, version)`.
- **Provenance:** `SOURCE`

#### 22. Versa Carton
- **Frappe DocType:** `Versa Carton` | **App:** `versa_export` | **Type:** Master / Logistics Container
- **Company Authority:** `COMPANY_OWNED` | **Autoname:** `field:carton_barcode` (Series: `CTN-.YYYY.-.#####.`)
- **Business Purpose:** Physical export carton unit containing ratio-packed garments.
- **Fields:**
  - `carton_barcode` (Data [Mandatory, Unique, Immutable])
  - `company` (Link: `Company` [Mandatory, Immutable])
  - `packing_plan` (Link: `Versa Packing Plan` [Mandatory, Immutable])
  - `carton_no` (Int [Mandatory])
  - `length_cm` (Float [Mandatory])
  - `width_cm` (Float [Mandatory])
  - `height_cm` (Float [Mandatory])
  - `gross_weight_kg` (Float [Mandatory])
  - `net_weight_kg` (Float [Mandatory])
  - `total_pcs` (Int [Mandatory, Read-only])
  - `items` (Table: `Versa Carton Item` [Mandatory])
- **Provenance:** `SOURCE`

---

### 3.3 Versa Custom Transactions (3 Entities)

#### 23. Versa Job Work Order
- **Frappe DocType:** `Versa Job Work Order` | **App:** `versa_jobwork` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `VJWO-.YYYY.-.#####.`
- **Document Lifecycle:** `Draft` $\to$ `Submitted` $\to$ `In Progress` $\to$ `Completed` $\to$ `Cancelled` / `Closed`.
- **Business Purpose:** Subcontracting execution document orchestrating process issue, receipt, yield calculation, and mass balance.
- **Fields:**
  - `company` (Link: `Company` [Mandatory, Immutable])
  - `job_worker` (Link: `Supplier` [Mandatory])
  - `process` (Select: `Knitting`, `Yarn Dyeing`, `Fabric Dyeing / Finishing`, `All-Over Printing`, `Chest Printing`, `Embroidery`, `Washing / Bio-Polishing`, `Stitching`, `Ironing / Packing` [Mandatory])
  - `source_sales_order` (Link: `Sales Order`)
  - `planned_input_qty` (Float [Mandatory])
  - `planned_output_qty` (Float [Mandatory])
  - `uom` (Link: `UOM` [Mandatory])
  - `allowed_loss_pct` (Float [Mandatory, Default: 3.0])
  - `rate_per_unit` (Currency [Mandatory])
  - `billing_basis` (Select: `Per Input Weight`, `Per Output Weight`, `Per Piece`, `Per Meter` [Mandatory])
  - `status` (Select: `Draft`, `Submitted`, `In Progress`, `Completed`, `Cancelled`, `Closed` [Default: 'Draft'])
  - `materials_issued` (Table: `Versa Job Work Material`)
  - `results_received` (Table: `Versa Job Work Result`)
- **Server-Side Validations:**
  - `before_submit`: AVL check (Job Worker must be `Compliant` and possess machine capability).
  - `before_save` / `validate`: Mass balance conservation check:
    $$\text{Issued Mass} \equiv \text{Output Mass} + \text{Process Loss} + \text{Scrap} + \text{Returned} + \text{Unaccounted}$$
    $$\text{Unaccounted Mass} \le 0.1\% \times \text{Issued Mass}$$
  - `on_submit`: Auto-creates ERPNext `Stock Entry` (Material Transfer to Subcontractor Warehouse).
- **Provenance:** `SOURCE`

#### 24. Versa QC Result
- **Frappe DocType:** `Versa QC Result` | **App:** `versa_quality` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `VQR-.YYYY.-.#####.`
- **Document Lifecycle:** `Draft` $\to$ `Submitted` $\to$ `Cancelled`.
- **Business Purpose:** Lab inspection event recording multi-point physical readings and calculating disposition.
- **Fields:**
  - `company` (Link: `Company` [Mandatory, Immutable])
  - `qc_spec` (Link: `Versa QC Spec` [Mandatory])
  - `inspection_type` (Select: `Incoming Material`, `In-Process Job Work`, `Cutting Panel`, `Stitching Inline`, `Final Garment AQL` [Mandatory])
  - `source_doctype` (Select: `Purchase Receipt`, `Versa Job Work Order`, `Stock Entry` [Mandatory])
  - `source_name` (Dynamic Link: `source_doctype` [Mandatory])
  - `item` (Link: `Item` [Mandatory])
  - `batch` (Link: `Batch`)
  - `roll_barcode` (Link: `Versa Fabric Roll`)
  - `sample_size` (Int [Mandatory, Default: 1])
  - `overall_status` (Select: `Accepted`, `Accepted with Concession`, `Quarantine`, `Rejected` [Mandatory, Default: 'Quarantine'])
  - `inspected_by` (Link: `User` [Mandatory])
  - `inspection_date` (Date [Mandatory])
  - `measurements` (Table: `Versa QC Measurement` [Mandatory])
- **Server-Side Validation:**
  - `validate`: Evaluates parameter tolerances; auto-computes disposition. If any Critical parameter fails, status defaults to `Rejected` unless signed off by QA Head.
- **Provenance:** `SOURCE`

#### 25. Versa Packing Plan
- **Frappe DocType:** `Versa Packing Plan` | **App:** `versa_export` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION` | **Autoname:** `VPP-.YYYY.-.#####.`
- **Document Lifecycle:** `Draft` $\to$ `Submitted` $\to$ `Completed` $\to$ `Cancelled`.
- **Business Purpose:** Ratio/solid packing plan allocating finished garment production into export cartons.
- **Fields:**
  - `company` (Link: `Company` [Mandatory, Immutable])
  - `sales_order` (Link: `Sales Order` [Mandatory])
  - `style` (Link: `Versa Style` [Mandatory])
  - `packing_type` (Select: `Solid Colour Solid Size`, `Solid Colour Ratio Size`, `Assorted Colour Ratio Size` [Mandatory])
  - `planned_total_cartons` (Int [Mandatory])
  - `planned_total_pcs` (Int [Mandatory])
  - `status` (Select: `Draft`, `Submitted`, `In Progress`, `Completed`, `Cancelled` [Default: 'Draft'])
- **Server-Side Validation:**
  - `before_submit`: Validates carton packing conservation against `Sales Order` order matrix.
- **Provenance:** `SOURCE`

---

### 3.4 Versa Child Tables (11 Entities)

All child tables derive their company context strictly from their parent document (`DERIVED_COMPANY_CONTEXT`).

#### 26. Versa Style Material
- **Parent:** `Versa Style` | **App:** `versa_textile`
- **Fields:** `item` (Link: `Item` [Mandatory]), `consumption_per_garment` (Float [Mandatory]), `uom` (Link: `UOM` [Mandatory]), `wastage_pct` (Float [Default: 3.0]), `component_name` (Data: e.g. "Body Fabric", "Neck Rib").

#### 27. Versa Style Operation
- **Parent:** `Versa Style` | **App:** `versa_textile`
- **Fields:** `operation_name` (Data [Mandatory]), `department` (Select: `Cutting`, `Printing`, `Embroidery`, `Stitching`, `Ironing`, `Packing` [Mandatory]), `sam_minutes` (Float [Mandatory]), `is_subcontracted` (Check: Default 0), `sequence_no` (Int [Mandatory]).

#### 28. Versa Style Colourway
- **Parent:** `Versa Style` | **App:** `versa_textile`
- **Fields:** `colour` (Link: `Versa Colour` [Mandatory]), `shade` (Link: `Versa Shade` [Mandatory]).

#### 29. Versa Style Size
- **Parent:** `Versa Style` | **App:** `versa_textile`
- **Fields:** `size_code` (Data [Mandatory, e.g. "S", "M", "L", "XL"]), `sort_order` (Int [Mandatory]).

#### 30. Versa Order Matrix
- **Parent:** `Sales Order` | **App:** `versa_textile`
- **Fields:**
  - `style` (Link: `Versa Style` [Mandatory])
  - `colour` (Link: `Versa Colour` [Mandatory])
  - `shade` (Link: `Versa Shade` [Mandatory])
  - `size_code` (Data [Mandatory])
  - `ordered_qty` (Int [Mandatory])
  - `confirmed_qty` (Int [Mandatory])
  - `produced_qty` (Int [Default: 0, Read-only])
  - `packed_qty` (Int [Default: 0, Read-only])
  - `delivered_qty` (Int [Default: 0, Read-only])
- **Conservation Invariant:** Enforced server-side per `(style, colour, shade, size_code)` tuple.

#### 31. Versa Job Worker Process
- **Parent:** `Versa Job Worker` | **App:** `versa_jobwork`
- **Fields:** `process` (Select: `Knitting`, `Yarn Dyeing`, `Fabric Dyeing / Finishing`, `All-Over Printing`, `Chest Printing`, `Embroidery`, `Washing / Bio-Polishing`, `Stitching` [Mandatory]), `machine_spec` (Data [Mandatory, e.g. "24GG 30-Inch Mayer & Cie"]), `daily_capacity` (Float [Mandatory]).

#### 32. Versa Job Work Material
- **Parent:** `Versa Job Work Order` | **App:** `versa_jobwork`
- **Fields:** `item` (Link: `Item` [Mandatory]), `batch` (Link: `Batch`), `roll_barcode` (Link: `Versa Fabric Roll`), `issued_qty` (Float [Mandatory]), `uom` (Link: `UOM` [Mandatory]), `stock_entry` (Link: `Stock Entry`).

#### 33. Versa Job Work Result
- **Parent:** `Versa Job Work Order` | **App:** `versa_jobwork`
- **Fields:**
  - `received_item` (Link: `Item` [Mandatory])
  - `output_qty` (Float [Mandatory])
  - `process_loss_qty` (Float [Mandatory])
  - `scrap_qty` (Float [Default: 0.0])
  - `returned_unprocessed_qty` (Float [Default: 0.0])
  - `unaccounted_qty` (Float [Default: 0.0, Read-only])
  - `yield_pct` (Float [Read-only])
  - `qc_result` (Link: `Versa QC Result`)
  - `stock_entry` (Link: `Stock Entry`)

#### 34. Versa QC Parameter
- **Parent:** `Versa QC Spec` | **App:** `versa_quality`
- **Fields:** `parameter_code` (Data [Mandatory]), `parameter_name` (Data [Mandatory]), `test_method` (Data [Mandatory, e.g. "ASTM D3776"]), `target_value` (Data [Mandatory]), `min_limit` (Float), `max_limit` (Float), `uom` (Link: `UOM`), `severity` (Select: `Critical`, `Major`, `Minor` [Mandatory]).

#### 35. Versa QC Measurement
- **Parent:** `Versa QC Result` | **App:** `versa_quality`
- **Fields:** `parameter_code` (Data [Mandatory]), `reading_1` (Float), `reading_2` (Float), `reading_3` (Float), `mean_reading` (Float [Read-only]), `reading_status` (Select: `Pass`, `Fail`, `Concession` [Read-only]).

#### 36. Versa Carton Item
- **Parent:** `Versa Carton` | **App:** `versa_export`
- **Fields:** `style` (Link: `Versa Style` [Mandatory]), `colour` (Link: `Versa Colour` [Mandatory]), `size_code` (Data [Mandatory]), `qty_pcs` (Int [Mandatory]).

---

### 3.5 Reference Taxonomies & Configuration (3 Entities)

#### 37. Versa Colour
- **Frappe DocType:** `Versa Colour` | **App:** `versa_textile` | **Type:** Reference Taxonomy
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `field:colour_name`
- **Fields:** `colour_name` (Data [Mandatory, Unique]), `colour_code` (Data), `pantone_ref` (Data), `rgb_hex` (Data), `is_active` (Check: Default 1).
- **Provenance:** `SOURCE`

#### 38. Versa Shade
- **Frappe DocType:** `Versa Shade` | **App:** `versa_textile` | **Type:** Reference Taxonomy
- **Company Authority:** `SHARED_MASTER` | **Autoname:** `VSH-.colour.-.shade_name.`
- **Fields:** `colour` (Link: `Versa Colour` [Mandatory]), `shade_name` (Data [Mandatory]), `lab_dip_no` (Data), `recipe_code` (Data), `is_active` (Check: Default 1).
- **Provenance:** `SOURCE`

#### 39. Versa Approval Rule
- **Frappe DocType:** `Versa Approval Rule` | **App:** `versa_core` | **Type:** Configuration
- **Company Authority:** `CONFIGURATION` | **Autoname:** `VAR-.document_type.-.#####.`
- **Fields:**
  - `document_type` (Select: `Purchase Order`, `Sales Order`, `Job Work Order`, `Quotation` [Mandatory])
  - `min_amount` (Currency [Mandatory])
  - `max_amount` (Currency)
  - `approver_role` (Link: `Role` [Mandatory])
  - `approver_user` (Link: `User`)
  - `business_unit` (Link: `Cost Center`)
  - `is_active` (Check: Default 1)
- **Provenance:** `SOURCE`

---

## 4. Canonical Relationships Mapping (All 28 Relationships)

| Relationship ID | Source DocType | Target DocType | Cardinality | Frappe Field | Field Type | Delete Behavior | Lifecycle Dependency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REL-001** | `Cost Center` | `Company` | Many-to-One | `company` | Link | Restrict | Cost Center cannot exist without Company |
| **REL-002** | `Warehouse` | `Company` | Many-to-One | `company` | Link | Restrict | Warehouse scoped by Company |
| **REL-003** | `Batch` | `Item` | Many-to-One | `item` | Link | Restrict | Batch belongs to Item |
| **REL-004** | `Sales Order` | `Customer` | Many-to-One | `customer` | Link | Restrict | Commercial buyer link |
| **REL-005** | `Purchase Order` | `Supplier` | Many-to-One | `supplier` | Link | Restrict | Procurement vendor link |
| **REL-006** | `Purchase Receipt` | `Supplier` | Many-to-One | `supplier` | Link | Restrict | GRN vendor link |
| **REL-007** | `Delivery Note` | `Customer` | Many-to-One | `customer` | Link | Restrict | Shipment customer link |
| **REL-008** | `Purchase Invoice` | `Supplier` | Many-to-One | `supplier` | Link | Restrict | Payable invoice vendor link |
| **REL-009** | `Sales Invoice` | `Customer` | Many-to-One | `customer` | Link | Restrict | Receivable invoice buyer link |
| **REL-010** | `Stock Entry` | `Warehouse` | Many-to-One | `to_warehouse` | Link | Restrict | Target storage ledger |
| **REL-011** | `Versa Material Spec` | `Item` | Many-to-One | `item` | Link | Restrict | Technical spec binds to Item |
| **REL-012** | `Versa Yarn Spec` | `Versa Material Spec` | One-to-One | `material_spec` | Link | Cascade | Spinning extension of Material Spec |
| **REL-013** | `Versa Fabric Spec` | `Versa Material Spec` | One-to-One | `material_spec` | Link | Cascade | Knitting extension of Material Spec |
| **REL-014** | `Versa Shade` | `Versa Colour` | Many-to-One | `colour` | Link | Restrict | Shade belongs to base Colour |
| **REL-015** | `Versa Fabric Roll` | `Item` | Many-to-One | `item` | Link | Restrict | Physical roll references Item SKU |
| **REL-016** | `Versa Fabric Roll` | `Batch` | Many-to-One | `batch` | Link | Restrict | Roll belongs to Dye/Knit Batch |
| **REL-017** | `Versa Fabric Roll` | `Warehouse` | Many-to-One | `warehouse` | Link | Restrict | Physical roll location |
| **REL-018** | `Versa Fabric Roll` | `Versa Shade` | Many-to-One | `shade` | Link | Restrict | Shade matching linkage |
| **REL-019** | `Versa Style` | `Customer` | Many-to-One | `buyer_customer` | Link | Restrict | Style belongs to Buyer |
| **REL-020** | `Versa Style` | `Item` | Many-to-One | `base_fabric_item`| Link | Restrict | Style engineered with Base Fabric |
| **REL-021** | `Versa Order Matrix` | `Sales Order` | Many-to-One | `parent` | Table | Cascade | Child table of Sales Order |
| **REL-022** | `Versa Order Matrix` | `Versa Style` | Many-to-One | `style` | Link | Restrict | Matrix cell references Style |
| **REL-023** | `Versa Job Worker` | `Supplier` | One-to-One | `supplier` | Link | Restrict | Job worker profile extends Supplier |
| **REL-024** | `Versa Job Work Order` | `Supplier` | Many-to-One | `job_worker` | Link | Restrict | Subcontract order assigned to Supplier |
| **REL-025** | `Versa QC Result` | `Versa QC Spec` | Many-to-One | `qc_spec` | Link | Restrict | Test results evaluate against Spec |
| **REL-026** | `Versa QC Result` | `Item` | Many-to-One | `item` | Link | Restrict | QC evaluates Item |
| **REL-027** | `Versa Packing Plan` | `Sales Order` | Many-to-One | `sales_order` | Link | Restrict | Packing plan fulfills Sales Order |
| **REL-028** | `Versa Carton` | `Versa Packing Plan` | Many-to-One | `packing_plan` | Link | Restrict | Carton belongs to Packing Plan |

---

## 5. Invariants & Business Rules Implementation

### 5.1 The Six Canonical Invariants

#### 1. `job_work_mass_balance` (CANONICAL_INVARIANT)
- **Formal Formula:**
  $$\sum \text{Issued Weight} \equiv \sum \text{Output Weight} + \text{Process Loss} + \text{Scrap} + \text{Returned Unprocessed} + \text{Unaccounted Weight}$$
- **Tolerance:** $\text{Unaccounted Weight} \le 0.1\% \times \text{Issued Weight}$ (weighing scale calibration limit).
- **Implementation Mechanism:** Python Controller Method `validate_mass_balance` executed in `Versa Job Work Order.before_submit` and `before_save`.
- **Failure Behavior:** Throws `frappe.ValidationError` blocking document submission if unaccounted loss exceeds $0.1\%$.

#### 2. `order_matrix_conservation` (CANONICAL_INVARIANT)
- **Formal Formula:**
  $$\text{Sales Order Item.qty} \equiv \sum_{\text{cell}} \text{Versa Order Matrix.ordered\_qty} \quad \forall (\text{style}, \text{colour}, \text{shade}, \text{size})$$
- **Implementation Mechanism:** Event Hook `versa_textile.events.sales_order.validate_order_matrix` on `Sales Order.validate`.
- **Failure Behavior:** Throws `frappe.ValidationError` blocking save if matrix breakdown sum does not match line item total.

#### 3. `carton_packing_conservation` (CANONICAL_INVARIANT)
- **Formal Formula:**
  $$\sum_{k \in \text{Cartons}} \text{Carton Item.qty}(s, c, z) \le \text{Sales Order Matrix.ordered\_qty}(s, c, z) \times (1 + \text{Customer.shipment\_tolerance\_pct})$$
- **Implementation Mechanism:** Python Controller Method on `Versa Packing Plan.before_submit`.
- **Failure Behavior:** Throws `frappe.ValidationError` preventing cartonization exceeding buyer tolerance.

#### 4. `fabric_roll_dual_uom_conservation` (CANONICAL_INVARIANT)
- **Formal Formula:**
  $$\text{Weight}(kg) = \frac{\text{Length}(m) \times (\text{Width}(\text{in}) \times 0.0254) \times \text{Actual GSM}}{1000} \pm 5.0\%$$
- **Implementation Mechanism:** Python Controller Method on `Versa Fabric Roll.validate`.
- **Failure Behavior:** Displays warning or flags roll for inspection if physical dimensions diverge from weight.

#### 5. `quality_gate_enforcement` (CANONICAL_INVARIANT)
- **Formal Formula:**
  $$\text{Item.is\_qc\_required} == 1 \implies \text{Purchase Receipt.status} \in \{\text{QC Passed}, \text{Concession}\} \text{ before Stock Release}$$
- **Implementation Mechanism:** Event Hook `versa_quality.events.purchase_receipt.before_submit`.
- **Failure Behavior:** Hard block preventing Purchase Receipt submission until `Versa QC Result` is approved.

#### 6. `multi_company_isolation` (CANONICAL_INVARIANT)
- **Formal Formula:**
  $$\text{User Session Company} == \text{Document.company} \quad \forall \text{ Transactional & Company-Owned DocTypes}$$
- **Implementation Mechanism:** Frappe Permission Query Conditions injected via `versa_core.permissions.apply_company_query_conditions`.
- **Failure Behavior:** SQL query restriction preventing cross-company document visibility or cross-posting.

---

### 5.2 Business Rules, Workflow Rules & Derived Metrics (7 Rules)

#### 7. `job_work_excess_loss_penalty` (BUSINESS_RULE)
- **Formula:** $\text{Excess Loss} = \max(0, \text{Actual Loss} - (\text{Issued Qty} \times \text{Allowed Loss Pct}))$. Material debit amount automatically credited against Job Worker's `Purchase Invoice`.
- **Implementation:** `versa_jobwork.events.purchase_invoice.apply_excess_loss_debit`.

#### 8. `three_way_matching` (BUSINESS_RULE)
- **Formula:** $\text{Invoice Qty} \le \text{Accepted Receipt Qty} \land \text{Invoice Rate} \le \text{PO Rate} \times (1 + \text{Price Tolerance})$.
- **Implementation:** `erpnext.accounts.doctype.purchase_invoice.purchase_invoice.validate`.

#### 9. `dispatch_invoice_reconciliation` (BUSINESS_RULE)
- **Formula:** $\text{Cumulative Invoiced Qty} \le \text{Accepted Delivered Qty} - \text{Returned Qty}$ and $\text{Total Invoiced Amount} \equiv \text{Delivered Net Value} \pm \text{Adjustments}$.
- **Implementation:** `erpnext.accounts.doctype.sales_invoice.sales_invoice.validate`.

#### 10. `production_cutting_allowance` (WORKFLOW_RULE)
- **Formula:** $\text{Cutting Issue Qty} = \text{Order Matrix Qty} \times (1 + \text{Cutting Allowance Pct})$.
- **Implementation:** `versa_textile.events.sales_order.calculate_cutting_allowance`.

#### 11. `order_fulfillment_closure` (WORKFLOW_RULE)
- **Formula:** Sales Order status closes when $\text{Delivered Qty} \ge \text{Ordered Qty} \times (1 - \text{Short Shipment Tolerance})$.
- **Implementation:** `erpnext.selling.doctype.sales_order.sales_order.update_status`.

#### 12. `astm_d5430_4point_defect_scoring` (DERIVED_METRIC)
- **Formula:** $\text{Points per 100 sq yds} = \frac{\text{Total Defect Points} \times 3600}{\text{Length (yds)} \times \text{Width (in)}}$.
- **Implementation:** `versa_quality.doctype.versa_qc_result.versa_qc_result.calculate_4point_score`.

#### 13. `supplier_otif_scoring` (DERIVED_METRIC)
- **Formula:** Running On-Time In-Full index calculated across historical Purchase Receipts.
- **Implementation:** Background Job `versa_core.analytics.update_supplier_otif`.

---

## 6. Job Work Subsystem Implementation Contract

### 6.1 State Machine & Lifecycles
```text
[ Draft ] ──(Submit)──> [ Submitted ] ──(Issue Material)──> [ In Progress ]
                             │                                    │
                       (Cancel VJWO)                      (Receive Goods)
                             │                                    │
                             ▼                                    ▼
                        [ Cancelled ]                     [ Fully Received ]
                                                                  │
                                                          (Mass Balance QC)
                                                                  │
                                                                  ▼
                                                             [ Completed ]
                                                                  │
                                                        (Settle Purchase Inv)
                                                                  │
                                                                  ▼
                                                               [ Closed ]
```

### 6.2 ERPNext Stock Posting Integration
1. **Material Issue:** When material is issued for Job Work, Versa triggers standard ERPNext `Stock Entry` (Type: `Send to Subcontractor`) moving items from Raw Material Warehouse to Job Worker Warehouse (`versa_warehouse_type == 'Job Worker Subcontract Store'`).
2. **Material Receipt:** When processed goods return, Versa triggers standard ERPNext `Stock Entry` (Type: `Receive at Subcontractor`) moving finished goods to Active Warehouse and posting Scrap.
3. **Financial Settlement:** The job work service charge is billed via standard ERPNext `Purchase Invoice` with an automatic debit line for any excess process loss.

---

## 7. Quality Assurance Subsystem Implementation Contract

1. **QC Gate Hook:** A standard `before_submit` hook intercepts `Purchase Receipt` and `Stock Entry`:
   ```python
   def check_qc_conformance(doc, method):
       for item in doc.items:
           if frappe.db.get_value("Item", item.item_code, "is_qc_required"):
               if not doc.versa_qc_result:
                   frappe.throw(f"Quality inspection mandatory for Item {item.item_code}. Create Versa QC Result first.")
               qc_status = frappe.db.get_value("Versa QC Result", doc.versa_qc_result, "overall_status")
               if qc_status not in ["Accepted", "Accepted with Concession"]:
                   frappe.throw(f"Cannot submit Purchase Receipt: QC Result {doc.versa_qc_result} is {qc_status}.")
   ```
2. **Concession Workflow:** If status is `Accepted with Concession`, the document requires explicit dual sign-off by `Quality Manager` and `Merchandiser`.

---

## 8. Fabric Roll Traceability Implementation Contract

1. **Role of Fabric Roll:** `Versa Fabric Roll` is a physical traceability overlay holding barcode serialization, physical roll length, actual GSM, cuttable width, and defect scores.
2. **Stock Ledger Integrity:** ERPNext `Stock Ledger Entry` holds the sole legal inventory weight ($kg$) and valuation. `Versa Fabric Roll` references `Item`, `Batch`, and `Warehouse`.
3. **Physical Sampling Protocol:** Explicitly preserved as `DEFERRED / OPEN` for Phase 0 discovery with customers.

---

## 9. Procure-to-Pay (P2P) Implementation Contract

- **Workflow:** `Purchase Order` $\to$ `Purchase Receipt` $\to$ `Versa QC Result` $\to$ `Stock Entry` (Quarantine $\to$ Active) $\to$ `Purchase Invoice` (3-way match) $\to$ `Payment Entry`.
- **Three-Way Match:** Standard ERPNext accounting validations enforce $\text{Invoice Qty} \le \text{Accepted Qty}$ and rate tolerances.

---

## 10. Order-to-Cash (O2C) Implementation Contract

- **Workflow:** `Sales Order` + `Versa Order Matrix` $\to$ `Versa Style` explosion $\to$ Production / Job Work $\to$ `Versa Packing Plan` $\to$ `Versa Carton` $\to$ `Delivery Note` $\to$ `Sales Invoice`.
- **Matrix Conservation:** Enforces strict cell-level conservation across style, colour, shade, and size code.
- **Dispatch/Invoice Rule:** $\text{Cumulative Invoiced Qty} \le \text{Delivered Qty} - \text{Returned Qty}$.

---

## 11. Role Profiles & Permissions Matrix

| DocType | Versa Admin | Merchandiser | Purchase User | Job Work User | QA Inspector | QA Head | Warehouse User | Accounts User |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Versa Style` | CRUD/S/C | CRUD/S | R | R | R | R | R | R |
| `Versa Material Spec` | CRUD/S/C | CRUD/S | R | R | R | R | R | R |
| `Versa Fabric Roll` | CRUD/S/C | R | R | R | R/W | R/W | CRUD | R |
| `Versa Job Worker` | CRUD/S/C | R | CRUD | CRUD/S | R | R | R | R |
| `Versa Job Work Order` | CRUD/S/C | R | R | CRUD/S/C | R | R | R/W | R |
| `Versa QC Spec` | CRUD/S/C | R | R | R | R | CRUD/S | R | R |
| `Versa QC Result` | CRUD/S/C | R | R | R | CRUD/S | CRUD/S/C | R | R |
| `Versa Packing Plan` | CRUD/S/C | CRUD/S | R | R | R | R | CRUD/S | R |
| `Versa Carton` | CRUD/S/C | R | R | R | R | R | CRUD | R |
| `Versa Approval Rule` | CRUD | R | R | R | R | R | R | R |

*Legend: C = Create, R = Read, U = Update, D = Delete, S = Submit, C = Cancel*

---

## 12. Server vs Client Responsibility Matrix

| Operational Capability | Client-Side (JavaScript) | Server-Side (Python Controller / Hooks) |
| :--- | :--- | :--- |
| **Order Matrix Grid UI** | Interactive grid rendering, row addition, dynamic sums | Strict sum conservation validation on `before_save` & `before_submit` |
| **Mass Balance Check** | Real-time yield & loss preview calculations in form | Hard-blocking validation & theft flag generation on `before_submit` |
| **Quality Gate Check** | Field filtering of QC specs and parameter entry forms | Hard-blocking submission prevention on `Purchase Receipt.before_submit` |
| **Approval Rule Trigger** | UI banner indicating required approver role | Server-side authorization check before transitioning `docstatus = 1` |
| **Company Isolation** | Default company selection in form fields | Mandatory SQL Permission Query Conditions filtering multi-tenant records |

---

## 13. ERPNext Posting Contracts & Idempotency

### 13.1 Idempotency Key Design
Every automated transaction posting from Versa into ERPNext embeds a deterministic idempotency key stored in a custom field:
$$\text{idempotency\_key} = \text{MD5}(\text{source\_doctype} + \text{source\_name} + \text{action\_event} + \text{docversion})$$

### 13.2 Posting Matrix
1. **`Versa Job Work Order (Issue)` $\to$ `Stock Entry (Send to Subcontractor)`:**
   - Idempotency Field: `versa_posting_key`
   - Trigger: `VJWO.on_submit`
   - Rollback: Cancelling VJWO cancels the linked `Stock Entry`.
2. **`Versa Job Work Order (Receipt)` $\to$ `Stock Entry (Receive from Subcontractor)`:**
   - Idempotency Field: `versa_posting_key`
   - Trigger: `VJWO.results_received` update
   - Rollback: Reverses inventory ledger posting.

---

## 14. API Contracts

### 14.1 Fabric Roll Weighment & Barcode Scan API
- **Endpoint:** `/api/method/versa_textile.api.scan_fabric_roll`
- **Method:** `POST`
- **Payload:** `{"roll_barcode": "ROLL-2026-00123", "scanned_weight_kg": 24.50, "warehouse": "Knitting Floor Store - VE"}`
- **Response:** `{"status": "success", "roll_status": "In Stock", "variance_kg": 0.00}`

### 14.2 Job Work Mass Balance Reconciliation API
- **Endpoint:** `/api/method/versa_jobwork.api.reconcile_mass_balance`
- **Method:** `POST`
- **Payload:** `{"job_work_order": "VJWO-2026-00045"}`
- **Response:** `{"status": "reconciled", "unaccounted_kg": 0.00, "yield_pct": 96.20, "excess_loss_debit": 0.00}`

---

## 15. Database Indexing & Optimization Strategy

1. **`Versa Fabric Roll`:** Unique Index on `(roll_barcode)`, Compound Index on `(company, item, warehouse, status)`.
2. **`Versa Style`:** Unique Index on `(company, style_no)`.
3. **`Versa Order Matrix`:** Compound Index on `(parent, style, colour, shade, size_code)`.
4. **`Versa Job Work Order`:** Compound Index on `(company, job_worker, status)`.
5. **`Versa QC Result`:** Compound Index on `(company, source_doctype, source_name, overall_status)`.

---

## 16. Open & Deferred Items for Customer Validation

The following items are deliberately preserved as **OPEN / DEFERRED** for customer workshops during Phase 0 bench commissioning:
1. **ASM-001:** Exact scale calibration tolerance threshold ($\le 0.1\%$ default vs process-specific setting).
2. **Fabric Roll Sampling Protocol:** Specific destructive/non-destructive sample cut intervals across roll lengths.
3. **ASM-011:** Free-text material composition string vs normalized blend child table for Phase 4 reporting.
4. **ASM-012:** Inter-company subcontracting GST tax invoice generation vs internal Cost Center transfer.
