# VERSA ERP DOMAIN MODEL SPECIFICATION

## 1. Document Context and Objective

- **Source Document:** `Source/Versa_ERP_Platform_Strategy_Tiruppur.docx`
- **Target Platform:** Versa ERP Platform (Regional Textile & Manufacturing ERP based on Frappe / ERPNext)
- **Role of GraphModel:** Design-time semantic analysis and domain model extraction environment. (Zero runtime dependency).
- **Domain Focus:** Tiruppur Textile & Garment Manufacturing Ecosystem, Procure-to-Pay (P2P), Order-to-Cash (O2C), Job Work Subcontracting, Multi-Tier Quality Control, and Cartonization/Export.

---

## 2. Core Business Entities & Classification

The Tiruppur textile ecosystem operates across interconnected, specialized manufacturing tiers: **Yarn Mills / Procurement → Knitting → Dyeing / Finishing → Printing / Embroidery → Garmenting (Cutting, Stitching, Trimming) → Quality Inspection → Packing / Cartonization → Export / Domestic Distribution**.

The domain architecture classifies entities into 5 primary categories:
1. **Foundation & Governance Masters** (Legal entities, commercial parties, locations, core catalog).
2. **Textile Domain Masters & Specifications** (Yarn, Fabric, Colour, Shade, Style, Routing, BOM).
3. **Physical & Inventory Traceability Objects** (Material Lots, Fabric Rolls, Production Batches, Cartons).
4. **Operational & Subcontracting Transactions** (Sales Matrix Orders, Job Work Orders, Material Movements).
5. **Quality Control & Assurance Evidence** (QC Specs, Parameters, Inspection Results, Physical Measurements).

---

## 3. Entity Classification & ERPNext Reuse Analysis

| Business Concept / Entity | Semantic Classification | ERPNext Binding Strategy | Justification & Architectural Boundary |
| :--- | :--- | :--- | :--- |
| **Company** | Foundation Master | `REUSE ERPNext` (`Company`) | Standard multi-company legal entity, GL root, chart of accounts. |
| **Business Unit / Branch** | Governance / Accounting | `REUSE ERPNext` (`Cost Center` / `Department`) | Organizational unit for budgeting, P&L segregation, and approval matrices. |
| **Customer** | Commercial Master | `REUSE ERPNext` (`Customer`) | Buyer / Brand legal entity, standard credit limits, invoicing party. |
| **Supplier** | Commercial Master | `REUSE ERPNext` (`Supplier`) | Raw material vendor, trims supplier, chemical supplier. |
| **Job Worker** | Commercial / Vendor Extension | `EXTEND ERPNext` (`Supplier` + `Versa Job Worker`) | ERPNext `Supplier` handles payables; `Versa Job Worker` captures process capabilities, machine gauge/dia, capacity, loss tolerances, compliance rating. |
| **Item** | Core Catalog | `REUSE ERPNext` (`Item`) | Base SKU for stock ledger, valuation, taxation, and billing. |
| **Item Group** | Catalog Taxonomy | `REUSE ERPNext` (`Item Group`) | Hierarchy: Raw Material (Yarn, Greige, Dye, Trims), Finished Goods (Fabric, Garment), Packing. |
| **Warehouse** | Storage / Location | `REUSE ERPNext` (`Warehouse`) | Physical & logical locations: Raw Material Store, Quarantine, Job Worker Floor, FG Warehouse. |
| **UOM** | Unit of Measure | `REUSE ERPNext` (`UOM`) | Standard UOMs (Kg, Meter, Roll, Cone, Pcs, Bag, Carton). |
| **Material Specification** | Domain Specification | `NEW VERSA OBJECT` (`Versa Material Spec`) | Domain-level specification attached to base Item to avoid SKU explosion. |
| **Yarn Specification** | Domain Specification | `NEW VERSA OBJECT` (`Versa Yarn Spec`) | Fibre composition, English Count (Ne), Ply, Combed/Carded, Compact, Rotor, Twist, Mill. |
| **Fabric Specification** | Domain Specification | `NEW VERSA OBJECT` (`Versa Fabric Spec`) | Structure (Single Jersey, Rib, Interlock, Fleece), Composition, GSM, Cut/Width, Gauge, Dia, Finish. |
| **Colour Master** | Controlled Taxonomy | `NEW VERSA OBJECT` (`Versa Colour`) | Standardized global/buyer colour library (e.g. Pantone, Buyer Colour Codes). |
| **Shade Master** | Controlled Taxonomy | `NEW VERSA OBJECT` (`Versa Shade`) | Production/Lot shade variations (e.g., Shade A/B/C/D, Lab Dip reference). |
| **Material Lot** | Traceability Master | `EXTEND ERPNext` (`Batch` + `Versa Material Lot`) | Combines ERPNext stock batch with supplier lot reference, mill certificate, and lab test status. |
| **Fabric Roll** | Physical Traceability | `NEW VERSA OBJECT` (`Versa Fabric Roll`) | Physical roll unit tracking: Roll ID, Length (m), Weight (kg), Actual GSM, Width, Inspection Grade, Defect Map. |
| **Style (Garment Master)** | Product / Engineering Master | `NEW VERSA OBJECT` (`Versa Style`) | Garment design master: Style No, Buyer, Season, Garment Type, Tech Pack, Base Fabric, Base GSM. |
| **Style Material (BOM)** | Child Table / Formulation | `CHILD TABLE` (`Versa Style Material`) | Material requirement per style: Component Item, Spec, Consumption per piece, Scrap/Loss %. |
| **Style Operation (Routing)** | Child Table / Operations | `CHILD TABLE` (`Versa Style Operation`) | Sequential routing: Operation, Machine Type, Standard SAM/SMV, Subcontractable flag, Default Piece Rate. |
| **Style Colourway** | Child Table / Taxonomy | `CHILD TABLE` (`Versa Style Colourway`) | Supported colour & shade combinations for the style. |
| **Style Size Range** | Child Table / Sizing | `CHILD TABLE` (`Versa Style Size`) | Size grid definition (e.g. XS, S, M, L, XL, XXL) with dimensional measurement charts. |
| **Order Matrix** | Transaction Extension | `CHILD TABLE` (`Versa Order Matrix`) | Colour × Size quantity grid attached to Sales Order; auto-reconciles to standard line items. |
| **Job Work Order** | Transaction (Subcontract) | `NEW VERSA OBJECT` (`Versa Job Work Order`) | Subcontract process control document: Process (Knitting, Dyeing, Printing, Washing), Worker, Rate, Expected Loss %. |
| **Job Work Material** | Child Table (Issue/Return) | `CHILD TABLE` (`Versa Job Work Material`) | Issued materials (Yarn, Greige Fabric, Chemicals) tracked against specific Lots/Rolls. |
| **Job Work Result** | Child Table (Receipt/Loss) | `CHILD TABLE` (`Versa Job Work Result`) | Received processed goods, Process Loss (kg/m), Wastage, Rework Qty, Rejected Qty, Net Yield. |
| **Production Batch** | Manufacturing Execution | `NEW VERSA OBJECT` (`Versa Production Batch`) | Work-in-progress batch tracking cutting/stitching lots linked to Sales Orders and Styles. |
| **Production Batch Material** | Child Table | `CHILD TABLE` (`Versa Production Batch Material`) | Material consumption per production batch with lot/roll linkage. |
| **Production Batch Operation** | Child Table | `CHILD TABLE` (`Versa Production Batch Operation`) | Operation completion, operator tracking, hourly output, defect log. |
| **Quality Specification** | Quality Master | `NEW VERSA OBJECT` (`Versa QC Spec`) | Version-controlled inspection standard for material, process, or garment. |
| **Quality Parameter** | Child Table | `CHILD TABLE` (`Versa QC Parameter`) | Test parameter: Name, Target, Min Limit, Max Limit, UOM, Test Method (ISO, AATCC, ASTM). |
| **Quality Result** | Quality Transaction | `NEW VERSA OBJECT` (`Versa QC Result`) | Inspection event header linked to Source Doc (Receipt, Job Work Receipt, Production Batch, FG). |
| **Quality Measurement** | Child Table | `CHILD TABLE` (`Versa QC Measurement`) | Actual recorded values per parameter, sample readings, variance calculation, pass/fail disposition. |
| **Packing Plan** | Logistics / Packaging | `NEW VERSA OBJECT` (`Versa Packing Plan`) | Packing instructions linked to Sales Order: Ratio packing, Solid colour/solid size, Assorted. |
| **Carton** | Physical Logistics | `NEW VERSA OBJECT` (`Versa Carton`) | Physical carton unit: Carton No, Barcode/RFID, Dimensions (L×W×H), Tare Weight, Gross Weight, Net Weight. |
| **Carton Item** | Child Table | `CHILD TABLE` (`Versa Carton Item`) | Style, Colour, Size, and Pieces packed per carton. |
| **Sales Order / Purchase Order** | Commercial Transaction | `REUSE ERPNext` (`Sales Order`, `Purchase Order`) | Standard commercial commitments with Versa extensions for Matrix, Specs, and Job Work. |
| **Purchase Receipt / Delivery Note** | Stock Movement | `REUSE ERPNext` (`Purchase Receipt`, `Delivery Note`) | Authoritative stock ledger updates integrated with Fabric Rolls, Lots, and Cartons. |
| **Purchase / Sales Invoice** | Financial Transaction | `REUSE ERPNext` (`Purchase Invoice`, `Sales Invoice`) | Authoritative Accounts Payable / Receivable and General Ledger postings. |
| **Payment Entry** | Treasury / Cash Flow | `REUSE ERPNext` (`Payment Entry`) | Authoritative bank and cash settlements against invoices. |

---

## 4. Detailed Entity Specifications

### 4.1 Textile Material Specification (`Versa Material Spec`)
- **Business Meaning:** Encapsulates the physical, structural, and chemical parameters of textile raw materials and intermediates. Decouples domain parameters from stock SKUs.
- **Identity & Keys:** Natural Key: `(item_code, specification_version)`. System ID: Auto-name hash/series (`VMS-.#####.`).
- **Attributes:**
  - `item` (Link: `Item` [Mandatory])
  - `material_type` (Select: `Yarn`, `Fabric`, `Dye/Chemical`, `Trim/Accessory`, `Packing Material`)
  - `composition` (Data: e.g., "100% Combed Cotton", "95% Cotton 5% Elastane", "60/40 CVC")
  - `is_active` (Check: Default 1)
  - `specification_version` (Data: e.g. "V1.0")
- **Lifecycle States:** `Draft` → `Active` → `Superseded` → `Deprecated`.
- **Relationships:**
  - 1-to-1 with `Versa Yarn Spec` (when `material_type == 'Yarn'`)
  - 1-to-1 with `Versa Fabric Spec` (when `material_type == 'Fabric'`)
  - 1-to-Many with `Item` (Multiple items can conform to a standard specification)

### 4.2 Yarn Specification (`Versa Yarn Spec`)
- **Business Meaning:** Captures spinning and yarn structural parameters essential for knitting and weaving yield calculations.
- **Attributes:**
  - `material_spec` (Link: `Versa Material Spec` [Mandatory])
  - `yarn_count` (Data: e.g., "30s", "34s", "40s", "20/2")
  - `count_system` (Select: `Ne` [English Cotton], `Nm` [Metric], `Denier`, `Tex`)
  - `ply` (Int: e.g., 1, 2, 3)
  - `spinning_process` (Select: `Carded`, `Combed`, `Compact Combed`, `Open End / Rotor`, `Airjet`)
  - `twist_type` (Select: `Z-Twist`, `S-Twist`)
  - `twist_per_inch_tpi` (Float)
  - `csp_min` (Float: Count Strength Product minimum threshold)
  - `origin_mill` (Data: Mill / Spinning Unit Name)

### 4.3 Fabric Specification (`Versa Fabric Spec`)
- **Business Meaning:** Defines structural knit/woven characteristics, weight, cut width, shrinkage tolerances, and finishing requirements.
- **Attributes:**
  - `material_spec` (Link: `Versa Material Spec` [Mandatory])
  - `fabric_structure` (Select: `Single Jersey`, `1x1 Rib`, `2x2 Rib`, `Interlock`, `Fleece - 2 Thread`, `Fleece - 3 Thread`, `Pique`, `Honey Comb`, `Waffle`, `Terry`, `Jacquard`)
  - `target_gsm` (Float: Grams per Square Meter)
  - `gsm_tolerance_pct` (Float: Default ± 3.0%)
  - `cuttable_width_inches` (Float)
  - `total_width_inches` (Float)
  - `knitting_gauge` (Data: e.g. "24GG", "28GG")
  - `knitting_diameter_dia` (Data: e.g. "30 Inch", "32 Inch", "34 Inch")
  - `finish_type` (Select: `Greige`, `Bleached`, `Dyed`, `Mercerized`, `Brushed / Sueded`, `Bio-Washed`, `Heat Set`)
  - `shrinkage_length_pct_max` (Float: Maximum allowed shrinkage %)
  - `shrinkage_width_pct_max` (Float: Maximum allowed shrinkage %)
  - `spirality_pct_max` (Float: Maximum allowed spirality/torque %)

### 4.4 Fabric Roll (`Versa Fabric Roll`)
- **Business Meaning:** Physical unit of roll-level inventory. Enables roll-by-roll defect tracking, shrinkage grading, and cut-plan allocation.
- **Identity & Keys:** `roll_barcode` (Unique String), `(batch_no, roll_no)`.
- **Attributes:**
  - `roll_barcode` (Data: Unique Barcode/QR Code)
  - `item` (Link: `Item`)
  - `batch` (Link: `Batch` / `Versa Material Lot`)
  - `roll_no` (Int: Roll index within lot)
  - `net_weight_kg` (Float: Net fabric weight)
  - `gross_weight_kg` (Float: Total weight including core/tube)
  - `length_meters` (Float: Physical or calculated length)
  - `actual_gsm` (Float: Measured sample GSM)
  - `actual_width_inches` (Float: Measured width)
  - `shade` (Link: `Versa Shade`)
  - `quality_grade` (Select: `Grade A`, `Grade B`, `Grade C`, `Quarantine`, `Rejected`)
  - `defect_points_4point` (Float: ASTM D5430 4-point defect score per 100 sq yds)
  - `warehouse` (Link: `Warehouse`)
  - `status` (Select: `In Stock`, `Issued to Cutting`, `Issued to Job Work`, `Consumed`, `Scrapped`)

### 4.5 Garment Style Master (`Versa Style`)
- **Business Meaning:** Central product lifecycle and engineering entity for garment manufacturers, holding BOM, operations, grading, and tech pack data.
- **Identity & Keys:** `style_no` (Unique per Buyer/Company).
- **Attributes:**
  - `style_no` (Data: Primary Business Key)
  - `buyer_customer` (Link: `Customer` [Mandatory])
  - `brand` (Data: Buyer Brand / Sub-brand)
  - `season` (Select/Data: `Spring/Summer 2027`, `Autumn/Winter 2026`, etc.)
  - `garment_type` (Select: `T-Shirt`, `Polo Shirt`, `Hoodie`, `Joggers`, `Pajama`, `Dress`, `Leggings`, `Babywear`)
  - `gender_category` (Select: `Men`, `Women`, `Boys`, `Girls`, `Infants`, `Unisex`)
  - `base_fabric_item` (Link: `Item`)
  - `base_fabric_spec` (Link: `Versa Fabric Spec`)
  - `target_sam_minutes` (Float: Standard Allowed Minutes for stitching)
  - `status` (Select: `Development`, `Sampling`, `Costed`, `Approved for Production`, `Archived`)
- **Child Tables:**
  - `materials` (`Versa Style Material`)
  - `operations` (`Versa Style Operation`)
  - `colourways` (`Versa Style Colourway`)
  - `size_range` (`Versa Style Size`)

### 4.6 Job Work Order (`Versa Job Work Order`)
- **Business Meaning:** Subcontracting work order issued to external job workers for processing (Knitting, Dyeing, Printing, Washing, Embroidery, Stitching).
- **Attributes:**
  - `job_worker` (Link: `Supplier` / `Versa Job Worker` [Mandatory])
  - `process` (Select: `Knitting`, `Dyeing / Finishing`, `All-Over Printing`, `Chest Printing`, `Embroidery`, `Washing / Bio-Polishing`, `Stitching`, `Ironing / Packing`)
  - `source_doctype` (Select: `Sales Order`, `Production Batch`, `Material Request`)
  - `source_name` (Dynamic Link)
  - `planned_input_qty` (Float)
  - `planned_output_qty` (Float)
  - `allowed_process_loss_pct` (Float: Contractual loss allowance, e.g. 3.0% for knitting, 5.0% for dyeing)
  - `rate_per_unit` (Currency: Rate per Kg / Meter / Piece)
  - `billing_basis` (Select: `Per Input Weight`, `Per Output Weight`, `Per Piece`, `Per Meter`)
  - `issue_stock_entry` (Link: `Stock Entry` [Material Issue to Job Worker Warehouse])
  - `receipt_stock_entry` (Link: `Stock Entry` [Material Receipt from Job Worker])
  - `status` (Select: `Draft`, `Issued`, `In Progress`, `Partially Received`, `Completed`, `Cancelled`, `Closed`)

---

## 5. Domain Invariants & Business Rules

1. **Dual-UOM Conservation Invariant:** Fabric rolls must maintain both Weight ($kg$) and Length ($m$). The relationship is governed by:
   $$\text{Weight (kg)} = \frac{\text{Length (m)} \times \text{Cuttable Width (m)} \times \text{GSM}}{1000} \pm \text{Tolerance}$$
2. **Job Work Mass Balance Invariant:**
   $$\text{Issued Material Weight} = \text{Received Processed Weight} + \text{Process Loss Weight} + \text{Wastage / Scrap Weight} + \text{Returned Unprocessed Weight} + \text{Unaccounted Weight}$$
   *Rule: Unaccounted Weight must equal 0.00 within a contractual scale calibration tolerance ($\le 0.1\%$). Any non-zero unaccounted weight requires supervisor debit authorization.*
3. **Matrix-to-Line-Item Consistency Invariant:**
   $$\sum_{\text{Colour } c} \sum_{\text{Size } s} \text{OrderMatrix}(c, s).\text{ordered\_qty} \equiv \sum_{i \in \text{Sales Order Items}} \text{ItemRow}_i.\text{qty}$$
4. **Quality Gate Invariant:** No fabric roll or lot marked as `Quarantine` or `Rejected` can be selected in a `Stock Entry` for Production Cutting or Delivery without an explicit written Quality Override concession.
5. **Multi-Company Data Boundary:** All Versa transaction records must carry a non-null `company` link matching the ERPNext transaction's financial root.

