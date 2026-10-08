# VERSA ERP — QUALITY SUBSYSTEM DECISIONS LOG (`versa_quality`)

## DEC-011: Strict Separation of Quality Evidence from ERPNext Stock & Accounting Ledgers
- **Issue:** Establishing the architectural boundary between quality evaluation and transactional inventory/financial posting.
- **Canonical Domain Meaning:** Quality inspection produces auditable physical and lab evidence and determines state readiness, but must never become an independent stock ledger or financial ledger.
- **Decision:** ERPNext remains the sole authority for Stock Ledger and General Ledger. Versa Quality provides quality gates (`before_submit` validation hooks) that permit or block ERPNext transactions based on deterministic quality evaluations.
- **Effect on Domain Semantics:** Eliminates ledger duplication, maintains dual-UOM integrity, and prevents valuation desynchronization.

---

## DEC-012: Versioned Specifications & Historical Immutability
- **Issue:** Ensuring historical quality results remain interpretable against the exact specification version that was effective when inspection took place.
- **Canonical Domain Meaning:** A quality specification must support controlled versions. Once a specification version is referenced by submitted inspection results, its parameter definitions cannot be altered in-place.
- **Decision:** `Versa QC Result` records and locks `spec_version`. `Versa QC Spec` controller rejects in-place mutations of parameter definitions for versions with submitted results, requiring creation of a new version (e.g. V2.0).
- **Effect on Domain Semantics:** Full compliance with ISO 9001 and buyer audit standards.

---

## DEC-013: Deterministic Evaluation & Elimination of AI/Heuristic Approximations
- **Issue:** Establishing the evaluation methodology for multi-point lab readings, statistical tolerances, and ASTM D5430 4-point defect scoring.
- **Canonical Domain Meaning:** Quality evaluation must be 100% reproducible, explainable, and deterministic. No probabilistic heuristics, hidden tolerances, or AI predictions.
- **Decision:** Implemented standard arithmetic mean, sample standard deviation, explicit tolerance type comparisons, and exact ASTM D5430 formula. Missing evidence evaluates strictly to `Inconclusive` and fails closed.
- **Effect on Domain Semantics:** 100% reproducible QA disposition across all tenant sites.

---

## DEC-014: Fail-Closed Quality Gate Enforcement on Purchase Receipts & Stock Issues
- **Issue:** Enforcing quality gates on goods receipts and production material issues.
- **Canonical Domain Meaning:** Material requiring quality inspection must not be accepted into active stock or issued to cutting/subcontracting without explicit quality clearance.
- **Decision:** Hooked `Purchase Receipt` and `Stock Entry` `before_submit` events to fail closed if inspection is required and no valid `Accepted` or authorized `Accepted with Concession` QC Result is present.
- **Effect on Domain Semantics:** Strict prevention of uninspected or off-spec material entering production.
