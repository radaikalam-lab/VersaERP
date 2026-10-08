# Versa Quality (`versa_quality`)

Multi-Tier Textile Quality Assurance, Versioned Specifications, Multi-Point Measurements, and Quality Gates for VersaERP.

## Architecture
- **Versioned Quality Specifications:** Configurable parameters, limits, severity ratings, and test methods (ASTM, ISO, AATCC).
- **Multi-Point Readings & Provenance:** Individual measurements with timestamp, operator, instrument, and calibration references.
- **Deterministic Evaluation Engine:** Reproducible statistical tolerance evaluations and ASTM D5430 4-point defect scoring.
- **Quality Gates:** Fail-closed business controls on ERPNext `Purchase Receipt` and `Stock Entry`.
- **Tenant & Multi-Company Isolation:** Fail-closed site-level tenant isolation and company-scoped document permissions.
