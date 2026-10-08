# VERSA ERP — QUALITY SUBSYSTEM ARCHITECTURE (`versa_quality`)

## 1. Executive Summary & Objective

The `versa_quality` application provides a **textile-domain quality assurance and quality-gate architecture** integrated with ERPNext. It operationalizes versioned quality specifications, multi-point physical readings, statistical tolerance limits, ASTM D5430 4-point defect scoring, and fail-closed quality gates.

The system adheres strictly to the canonical architectural boundary:
- **ERPNext** retains absolute authority over the Stock Ledger (inventory movements and valuations) and General Ledger (accounting).
- **Versa Quality** serves as the evidence-producing evaluation engine and business control gate.

---

## 2. Authority Model & Non-Duplication Principle

```text
ERPNext Authority (Accounting & Stock Ledgers)
├── Stock Ledger
│      = Inventory Authority (Balances, Valuation, Serial/Batch movements)
└── General Ledger
       = Financial Authority (Debits/Credits, Cost Centers, Invoicing)

Versa Quality Layer (Evidence, Evaluation & Governance)
├── Versioned Quality Specifications (`Versa QC Spec`)
├── Quality Parameters & Test Methods (`Versa QC Parameter`)
├── Multi-Point Readings & Provenance (`Versa QC Reading`)
├── Evaluated Measurements (`Versa QC Measurement`)
├── Inspection Event & Disposition (`Versa QC Result`)
├── Business Quality Gates (`Purchase Receipt`, `Stock Entry`)
└── Textile Traceability Overlay (Item, Batch, Fabric Roll, Supplier)
```

**Non-Duplication Invariants:**
1. Versa Quality does **not** create or maintain a secondary stock balance ledger.
2. Versa Quality does **not** create or maintain a secondary accounting ledger.
3. Versa Quality evaluates physical and laboratory evidence to determine whether material can advance through workflow states.

---

## 3. Subsystem Architecture & Component Hierarchy

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          VERSA QUALITY SUBSYSTEM                            │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         Versa QC Spec                               │   │
│   │  - spec_name, version, material_type, buyer_customer, is_active     │   │
│   │  - Parameters Child Table: [Versa QC Parameter]                     │   │
│   │    * parameter_code, test_method, target_value, min/max limits      │   │
│   │    * severity (Critical, Major, Minor), sampling_required           │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │ (Instantiates & Locks Spec Version)  │
│                                      ▼                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        Versa QC Result                              │   │
│   │  - company, inspection_type, source_doctype, source_name, item      │   │
│   │  - inspected_by, inspection_date, overall_status                    │   │
│   │  - 4-Point Defect Scoring: (inspected_length, width, points, score) │   │
│   │  - Concession Signoff: concession_reason, concession_approved_by    │   │
│   │  - Child Tables:                                                    │   │
│   │    * [Versa QC Reading]: Individual multi-point readings            │   │
│   │    * [Versa QC Measurement]: Aggregated stats & parameter status    │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                  Deterministic Evaluation Engine                    │   │
│   │  - Pure statistical aggregation (mean, min, max, std dev)           │   │
│   │  - Tolerance limit verification (Range, Minimum, Maximum, Visual)   │   │
│   │  - ASTM D5430 4-Point Defect Score Calculation                      │   │
│   │  - Overall Disposition: Accepted / Concession / Quarantine / Reject │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                   Quality Gate Business Controls                    │   │
│   │  - Purchase Receipt before_submit: Blocks unapproved material       │   │
│   │  - Stock Entry before_submit: Blocks issue of quarantined rolls     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Multi-Tenant & Multi-Company Isolation

1. **Site-per-Tenant Isolation:**
   - Quality DocTypes and tables reside exclusively in the tenant's dedicated database.
   - Zero cross-tenant SQL visibility or query leakage.
2. **Fail-Closed Multi-Company Scoping:**
   - Every `Versa QC Result` is mandatory-scoped to `company`.
   - Standard users receive dynamic SQL filters `tabVersa QC Result.company = '{user_company}'`.
   - Users lacking active company context receive `1 = 0`.
   - Cross-company operations raise `PermissionError`.

---

## 5. Provenance & Auditability Standard

Every measurement recorded in Versa Quality preserves its physical and operational provenance:
- **Timestamp:** Exact date and time of measurement.
- **Operator:** Verified Frappe user who conducted the test.
- **Instrument:** Registered testing apparatus (e.g. "GSM Cutter #2", "Tensile Tester TT-400").
- **Calibration Reference:** Active calibration certificate identifier.
- **Specification Version:** Immutable freeze of the exact specification version applied at inspection time.
