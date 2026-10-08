# VERSA ERP — RUNTIME VERSION & COMPATIBILITY MATRIX

## 1. Executive Summary & Reproducibility Standard

This document pins the exact runtime software versions, package releases, and Git commit hashes for the **VersaERP Platform Runtime Environment**. All dependencies are frozen to guarantee deterministic multi-tenant execution and reproducible development/production environments.

---

## 2. Core Runtime Software Stack

| Component | Exact Version | Repository / Source | Pinned Git Commit | Purpose / Role |
| :--- | :--- | :--- | :--- | :--- |
| **Operating System** | `Windows 11 Pro 64-bit (Build 26300)` | Host Environment | N/A | Development Host Operating System |
| **Python** | `3.13.14 (AMD64)` | Python Software Foundation | N/A | Primary Python Runtime Engine |
| **pip** | `26.1.2` | Python Package Installer | N/A | Python Dependency Resolver |
| **Frappe Framework** | `v15.122.0` (branch `version-15`) | `https://github.com/frappe/frappe.git` | `b0b5b99a1d9d2cb3d54b32293d3854bf2c15f4a4` | Core Metadata & Web Framework Engine |
| **ERPNext Core** | `v15.122.0` (branch `version-15`) | `https://github.com/frappe/erpnext.git` | `bfd8100d42162048248b7b947f2e21fdf7999a91` | Transactional & Accounting Engine (GL/Stock) |
| **Versa Core** | `v1.0.0` (Custom App) | `E:\VersaERP\bench\apps\versa_core` | Local Repository | Governance, Multi-Company & Approval Engine |
| **Git** | `2.55.0.windows.2` | Git for Windows | N/A | Version Control System |
| **Docker** | `29.6.2 (build dfc4efb)` | Docker Engine / Desktop | N/A | Containerized Services & Production Sandbox |
| **Node.js** | `v16.13.2` | `E:\nodejs\node.exe` | N/A | JavaScript Asset Compiler |
| **npm** | `8.1.2` | `E:\nodejs\npm.cmd` | N/A | Frontend Package Manager |
| **Database Engine** | `MariaDB 10.6 LTS` (Port 3307 / 3306) | Docker Official `mariadb:10.6` | N/A | Multi-Tenant Database Storage (DEC-010) |
| **Redis Cache / Queue** | `Redis 7-alpine` (Port 6381/6382) | Docker Official `redis:7-alpine` | N/A | In-Memory Caching & Background Workers |

---

## 3. Bench Directory Structure & App Locations

```text
E:\VersaERP\bench
├── apps
│   ├── frappe/                  # Frappe Framework v15.122.0 (Commit: b0b5b99)
│   ├── erpnext/                 # ERPNext Core v15.122.0 (Commit: bfd8100)
│   ├── versa_core/              # Versa Core Platform App v0.1.0
│   ├── versa_quality/           # (Reserved for Phase 4)
│   ├── versa_textile/           # (Reserved for Phase 5)
│   ├── versa_jobwork/           # (Reserved for Phase 6)
│   └── versa_export/            # (Reserved for Phase 7)
│
└── sites
    ├── apps.txt                 # frappe, erpnext, versa_core
    ├── common_site_config.json  # Bench-wide defaults
    ├── versa-dev.local/         # Primary Local Development Site
    ├── versa-tenant-a.local/    # Multi-Tenant Verification Site A
    └── versa-tenant-b.local/    # Multi-Tenant Verification Site B
```

---

## 4. Key Pinned Python Dependencies

| Package | Pinned Version | Role in Runtime |
| :--- | :--- | :--- |
| `PyMySQL` | `1.1.1` | MariaDB / MySQL Native Connection Driver |
| `PyPika` | `git@7ef6e40` | SQL Query Builder Engine |
| `Werkzeug` | `3.1.6` | WSGI Request Router & Server Utilities |
| `gunicorn` | `23.0.0 (git@bb55405)` | WSGI Production Web Server |
| `RestrictedPython`| `8.5` | Sandboxed Script Evaluation Engine |
| `duckdb` | `1.4.5` | In-Memory Analytical Query Accelerator |
| `pyarrow` | `25.0.1` | High-Performance Columnar Memory Engine |
| `redis` | `4.5.5` | Redis Client Protocol Driver |
| `rq` | `1.15.1` | Redis Queue Background Task Manager |
| `cairocffi` | `1.5.1` | High-Fidelity PDF & Print Engine |
| `WeasyPrint` | `69.0` | HTML/CSS to Document Renderer |

---

## 5. Docker Canonical Runtime Stack (Phase 3.6 Standard)

| Container / Layer | Image / Base | Port Mapping | Storage Volume | Role / Status |
| :--- | :--- | :--- | :--- | :--- |
| **Backend Runtime** | `versa-erp-runtime:15.122.0` (Debian Bookworm slim / Python 3.11) | `8008 -> 8000` | `versa_sites_data` | Canonical Execution Runtime |
| **Database Server** | `mariadb:10.6` (MariaDB 10.6 LTS) | `3307 -> 3306` | `versa_mariadb_data` | Pinned Canonical Database Engine (DEC-010) |
| **Redis Cache** | `redis:7-alpine` | `6381 -> 6379` | `versa_redis_cache_data` | Pinned Site Cache Engine |
| **Redis Queue** | `redis:7-alpine` | `6382 -> 6379` | `versa_redis_queue_data` | Pinned Background Worker Queue |

---

## 6. Resource Benchmarks & Memory Sizing Guidelines

| Component | Minimum Measured RAM (Idle / Suite) | Recommended Dev RAM | Recommended Prod RAM |
| :--- | :--- | :--- | :--- |
| **`versa_mariadb` (10.6 LTS)** | `65.07 MiB` | `256 MiB` | `2.0 - 8.0 GiB` (tuned buffer pool) |
| **`versa_backend`** | `24.14 MiB` | `512 MiB` | `2.0 - 4.0 GiB` (multi-worker gunicorn) |
| **`versa_redis_cache`** | `3.69 MiB` | `64 MiB` | `256 - 512 MiB` |
| **`versa_redis_queue`** | `6.20 MiB` | `64 MiB` | `256 - 512 MiB` |
| **Total Stack** | **`~99.1 MiB`** | **`1.0 - 2.0 GiB`** | **`4.0 - 16.0 GiB`** |

*Note: The constrained development host allocation of 2.842 GiB RAM comfortably accommodates the entire canonical Docker stack with over 96% memory headroom.*

