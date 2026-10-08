# VERSA PHASE 5 OPEN QUESTIONS & RESEARCH REGISTER

**Authoritative File Path:** `documents/versa/07_open_questions/VERSA_PHASE_5_OPEN_QUESTIONS.md`  
**Phase:** Phase 5 — Textile Processing & Fabric Processing  
**Status:** ACTIVE REGISTER  
**Governing Standard:** Open Question & Assumption Governance  

---

## 1. Active Open Questions for Phase 5 & Subsequent Phases

### `OQ-011`: Sub-Grade End-Bits (Chindi / Fents) Scrap Valuation
- **Question:** How should recoverable sub-grade fabric remnants (Chindi / cut pieces / end-bits) generated during compacting and cutting be valued in ERPNext inventory?
- **Impacted Subsystems:** `versa_textile`, ERPNext Stock & Valuation.
- **Candidate Approaches:**
  1. *Option A (Zero Value Byproduct):* Inwarded as zero-cost scrap inventory; revenue recognized upon salvage sale.
  2. *Option B (Standard Salvage Rate):* Assigned fixed predetermined salvage cost per kg, reducing the inventory value of prime fabric rolls proportionally.
- **Status:** Under Commercial Review for Phase 6.

---

### `OQ-012`: Automated Yarn Count Variation Compensation
- **Question:** In knitting operations, nominal yarn count (e.g. 34s Ne) typically varies by $\pm 1.5\%$. Should Versa automatically compensate theoretical fabric yield calculations based on the actual measured yarn count from `Versa QC Result`?
- **Impacted Subsystems:** `versa_textile`, `versa_quality`.
- **Candidate Approaches:**
  1. *Option A (Actual Count Dynamic Adjustment):* Recompute expected roll length using actual tested Ne from yarn inward QC.
  2. *Option B (Nominal Spec Baseline):* Maintain nominal specification length; attribute deviation to actual knitting process variance.
- **Status:** Open for Engineering Evaluation.

---

### `OQ-013`: Multi-Color Yarn-Dyed Fabric Batching
- **Question:** How should multi-color yarn-dyed fabrics (e.g. engineered feeder stripe polo shirt fabrics) track yarn lot lineage across multiple colored yarn inputs within a single knitting process batch?
- **Impacted Subsystems:** `versa_textile`, `Versa Fabric Roll`.
- **Candidate Approaches:**
  1. *Multi-Input Batch Mapping:* Allow a `Versa Fabric Roll` to link to multiple parent Yarn Lots via child table allocation.
  2. *Composite Batch Routing:* Group colored yarn lots under a composite preparation batch before knitting.
- **Status:** Scheduled for Phase 6 Formulation Architecture.

---

### `OQ-014`: Fabric Relaxation Protocol Gating
- **Question:** Knitted elastane/spandex and single jersey fabrics require a mandatory 24–48 hour relaxation period on the cutting table to release knitting/compacting tensions before cutting. Should Versa enforce a timestamped relaxation gate before allowing roll issuance to a cutting lay?
- **Impacted Subsystems:** `versa_textile`, `versa_quality.gates`.
- **Status:** Candidate for Phase 7 Garment Manufacturing.
