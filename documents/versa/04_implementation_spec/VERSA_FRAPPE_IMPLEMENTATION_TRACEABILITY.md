# VERSA ERP — FRAPPE IMPLEMENTATION TRACEABILITY MATRIX

## 1. Traceability Architecture & Methodology

This matrix provides a complete, machine-checkable end-to-end trace connecting the domain requirements extracted from `Versa_ERP_Platform_Strategy_Tiruppur.docx` through the canonical domain model (`versa_domain_model.json`), RDBMS schema, Frappe DocTypes, field definitions, relationship links, business invariants, and automated test IDs.

```text
Domain Requirement (Strategy Doc)
        ↓
Canonical Entity (versa_domain_model.json)
        ↓
RDBMS Schema Table (VERSA_RDBMS_MODEL.md)
        ↓
Frappe DocType & App (VERSA_FRAPPE_IMPLEMENTATION_SPECIFICATION.md)
        ↓
Fields & Relationships (REL-001 to REL-028)
        ↓
Invariants & Rules (6 Invariants + 7 Rules)
        ↓
Automated Test Cases (TEST-STR-*, TEST-DOM-*, TEST-INV-*)
```

---

## 2. Master Entity Traceability Matrix (All 39 Canonical Entities)

| Domain ID | Canonical Entity | Classification | Platform / App | Frappe DocType | Key Fields & Relationships | Rules & Invariants | Implementation Mechanism | Test ID | Provenance | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ENT-001** | `Company` | `ERPNext_STANDARD` | `erpnext` | `Company` | `company_name`, `default_currency` (REL-001, REL-002) | `multi_company_isolation` | ERPNext Master + Query Filter | `TEST-STR-001` | `SOURCE` | Traceable |
| **ENT-002** | `Cost Center` | `ERPNext_STANDARD` | `erpnext` | `Cost Center` | `cost_center_name`, `company` (REL-001) | `multi_company_isolation` | ERPNext Master | `TEST-STR-002` | `SOURCE` | Traceable |
| **ENT-003** | `Customer` | `ERPNext_STANDARD` | `erpnext` | `Customer` | `customer_name`, `versa_buyer_code` (REL-004, REL-007, REL-009, REL-019) | `order_fulfillment_closure` | ERPNext Master + Custom Fields | `TEST-STR-003` | `SOURCE` | Traceable |
| **ENT-004** | `Supplier` | `ERPNext_STANDARD` | `erpnext` | `Supplier` | `supplier_name`, `supplier_type` (REL-005, REL-006, REL-008, REL-023, REL-024) | `supplier_otif_scoring` | ERPNext Master + Extension | `TEST-STR-004` | `SOURCE` | Traceable |
| **ENT-005** | `Item` | `ERPNext_STANDARD` | `erpnext` | `Item` | `item_code`, `is_fabric_roll_tracked` (REL-003, REL-011, REL-015, REL-020, REL-026) | `quality_gate_enforcement` | ERPNext Master + Custom Fields | `TEST-STR-005` | `SOURCE` | Traceable |
| **ENT-006** | `Warehouse` | `ERPNext_STANDARD` | `erpnext` | `Warehouse` | `warehouse_name`, `company` (REL-002, REL-010, REL-017) | `multi_company_isolation` | ERPNext Master + Custom Fields | `TEST-STR-006` | `SOURCE` | Traceable |
| **ENT-007** | `Batch` | `ERPNext_STANDARD` | `erpnext` | `Batch` | `batch_id`, `item`, `versa_shade` (REL-003, REL-016) | `fabric_roll_dual_uom_conservation`| ERPNext Master + Custom Fields | `TEST-STR-007` | `SOURCE` | Traceable |
| **ENT-008** | `Sales Order` | `ERPNext_STANDARD` | `erpnext` | `Sales Order` | `customer`, `versa_style` (REL-004, REL-021, REL-027) | `order_matrix_conservation` | ERPNext Submittable + Hook | `TEST-INV-002` | `SOURCE` | Traceable |
| **ENT-009** | `Purchase Order` | `ERPNext_STANDARD` | `erpnext` | `Purchase Order` | `supplier`, `versa_material_spec` (REL-005) | `three_way_matching` | ERPNext Submittable + Approval Rule| `TEST-INV-008` | `SOURCE` | Traceable |
| **ENT-010** | `Purchase Receipt` | `ERPNext_STANDARD` | `erpnext` | `Purchase Receipt`| `supplier`, `versa_qc_result` (REL-006) | `quality_gate_enforcement` | ERPNext Submittable + Hook | `TEST-INV-005` | `SOURCE` | Traceable |
| **ENT-011** | `Delivery Note` | `ERPNext_STANDARD` | `erpnext` | `Delivery Note` | `customer`, `versa_packing_plan` (REL-007) | `dispatch_invoice_reconciliation` | ERPNext Submittable + Custom Fields | `TEST-INV-009` | `SOURCE` | Traceable |
| **ENT-012** | `Purchase Invoice` | `ERPNext_STANDARD` | `erpnext` | `Purchase Invoice`| `supplier`, `versa_job_work_order` (REL-008) | `job_work_excess_loss_penalty` | ERPNext Submittable + Debit Hook | `TEST-INV-007` | `SOURCE` | Traceable |
| **ENT-013** | `Sales Invoice` | `ERPNext_STANDARD` | `erpnext` | `Sales Invoice` | `customer`, `versa_style` (REL-009) | `dispatch_invoice_reconciliation` | ERPNext Submittable + Validation | `TEST-INV-009` | `SOURCE` | Traceable |
| **ENT-014** | `Stock Entry` | `ERPNext_STANDARD` | `erpnext` | `Stock Entry` | `to_warehouse`, `versa_job_work_order` (REL-010) | `job_work_mass_balance` | ERPNext Submittable + Hook | `TEST-INV-001` | `SOURCE` | Traceable |
| **ENT-015** | `Versa Material Spec` | `VERSA_EXTENSION` | `versa_textile` | `Versa Material Spec` | `item`, `specification_version` (REL-011, REL-012, REL-013) | Engineering Spec Binding | Custom DocType | `TEST-STR-015` | `SOURCE` | Traceable |
| **ENT-016** | `Versa Yarn Spec` | `VERSA_EXTENSION` | `versa_textile` | `Versa Yarn Spec` | `material_spec`, `yarn_count`, `csp_min` (REL-012) | Spinning Parameter Check | Custom DocType | `TEST-STR-016` | `SOURCE` | Traceable |
| **ENT-017** | `Versa Fabric Spec` | `VERSA_EXTENSION` | `versa_textile` | `Versa Fabric Spec` | `material_spec`, `target_gsm`, `cuttable_width_inches` (REL-013) | Fabric Dimension Check | Custom DocType | `TEST-STR-017` | `SOURCE` | Traceable |
| **ENT-018** | `Versa Fabric Roll` | `VERSA_EXTENSION` | `versa_textile` | `Versa Fabric Roll` | `roll_barcode`, `net_weight_kg`, `length_meters` (REL-015, REL-016, REL-017, REL-018) | `fabric_roll_dual_uom_conservation`, `astm_d5430_4point_defect_scoring` | Custom DocType + Controller | `TEST-INV-004` | `SOURCE` | Traceable |
| **ENT-019** | `Versa Style` | `VERSA_EXTENSION` | `versa_textile` | `Versa Style` | `style_no`, `buyer_customer`, `base_fabric_item` (REL-019, REL-020, REL-022) | Product Engineering Invariant | Custom DocType + Child Tables | `TEST-STR-019` | `SOURCE` | Traceable |
| **ENT-020** | `Versa Job Worker` | `VERSA_EXTENSION` | `versa_jobwork` | `Versa Job Worker` | `supplier`, `compliance_status` (REL-023) | Approved Vendor List (AVL) | Custom DocType + Child Table | `TEST-STR-020` | `SOURCE` | Traceable |
| **ENT-021** | `Versa QC Spec` | `VERSA_EXTENSION` | `versa_quality` | `Versa QC Spec` | `spec_name`, `version`, `material_type` (REL-025) | Versioned Spec Governance | Custom DocType + Child Table | `TEST-STR-021` | `SOURCE` | Traceable |
| **ENT-022** | `Versa Carton` | `VERSA_EXTENSION` | `versa_export` | `Versa Carton` | `carton_barcode`, `packing_plan` (REL-028) | `carton_packing_conservation` | Custom DocType + Child Table | `TEST-INV-003` | `SOURCE` | Traceable |
| **ENT-023** | `Versa Job Work Order`| `VERSA_TRANSACTION` | `versa_jobwork` | `Versa Job Work Order`| `job_worker`, `process`, `allowed_loss_pct` (REL-024) | `job_work_mass_balance`, `job_work_excess_loss_penalty` | Custom Submittable DocType | `TEST-INV-001` | `SOURCE` | Traceable |
| **ENT-024** | `Versa QC Result` | `VERSA_TRANSACTION` | `versa_quality` | `Versa QC Result` | `qc_spec`, `item`, `overall_status` (REL-025, REL-026) | `quality_gate_enforcement`, `astm_d5430_4point_defect_scoring` | Custom Submittable DocType | `TEST-INV-005` | `SOURCE` | Traceable |
| **ENT-025** | `Versa Packing Plan` | `VERSA_TRANSACTION` | `versa_export` | `Versa Packing Plan` | `sales_order`, `style`, `planned_total_pcs` (REL-027, REL-028) | `carton_packing_conservation` | Custom Submittable DocType | `TEST-INV-003` | `SOURCE` | Traceable |
| **ENT-026** | `Versa Style Material`| `VERSA_CHILD_TABLE` | `versa_textile` | `Versa Style Material`| `item`, `consumption_per_garment` | BOM Consumption Invariant | Custom Child Table | `TEST-STR-026` | `SOURCE` | Traceable |
| **ENT-027** | `Versa Style Operation`| `VERSA_CHILD_TABLE` | `versa_textile` | `Versa Style Operation`| `operation_name`, `sam_minutes` | Costing SAM Invariant | Custom Child Table | `TEST-STR-027` | `SOURCE` | Traceable |
| **ENT-028** | `Versa Style Colourway`| `VERSA_CHILD_TABLE` | `versa_textile` | `Versa Style Colourway`| `colour`, `shade` | Style Colourway Definition | Custom Child Table | `TEST-STR-028` | `SOURCE` | Traceable |
| **ENT-029** | `Versa Style Size` | `VERSA_CHILD_TABLE` | `versa_textile` | `Versa Style Size` | `size_code`, `sort_order` | Size Range Grid Invariant | Custom Child Table | `TEST-STR-029` | `SOURCE` | Traceable |
| **ENT-030** | `Versa Order Matrix` | `VERSA_CHILD_TABLE` | `versa_textile` | `Versa Order Matrix` | `style`, `colour`, `shade`, `size_code`, `ordered_qty` (REL-021, REL-022) | `order_matrix_conservation`, `production_cutting_allowance` | Custom Child Table on Sales Order | `TEST-INV-002` | `SOURCE` | Traceable |
| **ENT-031** | `Versa Job Worker Process`| `VERSA_CHILD_TABLE` | `versa_jobwork` | `Versa Job Worker Process`| `process`, `machine_spec`, `daily_capacity` | AVL Capability Matching | Custom Child Table | `TEST-STR-031` | `SOURCE` | Traceable |
| **ENT-032** | `Versa Job Work Material`| `VERSA_CHILD_TABLE` | `versa_jobwork` | `Versa Job Work Material`| `item`, `batch`, `roll_barcode`, `issued_qty` | Material Issue Lineage | Custom Child Table | `TEST-STR-032` | `SOURCE` | Traceable |
| **ENT-033** | `Versa Job Work Result`| `VERSA_CHILD_TABLE` | `versa_jobwork` | `Versa Job Work Result`| `output_qty`, `process_loss_qty`, `scrap_qty`, `unaccounted_qty` | `job_work_mass_balance` | Custom Child Table | `TEST-INV-001` | `SOURCE` | Traceable |
| **ENT-034** | `Versa QC Parameter` | `VERSA_CHILD_TABLE` | `versa_quality` | `Versa QC Parameter` | `parameter_code`, `test_method`, `min_limit`, `max_limit` | Parameter Specification | Custom Child Table | `TEST-STR-034` | `SOURCE` | Traceable |
| **ENT-035** | `Versa QC Measurement`| `VERSA_CHILD_TABLE` | `versa_quality` | `Versa QC Measurement`| `parameter_code`, `reading_1`, `reading_2`, `reading_3`, `reading_status` | Lab Reading Evaluation | Custom Child Table | `TEST-STR-035` | `SOURCE` | Traceable |
| **ENT-036** | `Versa Carton Item` | `VERSA_CHILD_TABLE` | `versa_export` | `Versa Carton Item` | `style`, `colour`, `size_code`, `qty_pcs` | `carton_packing_conservation` | Custom Child Table | `TEST-INV-003` | `SOURCE` | Traceable |
| **ENT-037** | `Versa Colour` | `REFERENCE` | `versa_textile` | `Versa Colour` | `colour_name`, `colour_code`, `pantone_ref` (REL-014) | Master Colour Taxonomy | Custom Reference Master | `TEST-STR-037` | `SOURCE` | Traceable |
| **ENT-038** | `Versa Shade` | `REFERENCE` | `versa_textile` | `Versa Shade` | `colour`, `shade_name`, `lab_dip_no` (REL-014, REL-018) | Master Shade Taxonomy | Custom Reference Master | `TEST-STR-038` | `SOURCE` | Traceable |
| **ENT-039** | `Versa Approval Rule` | `CONFIGURATION` | `versa_core` | `Versa Approval Rule`| `document_type`, `min_amount`, `max_amount`, `approver_role` | Multi-Level Financial Approval Matrix | Custom Configuration DocType | `TEST-STR-039` | `SOURCE` | Traceable |

---

## 3. Invariant & Rule Traceability Matrix (All 13 Rules)

| Invariant / Rule ID | Classification | Business Purpose | Trigger / Hook Point | Enforcing Controller / Method | Test ID | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `job_work_mass_balance` | `CANONICAL_INVARIANT` | Conserves raw material mass across subcontracting process | `Versa Job Work Order.before_submit` | `versa_jobwork.controllers.job_work_order.validate_mass_balance` | `TEST-INV-001` | Active |
| `order_matrix_conservation` | `CANONICAL_INVARIANT` | Matches Sales Order matrix cell totals to line items | `Sales Order.validate` | `versa_textile.events.sales_order.validate_order_matrix` | `TEST-INV-002` | Active |
| `carton_packing_conservation` | `CANONICAL_INVARIANT` | Ensures packed carton quantities do not exceed buyer tolerance | `Versa Packing Plan.before_submit` | `versa_export.controllers.packing_plan.validate_packing_conservation` | `TEST-INV-003` | Active |
| `fabric_roll_dual_uom_conservation` | `CANONICAL_INVARIANT` | Verifies weight vs length $\times$ width $\times$ GSM formula | `Versa Fabric Roll.validate` | `versa_textile.controllers.fabric_roll.validate_dual_uom` | `TEST-INV-004` | Active |
| `quality_gate_enforcement` | `CANONICAL_INVARIANT` | Blocks Purchase Receipt submission without approved QC | `Purchase Receipt.before_submit` | `versa_quality.events.purchase_receipt.check_qc_conformance` | `TEST-INV-005` | Active |
| `multi_company_isolation` | `CANONICAL_INVARIANT` | Prevents cross-company document visibility and postings | `frappe.permission_query_conditions` | `versa_core.permissions.apply_company_query_conditions` | `TEST-INV-006` | Active |
| `job_work_excess_loss_penalty` | `BUSINESS_RULE` | Applies material debit on subcontractor service invoice | `Purchase Invoice.validate` | `versa_jobwork.events.purchase_invoice.apply_excess_loss_debit` | `TEST-INV-007` | Active |
| `three_way_matching` | `BUSINESS_RULE` | Enforces PO price, Receipt qty, Invoice amount match | `Purchase Invoice.validate` | `erpnext.accounts.doctype.purchase_invoice.purchase_invoice.validate` | `TEST-INV-008` | Active |
| `dispatch_invoice_reconciliation` | `BUSINESS_RULE` | Validates cumulative invoiced qty $\le$ delivered - returned | `Sales Invoice.validate` | `erpnext.accounts.doctype.sales_invoice.sales_invoice.validate` | `TEST-INV-009` | Active |
| `production_cutting_allowance` | `WORKFLOW_RULE` | Adds fabric cutting allowance to raw material explosion | `Sales Order.on_submit` | `versa_textile.events.sales_order.calculate_cutting_allowance` | `TEST-INV-010` | Active |
| `order_fulfillment_closure` | `WORKFLOW_RULE` | Closes Sales Order when delivered within short tolerance | `Delivery Note.on_submit` | `erpnext.selling.doctype.sales_order.sales_order.update_status` | `TEST-INV-011` | Active |
| `astm_d5430_4point_defect_scoring` | `DERIVED_METRIC` | Computes 4-point defect score per 100 sq yds | `Versa QC Result.validate` | `versa_quality.doctype.versa_qc_result.versa_qc_result.calculate_4point_score` | `TEST-INV-012` | Active |
| `supplier_otif_scoring` | `DERIVED_METRIC` | Updates running on-time in-full performance index | `Purchase Receipt.on_submit` | `versa_core.analytics.update_supplier_otif` | `TEST-INV-013` | Active |

---

## 4. Relationship Traceability Verification (REL-001 to REL-028)

Every one of the 28 canonical relationships is implemented via standard Frappe `Link`, `Dynamic Link`, or `Table` fields:
- 10 ERPNext Standard Internal Relationships (`REL-001` to `REL-010`)
- 3 Spec Engineering & Extension Relationships (`REL-011`, `REL-012`, `REL-013`)
- 1 Master Taxonomy Relationship (`REL-014`)
- 4 Physical Fabric Roll Traceability Relationships (`REL-015` to `REL-018`)
- 2 Style Engineering Relationships (`REL-019`, `REL-020`)
- 2 Order Matrix Subcontracting Relationships (`REL-021`, `REL-022`)
- 2 Job Work Subcontracting Relationships (`REL-023`, `REL-024`)
- 2 Quality Inspection Target Relationships (`REL-025`, `REL-026`)
- 2 Export Packing & Cartonization Relationships (`REL-027`, `REL-028`)
