# VERSA PHASE 5 CONTRACT REVIEW OPEN QUESTIONS REGISTER

**Document Path:** `documents/versa/07_open_questions/VERSA_PHASE_5_CONTRACT_REVIEW_OPEN_QUESTIONS.md`  
**Governing Prompt:** [`P05_003_ADVERSARIAL_TEXTILE_CONTRACT_REVIEW.md`](file:///e:/VersaERP/documents/versa/09_prompt_history/PHASE_05/P05_003_ADVERSARIAL_TEXTILE_CONTRACT_REVIEW.md)  
**Parent Register:** [`VERSA_PHASE_5_OPEN_QUESTIONS.md`](file:///e:/VersaERP/documents/versa/07_open_questions/VERSA_PHASE_5_OPEN_QUESTIONS.md)  
**Date:** 2026-10-08  
**Status:** `ACTIVE REVIEW REGISTER`  

---

## 1. Adversarial Review Open Questions (`OQ-015` to `OQ-018`)

### `OQ-015`: Non-Linear Branched Process Routing Semantics
- **Context:** Rule `R-TEX-005` establishes sequential integrity ($\text{Stage } N \to \text{Stage } N+1$). In certain operations, a single greige batch is split into multiple parallel branches (e.g. 50% dyed to Navy Blue, 50% dyed to Olive Green) or routed through rework (e.g. re-stentering after skewness test failure).
- **Question:** How should branched and looping job work routes be represented without breaking the linear parent Job Work Order structure?
- **Impacted Subsystems:** `versa_jobwork`, `versa_textile`.
- **Candidate Solutions:**
  1. *Sub-Route Forking:* Parent Job Work Order generates linked child routes with allocated input proportions.
  2. *Independent Job Work Orders with Lineage Link:* Issue child batches on separate Job Work Orders with `parent_job_work_order` and source roll traceability.
- **Status:** Open for Phase 6 Job Work Subsystem Design.

---

### `OQ-016`: Standard Regain & Moisture Equilibrium Compensation
- **Context:** Cotton has a standard commercial moisture regain of 8.5%. In humid coastal areas or post-hydroextraction, fabric roll weight can vary by 2–4% based solely on moisture content without loss of physical fiber mass.
- **Question:** Should Versa require conditioned/dry-basis mass normalization during QC inspection to prevent false excess loss debits?
- **Impacted Subsystems:** `versa_quality`, `versa_textile`.
- **Candidate Solutions:**
  1. *Conditioned Mass Normalization:* Record moisture percentage during QC and compute standard conditioned weight:
     $$\text{Conditioned Weight} = \text{Measured Weight} \times \frac{100 + \text{Commercial Regain \%}}{100 + \text{Measured Moisture \%}}$$
  2. *Tiruppur Commercial Allowance Range:* Rely on broad contractual loss tolerance bands without instrumented moisture testing.
- **Status:** Open for Regional Metrology Review.

---

### `OQ-017`: Cut Order Plan & Fabric Grouping by Shade Lot (Dyeing Lots)
- **Context:** In garment manufacturing, fabric rolls from different dyeing lots (even of the same color) have slight delta-E shade variations. Spreading rolls from different dye lots in the same garment cutting marker causes shade variation across garment panels.
- **Question:** How should the fabric allocation engine enforce that only rolls from identical shade lots / dye batches are grouped together in a single cutting lay?
- **Impacted Subsystems:** `versa_textile`, `versa_order_matrix`, `versa_quality`.
- **Candidate Solutions:**
  1. *Shade Band Locking:* Mandatory `shade_band` attribute on `Versa Fabric Roll`; cutting plan enforces single shade band per lay.
  2. *Marker Advisory Warning:* Non-blocking warning when mixing dye batches in a marker.
- **Status:** Scheduled for Phase 7 Cutting Room Specification.

---

### `OQ-018`: Residual Roll Return vs Auto-Scrap Threshold
- **Context:** When a 25 kg roll is issued to a spreading table and 23.8 kg is consumed, a 1.2 kg remnant roll remains. If the remnant is too small for further garments, it must be scrapped.
- **Question:** What is the threshold and workflow for deciding whether an end-of-lay remnant is re-inventoried as a usable short roll or auto-scrapped to Chindi?
- **Impacted Subsystems:** `versa_textile`, ERPNext Stock.
- **Candidate Solutions:**
  1. *Threshold-Based Auto-Disposition:* Remnants $> 5.0\text{ m}$ return to fabric store; remnants $\le 5.0\text{ m}$ auto-transferred to scrap warehouse.
  2. *Operator Manual Selection:* Operator explicitly selects `Return to Store` or `Scrap to Chindi` at cutting entry completion.
- **Status:** Open for Phase 7 Garment Manufacturing Design.
