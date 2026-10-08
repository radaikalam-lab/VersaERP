# VERSA ERP PROMPT PROVENANCE & SEMANTIC TRACEABILITY SYSTEM

**Root Directory:** `documents/versa/09_prompt_history/`  
**System Status:** Active & Governed  
**Governing Standard:** Semantic Traceability & Engineering Lineage  

---

## 1. Objective & Architectural Boundary

VersaERP is engineered using a **semantic-first, contract-driven architecture**. To maintain total long-term audibility and epistemic integrity, every material requirement, architecture decision, domain contract, implementation module, and test suite must possess verifiable provenance back to its originating engineering request, analytical rationale, or empirical evidence.

### Core Authority Invariant
> **Prompts are provenance records describing how engineering work was requested, scoped, or reasoned about. Prompts do not possess production authority.**

Runtime execution, data models, business rules, and invariant validations are governed exclusively by:
```text
       Prompt (Originating Engineering Intent / Provenance)
                            │
                            ▼
       Evidence / Analysis (Archaeology, Standards, Domain Research)
                            │
                            ▼
       Approved Decision (06_decisions/ - Authoritative Architecture Decisions)
                            │
                            ▼
       Authoritative Contract (02_contracts/ - Normative Domain Contracts)
                            │
                            ▼
       Implementation (bench/apps/ - Non-invasive, fail-closed runtime code)
                            │
                            ▼
       Tests & Validation (Automated regression & verification gates)
                            │
                            ▼
       Phase Closure (Formal gate sign-off)
```

**If a prompt and an approved contract disagree, the approved contract is authoritative.**

---

## 2. Directory Topology

```text
documents/versa/09_prompt_history/
│
├── README.md                                     # System specification, principles & reusable template
│
├── 00_index/
│   ├── VERSA_PROMPT_REGISTER.md                 # Complete catalog of all material prompts
│   └── VERSA_SEMANTIC_TRACEABILITY_INDEX.md     # Bidirectional Prompt ↔ Decision ↔ Contract ↔ Code index
│
├── PHASE_00/                                     # Initial domain & architecture establishment
├── PHASE_01/                                     # Canonical domain model & semantic extraction
├── PHASE_02/                                     # Frappe implementation specification & architecture challenge
├── PHASE_03/                                     # Design-time workspace & versa_core implementation/hardening
├── PHASE_03_5/                                   # Real Frappe/ERPNext runtime bootstrap
├── PHASE_03_6/                                   # Canonical Docker runtime & deployment hardening
├── PHASE_04/                                     # Textile archaeology, semantic reconciliation & Quality closure
└── PHASE_05/                                     # Reserved location for upcoming Phase 5 sequencing
```

---

## 3. Provenance Classification Scheme

Every prompt artifact is assigned exactly one strict classification:

1. **`ORIGINAL`**: The exact original prompt text is captured directly from recorded execution transcripts.
2. **`RECONSTRUCTED`**: The prompt record has been reconstructed from authoritative artifact history, reports, and committed diffs; exact phrasing is preserved where known, but marked reconstructed.
3. **`REFERENCED`**: The prompt is known to exist and is cited by existing project artifacts, but full text is archived externally.
4. **`DERIVED`**: The record summarizes an inferred operational transition from project artifacts and must not be represented as an explicit prompt.

*Rule:* Never label reconstructed or derived prompts as `ORIGINAL`.

---

## 4. Prompt Identifier Standard

Every material prompt uses a stable, sequential identifier:

$$\text{P}\langle\text{PHASE}\rangle\text{-}\langle\text{SEQUENCE}\rangle$$

Examples:
- `P00-001` (Phase 0 Platform Strategy)
- `P01-001` (Phase 1 Canonical Model)
- `P02-001` (Phase 2 Frappe Spec)
- `P03-001` (Phase 3 Core Bootstrap)
- `P03.5-001` (Phase 3.5 Runtime Bootstrap)
- `P03.6-001` (Phase 3.6 Docker Canonical Runtime)
- `P04-001` (Phase 4 Textile Repository Archaeology)
- `P04-002` (Phase 4 Semantic Reconciliation)
- `P04-003` (Phase 4 Quality Implementation Review)
- `P04-004` (Phase 4 Quality Integration Validation)
- `P04-005` (Phase 4 Final Quality Closure)
- `P05-001` (Phase 5 Sequencing Entrypoint)

---

## 5. Reusable Prompt Artifact Template

```markdown
# Prompt ID: P<PHASE>-<SEQUENCE>

## Metadata
- **Phase:** Phase <X>
- **Date:** YYYY-MM-DD
- **Title:** <Descriptive Title>
- **Status:** COMPLETED | SUPERSEDED | ACTIVE
- **Provenance Classification:** ORIGINAL | RECONSTRUCTED | REFERENCED | DERIVED

---

## 1. Lineage & Relationships
- **Parent Prompt:** `P<PREV>-<SEQ>` (or Root)
- **Supersedes:** `None` (or Prompt ID)
- **Related Prompt(s):** `P<PHASE>-<SEQ>`

---

## 2. Intent & Scoping
- **Purpose:** <High-level intent of the prompt>
- **Semantic Authority:** <Governing decision or contract>
- **Decision Authority:** <DEC-XXX>
- **Input Artifacts:**
  - `documents/versa/...`
- **Evidence Sources:**
  - `documents/versa/...`

---

## 3. Constraints & Invariants
- <Explicit constraints: e.g. read-only, no runtime modification, fail-closed>

---

## 4. Requested Actions
1. <Step 1>
2. <Step 2>

---

## 5. Expected & Resulting Outputs
- **Expected Outputs:** <List of deliverables requested>
- **Resulting Decisions:** `documents/versa/06_decisions/DEC-XXX.md`
- **Resulting Contracts:** `documents/versa/02_contracts/...`
- **Resulting Implementation:** `bench/apps/...`
- **Resulting Tests:** `bench/apps/.../tests/...`
- **Resulting Validation Artifacts:** `documents/versa/05_validation/...`

---

## 6. Change Impact Classification
- **Classification:** `IMPLEMENTATION_ONLY` | `SEMANTIC_CHANGE` | `CONTRACT_CHANGE` | `ARCHITECTURAL_CHANGE`
- **Rationale:** <Explanation of impact>
```
