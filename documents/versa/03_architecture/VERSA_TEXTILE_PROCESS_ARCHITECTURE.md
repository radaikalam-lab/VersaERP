# VERSA TEXTILE PROCESS ARCHITECTURE

**Authoritative File Path:** `documents/versa/03_architecture/VERSA_TEXTILE_PROCESS_ARCHITECTURE.md`  
**Phase:** Phase 5 — Textile Processing Architecture  
**Status:** `FROZEN FOR IMPLEMENTATION REVIEW`  
**Governing Contract:** [`VERSA_TEXTILE_PROCESS_CONTRACT.md`](file:///e:/VersaERP/documents/versa/02_contracts/VERSA_TEXTILE_PROCESS_CONTRACT.md)

---

## 1. Subsystem Architecture Topology

The Textile Processing Subsystem (`versa_textile`) operates as a modular, non-invasive Frappe application providing textile domain entities, fabric roll tracking, mass-balance calculations, and multi-stage process overlays on top of the canonical Docker runtime.

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    VERSA ERP APPS                                       │
│                                                                                         │
│   ┌────────────────────┐     ┌─────────────────────┐     ┌──────────────────────────┐   │
│   │    versa_core      │     │    versa_quality    │     │      versa_textile       │   │
│   │  (Company Isolate, │◄────┤   (QC Spec, Result, ├────►│  (Fabric Roll, Process  │   │
│   │   Approval Engine) │     │    4-Point Scoring) │     │   Mass-Balance Overlay)  │   │
│   └─────────┬──────────┘     └──────────┬──────────┘     └────────────┬─────────────┘   │
└─────────────┼───────────────────────────┼─────────────────────────────┼─────────────────┘
              │                           │                             │
              ▼ (Non-Invasive Hooks)      ▼ (Quality Gating Hooks)      ▼ (Doc Events)
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                FRAPPE & ERPNEXT v15 CORE                                │
│                                                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       ERPNext Stock & Manufacturing Engines                     │   │
│   │  - Stock Entry (Material Issue / Transfer / Manufacture)                        │   │
│   │  - Purchase Receipt (Subcontracted Goods Inward)                                │   │
│   │  - Work Order & Job Card (Operational Routing)                                  │   │
│   └────────────────────────────────────────┬────────────────────────────────────────┘   │
│                                            │                                            │
│                                            ▼ (Exclusive Ledger Write Authority)         │
│   ┌────────────────────────────────────────┴────────────────────────────────────────┐   │
│   │                       Authoritative Transaction Ledgers                         │   │
│   │  - tabStock Ledger Entry (Exclusive Inventory Balance & Valuation Authority)    │   │
│   │  - tabGL Entry (Exclusive Financial & Cost Accounting Authority)                │   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Interactions & Responsibilities

### 2.1 `versa_textile` (Textile Process Domain Layer)
- **Entities Managed:** `Versa Fabric Roll` (ENT-017), `Versa Textile Process Stage`, `Versa Process Batch`.
- **Responsibilities:**
  1. Manages physical roll lifecycle (Inward $\to$ Inspection $\to$ Batching $\to$ Issue $\to$ Split $\to$ Merge $\to$ Cutting Lay).
  2. Executes dynamic physical measurement formulation ($\text{GLM} = \frac{\text{GSM} \times \text{Width}}{1000}$).
  3. Enforces mass-balance calculations on stage completion ($\text{Input} \equiv \text{Output} + \text{Allowed Loss} + \text{Excess Loss}$).

### 2.2 `versa_quality` Integration
- Before any fabric roll or process batch is released from a process stage or issued into cutting, `versa_textile` queries `versa_quality.gates` to verify that a submitted `Versa QC Result` exists with disposition `Accepted` or `Accepted with Concession`.
- Rolls marked `Quarantine` or `Rejected` are strictly blocked from stock movement hooks.

### 2.3 `versa_core` Integration
- All textile process records, fabric rolls, and batches are strictly scoped to `company` and respect fail-closed multi-company isolation query conditions (`permissions.py`).

---

## 3. Data Flow & Transaction Lifecycle

```text
1. Yarn Receipt ──► Purchase Receipt (Yarn Lot created in ERPNext Stock)
                         │
                         ▼
2. Knitting Stage ──► Stock Entry (Yarn Issued) ──► Knitted Greige Batch (Versa Fabric Rolls generated)
                         │
                         ▼
3. Greige QC Gate ──► Versa QC Result (GSM, Width, Spirality evaluated)
                         │
                         ▼
4. Dyeing Job Work ──► Versa Job Work Order ──► Stock Entry (Greige Rolls sent to Dyer)
                         │
                         ▼
5. Dyeing Receipt ──► Purchase Receipt ──► Mass-Balance Check ──► Dyed Fabric Batch Inward
                         │
                         ▼
6. Finishing / Stenter ──► Mass-Balance Loss Reconciled ──► Finished Fabric Rolls Barcoded
                         │
                         ▼
7. Final Fabric QC ──► ASTM D5430 4-Point Inspection (Grade A/B/C) ──► Released to Finished Fabric Store
                         │
                         ▼
8. Cutting Issue ──► Stock Entry (Material Issue to Cutting Lay Plan)
```

---

## 4. Architectural Invariants Preserved

1. **ERPNext Stock Exclusivity:** `versa_textile` never creates custom stock tables. Warehouse stock balances reside solely in `tabStock Ledger Entry`.
2. **ERPNext GL Exclusivity:** Commercial debits for excess process loss are posted via standard ERPNext `Purchase Invoice` debit notes.
3. **GraphModel Boundary:** GraphModel remains design-time semantic analysis tooling with zero runtime footprint.
