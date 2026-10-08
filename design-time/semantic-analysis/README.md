# VersaERP Design-Time Semantic Analysis Toolkit

================================================================================
CRITICAL ARCHITECTURAL DISCLAIMER:
This directory contains DESIGN-TIME SEMANTIC ANALYSIS TOOLING ONLY.
It is NOT runtime code, NOT a Frappe app, NOT an ERPNext extension,
and NOT a production dependency of VersaERP.

Runtime implementations under `E:\VersaERP\bench\apps\` must NEVER
import from this toolkit.
================================================================================

## 1. Purpose
Preserves the capability to perform design-time domain extraction, entity/invariant
reconciliation, and canonical JSON generation locally within the VersaERP repository
without creating a runtime dependency on GraphModel.

## 2. Directory Structure
- `toolkit/`: Minimal self-contained semantic analysis and reconciliation modules.
- `scripts/`: Canonical JSON generator and 3-tier domain model validator.
- `tests/`: Design-time toolkit verification tests.

## 3. Authority Hierarchy
```text
Business / Source Strategy Document
        ↓
VersaERP Design-Time Semantic Analysis (Tooling)
        ↓
Authoritative Versa Knowledge Base (E:\VersaERP\documents\versa)
        ↓
Frappe Implementation Specification (04_implementation_spec)
        ↓
Executable Versa ERP Runtime Bench (E:\VersaERP\bench\apps)
```
