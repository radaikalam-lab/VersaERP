# VERSA ERP — CANONICAL DOCKER RUNTIME ARCHITECTURE

## 1. Executive Summary & Objective

Phase 3.6 establishes **Docker as the canonical runtime and deployment architecture for VersaERP**. While local development on Windows or Linux remains supported as a reference environment, all canonical testing, multi-tenant isolation, CI validation, and production cloud deployments standardize upon this containerized architecture.

---

## 2. Containerized Architecture Topology

The VersaERP Docker deployment architecture implements the official Frappe multi-container pattern:

```text
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           VERSA ERP DOCKER NETWORK                                │
│                                                                                   │
│   ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐   │
│   │   versa_mariadb     │    │  versa_redis_cache  │    │  versa_redis_queue  │   │
│   │  (MariaDB 10.6 LTS) │    │   (Redis 7 Alpine)  │    │   (Redis 7 Alpine)  │   │
│   │   Port: 3307        │    │   Port: 6381        │    │   Port: 6382        │   │
│   │   Vol: mariadb_data │    │   Vol: cache_data   │    │   Vol: queue_data   │   │
│   └──────────┬──────────┘    └──────────┬──────────┘    └──────────┬──────────┘   │
│              │                          │                          │              │
│              └──────────────────────────┼──────────────────────────┘              │
│                                         ▼                                         │
│                      ┌────────────────────────────────────┐                       │
│                      │           versa_backend            │                       │
│                      │   Frappe 15.122.0 + ERPNext 15.122 │                       │
│                      │        + versa_core (v0.1.0)       │                       │
│                      │   Port: 8008 / Vol: sites_data     │                       │
│                      └──────────────────┬─────────────────┘                       │
└─────────────────────────────────────────┼─────────────────────────────────────────┘
                                          │
                        ┌─────────────────┴─────────────────┐
                        ▼                                   ▼
          ┌───────────────────────────┐       ┌───────────────────────────┐
          │    versa-tenant-a.local   │       │    versa-tenant-b.local   │
          │    Database: tenant_a_db  │       │    Database: tenant_b_db  │
          │    Files: /private/files  │       │    Files: /private/files  │
          └───────────────────────────┘       └───────────────────────────┘
```

---

## 3. Storage & Volume Management

To preserve clean Git hygiene and avoid accidental disk bloat, container runtime state is isolated strictly within Docker named volumes:

| Volume Name | Mount Point in Container | Purpose |
| :--- | :--- | :--- |
| `versa_mariadb_data` | `/var/lib/mysql` | Persistent database storage for all tenant databases. |
| `versa_redis_cache_data`| `/data` | Redis persistent cache store (`appendonly yes`). |
| `versa_redis_queue_data`| `/data` | Redis persistent queue store for background jobs. |
| `versa_sites_data` | `/home/frappe/frappe-bench/sites` | Site configurations, encryption keys, and private files. |

---

## 4. Multi-Tenant Docker Site Lifecycle

Tenant sites are provisioned via programmatic scripts located in `deployment/docker/scripts/bootstrap_tenants.py`:
1. **Site Config Generation:** Each tenant site receives an isolated `site_config.json` defining dedicated database credentials and cryptographic encryption keys.
2. **Application Registration:** `sites/apps.txt` explicitly activates `frappe`, `erpnext`, and `versa_core`.
3. **Database Isolation:** Database users and schemas (`versa_tenant_a_db`, `versa_tenant_b_db`) are distinct, guaranteeing zero cross-tenant SQL visibility.

---

## 5. Resource Benchmarks & Sizing Guidelines

Live container measurements on the pinned runtime stack:

| Container | Measured Runtime RAM | Dev Baseline | Prod Recommended |
| :--- | :--- | :--- | :--- |
| `versa_mariadb` (10.6 LTS) | `65.07 MiB` | `256 MiB` | `2.0 - 8.0 GiB` |
| `versa_backend` | `24.14 MiB` | `512 MiB` | `2.0 - 4.0 GiB` |
| `versa_redis_cache` | `3.69 MiB` | `64 MiB` | `256 - 512 MiB` |
| `versa_redis_queue` | `6.20 MiB` | `64 MiB` | `256 - 512 MiB` |
| **Total Stack** | **`~99.1 MiB`** | **`1.0 - 2.0 GiB`** | **`4.0 - 16.0 GiB`** |

---

## 6. Operations & Lifecycle Commands

### 6.1 Clean Cold Bootstrap (from Scratch)
```bash
cd E:\VersaERP\deployment\docker
docker compose down -v
docker compose up -d
docker exec versa_backend python3 /home/frappe/frappe-bench/deployment/docker/scripts/run_docker_tests.py
```

### 6.2 Stack Startup (Existing Volumes)
```bash
docker compose up -d
```

### 6.3 Health Check Verification
```bash
docker ps --filter "name=versa"
```

### 6.4 Test Execution inside Docker
```bash
docker exec versa_backend python3 /home/frappe/frappe-bench/deployment/docker/scripts/run_docker_tests.py
```

### 6.5 Graceful Shutdown & Persistence Recovery
```bash
# Graceful stop preserving volumes:
docker compose down

# Start and recover persistent state:
docker compose up -d
```

---

## 7. Cloud Portability Guarantee

The Docker container definition uses standard OCI-compliant container standards:
- Base: `python:3.11-slim-bookworm`
- Database: `mariadb:10.6` LTS (DEC-010)
- In-memory store: `redis:7-alpine`
- Environment-agnostic volume mounts and port bindings.
- Zero local filesystem paths baked into application code.
- Identical deployment image functions on local developer machines, GitHub Actions CI runners, or production cloud container services (Kubernetes, AWS ECS, Oracle OKE, Hetzner Cloud).

