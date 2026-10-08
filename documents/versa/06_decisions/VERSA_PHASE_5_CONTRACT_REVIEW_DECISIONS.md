# VERSA PHASE 5 CONTRACT REVIEW DECISIONS (DECISION CANDIDATES)

**Document Path:** `documents/versa/06_decisions/VERSA_PHASE_5_CONTRACT_REVIEW_DECISIONS.md`  
**Decision Reference:** `DEC-013` (Candidate Decisions)  
**Governing Prompt:** [`P05_003_ADVERSARIAL_TEXTILE_CONTRACT_REVIEW.md`](file:///e:/VersaERP/documents/versa/09_prompt_history/PHASE_05/P05_003_ADVERSARIAL_TEXTILE_CONTRACT_REVIEW.md)  
**Target Contract:** [`CONTRACT-005` (Versa Textile Process Contract)](file:///e:/VersaERP/documents/versa/02_contracts/VERSA_TEXTILE_PROCESS_CONTRACT.md)  
**Date:** 2026-10-08  
**Status:** `PROPOSED / READY FOR ARCHITECTURAL APPROVAL`  

---

## 1. Context & Authority

During the adversarial review of `CONTRACT-005` under prompt `P05-003`, five specific semantic and boundary ambiguities were discovered. In accordance with the Versa change control rules, these defects are NOT silently edited into `CONTRACT-005`. Instead, they are formally formulated as Decision Candidates under `DEC-013`.

Upon approval of `DEC-013`, `CONTRACT-005` will be revised to incorporate these clarifications.

---

## 2. Decision Candidates

### Decision `DEC-013.1`: Financial Authority of Excess Loss Settlement
- **Finding ID:** `F-TEX-001`
- **Context:** `R-TEX-001` previously referenced "generating a debit note", risking accidental implementation of automated GL posting outside ERPNext.
- **Decision:** VersaERP shall compute and record **Debit Candidates / Settlement Obligations** within domain documents. VersaERP shall NOT autonomously create or submit `GL Entry` or `Debit Note` transactions. All financial postings remain strictly within ERPNext Accounts approval workflows.
- **Affected Artifacts:** `CONTRACT-005` (`R-TEX-001`), `VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md`.

---

### Decision `DEC-013.2`: Expected Loss Tolerance Precedence & Terminology
- **Finding ID:** `F-TEX-002`
- **Context:** Lack of explicit tolerance governance hierarchy and conflation between "Allowed Loss" and "Expected Loss".
- **Decision:**
  1. Terminology is formally frozen:
     - **Actual Loss ($L_{\text{actual}}$):** Total physical mass deficit $= M_{\text{in}} - (M_{\text{out}} + M_{\text{scrap}})$.
     - **Expected Loss Allowance ($L_{\text{expected}}$):** Planned allowance $= M_{\text{in}} \times \text{Tolerance}\%$.
     - **Allowed Loss ($L_{\text{allowed}}$):** $\min(L_{\text{actual}}, L_{\text{expected}})$.
     - **Excess Loss ($L_{\text{excess}}$):** $\max(0, L_{\text{actual}} - L_{\text{expected}})$.
  2. Tolerance resolution follows a strict 4-level precedence hierarchy:
     $$\text{Job Work Order Agreement} > \text{Vendor Master Agreement} > \text{Process Stage Master} > \text{Strict Zero Tolerance (0.0\%) Default}$$
  3. Tolerances are immutable once the Job Work Order is submitted.
- **Affected Artifacts:** `CONTRACT-005` (`R-TEX-001`), `VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md`.

---

### Decision `DEC-013.3`: Generalized $M:N$ Directed Acyclic Graph (DAG) Roll Lineage
- **Finding ID:** `F-TEX-003`
- **Context:** `R-TEX-003` previously stated a roll must link to "exactly one parent Batch", breaking multi-roll continuous dyeing pad operations and composite roll merges.
- **Decision:** Fabric roll lineage shall be modeled as a Directed Acyclic Graph (DAG) mediated by **Material Allocations** (Input Allocation & Output Allocation). A process stage may consume $M$ input rolls and produce $N$ output rolls while preserving 100% proportional mass and lot genealogy back to source yarn lots.
- **Affected Artifacts:** `CONTRACT-005` (`R-TEX-003`), `VERSA_TEXTILE_PROCESS_ARCHITECTURE.md`.

---

### Decision `DEC-013.4`: Stage-Specific Process Conservation Models
- **Finding ID:** `F-TEX-004`
- **Context:** Universal dry mass-balance fails for wet chemical processes (bleaching, dyeing, printing) and dimensional transformations (stentering, compacting).
- **Decision:** Every `Process Stage Type` shall be explicitly categorized under one of four normative Conservation Models:
  1. `DRY_MASS_CONSERVATION`: Strict mass balance (Knitting, Winding).
  2. `CHEMICAL_MASS_ADJUSTED`: Mass balance adjusted for chemical pickup or scouring loss (Bleaching, Dyeing, Printing).
  3. `DIMENSIONAL_TRANSFORMATION`: Dry mass conservation with expected length/width dimensional shifts and GSM changes (Stentering, Compacting).
  4. `DISCRETE_PIECE_MASS`: Piece count conservation + remnant mass balance (Garment Cutting).
- **Affected Artifacts:** `CONTRACT-005` (`R-TEX-001`), `VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md`.

---

### Decision `DEC-013.5`: Five-Tier Metrology Epistemic Hierarchy
- **Finding ID:** `F-TEX-005`
- **Context:** Ambiguity between supplier packing list claims and calibrated machine readings.
- **Decision:** Physical measurements in VersaERP shall adhere to a strict 5-tier lifecycle:
  $$\text{DECLARED} \longrightarrow \text{MEASURED} \longrightarrow \text{CALCULATED} \longrightarrow \text{VERIFIED} \longrightarrow \text{ACCEPTED}$$
  Raw `MEASURED` values are immutable. ERPNext Stock Ledger transactions record accepted quantities in base stock UOM (kg), while calculated length and GSM remain physical attributes within `Versa Fabric Roll`.
- **Affected Artifacts:** `CONTRACT-005` (`R-TEX-002`), `VERSA_TEXTILE_PROCESS_SEMANTIC_MODEL.md`.

---

## 3. Summary of Decision Impact

| Decision ID | Target Rule | Contract Impact | Implementation Impact |
| :--- | :--- | :--- | :--- |
| **`DEC-013.1`** | `R-TEX-001` | Replaces "automatic debit note" with "Debit Candidate". | Prevents unauthorized GL posting hooks in `versa_jobwork`. |
| **`DEC-013.2`** | `R-TEX-001` | Formalizes 4-tier tolerance precedence and math definitions. | Standardizes tolerance calculation utility in `versa_core`. |
| **`DEC-013.3`** | `R-TEX-003` | Replaces 1:N tree constraint with M:N DAG allocation. | Allows flexible child table roll allocation schemas. |
| **`DEC-013.4`** | `R-TEX-001` | Introduces 4 distinct Conservation Models for stages. | Enables stage-specific validation routines in `versa_textile`. |
| **`DEC-013.5`** | `R-TEX-002` | Establishes 5-tier metrology status hierarchy. | Standardizes inspection field states in `versa_quality`. |
