# VERSA ERP — PHASE 2.1 ARCHITECTURAL DECISIONS

## 1. Overview & Context

This document logs implementation-level clarification decisions resulting from the adversarial review in Phase 2.1, building upon decisions `DEC-001` through `DEC-006` recorded in [`VERSA_FRAPPE_IMPLEMENTATION_DECISIONS.md`](file:///e:/GraphModel/VERSA_FRAPPE_IMPLEMENTATION_DECISIONS.md).

---

## 2. Decision Log

### DEC-007: Invariant Taxonomy Formalization & Implementation Enforcement
- **Issue:** Terminology ambiguity where all 13 normative items were colloquially referred to as "invariants", risking treating softer business/workflow rules as immutable mathematical laws.
- **Canonical Domain Meaning:** The frozen canonical domain model (`versa_domain_model.json`) formally distinguishes:
  1. `CANONICAL_INVARIANT` (6 items): Strict, non-negotiable mathematical/physical conservation laws. Hard block on save/submit. Zero tolerance.
  2. `BUSINESS_RULE` (3 items): Commercial policy constraints (e.g. 3-way match, excess loss penalty). Can have configurable tolerances and concession paths.
  3. `WORKFLOW_RULE` (2 items): Operational lifecycle transitions (e.g. cutting allowance, short shipment closure).
  4. `DERIVED_METRIC` (2 items): Analytical scores (e.g. 4-point defect score, OTIF index).
- **Selected Implementation:** The Frappe implementation spec strictly segregates enforcement mechanisms:
  - `CANONICAL_INVARIANT` $\to$ Enforced via Python controller `validate` and `before_submit` methods throwing fatal `frappe.ValidationError`.
  - `BUSINESS_RULE` $\to$ Enforced via controller methods with configurable tolerance fields from `Company` settings and explicit supervisor override permissions.
  - `WORKFLOW_RULE` $\to$ Managed via standard document status updates and event hooks.
  - `DERIVED_METRIC` $\to$ Asynchronous background jobs and read-only calculated fields.
- **Effect on Domain Semantics:** Exactly preserves the 4-tier canonical classification.
- **Affected DocTypes:** All 39 canonical DocTypes.
- **Affected Tests:** `TEST-INV-001` to `TEST-INV-013`.

---

### DEC-008: App Dependency DAG & Fixture Packaging Contract
- **Issue:** Multi-app Frappe architectures can suffer from circular imports and installation race conditions if app dependencies are not strictly acyclic.
- **Canonical Domain Meaning:** The domain model decomposes into distinct architectural concerns: Governance, Quality, Textile Masters, Subcontracting, and Export Logistics.
- **Selected Implementation:** Strict unidirectional Directed Acyclic Graph (DAG):
  $$\text{erpnext} \longrightarrow \text{versa\_core} \longrightarrow \text{versa\_quality} \longrightarrow \text{versa\_textile} \longrightarrow \text{versa\_jobwork} \longrightarrow \text{versa\_export}$$
  - Upstream apps must never import downstream apps.
  - Cross-cutting links from downstream to upstream use Frappe standard `Link` fields.
  - Upstream apps referencing downstream transactions use `Dynamic Link` fields or event hooks registered in downstream `hooks.py`.
- **Effect on Domain Semantics:** Prevents architectural spaghetti and circular dependencies.
- **Affected Apps:** All 5 Versa applications.

---

### DEC-009: Shared Master vs Company Applicability Architecture
- **Issue:** A risk was identified that classifying masters (`Item`, `Supplier`, `Versa QC Spec`, `Versa Colour`) as `SHARED_MASTER` might make them globally writable across legal tenants or conflate master identity with transactional ownership.
- **Canonical Domain Meaning:**
  $$\text{Master Identity (Shared Definition)} \neq \text{Company Applicability (Item Defaults / Pricing)} \neq \text{Transaction Ownership (Document Company)}$$
- **Selected Implementation:**
  1. `SHARED_MASTER` DocTypes store universal technical specifications (e.g. Yarn 30s Combed, Pantone 19-4052, ASTM D3776 spec) without a mandatory `company` foreign key.
  2. Write permissions on shared masters are restricted to `System Manager` and `Versa Administrator`.
  3. Company-specific defaults (e.g. default warehouse, expense account, cost center) are maintained in ERPNext `Item Default` child table keyed by `company`.
  4. All transactional documents (SO, PO, PR, DN, PI, SI, SE, VJWO, VQR, VPP) enforce strict `company` scoping via mandatory field and Frappe permission query conditions.
- **Effect on Domain Semantics:** Complete tenant isolation without master data duplication.
- **Affected DocTypes:** `Item`, `Supplier`, `Versa Material Spec`, `Versa QC Spec`, `Versa Colour`, `Versa Shade`.

---

### DEC-010: Precise Order Matrix Conservation Tuple Identity
- **Issue:** Verifying whether `order_matrix_conservation` could accidentally perform a loose global quantity sum rather than conserving quantities across multi-dimensional product identities.
- **Canonical Domain Meaning:** Quantity conservation must hold across the exact dimensional tuple:
  $$(\text{Parent Sales Order}, \text{Style}, \text{Colour}, \text{Shade}, \text{Size Code})$$
- **Selected Implementation:**
  - `Versa Order Matrix` child table enforces composite identity `(style, colour, shade, size_code)`.
  - The `before_save` and `before_submit` hook evaluates line-by-line:
    $$\forall (s, c, h, z) \in \text{Sales Order Item}: \quad \text{line.qty} \equiv \sum \text{MatrixRow}(s, c, h, z).\text{ordered\_qty}$$
  - Throws `frappe.ValidationError` specifying the exact $(s, c, h, z)$ mismatch if quantities diverge.
- **Effect on Domain Semantics:** Zero semantic drift; exact mathematical conservation.
- **Affected DocTypes:** `Sales Order`, `Versa Order Matrix`, `Sales Order Item`.
- **Affected Tests:** `TEST-INV-002`.

---

### DEC-011: Minimum Viable Job Work Orchestration Scope
- **Issue:** Avoiding rebuilding standard ERPNext purchasing/inventory functions while fully capturing Tiruppur subcontracting mass balance.
- **Canonical Domain Meaning:** Versa Job Work owns process routing, machine capability matching, stage yield calculation, loss classification, and unaccounted theft governance. ERPNext owns inventory ledger movements and AP invoice posting.
- **Selected Implementation:**
  - `Versa Job Work Order` acts as the operational orchestrator.
  - On submit: Automatically creates and submits ERPNext `Stock Entry` (Type: `Send to Subcontractor`).
  - On material receipt: Updates `Versa Job Work Result`, calculates yield/loss, and triggers ERPNext `Stock Entry` (Type: `Receive at Subcontractor`).
  - On settlement: Creates ERPNext `Purchase Invoice` for service rate $\times$ output quantity, minus auto-calculated debit line for excess process loss.
  - Zero custom inventory or AP ledger tables created.
- **Effect on Domain Semantics:** Eliminates duplicate authority while delivering 100% domain fidelity.
- **Affected DocTypes:** `Versa Job Work Order`, `Stock Entry`, `Purchase Invoice`.
- **Affected Tests:** `TEST-INV-001`, `TEST-INV-007`.

---

### DEC-012: Multi-Vertical Coexistence Protocol (Bike Workshop Proofing)
- **Issue:** Testing whether the Versa architecture can support a non-textile vertical (e.g. Motorcycle / Bike Workshop) without contaminating textile semantics or ERPNext core.
- **Selected Implementation:**
  - `versa_core` provides shared governance: `Versa Approval Rule`, credit checks, multi-company isolation query conditions.
  - `versa_quality` provides domain-agnostic inspection engine: versioned specs, parameter limits, multi-point measurement capture (applicable to vehicle parts inspection).
  - Vertical-specific applications (`versa_textile`, `versa_jobwork`, `versa_export`) remain completely decoupled.
  - A new vertical (e.g. `versa_workshop`) simply installs on top of `versa_core` and `versa_quality` with zero changes to textile DocTypes or ERPNext core.
- **Effect on Domain Semantics:** Proves long-term multi-vertical architectural durability.
- **Affected Apps:** `versa_core`, `versa_quality`.
