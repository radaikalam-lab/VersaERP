# VERSA PHASE 5 DECISION RESOLUTION & CONTRACT FREEZE

**Document Path:** `documents/versa/06_decisions/VERSA_PHASE_5_DECISION_RESOLUTION.md`  
**Governing Prompt:** [`P05_004_DECISION_RESOLUTION_AND_CONTRACT_FREEZE.md`](file:///e:/VersaERP/documents/versa/09_prompt_history/PHASE_05/P05_004_DECISION_RESOLUTION_AND_CONTRACT_FREEZE.md)  
**Decision Reference:** `DEC-013` (Formally Resolved)  
**Target Contract:** [`CONTRACT-005 v1.1` (Versa Textile Process Contract)](file:///e:/VersaERP/documents/versa/02_contracts/VERSA_TEXTILE_PROCESS_CONTRACT.md)  
**Date:** 2026-10-08  
**Status:** `APPROVED & AUTHORITATIVE`  

---

## 1. Executive Summary & Resolution Authority

This decision document formally resolves the five candidate decisions formulated in [`VERSA_PHASE_5_CONTRACT_REVIEW_DECISIONS.md`](file:///e:/VersaERP/documents/versa/06_decisions/VERSA_PHASE_5_CONTRACT_REVIEW_DECISIONS.md) following the adversarial contract review under prompt `P05-003`. 

Each candidate decision has been evaluated against business authority, mathematical consistency, regional manufacturing evidence, and ERPNext core boundaries. The resulting approved decisions authorize the formal amendment and freezing of `CONTRACT-005` as **`v1.1`**.

---

## 2. Formal Resolution of Candidate Decisions

### Decision `DEC-013.1`: Financial Authority of Excess Loss Settlement
- **Resolution:** **`ACCEPT`**
- **Authoritative Rule:**
  1. Versa Textile / Job Work subsystems determine physical mass deficits and compute a **Debit Candidate / Settlement Obligation**.
  2. VersaERP shall NEVER autonomously create or submit ERPNext `GL Entry` or `Debit Note` transactions.
  3. ERPNext Accounts retains 100% exclusive authority for reviewing, approving, creating, and submitting commercial Purchase Invoices, Credit/Debit Notes, and General Ledger postings.
  4. The Debit Candidate serves strictly as an auditable domain recommendation containing calculated excess loss mass ($L_{\text{excess}}$), agreed contract valuation rate, processor attribution, and source transaction references.
- **Authority:** ERPNext Accounts GL Authority Invariant, `VERSA_DATA_OWNERSHIP.md`.
- **Contract Impact:** Modifies `CONTRACT-005` Rule `R-TEX-001`.

---

### Decision `DEC-013.2`: Loss Tolerance Authority, Precedence & Effective Dating
- **Resolution:** **`ACCEPT WITH AMENDMENT`**
- **Amendment Details:** The previously proposed speculative fallback to stage masters is rejected as an automatic business allowance. In regional commercial practice, process loss allowances are strictly commercial terms negotiated between the buyer/manufacturer and the subcontracted processor.
- **Authoritative Rule:**
  1. **Authority Hierarchy:** Tolerance percentage is resolved exclusively from legally authorized commercial and operational agreements in the following strict order:
     $$\text{Job Work Order Agreement} \longrightarrow \text{Vendor Master Subcontracting Agreement} \longrightarrow \text{Strict Zero Tolerance (0.0\%) Default}$$
  2. **Technical Benchmarks vs Contractual Allowance:** Process Stage Masters and Quality Specs may declare *Technical Target Losses* for planning and BOM simulation, but they do NOT constitute automatic commercial loss allowances unless explicitly referenced in the Job Work Order.
  3. **Effective Dating & Immutability:** The applicable tolerance is captured and permanently frozen upon Job Work Order submission (`docstatus = 1`). Subsequent modifications to vendor masters or process templates cannot retroactively alter in-flight or historical processing settlements.
  4. **Missing Tolerance Fail-Safe:** If no authorized tolerance is configured, the system enforces **Zero Tolerance ($0.0\%$)**, requiring explicit managerial concession approval to waive excess loss.
- **Terminology Standard:**
  - **Actual Loss ($L_{\text{actual}}$):** Total physical mass loss $= M_{\text{in}} - (M_{\text{out\_usable}} + M_{\text{recoverable\_scrap}})$.
  - **Expected Loss Allowance ($L_{\text{expected}}$):** Contractually agreed upper bound $= M_{\text{in}} \times \text{Tolerance}\%$.
  - **Allowed Loss ($L_{\text{allowed}}$):** $\min(L_{\text{actual}}, L_{\text{expected}})$.
  - **Excess Loss ($L_{\text{excess}}$):** $\max(0, L_{\text{actual}} - L_{\text{expected}})$.
- **Contract Impact:** Modifies `CONTRACT-005` Rule `R-TEX-001`.

---

### Decision `DEC-013.3`: Material Transformation Lineage & Cardinality
- **Resolution:** **`ACCEPT WITH AMENDMENT`**
- **Amendment Details:** Replaces rigid database cardinality assumptions ($1:N$ vs $M:N$) with the domain abstraction of **Material Transformation Lineage**.
- **Authoritative Rule:**
  1. A `Material Transformation Event` represents an operational processing stage (e.g. knitting, continuous rope dyeing, stenter finishing, compacting, cutting).
  2. A transformation event consumes 1..M `Input Material Allocations` (e.g. yarn lots, fabric rolls) and generates 1..N `Output Material Allocations` (e.g. finished rolls, cut garment panels) plus recoverable scrap remnants.
  3. Supports all operational topology variants:
     - **$1 \to 1$:** Single roll finishing / re-inspection.
     - **$1 \to N$:** Roll split (e.g. dividing a 50 kg roll into two 25 kg rolls or cutting out defective sections).
     - **$N \to 1$:** Roll merge / continuous pad dyeing where multiple greige rolls are stitched together.
     - **$N \to N$:** Multi-roll batch processing across stenter / compacting lines.
     - **$1 \to \text{Pieces} + \text{Scrap}$:** Cutting lay panel creation with remnants.
  4. Invariant: Every output allocation maintains an immutable, proportionally traceable lineage back to its parent input allocations, preserving end-to-end auditability from yarn lot to finished garment bundle.
- **Contract Impact:** Modifies `CONTRACT-005` Rule `R-TEX-003`.

---

### Decision `DEC-013.4`: Stage-Specific Process Conservation Taxonomy
- **Resolution:** **`ACCEPT`**
- **Authoritative Rule:** Every textile transformation stage type must declare its governing **Conservation Model** from the normative 4-tier taxonomy:
  1. **`MASS_CONSERVATION_DRY`:**
     - *Conserved Property:* Total dry fiber mass.
     - *Formula:* $M_{\text{in}} = M_{\text{out\_usable}} + M_{\text{scrap}} + L_{\text{actual}}$.
     - *Applicable Processes:* Yarn Winding, Circular Knitting, Flat Knitting, Greige Inspection.
  2. **`MASS_CONSERVATION_ADJUSTED`:**
     - *Conserved Property:* Mass adjusted for chemical pickup or natural loss.
     - *Formula:* $M_{\text{in}} \times (1 + \Delta_{\text{chem}}\%) = M_{\text{out\_usable}} + M_{\text{scrap}} + L_{\text{actual}}$, where $\Delta_{\text{chem}}$ represents chemical pickup (+1% to +3% in dyeing/printing) or scouring weight loss (-3% to -5% in bleaching).
     - *Applicable Processes:* Scouring, Bleaching, Exhaust Dyeing, Continuous Dyeing, Screen/Rotary Printing.
  3. **`DIMENSIONAL_TRANSFORMATION`:**
     - *Conserved Property:* Dry mass conserved; linear length and cuttable width transform under tension/overfeed with dynamic GSM shift.
     - *Formula:* $M_{\text{in}} = M_{\text{out}} + L_{\text{actual}}$; $\text{Length}_{\text{out}}$ and $\text{GSM}_{\text{out}}$ validated against physical formula $\text{Length} = (M \times 10^6) / (\text{GSM} \times W)$.
     - *Applicable Processes:* Stentering, Heat Setting, Sanforizing, Compacting, Relaxation Drying.
  4. **`PIECE_COUNT_MASS_CONSERVATION`:**
     - *Conserved Property:* Discrete garment panel count + remnant trim mass.
     - *Formula:* $M_{\text{in\_rolls}} = \sum M_{\text{cut\_panels}} + M_{\text{end\_bits}} + M_{\text{chindi\_scrap}} + L_{\text{dust\_loss}}$.
     - *Applicable Processes:* Spreading, Marker Cutting, Band-knife Cutting.
- **Contract Impact:** Modifies `CONTRACT-005` Rule `R-TEX-001`.

---

### Decision `DEC-013.5`: Multi-Dimensional Metrology Epistemics
- **Resolution:** **`ACCEPT WITH AMENDMENT`**
- **Amendment Details:** Replaces the linear 5-step lifecycle with a **3-Dimensional Metrology Model** that decouples Value Origin, Verification State, and Inventory Disposition.
- **Authoritative Rule:** Every physical property reading (Weight, Length, Width, GSM, Moisture, Defect Score) is modeled across three orthogonal dimensions:
  1. **Dimension 1: Value Origin (Provenance):**
     - `DECLARED`: Value stated on vendor packing list or delivery challan.
     - `MEASURED`: Raw value read from a calibrated physical instrument (scale, fabric inspection machine, GSM cutter).
     - `CALCULATED`: Value derived mathematically via physical formula (e.g. GLM, calculated length).
  2. **Dimension 2: Verification State:**
     - `UNVERIFIED`: Initial unconfirmed entry.
     - `VERIFIED`: Confirmed by qualified Quality Inspector to be within instrument tolerance.
  3. **Dimension 3: Inventory / Commercial Disposition:**
     - `PENDING`: Awaiting QC evaluation.
     - `ACCEPTED`: Approved for stock ingestion.
     - `CONCESSION`: Approved with deviation sign-off.
     - `REJECTED`: Blocked / quarantined from inventory ingestion.
- **Immutability & Authority Invariant:** Raw `MEASURED` values are immutable historical audit records. ERPNext Stock Ledger transactions record accepted quantities in base stock UOM (kg), while calculated length and measured GSM remain physical piece-goods attributes within the Versa Quality/Textile overlay.
- **Contract Impact:** Modifies `CONTRACT-005` Rule `R-TEX-002`.

---

## 3. Cross-Decision Consistency Matrix

| Dimension | Governing Rules | Inter-Decision Coherence Verification |
| :--- | :--- | :--- |
| **Loss & Settlement** | `DEC-013.1`, `DEC-013.2` | Loss terminology is rigorous; Debit Candidates are generated without violating ERPNext GL authority. |
| **Physical Measurement** | `DEC-013.4`, `DEC-013.5` | Dimensional transformations in stenters reconcile dynamically with 3D metrology readings without static UOM conversion errors. |
| **Material Lineage** | `DEC-013.3`, `DEC-013.4` | Transformation events support $M:N$ roll allocations under specific stage conservation models without orphaned scrap. |
| **Quality & Governance** | `DEC-013.1`, `DEC-013.5` | Disposition states (`Accepted`, `Concession`, `Rejected`) seamlessly drive fail-closed issue gates. |

---

## 4. Contract Freeze Authorization

With decisions `DEC-013.1` through `DEC-013.5` formally approved, `CONTRACT-005` is authorized for amendment to **`v1.1`** and declared **`FROZEN FOR IMPLEMENTATION SPECIFICATION`**.
