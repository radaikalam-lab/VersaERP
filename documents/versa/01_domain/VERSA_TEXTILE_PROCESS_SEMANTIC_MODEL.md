# VERSA TEXTILE PROCESS SEMANTIC MODEL

**Authoritative File Path:** `documents/versa/01_domain/VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md`  
**Phase:** Phase 5 — Textile Processing & Fabric Processing  
**Status:** `FROZEN FOR CONTRACT REVIEW`  
**Governing Context:** Regional Textile Cluster Operations (Tiruppur, Erode, Salem)  

---

## 1. Domain Objective & Scope

The **Versa Textile Process Semantic Model** provides the formal conceptual definitions, entities, relationships, state machines, and mass-balance conservation rules for textile transformation operations (Yarn Spinning $\to$ Knitting/Weaving $\to$ Wet Processing/Dyeing $\to$ Compacting/Finishing $\to$ Printing).

```text
  [ Yarn Lot / Bag ]
         │
         ▼ (Knitting / Weaving Stage)
  [ Greige Fabric Batch / Rolls ]
         │
         ▼ (Wet Processing / Dyeing Stage)
  [ Dyed Wet Fabric Batch ]
         │
         ▼ (Compacting / Stentering / Finishing Stage)
  [ Finished Fabric Rolls ] ──► [ Quality Gate (Versa QC Result) ]
                                          │
                                          ▼
                               [ Cutting / Garment Assembly ]
```

---

## 2. Answers to the 22 Core Semantic Questions

### 1. What is a Textile Process?
A **Textile Process** is an ordered sequence of physical, chemical, or mechanical transformations applied to raw or semi-finished textile materials (fiber, yarn, fabric) to alter their structural, dimensional, or aesthetic properties (e.g., Greige Knitting, Yarn Dyeing, Fabric Dyeing, Rotary Printing, Mercerizing, Compacting).

### 2. What is a Process Stage?
A **Process Stage** is an atomic operational unit within a textile process having defined inputs, specific machine/vendor routing, operational control parameters (temperature, speed, tension), allowed process loss tolerances, and a mandatory quality completion boundary.

### 3. What is a Process Batch?
A **Process Batch** (`Batch`) is a discrete commercial and operational tracking lot of homogeneous material processed together under identical recipe, machine, and environmental conditions (e.g., Dyeing Lot `DYE-2026-0841` of 500 kg single jersey fabric).

### 4. What is a Fabric Roll?
A **Fabric Roll** (`Versa Fabric Roll`, ENT-017) is a continuous, indivisible physical length of fabric wound on a core, possessing unique physical attributes (gross weight, tare weight, net weight, measured GSM, cuttable width, calculated length, quality grade, roll barcode).

### 5. What is the relationship between Batch and Roll?
- A **Process Batch** is a collection of one or more **Fabric Rolls** ($1 : N$).
- Every Fabric Roll must belong to exactly one parent Batch during a processing stage.
- Rolls within a Batch share chemical history (dye lot, shade) but maintain individual physical measurements (roll weight, continuous length, defect points).

### 6. What constitutes process input?
**Process Input** is the exact physical mass and length of material issued into a stage (e.g., $520.0\text{ kg}$ of 34s Combed Cotton Greige Fabric across 20 rolls) plus auxiliary process inputs (dyes, chemicals, water).

### 7. What constitutes process output?
**Process Output** is the net usable finished material resulting from the transformation stage (e.g., $498.5\text{ kg}$ of Navy Blue Finished Fabric across 20 finished rolls) plus recoverable byproduct (e.g., fabric end-bits/chindi).

### 8. What constitutes process loss?
**Process Loss** is the physical mass deficit between total material input and total material output:
$$\text{Total Loss (kg)} = \text{Input Mass (kg)} - \text{Output Usable Mass (kg)} - \text{Recoverable Scrap (kg)}$$
$$\text{Actual Loss \%} = \left(\frac{\text{Total Loss}}{\text{Input Mass}}\right) \times 100$$

### 9. What constitutes expected loss?
**Expected Loss** (or *Allowed Process Loss*) is the contractual and technological tolerance agreed upon for a specific stage/subcontractor (e.g., $\text{Allowed Loss} = 4.0\%$ for reactive fabric dyeing).

### 10. What constitutes excess loss?
**Excess Loss** is any physical deficit beyond the contractual allowed tolerance:
$$\text{Excess Loss (kg)} = \max\left(0, \text{Total Loss (kg)} - \left(\text{Input Mass} \times \frac{\text{Allowed Loss \%}}{100}\right)\right)$$
- Under invariant `job_work_mass_balance`, excess loss represents commercial liability and automatically triggers a financial debit against the processor.

### 11. Who owns physical measurement?
**Versa Quality & Textile Subsystems** own the capture, derivation, and validation of physical characteristics:
- Measured GSM ($g/m^2$)
- Cuttable Width (inches/mm)
- Gross, Tare, and Net Roll Weights (kg)
- 4-Point Defect Score (points/100 sq yds)
- Calculated Linear Length ($\text{Meters} = \frac{\text{Net Weight (kg)} \times 1,000,000}{\text{GSM} \times \text{Width (mm)}}$)

### 12. Who owns inventory valuation?
**ERPNext Inventory / Stock Subsystem** exclusively owns inventory valuation based on standard moving average or FIFO cost recorded in `tabStock Ledger Entry`.

### 13. Who owns accounting?
**ERPNext Accounts Subsystem** exclusively owns general ledger accounting, invoicing, tax calculation, and financial settlements recorded in `tabGL Entry`.

### 14. What constitutes a completed process stage?
A process stage is **Completed** when:
1. All output rolls/batches are physically weighed and recorded.
2. Actual loss and yield are computed against mass-balance tolerances.
3. A `Versa QC Result` is recorded with disposition `Accepted` or `Accepted with Concession`.
4. ERPNext `Stock Entry (Manufacture / Subcontract Receipt)` is successfully submitted.

### 15. What constitutes a failed process stage?
A process stage is **Failed** when:
- Output material suffers irrecoverable defect (e.g., severe shade patchiness, fabric tenderizing/tearing, extreme GSM deviation).
- `Versa QC Result` disposition is `Rejected`.
- Material is placed in `Quarantine` warehouse; downstream processing is blocked.

### 16. What triggers a Quality Gate?
A **Quality Gate** is triggered automatically on:
- Inward receipt of greige fabric from knitting/weaving mill (`Purchase Receipt`).
- Receipt of processed fabric from dyeing/finishing house (`Purchase Receipt` / `Versa Job Work Order`).
- Material issue of fabric rolls to cutting department (`Stock Entry - Material Issue`).

### 17. How does Quality disposition affect downstream processing?
- **`Accepted`:** Material released to active stock; cutting/downstream stage permitted.
- **`Accepted with Concession`:** Material released under dual QA Head + Buyer commercial sign-off.
- **`Quarantine` / `Rejected`:** Material locked; issuing into cutting or next processing stage raises `ValidationError`.

### 18. How does processing integrate with Job Work?
Textile process stages map directly to **`Versa Job Work Order`** routes:
- Stage 1 (Knitting): Yarn issued $\to$ Greige fabric received.
- Stage 2 (Dyeing): Greige fabric issued $\to$ Dyed fabric received.
- Stage 3 (Finishing/Compacting): Dyed fabric issued $\to$ Finished fabric received.
- Lineage is preserved across stages via parent batch and roll barcode tracking.

### 19. How does processing integrate with Order Matrix?
Fabric processing runs at the **Style / Colour / Shade** level:
- Knitting produces greige fabric allocated to parent `Versa Style`.
- Dyeing processes fabric batches to match specific `Colour` and `Shade` requirements in the `Versa Order Matrix`.
- Finished fabric rolls are allocated to production cutting orders satisfying the total Matrix quantity.

### 20. How does processing preserve roll traceability?
- Every roll receives a unique Barcode (`roll_barcode`).
- Roll genealogy tracks: `Yarn Lot` $\to$ `Greige Roll Barcode` $\to$ `Dye Batch ID` $\to$ `Finished Roll Barcode` $\to$ `Cutting Lay Plan`.
- Splits (dividing a roll) and Merges (piecing together rolls) create linked child rolls with preserved batch provenance.

### 21. What is intentionally NOT modeled in Phase 5?
- Machine PLC / SCADA real-time telemetry (deferred to Phase 8).
- AI color matching / spectrophotometer automated recipe optimization (deferred).
- Chemical thermodynamic dye bath simulation (deferred).
- Plant energy and water consumption telemetry (deferred to Phase 8).

### 22. Which semantics are still unresolved?
- Commercial handling of sub-grade end-bits (Chindi / Fents) salvage valuation (Open Question).
- Automated yarn count variation compensation in fabric weight calculations (Open Question).

---

## 3. Epistemic Classification of Textile Concepts

| Concept | Classification | Definition & Scope |
| :--- | :--- | :--- |
| **`Fabric Roll`** | `VERSA_SEMANTIC` | Physical traceability entity; auxiliary layer over ERPNext stock. |
| **`Process Loss Mass Balance`** | `VERSA_SEMANTIC` | Invariant enforcing $\text{Input} = \text{Output} + \text{Allowed Loss} + \text{Excess Loss}$. |
| **`Physical GLM Conversion`** | `VERSA_SEMANTIC` | Formula $\text{GLM} = \frac{\text{GSM} \times \text{Width}}{1000}$ as specimen attribute. |
| **`Linear Static kg/m Ratio`** | `VERSA_CONFLICT` | Rejected in favor of dynamic physical calculation. |
| **`Chemical Recipe Formulation`** | `DEFERRED` | % OWF and g/L formulations deferred to Phase 6. |
| **`IoT Sensor Telemetry`** | `DEFERRED` | Real-time machine monitoring deferred to Phase 8. |
| **`CAD Weave Pattern Design`** | `NOT_RELEVANT` | Loom binary generation belongs in external CAD software. |
