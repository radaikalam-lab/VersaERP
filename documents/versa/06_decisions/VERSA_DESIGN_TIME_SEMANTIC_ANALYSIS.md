# VERSA ERP — DESIGN-TIME SEMANTIC ANALYSIS CAPABILITY DECISION

## 1. Provenance & Metadata

- **Decision ID:** `DEC-013`
- **Topic:** Versa-Local Design-Time Semantic Analysis Toolkit
- **Date Established:** 2026-10-08
- **Source Repository:** `E:\GraphModel\src\graphmodel\` and `E:\GraphModel\scripts\`
- **Target Location:** `E:\VersaERP\design-time\semantic-analysis\`
- **Status:** `AUTHORITATIVE (TOOLING ONLY)`
- **Runtime Dependency Status:** `NONE (Zero Runtime Dependency)`

---

## 2. Core Statement

> **"This design-time semantic-analysis capability is derived from the GraphModel semantic-analysis work but is not a runtime dependency of VersaERP."**

The copied workspace is a local design-time semantic analysis and canonicalization toolkit. It is NOT runtime code, NOT a Frappe app, NOT an ERPNext extension, NOT a production dependency, and NOT the authoritative Versa artifact repository.

---

## 3. Components Copied vs Intentionally Excluded

### 3.1 Copied Components (`toolkit/` and `scripts/`)
1. `toolkit/semantics/`: Semantic mapping, layers, models, inference, and graph projection.
2. `toolkit/domain/`: Canonical domain entity modeling, requirements, and assurance.
3. `toolkit/reconciliation/`: Reconciliation engine, cross-system alignment, and traceability.
4. `toolkit/requirements/`: Trace and requirements parsing builders.
5. `toolkit/provenance/`: Provenance tracking interfaces.
6. `scripts/generate_canonical_json.py`: Deterministic canonical JSON generator.
7. `scripts/validate_versa_domain_model.py`: 3-Tier canonical domain model validator.

### 3.2 Intentionally Excluded Components
1. GraphModel runtime engines (Execution, Gateway, Cognitia, Integration Fabric).
2. Unrelated domain implementations (Banking, Cement, Agriculture, SENAITE/LIMS).
3. Historical benchmark suites and regression test harnesses.
4. Python virtual environments, caches (`__pycache__`, `.pytest_cache`), and `.git`.
5. Experimental notebooks and scratch files.

---

## 4. Purpose & Authority Boundary

```text
================================================================================
                        AUTHORITY HIERARCHY
================================================================================
  1. Business Source Requirements
     `E:\VersaERP\documents\versa\00_source\Versa_ERP_Platform_Strategy_Tiruppur.docx`
           │
           ▼
  2. Versa Design-Time Semantic Analysis (Tooling Only)
     `E:\VersaERP\design-time\semantic-analysis\`
           │
           ▼
  3. Authoritative Versa Knowledge Base (Frozen Canonical Baseline)
     `E:\VersaERP\documents\versa\01_domain\versa_domain_model.json`
           │
           ▼
  4. Frappe Implementation Specification
     `E:\VersaERP\documents\versa\04_implementation_spec\`
           │
           ▼
  5. Executable Runtime Bench (Frappe / ERPNext)
     `E:\VersaERP\bench\apps\`
================================================================================
```
