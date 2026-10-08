# VERSA ERP — FRAPPE IMPLEMENTATION DECISION LOG

## 1. Objective & Governance Principles

This log records every technical and architectural implementation decision made during the translation of the frozen canonical domain model (`versa_domain_model.json`) into Frappe Framework v15 and ERPNext v15.

### Governing Principles:
1. **Preserve Domain Semantics:** Frappe implementation convenience must never silently alter or dilute canonical business semantics.
2. **Single Source of Truth:** ERPNext `Stock Ledger Entry` and `GL Entry` are the sole financial and inventory authorities.
3. **Upgrade Safety:** Zero core ERPNext code modifications; all extensions use custom DocTypes, child tables, custom fields, and event hooks.

---

## 2. Implementation Decisions Catalog

### DEC-001: Subcontracting Execution via `Versa Job Work Order` vs ERPNext `Subcontracting Order`
- **Issue:** ERPNext v15 has a native `Subcontracting Order` doctype, but it assumes rigid 1-to-1 BOM consumption and cannot handle dynamic textile mass balance, multi-stage yield reconciliation, or unaccounted theft penalties.
- **Canonical Domain Meaning:** In Tiruppur textile operations, subcontracted yarn knitting, fabric dyeing, and printing require dynamic input-to-output mass balance reconciliation ($\sum \text{Issued} \equiv \text{Output} + \text{Loss} + \text{Scrap} + \text{Returned} + \text{Unaccounted}$) with scale calibration tolerances ($\le 0.1\%$).
- **Implementation Alternatives:**
  - *Option A:* Force-fit ERPNext's standard `Subcontracting Order` by monkey-patching core controllers.
  - *Option B:* Implement a standalone `Versa Job Work Order` that orchestrates domain state, yield calculations, and mass balance, while delegating physical stock movements and AP billing to standard ERPNext `Stock Entry` and `Purchase Invoice`.
- **Selected Implementation:** **Option B.**
- **Reason:** Preserves upgrade safety and models textile mass balance accurately without corrupting core ERPNext subcontracting logic.
- **Effect on Domain Semantics:** None. Exact canonical domain semantics preserved.
- **Reversibility:** High. Standard ERPNext transactions remain the underlying inventory records.
- **Affected DocTypes:** `Versa Job Work Order`, `Versa Job Work Material`, `Versa Job Work Result`, `Stock Entry`, `Purchase Invoice`.
- **Affected Tests:** `TEST-INV-001`, `TEST-INV-007`.

---

### DEC-002: Dynamic Matrix Ordering via Embedded Child Table on `Sales Order`
- **Issue:** ERPNext standard `Sales Order Item` requires one discrete row per SKU variant, making the entry of a $10 \text{ colours} \times 6 \text{ sizes} = 60 \text{ SKU}$ order cumbersome and prone to error.
- **Canonical Domain Meaning:** Garment buyer purchase orders are contracted as a multi-dimensional matrix grid: $\text{Style} \times \text{Colour} \times \text{Shade} \times \text{Size}$.
- **Implementation Alternatives:**
  - *Option A:* Create separate custom `Versa Sales Order` DocType replacing ERPNext `Sales Order`.
  - *Option B:* Embed a custom Child Table `Versa Order Matrix` on standard `Sales Order` with a JavaScript grid renderer and server-side `before_save` synchronization to `Sales Order Item`.
- **Selected Implementation:** **Option B.**
- **Reason:** Keeps `Sales Order` within standard ERPNext O2C workflows (Delivery Note, Sales Invoice, Payment Entry) while giving merchandisers an intuitive matrix interface.
- **Effect on Domain Semantics:** None. Strict cell-level sum conservation is enforced server-side.
- **Reversibility:** High.
- **Affected DocTypes:** `Sales Order`, `Versa Order Matrix`, `Versa Style`.
- **Affected Tests:** `TEST-INV-002`, `TEST-INV-010`.

---

### DEC-003: Fabric Roll Physical Traceability Overlay vs Second Stock Ledger
- **Issue:** Fabric rolls require barcode serialization, roll length in meters, actual GSM, and 4-point defect scoring. ERPNext standard inventory valuation tracks stock by Weight ($kg$) in `Stock Ledger Entry`.
- **Canonical Domain Meaning:** `Versa Fabric Roll` represents physical roll-level traceability, while accounting valuation is based on standard $kg$ weight.
- **Implementation Alternatives:**
  - *Option A:* Create a parallel custom stock ledger table tracking every meter movement.
  - *Option B:* Model `Versa Fabric Roll` as a master / traceability unit linking `Item`, `Batch`, and `Warehouse`, while using ERPNext `Stock Entry` as the sole inventory movement ledger.
- **Selected Implementation:** **Option B.**
- **Reason:** Prevents ledger desynchronization and dual-authority bugs. ERPNext retains sole financial/inventory authority; `Versa Fabric Roll` provides physical attribute tracking.
- **Effect on Domain Semantics:** None. Dual-UOM formula $\text{Weight} = (\text{Length} \times \text{Width} \times \text{GSM})/1000 \pm 5\%$ is validated in Python.
- **Reversibility:** High.
- **Affected DocTypes:** `Versa Fabric Roll`, `Stock Entry`, `Purchase Receipt`, `Batch`, `Warehouse`.
- **Affected Tests:** `TEST-INV-004`, `TEST-INV-012`.

---

### DEC-004: Versioned Quality Inspection Engine & Gatekeeper Hook
- **Issue:** ERPNext standard `Quality Inspection` has fixed single-reading fields and cannot express versioned specifications, multi-point ASTM/ISO lab measurements, or concession approval workflows.
- **Canonical Domain Meaning:** Versa Quality requires versioned QC specifications (`Versa QC Spec`), multi-point readings (`Versa QC Measurement`), and disposition states (`Accepted`, `Concession`, `Quarantine`, `Rejected`).
- **Implementation Alternatives:**
  - *Option A:* Overwrite ERPNext `Quality Inspection` Python controller.
  - *Option B:* Implement dedicated `Versa QC Spec` and `Versa QC Result` DocTypes, connecting to ERPNext `Purchase Receipt` and `Stock Entry` via a `before_submit` gatekeeper hook.
- **Selected Implementation:** **Option B.**
- **Reason:** Eliminates core modification risks while providing enterprise lab inspection capabilities.
- **Effect on Domain Semantics:** None. Pushes authoritative disposition (`QC Passed`, `Concession`, `Rejected`) into ERPNext standard documents.
- **Reversibility:** High.
- **Affected DocTypes:** `Versa QC Spec`, `Versa QC Parameter`, `Versa QC Result`, `Versa QC Measurement`, `Purchase Receipt`, `Stock Entry`.
- **Affected Tests:** `TEST-INV-005`, `TEST-STR-021`, `TEST-STR-034`.

---

### DEC-005: Cumulative Billing Constraint for Dispatch-to-Invoice Reconciliation
- **Issue:** Early drafts assumed universal equality between dispatch quantity and invoice quantity ($\sum \text{Delivered} \equiv \sum \text{Invoiced}$). Real-world operations require partial billing, advance export invoices, and credit/debit return adjustments.
- **Canonical Domain Meaning:** Cumulative invoiced quantity must not exceed net accepted delivered quantity:
  $$\text{Cumulative Invoiced Qty} \le \text{Accepted Delivered Qty} - \text{Returned Qty}$$
- **Implementation Alternatives:**
  - *Option A:* Enforce rigid 1-to-1 Delivery Note to Sales Invoice matching.
  - *Option B:* Implement cumulative inequality validation on `Sales Invoice.validate` allowing partial billing while preventing over-invoicing.
- **Selected Implementation:** **Option B.**
- **Reason:** Reflects real-world garment export trade mechanics without sacrificing financial governance.
- **Effect on Domain Semantics:** Preserves the latest reconciled canonical rule.
- **Reversibility:** High.
- **Affected DocTypes:** `Delivery Note`, `Sales Invoice`, `Sales Order`.
- **Affected Tests:** `TEST-INV-009`.

---

### DEC-006: Multi-Company Scoping Architecture
- **Issue:** Deciding which DocTypes must be strictly company-owned vs globally shared across group companies.
- **Canonical Domain Meaning:** Group textile enterprises share standard master catalogs (yarn specifications, dye colours, QC standards) but isolate legal financial transactions, inventory warehouses, and styles.
- **Implementation Alternatives:**
  - *Option A:* Force `company` field on every single master and taxonomy table.
  - *Option B:* Categorize entities into 5 clear tiers:
    1. `COMPANY_OWNED`: `Cost Center`, `Warehouse`, `Versa Fabric Roll`, `Versa Style`, `Versa Carton`.
    2. `COMPANY_SCOPED_TRANSACTION`: All 10 transactional documents (SO, PO, PR, DN, PI, SI, SE, VJWO, VQR, VPP).
    3. `SHARED_MASTER`: Catalogs (`Item`, `Versa Material Spec`, `Versa Yarn Spec`, `Versa Fabric Spec`, `Versa Colour`, `Versa Shade`, `Versa QC Spec`, `Versa Job Worker`, `Customer`, `Supplier`, `Batch`).
    4. `DERIVED_COMPANY_CONTEXT`: All 11 child tables.
    5. `CONFIGURATION`: `Versa Approval Rule`.
- **Selected Implementation:** **Option B.**
- **Reason:** Maximizes master data reusability while ensuring bulletproof financial and inventory tenant isolation.
- **Effect on Domain Semantics:** Exactly implements canonical multi-company authority taxonomy.
- **Reversibility:** High.
- **Affected DocTypes:** All 39 canonical DocTypes.
- **Affected Tests:** `TEST-INV-006`, `TEST-STR-001` to `TEST-STR-039`.

---

### DEC-007: Deferment of Runtime Supplier OTIF Calculation Pending Precise Reconciliation Specification
- **Issue:** The preliminary runtime implementation calculated OTIF as `(total / total) * 100.0` (always 100%) or returned 98.5% on fallback. The authoritative contracts specify the high-level formula $\text{OTIF} = (\text{On-Time In-Full Receipts} / \text{Total Receipts}) \times 100$, but lack formal rules for line-level schedule date matching, delivery tolerance windows, and split-shipment fulfillment tracking.
- **Canonical Domain Meaning:** In textile procurement, delivery schedules may span multiple partial receipts against scheduled PO lines with allowed weight/quantity tolerances.
- **Implementation Alternatives:**
  - *Option A:* Invent an unvalidated heuristic for on-time and in-full thresholds.
  - *Option B:* Mark the runtime implementation as explicitly DEFERRED, log the gap in Open Questions (Question 6), and ensure the runtime returns `None` without polluting the Supplier master with fabricated scores.
- **Selected Implementation:** **Option B.**
- **Reason:** A knowingly fabricated metric violates governance integrity. Explicit deferral preserves semantic honesty until customer validation in Phase 0.
- **Effect on Domain Semantics:** Prevents false metric generation; records formal requirement for Phase 0 discovery.
- **Reversibility:** High.
- **Affected DocTypes:** `Supplier`, `Purchase Receipt`.
- **Affected Tests:** `TEST-INV-013`.

---

### DEC-008: Fail-Closed Security Policy and Elimination of Permissive Fallbacks
- **Issue:** Early development stubs used permissive exception handlers (`except Exception: return True`) and mock fallback values (`(`company` = 'Test Company')`, mock rule `VAR-PO-001`), which silently allowed unauthorized operations or masked missing database contexts.
- **Canonical Domain Meaning:** Multi-company isolation, approval matrix thresholds, and governance gates are hard invariants that must never fail open.
- **Implementation Alternatives:**
  - *Option A:* Maintain permissive exception handling for developer convenience.
  - *Option B:* Enforce strict fail-closed semantics across all controllers: missing company context returns `1 = 0` or raises `PermissionError`/`ValidationError`, and rule lookup failures reject submission.
- **Selected Implementation:** **Option B.**
- **Reason:** Core governance and security mechanisms must fail securely by default in production.
- **Effect on Domain Semantics:** Enforces absolute fidelity to canonical invariants `multi_company_isolation` and `approval_matrix_invariant`.
- **Reversibility:** Low (permanent architectural standard).
- **Affected DocTypes:** `Purchase Order`, `Sales Order`, `Purchase Receipt`, `Delivery Note`, `Purchase Invoice`, `Sales Invoice`, `Stock Entry`, `Cost Center`, `Warehouse`, `Versa Approval Rule`.
- **Affected Tests:** `test_core_suite.py`, `test_versa_approval_rule.py`.

---

### DEC-009: Physical Multi-Tenant Isolation Architecture (Site-per-Tenant Model)
- **Issue:** Establishing the technical boundary model for multi-tenant customer isolation in SaaS deployments of VersaERP on Frappe/ERPNext.
- **Canonical Domain Meaning:** Customer tenants must have fail-hard isolation with zero possibility of cross-tenant data leakage, independent database lifecycles, and independent backup/restore capability, while multi-company group operations within a single tenant share master catalogs.
- **Implementation Alternatives:**
  - *Option A:* Row-level multi-tenancy by adding a custom `tenant_id` field to all 300+ DocTypes in a single shared database.
  - *Option B:* Physical Site-per-Tenant multi-tenancy, where each SaaS customer is allocated a dedicated Frappe Site (`site_config.json`, dedicated database schema, dedicated private file directory, and site-prefixed Redis cache).
- **Selected Implementation:** **Option B.**
- **Reason:** Provides cryptographic, filesystem, and database-level isolation. Eliminates data bleed risks caused by missing SQL `WHERE` clauses, allows per-tenant backup/restore and schema upgrades, and cleanly separates tenant-level SaaS boundaries from intra-tenant multi-company boundaries.
- **Effect on Domain Semantics:** Exactly aligns with the Versa domain model and canonical invariants.
- **Reversibility:** High.
- **Affected DocTypes:** Entire Frappe Bench / Site Architecture.
- **Affected Tests:** `test_runtime_bootstrap.py` (`test_tenant_isolation_site_directory_boundary`, `test_tenant_backup_restore_separation`).

---

### DEC-010: Pinned MariaDB 10.6 LTS Baseline for Frappe Framework v15 Canonical Docker Runtime
- **Issue:** Selecting the supported and deterministic MariaDB engine version for the canonical Dockerized Frappe/ERPNext v15 runtime.
- **Canonical Domain Meaning:** The runtime environment must adhere strictly to officially supported and validated upstream dependencies to ensure database stability, transaction isolation, migration consistency, and deterministic reproducibility across development, CI, and production.
- **Implementation Alternatives:**
  - *Option A:* Use unpinned or rolling MariaDB tags (e.g., `mariadb:latest` or `mariadb:12.3`), which introduce breaking engine changes (such as deprecation of `--innodb-file-per-table` parameters and collation incompatibilities with Frappe schema fixtures).
  - *Option B:* Pin `mariadb:10.6` (MariaDB 10.6 LTS), which is the officially documented, tested, and supported database engine for Frappe Framework v15.
- **Selected Implementation:** **Option B (`mariadb:10.6`).**
- **Reason:** Frappe Framework v15 is certified and officially supported on MariaDB 10.6 LTS. MariaDB 10.6 provides rock-solid ACID transactions, predictable row locking semantics, and full backward compatibility with Frappe schema migrations and site creation scripts without requiring experimental flags.
- **Effect on Domain Semantics:** Guarantees database integrity and reproducible multi-tenant site bootstrap across all environments.
- **Reversibility:** Medium (database schema compatibility).
- **Affected Services:** `versa_mariadb` service in `docker-compose.yml`, tenant database instances.
- **Affected Tests:** All Docker runtime and tenant isolation tests.


