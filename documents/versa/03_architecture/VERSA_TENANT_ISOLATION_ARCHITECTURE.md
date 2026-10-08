# VERSA ERP — TENANT ISOLATION ARCHITECTURE SPECIFICATION

## 1. Executive Summary & Architectural Invariant

VersaERP establishes a **Physical Site-per-Tenant Multi-Tenancy Architecture** on top of Frappe Framework and ERPNext.

```text
Tenant A (Customer A)             Tenant B (Customer B)
       │                                 │
       ▼                                 ▼
Frappe Site A                     Frappe Site B
(`versa-tenant-a.local`)          (`versa-tenant-b.local`)
       │                                 │
       ▼                                 ▼
Database A (`_db_tenant_a`)       Database B (`_db_tenant_b`)
       │                                 │
       ▼                                 ▼
Private Storage A                 Private Storage B
(`/sites/versa-tenant-a/private`) (`/sites/versa-tenant-b/private`)
```

### Core Invariant
> **Strict Multi-Tenant Isolation Rule:**
> One Customer Tenant = One Frappe Site = One Dedicated Database & File Root.
>
> Tenant boundaries MUST NEVER be implemented solely via application-level database row filtering (e.g. a shared `tenant_id` column across a single monolithic database). The physical database, encryption keys, and filesystem boundaries serve as the primary isolation layer.

---

## 2. Multi-Tenant vs Multi-Company Hierarchy

VersaERP distinguishes between **Tenant Boundaries** (SaaS isolation) and **Company Boundaries** (Enterprise legal entities within a single tenant):

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                           TENANT A (Frappe Site A)                            │
│  - Dedicated Database (MariaDB/PostgreSQL)                                   │
│  - Dedicated Encryption Key (`site_config.json`)                             │
│  - Dedicated Private File Storage (`/sites/tenant-a/private/files`)          │
│                                                                               │
│   ┌─────────────────────────────┐         ┌─────────────────────────────┐   │
│   │ Company 1: Spinning Mills   │         │ Company 2: Garment Export   │   │
│   │ (Legal Entity, Tax ID 1)    │         │ (Legal Entity, Tax ID 2)    │   │
│   └──────────────┬──────────────┘         └──────────────┬──────────────┘   │
│                  │                                       │                  │
│                  └───────────────────┬───────────────────┘                  │
│                                      ▼                                      │
│                         Shared Master Catalogs                              │
│             (Yarn Specs, Fabric Specs, QC Specs, Colours)                   │
└───────────────────────────────────────────────────────────────────────────────┘
```

| Isolation Dimension | Scope / Level | Mechanism | Security Guarantee |
| :--- | :--- | :--- | :--- |
| **Tenant Isolation** | Customer SaaS Boundary | Physical Site & Dedicated Database | Fail-hard physical isolation. Zero shared tables or cross-tenant query vectors. |
| **Company Isolation** | Legal entities within 1 tenant | Frappe User Permissions & Fail-Closed Scoping | Strict logical & role-based separation with shared master data catalog efficiency. |

---

## 3. Physical Boundary Implementation

### 3.1 Database Isolation
- Each tenant site connects to a dedicated SQL database (`db_name` in `site_config.json`).
- Database user credentials (`db_user`, `db_password`) are isolated per tenant.
- No cross-database joins or global queries exist at the database engine level.

### 3.2 Filesystem & Private Storage Isolation
- Uploaded business documents, export invoices, QC measurement certs, and attachments are stored strictly under:
  ```text
  E:\VersaERP\bench\sites\<tenant-site-name>\private\files\
  ```
- Public assets (unauthenticated web assets) are confined to:
  ```text
  E:\VersaERP\bench\sites\<tenant-site-name>\public\files\
  ```
- No tenant has filesystem visibility or directory traversal access to another tenant's site directory.

### 3.3 Cache & Background Task Namespacing
- Frappe namespacing uses the site name as a prefix for all Redis keys:
  - Cache: `frappe.cache().hset(site, ...)`
  - Background Queue: RQ jobs are tagged with site context and executed with strict site activation (`frappe.init(site)` and `frappe.connect()`).

---

## 4. Rejection of Row-Level Monolithic Multi-Tenancy

Shared-database multi-tenancy (adding `tenant_id` to all 300+ ERPNext and Versa tables) was formally evaluated and rejected based on the following failure modes:

1. **Catastrophic Leakage on Query Bugs:** A single developer oversight omitting `WHERE tenant_id = ...` leaks confidential financial, payroll, and proprietary garment costing data across competitors.
2. **Schema & Migration Lockstep:** Monolithic multi-tenancy prevents staged tenant rollouts, schema migrations, and custom tenant patching.
3. **Regulatory Non-Compliance:** Global textile brands demand distinct data storage locations and encryption boundaries to satisfy EU GDPR, SOC 2, and ISO 27001 requirements.
4. **Performance & Lock Contention:** High-volume transaction processing (e.g. barcode scanning 10,000 fabric rolls/day) in Tenant A degrades database locking and write throughput for Tenant B.

---

## 5. Backup, Restore & Disaster Recovery Architecture

Because each tenant is an independent Frappe site, backup and restore operations are completely isolated and atomic.

### 5.1 Independent Backup Generation
```bash
bench --site versa-tenant-a.local backup --with-files
```
Produces an independent artifact bundle:
- Database dump: `[site_dir]/private/backups/[timestamp]-versa_tenant_a-database.sql.gz`
- Site Config: `[site_dir]/private/backups/[timestamp]-versa_tenant_a-site_config_backup.json`
- Private files: `[site_dir]/private/backups/[timestamp]-versa_tenant_a-private-files.tar`
- Public files: `[site_dir]/private/backups/[timestamp]-versa_tenant_a-files.tar`

### 5.2 Independent Point-in-Time Recovery
- Tenant A can be restored to a previous point in time or migrated across physical servers without taking down or affecting Tenant B.
- Zero risk of cross-tenant data overwrite during database restoration.

---

## 6. Runtime Verification

The site-per-tenant isolation architecture is validated by the test suite `E:\VersaERP\bench\apps\versa_core\versa_core\tests\test_runtime_bootstrap.py`:
- `test_tenant_isolation_site_directory_boundary`: Confirms distinct site configurations, database pointers, and private directory paths.
- `test_tenant_backup_restore_separation`: Confirms that backup snapshots and database identifiers for Tenant A and Tenant B are completely separate.
