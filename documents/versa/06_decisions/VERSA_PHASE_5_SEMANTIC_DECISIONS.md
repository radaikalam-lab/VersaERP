# VERSA ARCHITECTURE DECISION: PHASE 5 TEXTILE PROCESS SEMANTICS

**Document Identifier:** `DEC-012`  
**Authoritative File Path:** `documents/versa/06_decisions/VERSA_PHASE_5_SEMANTIC_DECISIONS.md`  
**Phase:** Phase 5 — Textile Processing & Fabric Processing  
**Status:** `APPROVED`  
**Date:** 2026-10-08  
**Governing Contract:** [`VERSA_TEXTILE_PROCESS_CONTRACT.md`](file:///e:/VersaERP/documents/versa/02_contracts/VERSA_TEXTILE_PROCESS_CONTRACT.md)

---

## 1. Context & Problem Statement

Textile manufacturing in regional clusters (Tiruppur, Erode, Salem) involves multi-stage physical and chemical transformations with process loss, variable fabric shrinkage, dynamic linear density, and external subcontractor chaining. Previous analyses revealed that standard ERPNext Item Variants and static UOM conversion factors fail to accurately capture fabric mass balance and physical roll attributes.

---

## 2. Formal Architecture Decisions

### Decision 1: Scope Boundary of Phase 5
- **Decision:** Phase 5 is strictly scoped to **Textile Process Stages, Fabric Roll Traceability, Mass-Balance Loss Governance, and Physical Measurement Formulations**.
- **Exclusions:** Chemical recipe optimization (% OWF, g/L formulation BOMs) is formally deferred to Phase 6. Real-time machine SCADA/IoT telemetry is formally deferred to Phase 8.

### Decision 2: Mass-Balance Conservation Invariant
- **Decision:** All textile process stages must enforce the strict mass-balance identity:
  $$\text{Input Mass} \equiv \text{Output Usable Mass} + \text{Recoverable Scrap Mass} + \text{Allowed Loss} + \text{Excess Loss}$$
  Excess loss beyond the contractual threshold automatically generates a financial debit liability against the processor on invoice settlement.

### Decision 3: Physical GLM Formulation over Static UOM Conversions
- **Decision:** Fabric weight-to-length conversions are treated as **specimen-specific physical measurements** calculated dynamically via:
  $$\text{GLM} = \frac{\text{GSM} \times \text{Width (mm)}}{1000}$$
  Static linear UOM conversion factors in ERPNext Item masters are prohibited for knitted fabric goods.

### Decision 4: Fabric Roll as Physical Traceability Overlay
- **Decision:** `Versa Fabric Roll` (ENT-017) serves as a physical piece-goods tracking overlay. ERPNext's native `tabStock Ledger Entry` remains the sole inventory and valuation authority. Versa will not maintain duplicate stock balances.

### Decision 5: Non-Invasive Subsystem Packaging
- **Decision:** Textile processing capabilities shall be packaged inside a modular Frappe application (`versa_textile`), integrating non-invasively via standard Frappe document events and permission query conditions without modifying ERPNext core.

---

## 3. Epistemic Impact & Change Control

- **Canonical Invariants:** Reaffirmed Invariants #2 (`job_work_mass_balance`) and #6 (`multi_company_isolation`).
- **Domain Contracts:** Authorized `CONTRACT-005` (`VERSA_TEXTILE_PROCESS_CONTRACT.md`).
- **Phase 4 Baseline:** Preserved Phase 4 closure without modifications.
