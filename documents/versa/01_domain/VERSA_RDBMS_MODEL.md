# VERSA ERP LOGICAL RDBMS SCHEMA MODEL

## 1. Scope & Design Principles

- **Environment:** Logical RDBMS Schema (Target: MariaDB 10.6+ / PostgreSQL 14+ through Frappe ORM).
- **Design Rules:**
  - Strict Third Normal Form (3NF) for transactional and master data.
  - Foreign keys reference ERPNext standard tables (`tabItem`, `tabCustomer`, `tabSupplier`, `tabWarehouse`, `tabSales Order`, `tabPurchase Order`, etc.) without altering base schemas.
  - Synthetic Primary Keys (`VARCHAR(140)` conforming to Frappe document naming standards).
  - Explicit Natural Keys enforced via `UNIQUE` constraints.
  - Audit columns (`creation`, `modified`, `modified_by`, `owner`, `docstatus`) included across all tables.
  - Multi-tenant company isolation enforced with indexed `company` column.

---

## 2. Table Specifications & Schema Definitions

### 2.1 Textile Specifications & Master Data

#### `tabVersa Material Spec`
```sql
CREATE TABLE `tabVersa Material Spec` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `creation` DATETIME(6) NOT NULL,
    `modified` DATETIME(6) NOT NULL,
    `modified_by` VARCHAR(140) NOT NULL,
    `owner` VARCHAR(140) NOT NULL,
    `docstatus` INT(1) NOT NULL DEFAULT 0,
    `company` VARCHAR(140) NOT NULL,
    `item` VARCHAR(140) NOT NULL,
    `specification_version` VARCHAR(20) NOT NULL DEFAULT 'V1.0',
    `material_type` ENUM('Yarn', 'Fabric', 'Dye/Chemical', 'Trim/Accessory', 'Packing Material') NOT NULL,
    `composition` VARCHAR(255) NOT NULL,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `remarks` TEXT NULL,
    UNIQUE KEY `uk_item_version` (`item`, `specification_version`),
    INDEX `idx_vms_item` (`item`),
    INDEX `idx_vms_type` (`material_type`),
    INDEX `idx_vms_company` (`company`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Yarn Spec`
```sql
CREATE TABLE `tabVersa Yarn Spec` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `material_spec` VARCHAR(140) NOT NULL,
    `yarn_count` VARCHAR(50) NOT NULL,
    `count_system` ENUM('Ne', 'Nm', 'Denier', 'Tex') NOT NULL DEFAULT 'Ne',
    `ply` INT NOT NULL DEFAULT 1,
    `spinning_process` ENUM('Carded', 'Combed', 'Compact Combed', 'Open End / Rotor', 'Airjet') NOT NULL,
    `twist_type` ENUM('Z-Twist', 'S-Twist') NOT NULL DEFAULT 'Z-Twist',
    `tpi` DECIMAL(8,2) NULL,
    `csp_min` DECIMAL(8,2) NULL,
    `origin_mill` VARCHAR(140) NULL,
    UNIQUE KEY `uk_vys_spec` (`material_spec`),
    INDEX `idx_vys_count` (`yarn_count`),
    FOREIGN KEY (`material_spec`) REFERENCES `tabVersa Material Spec`(`name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Fabric Spec`
```sql
CREATE TABLE `tabVersa Fabric Spec` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `material_spec` VARCHAR(140) NOT NULL,
    `fabric_structure` ENUM('Single Jersey', '1x1 Rib', '2x2 Rib', 'Interlock', 'Fleece - 2 Thread', 'Fleece - 3 Thread', 'Pique', 'Honey Comb', 'Waffle', 'Terry', 'Jacquard') NOT NULL,
    `target_gsm` DECIMAL(8,2) NOT NULL,
    `gsm_tolerance_pct` DECIMAL(5,2) NOT NULL DEFAULT 3.00,
    `cuttable_width_inches` DECIMAL(8,2) NOT NULL,
    `total_width_inches` DECIMAL(8,2) NULL,
    `knitting_gauge` VARCHAR(20) NULL,
    `knitting_dia` VARCHAR(20) NULL,
    `finish_type` ENUM('Greige', 'Bleached', 'Dyed', 'Mercerized', 'Brushed / Sueded', 'Bio-Washed', 'Heat Set') NOT NULL DEFAULT 'Greige',
    `shrinkage_length_pct_max` DECIMAL(5,2) NOT NULL DEFAULT 5.00,
    `shrinkage_width_pct_max` DECIMAL(5,2) NOT NULL DEFAULT 5.00,
    `spirality_pct_max` DECIMAL(5,2) NOT NULL DEFAULT 4.00,
    UNIQUE KEY `uk_vfs_spec` (`material_spec`),
    INDEX `idx_vfs_gsm` (`target_gsm`),
    FOREIGN KEY (`material_spec`) REFERENCES `tabVersa Material Spec`(`name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Colour` & `tabVersa Shade`
```sql
CREATE TABLE `tabVersa Colour` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `colour_code` VARCHAR(50) NOT NULL UNIQUE,
    `colour_name` VARCHAR(100) NOT NULL,
    `colour_family` VARCHAR(50) NOT NULL,
    `pantone_ref` VARCHAR(50) NULL,
    `hex_code` VARCHAR(7) NULL,
    INDEX `idx_vc_family` (`colour_family`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tabVersa Shade` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `colour` VARCHAR(140) NOT NULL,
    `shade_code` VARCHAR(50) NOT NULL,
    `shade_name` VARCHAR(100) NOT NULL,
    `lab_dip_no` VARCHAR(50) NULL,
    `recipe_ref` VARCHAR(140) NULL,
    UNIQUE KEY `uk_colour_shade` (`colour`, `shade_code`),
    INDEX `idx_vs_colour` (`colour`),
    FOREIGN KEY (`colour`) REFERENCES `tabVersa Colour`(`name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.2 Traceability & Physical Inventory Units

#### `tabVersa Fabric Roll`
```sql
CREATE TABLE `tabVersa Fabric Roll` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `creation` DATETIME(6) NOT NULL,
    `modified` DATETIME(6) NOT NULL,
    `modified_by` VARCHAR(140) NOT NULL,
    `owner` VARCHAR(140) NOT NULL,
    `docstatus` INT(1) NOT NULL DEFAULT 0,
    `company` VARCHAR(140) NOT NULL,
    `roll_barcode` VARCHAR(100) NOT NULL UNIQUE,
    `item` VARCHAR(140) NOT NULL,
    `batch` VARCHAR(140) NOT NULL,
    `roll_no` INT NOT NULL,
    `warehouse` VARCHAR(140) NOT NULL,
    `net_weight_kg` DECIMAL(12,3) NOT NULL,
    `gross_weight_kg` DECIMAL(12,3) NOT NULL,
    `length_meters` DECIMAL(12,3) NOT NULL,
    `actual_gsm` DECIMAL(8,2) NULL,
    `actual_width_inches` DECIMAL(8,2) NULL,
    `shade` VARCHAR(140) NULL,
    `quality_grade` ENUM('Grade A', 'Grade B', 'Grade C', 'Quarantine', 'Rejected') NOT NULL DEFAULT 'Quarantine',
    `defect_points_4point` DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    `status` ENUM('In Stock', 'Issued to Cutting', 'Issued to Job Work', 'Consumed', 'Scrapped') NOT NULL DEFAULT 'In Stock',
    INDEX `idx_vfr_item_batch` (`item`, `batch`),
    INDEX `idx_vfr_wh` (`warehouse`),
    INDEX `idx_vfr_grade` (`quality_grade`),
    INDEX `idx_vfr_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.3 Garment Style Master & Matrix Modeling

#### `tabVersa Style`
```sql
CREATE TABLE `tabVersa Style` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `creation` DATETIME(6) NOT NULL,
    `modified` DATETIME(6) NOT NULL,
    `modified_by` VARCHAR(140) NOT NULL,
    `owner` VARCHAR(140) NOT NULL,
    `docstatus` INT(1) NOT NULL DEFAULT 0,
    `company` VARCHAR(140) NOT NULL,
    `style_no` VARCHAR(100) NOT NULL,
    `buyer_customer` VARCHAR(140) NOT NULL,
    `brand` VARCHAR(100) NULL,
    `season` VARCHAR(50) NOT NULL,
    `garment_type` VARCHAR(50) NOT NULL,
    `gender_category` ENUM('Men', 'Women', 'Boys', 'Girls', 'Infants', 'Unisex') NOT NULL DEFAULT 'Unisex',
    `base_fabric_item` VARCHAR(140) NOT NULL,
    `target_sam_minutes` DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    `status` ENUM('Development', 'Sampling', 'Costed', 'Approved for Production', 'Archived') NOT NULL DEFAULT 'Development',
    UNIQUE KEY `uk_style_buyer` (`company`, `buyer_customer`, `style_no`),
    INDEX `idx_vs_buyer` (`buyer_customer`),
    INDEX `idx_vs_season` (`season`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Style Material` (Child Table)
```sql
CREATE TABLE `tabVersa Style Material` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `item` VARCHAR(140) NOT NULL,
    `material_type` VARCHAR(50) NOT NULL,
    `consumption_per_pc` DECIMAL(12,4) NOT NULL,
    `uom` VARCHAR(50) NOT NULL,
    `wastage_pct` DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    `is_mandatory` TINYINT(1) NOT NULL DEFAULT 1,
    INDEX `idx_vsm_parent` (`parent`),
    INDEX `idx_vsm_item` (`item`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Style Operation` (Child Table)
```sql
CREATE TABLE `tabVersa Style Operation` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `operation_name` VARCHAR(140) NOT NULL,
    `sequence_no` INT NOT NULL,
    `standard_sam` DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    `subcontractable` TINYINT(1) NOT NULL DEFAULT 0,
    `default_piece_rate` DECIMAL(12,4) NOT NULL DEFAULT 0.00,
    INDEX `idx_vso_parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Order Matrix` (Child Table on Sales Order)
```sql
CREATE TABLE `tabVersa Order Matrix` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `style` VARCHAR(140) NOT NULL,
    `colour` VARCHAR(140) NOT NULL,
    `shade` VARCHAR(140) NULL,
    `size_code` VARCHAR(20) NOT NULL,
    `ordered_qty` INT NOT NULL DEFAULT 0,
    `confirmed_qty` INT NOT NULL DEFAULT 0,
    `produced_qty` INT NOT NULL DEFAULT 0,
    `packed_qty` INT NOT NULL DEFAULT 0,
    `delivered_qty` INT NOT NULL DEFAULT 0,
    INDEX `idx_vom_parent` (`parent`),
    INDEX `idx_vom_style_matrix` (`style`, `colour`, `size_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.4 Job Work Subcontracting Schema

#### `tabVersa Job Worker` (Vendor Profile Extension)
```sql
CREATE TABLE `tabVersa Job Worker` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `supplier` VARCHAR(140) NOT NULL UNIQUE,
    `process_capabilities` TEXT NOT NULL,
    `machine_count` INT NOT NULL DEFAULT 0,
    `daily_capacity_kg` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `standard_loss_tolerance_pct` DECIMAL(5,2) NOT NULL DEFAULT 3.00,
    `quality_rating` DECIMAL(3,2) NOT NULL DEFAULT 5.00,
    `compliance_status` ENUM('Compliant', 'Under Review', 'Blacklisted') NOT NULL DEFAULT 'Compliant',
    INDEX `idx_vjw_supplier` (`supplier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Job Work Order`
```sql
CREATE TABLE `tabVersa Job Work Order` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `creation` DATETIME(6) NOT NULL,
    `modified` DATETIME(6) NOT NULL,
    `modified_by` VARCHAR(140) NOT NULL,
    `owner` VARCHAR(140) NOT NULL,
    `docstatus` INT(1) NOT NULL DEFAULT 0,
    `company` VARCHAR(140) NOT NULL,
    `job_worker` VARCHAR(140) NOT NULL,
    `process` ENUM('Knitting', 'Dyeing / Finishing', 'All-Over Printing', 'Chest Printing', 'Embroidery', 'Washing / Bio-Polishing', 'Stitching', 'Ironing / Packing') NOT NULL,
    `source_doctype` VARCHAR(50) NULL,
    `source_name` VARCHAR(140) NULL,
    `planned_start_date` DATE NOT NULL,
    `due_date` DATE NOT NULL,
    `planned_input_qty` DECIMAL(12,3) NOT NULL,
    `planned_output_qty` DECIMAL(12,3) NOT NULL,
    `uom` VARCHAR(50) NOT NULL,
    `allowed_loss_pct` DECIMAL(5,2) NOT NULL DEFAULT 3.00,
    `rate_per_unit` DECIMAL(12,4) NOT NULL,
    `billing_basis` ENUM('Per Input Weight', 'Per Output Weight', 'Per Piece', 'Per Meter') NOT NULL,
    `status` ENUM('Draft', 'Issued', 'In Progress', 'Partially Received', 'Completed', 'Cancelled', 'Closed') NOT NULL DEFAULT 'Draft',
    INDEX `idx_vjwo_worker` (`job_worker`),
    INDEX `idx_vjwo_company` (`company`),
    INDEX `idx_vjwo_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Job Work Material` (Child Table: Input/Issue)
```sql
CREATE TABLE `tabVersa Job Work Material` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `item` VARCHAR(140) NOT NULL,
    `batch` VARCHAR(140) NULL,
    `roll_barcode` VARCHAR(100) NULL,
    `qty_issued` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `qty_returned` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `uom` VARCHAR(50) NOT NULL,
    INDEX `idx_vjwm_parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa Job Work Result` (Child Table: Output/Reconciliation)
```sql
CREATE TABLE `tabVersa Job Work Result` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `output_item` VARCHAR(140) NOT NULL,
    `output_batch` VARCHAR(140) NOT NULL,
    `qty_received` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `process_loss_qty` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `wastage_qty` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `rework_qty` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `rejected_qty` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `unaccounted_qty` DECIMAL(12,3) NOT NULL DEFAULT 0.00,
    `quality_status` ENUM('Pending Inspection', 'Passed', 'Concession', 'Rejected') NOT NULL DEFAULT 'Pending Inspection',
    INDEX `idx_vjwr_parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.5 Quality Inspection & Measurement Schema

#### `tabVersa QC Spec` & `tabVersa QC Parameter`
```sql
CREATE TABLE `tabVersa QC Spec` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `spec_code` VARCHAR(100) NOT NULL UNIQUE,
    `spec_name` VARCHAR(140) NOT NULL,
    `material_type` VARCHAR(50) NOT NULL,
    `version` VARCHAR(20) NOT NULL DEFAULT '1.0',
    `is_active` TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tabVersa QC Parameter` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `parameter_code` VARCHAR(50) NOT NULL,
    `parameter_name` VARCHAR(100) NOT NULL,
    `target_value` VARCHAR(100) NULL,
    `lower_limit` DECIMAL(12,4) NULL,
    `upper_limit` DECIMAL(12,4) NULL,
    `uom` VARCHAR(50) NULL,
    `test_method` VARCHAR(140) NULL,
    `is_mandatory` TINYINT(1) NOT NULL DEFAULT 1,
    INDEX `idx_vqp_parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### `tabVersa QC Result` & `tabVersa QC Measurement`
```sql
CREATE TABLE `tabVersa QC Result` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `creation` DATETIME(6) NOT NULL,
    `modified` DATETIME(6) NOT NULL,
    `docstatus` INT(1) NOT NULL DEFAULT 0,
    `company` VARCHAR(140) NOT NULL,
    `qc_spec` VARCHAR(140) NOT NULL,
    `inspection_type` ENUM('Incoming Material', 'In-Process Job Work', 'Cutting Panel', 'Stitching Inline', 'Final Garment AQL') NOT NULL,
    `source_doctype` VARCHAR(50) NOT NULL,
    `source_name` VARCHAR(140) NOT NULL,
    `item` VARCHAR(140) NOT NULL,
    `batch` VARCHAR(140) NULL,
    `roll_barcode` VARCHAR(100) NULL,
    `inspected_by` VARCHAR(140) NOT NULL,
    `inspection_date` DATE NOT NULL,
    `sample_size` INT NOT NULL DEFAULT 1,
    `overall_status` ENUM('Accepted', 'Accepted with Concession', 'Quarantine', 'Rejected') NOT NULL DEFAULT 'Quarantine',
    INDEX `idx_vqr_source` (`source_doctype`, `source_name`),
    INDEX `idx_vqr_item` (`item`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tabVersa QC Measurement` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `parameter_code` VARCHAR(50) NOT NULL,
    `reading_value` DECIMAL(12,4) NOT NULL,
    `status` ENUM('Pass', 'Fail', 'Deviation') NOT NULL,
    `remarks` VARCHAR(255) NULL,
    INDEX `idx_vqm_parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.6 Packing Plan & Carton Traceability Schema

#### `tabVersa Packing Plan` & `tabVersa Carton`
```sql
CREATE TABLE `tabVersa Packing Plan` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `company` VARCHAR(140) NOT NULL,
    `sales_order` VARCHAR(140) NOT NULL,
    `customer` VARCHAR(140) NOT NULL,
    `packing_type` ENUM('Solid Colour Solid Size', 'Ratio Packing Assorted', 'Customer Custom') NOT NULL,
    `total_planned_cartons` INT NOT NULL DEFAULT 0,
    `status` ENUM('Draft', 'In Packing', 'Completed', 'Dispatched') NOT NULL DEFAULT 'Draft'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tabVersa Carton` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `packing_plan` VARCHAR(140) NOT NULL,
    `carton_barcode` VARCHAR(100) NOT NULL UNIQUE,
    `carton_no` INT NOT NULL,
    `length_cm` DECIMAL(8,2) NOT NULL,
    `width_cm` DECIMAL(8,2) NOT NULL,
    `height_cm` DECIMAL(8,2) NOT NULL,
    `gross_weight_kg` DECIMAL(8,3) NOT NULL,
    `net_weight_kg` DECIMAL(8,3) NOT NULL,
    `total_pcs` INT NOT NULL DEFAULT 0,
    `delivery_note` VARCHAR(140) NULL,
    INDEX `idx_vc_plan` (`packing_plan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tabVersa Carton Item` (
    `name` VARCHAR(140) NOT NULL PRIMARY KEY,
    `parent` VARCHAR(140) NOT NULL,
    `parentfield` VARCHAR(140) NOT NULL,
    `parenttype` VARCHAR(140) NOT NULL,
    `idx` INT NOT NULL,
    `style` VARCHAR(140) NOT NULL,
    `colour` VARCHAR(140) NOT NULL,
    `size_code` VARCHAR(20) NOT NULL,
    `qty` INT NOT NULL DEFAULT 0,
    INDEX `idx_vci_parent` (`parent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 3. Referential Integrity & Deletion Rules

1. **Cascade vs Restrict Rules:**
   - Deleting a parent `Versa Material Spec`, `Versa Style`, `Versa Job Work Order`, or `Versa QC Spec` triggers `CASCADE` deletion on its child tables.
   - Deleting an ERPNext standard `Item`, `Customer`, or `Supplier` is **RESTRICTED** if references exist in active Versa domain tables.
2. **Audit Invariance:** All state-changing transactions write to Frappe's audit log (`tabVersion` / `tabActivity Log`).

