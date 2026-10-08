# VERSA ERP FRAPPE / ERPNext METADATA & MODEL MAPPING

## 1. Architectural Strategy & Modular Organization

To ensure complete **upgrade safety** without modifying ERPNext core, the Versa ERP platform is organized into 5 focused Frappe applications:

```text
E:\VersaERP\bench\apps\
├── frappe/                      # Framework engine
├── erpnext/                     # Core enterprise transaction engine
├── versa_core/                  # Governance, approval matrix, credit policies, business units
├── versa_textile/               # Yarn/Fabric specs, fabric rolls, styles, order matrices
├── versa_jobwork/               # Job worker profiles, job work orders, mass-balance reconciliation
├── versa_quality/               # Multi-tier inspection specs, physical parameter measurements
└── versa_export/                # Cartonization, packing plans, export packing lists
```

---

## 2. Frappe DocType Catalog & Specifications

### 2.1 App: `versa_core` (Governance & Business Controls)

#### DocType: `Versa Approval Rule`
- **Module:** `versa_core` | **Type:** Master / Configuration
- **Purpose:** Multi-level dynamic approval thresholds for Sales Orders, Purchase Orders, and Job Work Orders based on Amount, Department, Item Group, and Business Unit.
- **Naming:** Prompt / `VAR-.#####.`
- **Fields:**
  - `document_type` (Select: `Purchase Order`, `Sales Order`, `Job Work Order`, `Quotation` [Mandatory])
  - `min_amount` (Currency [Mandatory])
  - `max_amount` (Currency)
  - `approver_role` (Link: `Role` [Mandatory])
  - `approver_user` (Link: `User`)
  - `business_unit` (Link: `Cost Center`)
  - `is_active` (Check: Default 1)
- **Validation:** Server-side validation ensuring no overlapping amount bands for the same document type and business unit.
- **ERPNext Dependency:** Standard `Purchase Order` and `Sales Order` workflows invoke `versa_core.approvals.check_approval_permission`.

---

### 2.2 App: `versa_textile` (Textile Master Data & Style Engineering)

#### DocType: `Versa Material Spec`
- **Module:** `versa_textile` | **Type:** Master
- **Purpose:** Decouples detailed technical specifications from ERPNext Item master.
- **Naming:** `VMS-.item_code.-.version.`
- **Fields:**
  - `item` (Link: `Item` [Mandatory])
  - `specification_version` (Data [Mandatory, Default: 'V1.0'])
  - `material_type` (Select: `Yarn`, `Fabric`, `Dye/Chemical`, `Trim/Accessory`, `Packing Material` [Mandatory])
  - `composition` (Data: e.g. "100% Combed Cotton" [Mandatory])
  - `is_active` (Check: Default 1)
  - `yarn_spec_section` (Section Break, depends_on: `eval:doc.material_type=='Yarn'`)
  - `yarn_count` (Data), `count_system` (Select), `ply` (Int), `spinning_process` (Select), `origin_mill` (Data)
  - `fabric_spec_section` (Section Break, depends_on: `eval:doc.material_type=='Fabric'`)
  - `fabric_structure` (Select), `target_gsm` (Float), `cuttable_width_inches` (Float), `finish_type` (Select), `shrinkage_length_pct_max` (Float), `spirality_pct_max` (Float)

#### DocType: `Versa Fabric Roll`
- **Module:** `versa_textile` | **Type:** Master / Traceability Unit
- **Purpose:** Real-time physical inventory and defect traceability unit for fabric rolls.
- **Naming:** `roll_barcode` (Barcode / Series: `ROLL-.YYYY.-.#####.`)
- **Fields:**
  - `roll_barcode` (Data: Unique, Barcode format [Mandatory])
  - `item` (Link: `Item` [Mandatory])
  - `batch` (Link: `Batch` [Mandatory])
  - `roll_no` (Int [Mandatory])
  - `warehouse` (Link: `Warehouse` [Mandatory])
  - `net_weight_kg` (Float [Mandatory])
  - `gross_weight_kg` (Float [Mandatory])
  - `length_meters` (Float [Mandatory])
  - `actual_gsm` (Float)
  - `actual_width_inches` (Float)
  - `shade` (Link: `Versa Shade`)
  - `quality_grade` (Select: `Grade A`, `Grade B`, `Grade C`, `Quarantine`, `Rejected` [Default: 'Quarantine'])
  - `defect_points_4point` (Float [Default: 0.0])
  - `status` (Select: `In Stock`, `Issued to Cutting`, `Issued to Job Work`, `Consumed`, `Scrapped` [Default: 'In Stock'])
- **Validation:** Dual-UOM weight-to-length consistency validation against target GSM and width.
- **ERPNext Dependency:** Intercepts `Stock Entry` (Material Issue) to update roll status to `Issued` or `Consumed`.

#### DocType: `Versa Style`
- **Module:** `versa_textile` | **Type:** Product Master
- **Purpose:** Master product sheet for garment manufacturing holding BOM, grading, operations, and tech packs.
- **Naming:** `style_no` (Data [Mandatory, Unique])
- **Fields:**
  - `style_no` (Data [Mandatory, Unique])
  - `buyer_customer` (Link: `Customer` [Mandatory])
  - `brand` (Data)
  - `season` (Data [Mandatory])
  - `garment_type` (Select: `T-Shirt`, `Polo Shirt`, `Hoodie`, `Joggers`, `Pajama`, `Dress`, `Babywear` [Mandatory])
  - `base_fabric_item` (Link: `Item` [Mandatory])
  - `target_sam_minutes` (Float [Default: 0.0])
  - `status` (Select: `Development`, `Sampling`, `Costed`, `Approved for Production`, `Archived` [Default: 'Development'])
  - `materials` (Table: `Versa Style Material`)
  - `operations` (Table: `Versa Style Operation`)
  - `colourways` (Table: `Versa Style Colourway`)
  - `size_range` (Table: `Versa Style Size`)

#### DocType: `Versa Order Matrix` (Child Table)
- **Module:** `versa_textile` | **Type:** Child Table (Embedded on `Sales Order`)
- **Fields:** `style` (Link: `Versa Style`), `colour` (Link: `Versa Colour`), `shade` (Link: `Versa Shade`), `size_code` (Data), `ordered_qty` (Int), `confirmed_qty` (Int), `produced_qty` (Int), `packed_qty` (Int), `delivered_qty` (Int).

---

### 2.3 App: `versa_jobwork` (Job Work Subcontracting)

#### DocType: `Versa Job Worker`
- **Module:** `versa_jobwork` | **Type:** Master / Extension
- **Purpose:** Subcontractor capability, machine profile, and quality rating.
- **Naming:** `job_worker_name` (Linked to `Supplier`)
- **Fields:** `supplier` (Link: `Supplier` [Mandatory, Unique]), `process_capabilities` (Table: `Versa Job Worker Process`), `daily_capacity_kg` (Float), `standard_loss_tolerance_pct` (Float), `quality_rating` (Float), `compliance_status` (Select: `Compliant`, `Under Review`, `Blacklisted`).

#### DocType: `Versa Job Work Order`
- **Module:** `versa_jobwork` | **Type:** Transaction / Subcontract Document
- **Naming:** `VJWO-.YYYY.-.#####.`
- **Fields:**
  - `job_worker` (Link: `Supplier` [Mandatory])
  - `process` (Select: `Knitting`, `Dyeing / Finishing`, `All-Over Printing`, `Chest Printing`, `Embroidery`, `Washing / Bio-Polishing`, `Stitching`, `Ironing / Packing` [Mandatory])
  - `source_doctype` (Select: `Sales Order`, `Production Batch`, `Material Request`)
  - `source_name` (Dynamic Link: `source_doctype`)
  - `planned_input_qty` (Float [Mandatory]), `planned_output_qty` (Float [Mandatory]), `uom` (Link: `UOM` [Mandatory])
  - `allowed_loss_pct` (Float [Default: 3.00]), `rate_per_unit` (Currency [Mandatory]), `billing_basis` (Select: `Per Input Weight`, `Per Output Weight`, `Per Piece`, `Per Meter`)
  - `materials_issued` (Table: `Versa Job Work Material`)
  - `results_received` (Table: `Versa Job Work Result`)
  - `status` (Select: `Draft`, `Issued`, `In Progress`, `Partially Received`, `Completed`, `Cancelled`, `Closed` [Default: 'Draft'])
- **Validation:** Mass-balance reconciliation invariant validation on document submit.

---

### 2.4 App: `versa_quality` (Multi-Tier Quality Assurance)

#### DocType: `Versa QC Spec` & `Versa QC Result`
- **Module:** `versa_quality` | **Type:** Master & Transaction
- **Purpose:** Engineering quality specifications and multi-point inspection recordings.
- **Fields on `Versa QC Result`:**
  - `qc_spec` (Link: `Versa QC Spec` [Mandatory])
  - `inspection_type` (Select: `Incoming Material`, `In-Process Job Work`, `Cutting Panel`, `Stitching Inline`, `Final Garment AQL` [Mandatory])
  - `source_doctype` (Select: `Purchase Receipt`, `Versa Job Work Order`, `Versa Production Batch`, `Stock Entry` [Mandatory])
  - `source_name` (Dynamic Link [Mandatory])
  - `item` (Link: `Item` [Mandatory]), `batch` (Link: `Batch`), `roll_barcode` (Link: `Versa Fabric Roll`)
  - `sample_size` (Int [Default: 1]), `overall_status` (Select: `Accepted`, `Accepted with Concession`, `Quarantine`, `Rejected`)
  - `measurements` (Table: `Versa QC Measurement`)

---

### 2.5 App: `versa_export` (Packing, Cartonization & Export)

#### DocType: `Versa Packing Plan` & `Versa Carton`
- **Module:** `versa_export` | **Type:** Transaction & Logistics Unit
- **Purpose:** Manages ratio packing, carton barcode serialization, net/gross weights, and carton breakdown per container.
- **Fields on `Versa Carton`:**
  - `packing_plan` (Link: `Versa Packing Plan` [Mandatory])
  - `carton_barcode` (Data: Unique [Mandatory])
  - `carton_no` (Int [Mandatory]), `length_cm` (Float), `width_cm` (Float), `height_cm` (Float), `gross_weight_kg` (Float), `net_weight_kg` (Float), `total_pcs` (Int)
  - `items` (Table: `Versa Carton Item`)

---

## 3. ERPNext Standard Extension Points (Hooks & Custom Fields)

To avoid modifying ERPNext core files, all extensions are injected using Frappe's `hooks.py` and `fixtures/custom_field.json`:

1. **`Sales Order` Custom Fields:**
   - `versa_style` (Link: `Versa Style`)
   - `versa_order_matrix` (Table: `Versa Order Matrix`)
   - `versa_packing_status` (Select: `Unplanned`, `Partially Packed`, `Fully Packed`)
2. **`Purchase Receipt` Custom Fields:**
   - `versa_qc_status` (Select: `Pending QC`, `QC Passed`, `Quarantined`, `Rejected`)
   - `versa_qc_result` (Link: `Versa QC Result`)
3. **`Item` Custom Fields:**
   - `versa_material_spec` (Link: `Versa Material Spec`)
   - `is_fabric_roll_tracked` (Check: Default 0)
4. **`DocType Event Hooks` (`hooks.py`):**
   ```python
   doc_events = {
       "Sales Order": {
           "validate": "versa_textile.events.sales_order.validate_order_matrix",
           "on_submit": "versa_textile.events.sales_order.create_production_allocation"
       },
       "Purchase Receipt": {
           "on_submit": "versa_textile.events.purchase_receipt.create_fabric_rolls",
           "before_submit": "versa_quality.events.purchase_receipt.check_qc_conformance"
       },
       "Stock Entry": {
           "before_submit": "versa_textile.events.stock_entry.validate_fabric_roll_availability"
       }
   }
   ```

---

## 4. Workspaces & Role Profiles

1. **Workspaces:**
   - `Textile Master Desk` (Yarn, Fabric, Specs, Colours, Shades)
   - `Garment Merchandising` (Styles, Tech Packs, Colourways, Order Matrices)
   - `Job Work Subcontract Desk` (Job Workers, Job Work Orders, Material Balance)
   - `Textile Quality Lab` (QC Specs, Test Methods, Inspection Results, Roll Grading)
   - `Packing & Dispatch Tower` (Packing Plans, Cartons, Weight Audits, Container Lists)
2. **Role Profiles:**
   - `Versa Merchandiser` (Styles, Sales Order Matrix, Sampling)
   - `Versa Subcontract Manager` (Job Work Orders, Process Losses, Settlements)
   - `Versa QA Inspector` (QC Results, Concessions, Roll Grading)
   - `Versa Packing Supervisor` (Packing Plans, Carton Barcodes, Weighment)

