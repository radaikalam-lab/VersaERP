# VERSA ERP — ARTIFACT & WORKSPACE GOVERNANCE POLICY

## 1. Core Principle & Workspace Topology

To ensure strict separation of concerns and prevent runtime contamination, the filesystem topology is frozen as follows:

```text
================================================================================
                    PERMANENT WORKSPACE TOPOLOGY
================================================================================
E:\GraphModel\
    │
    └── Design-Time Semantic Analysis Laboratory
            │
            └── Generates & Audits Canonical Domain Artifacts

E:\VersaERP\
    │
    ├── documents\
    │      └── versa\
    │             ├── 00_source\             # Original business strategy & requirements
    │             ├── 01_domain\             # Canonical domain models & JSON
    │             ├── 02_contracts\          # Business process contracts (P2P, O2C, etc.)
    │             ├── 03_architecture\       # Architecture audits, DAG analysis & reports
    │             ├── 04_implementation_spec\# Frappe DocType specifications & traceability
    │             ├── 05_validation\         # Domain & specification validation scripts
    │             ├── 06_decisions\          # Architectural decision logs (DEC-001..012)
    │             ├── 07_open_questions\     # Assumption register & deferred discovery
    │             └── 08_archive\            # Historical superseded artifacts
    │
    └── bench\
           └── apps\
                 ├── versa_core\             # Platform governance & approvals
                 ├── versa_quality\          # Lab test methods & QC results
                 ├── versa_textile\          # Fabric rolls, styles & order matrix
                 ├── versa_jobwork\          # Subcontracting yield & mass balance
                 └── versa_export\           # Carton packing & container lists
================================================================================
```

---

## 2. Authoritative Artifact Location Rules

1. **Single Authoritative Location:** `E:\VersaERP\documents\versa\` is the **only authoritative location** for all Versa domain, architecture, specification, and decision documents.
2. **GraphModel Cleanliness:** No `VERSA_*.md`, `versa_domain_model.json`, or Versa Frappe runtime code may be created in `E:\GraphModel\` root.
3. **Coding Agent Working Directory:** For all future Versa implementation tasks:
   ```text
   PROJECT_ROOT = E:\VersaERP
   RUNTIME_ROOT = E:\VersaERP\bench
   ARTIFACT_ROOT = E:\VersaERP\documents\versa
   ```

---

## 3. Artifact Classification & Lifecycle Governance

Every Versa document belongs to exactly one category:
- `00_source`: External customer requirements.
- `01_domain`: Canonical entity and semantic definitions.
- `02_contracts`: Operational business lifecycle contracts.
- `03_architecture`: Architectural audits, trade-off studies, and phase reports.
- `04_implementation_spec`: DocType specifications, field types, and traceability.
- `05_validation`: Test scripts and automated validators.
- `06_decisions`: Formally recorded architectural choices (`DEC-001` through `DEC-012`).
- `07_open_questions`: Explicitly isolated customer discovery items (`ASM-001` to `ASM-012`).
- `08_archive`: Superseded versions preserved for historical provenance.

---

## 4. Cryptographic Hash Integrity Rule

Every machine-readable and authoritative document must be tracked in `ARTIFACT_MANIFEST.md` with its SHA-256 hash. Any modification without updating the manifest fails automated validation.
