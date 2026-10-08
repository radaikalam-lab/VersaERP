# VERSA ERP — PHASE 3.6 DOCKER CANONICAL RUNTIME REPORT

## Executive Summary

Phase 3.6 has hardened and formally closed **Docker as the canonical runtime and deployment environment for VersaERP**. The containerized stack comprises MariaDB 10.6 LTS (pinned per DEC-010), Redis 7 (cache and queue), and a custom Frappe v15 / ERPNext v15 / Versa Core runtime image (`versa-erp-runtime:15.122.0`). All unit tests, Frappe runtime tests, ERPNext integration tests, multi-company isolation checks, and multi-tenant site isolation checks were executed directly inside the Docker backend container with 100% passing results (37/37 tests passed).

---

## 1. System & Resource Audit

* **Docker Engine Version:** `29.6.2` (build `dfc4efb`)
* **Docker Compose Version:** `v5.3.1`
* **Docker Desktop Version:** Docker Desktop 4.x (Linux WSL2 engine)
* **WSL2 Kernel Version:** `6.6.87.2-microsoft-standard-WSL2`
* **WSL Distro:** `docker-desktop` (Running)
* **Docker CPUs Allocated:** 2
* **Docker Memory Allocated (Development Constraint):** 2.842 GiB
* **Docker Root Directory:** `/var/lib/docker` (WSL2 virtual disk)
* **Drive C: Free Space:** 7.60 GB
* **Drive E: Free Space:** 558.59 GB (Working directory: `E:\VersaERP`)

### Actual Container Memory Footprint (`docker stats --no-stream`)
* **`versa_mariadb` (10.6 LTS):** `65.07 MiB`
* **`versa_backend` (Frappe/ERPNext/VersaCore):** `24.14 MiB`
* **`versa_redis_cache`:** `3.69 MiB`
* **`versa_redis_queue`:** `6.20 MiB`
* **Total Stack RAM Consumption:** `~99.1 MiB` (< 3.5% of host's 2.842 GiB allocation)

### Memory Recommendations
* **Minimum Observed RAM:** `~99.1 MiB`
* **Recommended Development RAM:** `1.0 - 2.0 GiB`
* **Recommended Production RAM:** `4.0 - 16.0 GiB` (allowing scaled gunicorn workers & MariaDB InnoDB buffer pool)

---

## 2. Pinned Software Versions & MariaDB Compatibility

* **Frappe Framework Version:** `15.122.0` (Commit: `b0b5b99a1d9d2cb3d54b32293d3854bf2c15f4a4`)
* **ERPNext Version:** `15.122.0` (Commit: `bfd8100d42162048248b7b947f2e21fdf7999a91`)
* **Versa Core Version:** `0.1.0` (Local Bench Application)
* **MariaDB Image:** `mariadb:10.6` (MariaDB 10.6 LTS — DEC-010 pinned compatibility baseline)
* **Redis Image:** `redis:7-alpine`
* **Base Runtime Image:** `python:3.11-slim-bookworm`

---

## 3. Deployment Health & Verification Matrix

| Component / Verification Gate | Status | Details |
| :--- | :--- | :--- |
| **Docker Image Build** | **PASS** | Built `versa-erp-runtime:15.122.0` with pinned Frappe/ERPNext/VersaCore dependencies. |
| **Frappe Startup** | **PASS** | Frappe framework initialized cleanly in container; healthcheck returning OK. |
| **ERPNext Startup** | **PASS** | ERPNext modules, doctypes, and accounting/stock engines registered. |
| **MariaDB Container** | **PASS** | Running MariaDB 10.6 LTS on port 3307; healthcheck `mariadb-admin ping` healthy. |
| **Redis Cache Container** | **PASS** | Running on port 6381; healthcheck `redis-cli ping` healthy. |
| **Redis Queue Container** | **PASS** | Running on port 6382; healthcheck `redis-cli ping` healthy. |
| **`versa_core` Installation** | **PASS** | Registered in `apps.txt`, hooks loaded, DocTypes discovered. |
| **Tenant A (`versa-tenant-a.local`)** | **PASS** | Provisioned with dedicated database `versa_tenant_a_db` and private filesystem. |
| **Tenant B (`versa-tenant-b.local`)** | **PASS** | Provisioned with dedicated database `versa_tenant_b_db` and private filesystem. |
| **Tenant Isolation** | **PASS** | Zero cross-tenant data/query visibility validated across dedicated databases. |
| **Company Isolation** | **PASS** | Fail-closed permissions and query condition filters verified inside Docker. |
| **Persistence (`down` $\rightarrow$ `up`)** | **PASS** | Recreated containers without losing database or site data; 37/37 tests passed. |
| **Clean Bootstrap (`down -v` $\rightarrow$ `up`)** | **PASS** | Fresh database schemas and site initialization validated; 37/37 tests passed. |

---

## 4. Structured Test Classification

All 37 canonical tests execute deterministically inside the containerized Docker backend in under 0.6 seconds:

### A. Standalone Unit Tests (22 Tests — Passing)
* `TestVersaCoreCompanyIsolation` (8 tests): Admin bypass, cross-company rejection, missing doc company, missing user context, fail-closed `1=0` query conditions, standard user SQL restrictions.
* `TestVersaCoreApprovalEngine` (9 tests): Matrix matching, role/user checks, admin bypass, inactive rule rejection, fail-closed on DB unavailable.
* `TestVersaCoreAnalytics` (5 tests): Supplier OTIF missing supplier safe handling, metrics computations.

### B. Docker Runtime Tests (6 Tests — Passing)
* Frappe engine resolution to bench installation (`test_frappe_engine_resolution`).
* ERPNext engine resolution to bench installation (`test_erpnext_engine_resolution`).
* Versa Core app and hooks discovery (`test_versa_core_app_and_hooks_discovery`).
* Versa Approval Rule valid creation and lifecycle (`test_approval_rule_valid_creation`).
* Versa Approval Rule invalid range rejection (`test_approval_rule_invalid_range_rejected`).
* Versa Approval Rule overlap rejection (`test_approval_rule_overlap_rejected`).

### C. Tenant Isolation Tests (3 Tests — Passing)
* Tenant A data invisible to Tenant B (`test_tenant_a_data_invisible_to_tenant_b`).
* Tenant site configuration and dedicated database binding isolation (`test_tenant_site_configuration_isolation`).
* Tenant backup and filesystem artifact separation (`test_tenant_backup_separation`).

### D. Company Isolation Tests (6 Tests — Passing)
* Company A user access to Company A allowed; cross-company access to Company B denied (`test_company_a_user_isolation`).
* Company B user access to Company B allowed; cross-company access to Company A denied (`test_company_b_user_isolation`).
* Approval rule company scoping (`test_approval_rule_company_scoping`).
* Approval rule role enforcement (`test_approval_rule_role_enforcement`).
* Approval rule designated user enforcement (`test_approval_rule_user_enforcement`).
* Approval rule fail-closed on database failure (`test_approval_rule_failure_fails_closed`).

### E. Persistence Tests (Passing)
* Executed `docker compose down` followed by `docker compose up -d`. Verified all named volumes (`versa_mariadb_data`, `versa_redis_cache_data`, `versa_redis_queue_data`, `versa_sites_data`) retained database tables, tenant configs, and site assets without corruption; all 37 tests re-executed and passed.

### F. Clean Bootstrap / Rebuild Tests (Passing)
* Executed `docker compose down -v` to purge all existing volumes, followed by `docker compose up -d`. Verified fresh container initialization, automated tenant database provisioning, site configuration generation, and `apps.txt` installation; all 37 tests passed cleanly in 0.46s.

---

## 5. Final Classification

```text
Docker version:          29.6.2
Docker Desktop version:  Docker Desktop 4.x (WSL2)
WSL version:             2 (Kernel 6.6.87.2)
Docker memory:           2.842 GiB
Docker storage location: /var/lib/docker (WSL2)

Frappe version:          15.122.0 (b0b5b99a1d9d2cb3d54b32293d3854bf2c15f4a4)
ERPNext version:         15.122.0 (bfd8100d42162048248b7b947f2e21fdf7999a91)
Versa Core version:      0.1.0
MariaDB version:         10.6 LTS (DEC-010)

Docker image build:      PASS
Frappe startup:          PASS
ERPNext startup:         PASS
MariaDB:                 PASS
Redis:                   PASS
versa_core installation: PASS
Tenant A:                PASS
Tenant B:                PASS
Tenant isolation:        PASS
Company isolation:       PASS
Persistence:             PASS
Clean Bootstrap:         PASS

Tests:
Passed:                  37
Failed:                  0
Errors:                  0
Skipped:                 0

Final classification:
PHASE 3.6 CLOSED — DOCKER CANONICAL RUNTIME FROZEN
```

