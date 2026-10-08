# VERSA ERP — QUALITY SUBSYSTEM IMPLEMENTATION SPECIFICATION

## 1. Executive Summary

This document specifies the technical implementation of the `versa_quality` application for VersaERP.

---

## 2. DocType Specifications

### 2.1 `Versa QC Spec` (Master DocType)
- **Module:** `Versa Quality` | **Type:** Master (Versioned)
- **Company Authority:** `SHARED_MASTER` (or optional Company link)
- **Naming Rule:** `format:VQC-{spec_name}-{version}`
- **Fields:**
  - `spec_name` (Data, Mandatory)
  - `version` (Data, Mandatory, Default: "V1.0")
  - `company` (Link: `Company`)
  - `material_type` (Select: `Yarn`, `Fabric`, `Dye/Chemical`, `Trim`, `Garment Final AQL`, Mandatory)
  - `buyer_customer` (Link: `Customer`)
  - `is_active` (Check, Default: 1)
  - `status` (Select: `Draft`, `Approved`, `Obsolete`, Default: `Draft`)
  - `effective_from` (Date)
  - `effective_to` (Date)
  - `approved_by` (Link: `User`)
  - `approval_date` (Date)
  - `parameters` (Table: `Versa QC Parameter`, Mandatory)
- **Server Validations:**
  - Enforces version syntax (`V1.0`, `V2.1`, etc.).
  - Ensures at least one parameter row is defined.
  - Ensures `min_limit <= max_limit`.
  - Rejects in-place mutation if historical `Versa QC Result` records reference this version.

### 2.2 `Versa QC Parameter` (Child Table of `Versa QC Spec`)
- **Module:** `Versa Quality` | **Type:** Child Table
- **Fields:**
  - `parameter_code` (Data, Mandatory, e.g. `FAB_GSM_ACTUAL`, `YRN_CSP`)
  - `parameter_name` (Data, Mandatory)
  - `test_method` (Data, Mandatory, e.g. `ASTM D3776`, `ISO 105-C06`)
  - `severity` (Select: `Critical`, `Major`, `Minor`, Mandatory)
  - `target_value` (Data)
  - `min_limit` (Float)
  - `max_limit` (Float)
  - `uom` (Link: `UOM`)
  - `sampling_required` (Int, Default: 3)
  - `tolerance_type` (Select: `Range`, `Minimum`, `Maximum`, `Exact`, `Visual/Pass-Fail`, Default: `Range`)

### 2.3 `Versa QC Result` (Transaction DocType)
- **Module:** `Versa Quality` | **Type:** Transaction (Submittable)
- **Company Authority:** `COMPANY_SCOPED_TRANSACTION`
- **Naming Rule:** `By "Naming Series" field` (`VQR-.YYYY.-.#####.`)
- **Fields:**
  - `company` (Link: `Company`, Mandatory, Immutable)
  - `qc_spec` (Link: `Versa QC Spec`, Mandatory)
  - `spec_version` (Data, Read-only)
  - `inspection_type` (Select: `Incoming Material`, `In-Process Job Work`, `Cutting Panel`, `Stitching Inline`, `Final Garment AQL`, Mandatory)
  - `source_doctype` (Select: `Purchase Receipt`, `Versa Job Work Order`, `Stock Entry`, Mandatory)
  - `source_name` (Dynamic Link: `source_doctype`, Mandatory)
  - `item` (Link: `Item`, Mandatory)
  - `batch` (Link: `Batch`)
  - `roll_barcode` (Data)
  - `sample_size` (Int, Default: 1, Mandatory)
  - `inspected_by` (Link: `User`, Mandatory)
  - `inspection_date` (Date, Mandatory)
  - `inspection_time` (Time)
  - `overall_status` (Select: `Draft`, `Accepted`, `Accepted with Concession`, `Quarantine`, `Rejected`, `Inconclusive`, Default: `Quarantine`, Mandatory)
  - `evaluation_summary` (Small Text, Read-only)
  - `concession_reason` (Small Text)
  - `concession_approved_by` (Link: `User`)
  - `concession_approval_date` (Date)
  - `inspected_length_yds` (Float)
  - `cuttable_width_inches` (Float)
  - `total_defect_points` (Float)
  - `defect_score_4point` (Float, Read-only)
  - `measurements` (Table: `Versa QC Measurement`, Mandatory)
  - `readings` (Table: `Versa QC Reading`)

### 2.4 `Versa QC Measurement` (Child Table of `Versa QC Result`)
- **Module:** `Versa Quality` | **Type:** Child Table
- **Fields:** `parameter_code`, `parameter_name`, `test_method`, `severity`, `target_value`, `min_limit`, `max_limit`, `reading_count`, `mean_reading`, `min_reading`, `max_reading`, `std_dev_reading`, `reading_status` (`Pass`, `Fail`, `Concession`, `Inconclusive`, `Not Evaluated`), `remarks`.

### 2.5 `Versa QC Reading` (Child Table of `Versa QC Result`)
- **Module:** `Versa Quality` | **Type:** Child Table
- **Fields:** `parameter_code`, `reading_no`, `reading_value`, `sampling_point`, `timestamp`, `operator`, `instrument`, `calibration_ref`.

---

## 3. Deterministic Evaluation Algorithms

### 3.1 Multi-Point Statistical Aggregation
$$\mu = \frac{1}{n} \sum_{i=1}^{n} x_i, \quad s = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (x_i - \mu)^2}$$

### 3.2 ASTM D5430 4-Point Defect Score
$$\text{Score} = \frac{\text{Total Defect Points} \times 3600}{\text{Inspected Length (yds)} \times \text{Cuttable Width (inches)}}$$
- **Score $\le 20.0 \implies$ Grade A (Accepted)**
- **$20.0 < \text{Score} \le 28.0 \implies$ Grade B (Concession)**
- **Score $> 28.0 \implies$ Grade C (Rejected)**

---

## 4. Quality Gate Integration Points

1. **Purchase Receipt Gate (`before_submit`):**
   - Blocks submission if items require QC and no `Accepted` or `Accepted with Concession` QC Result exists.
2. **Stock Entry Gate (`before_submit`):**
   - Blocks material issue movements if referenced rolls/batches are in `Quarantine` or `Rejected` status.
