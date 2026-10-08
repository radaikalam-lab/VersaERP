#!/usr/bin/env python3
"""
VersaERP Docker Tenant Provisioning & Isolation Bootstrap Script.
Establishes the physical Site-per-Tenant model:
- Tenant A: versa-tenant-a.local -> db_tenant_a
- Tenant B: versa-tenant-b.local -> db_tenant_b
"""

import json
import os
import sys
from pathlib import Path

def bootstrap_tenants(bench_root: Path):
    print("=" * 70)
    print("BOOTSTRAPPING VERSA MULTI-TENANT DOCKER SITES")
    print("=" * 70)
    
    sites_dir = bench_root / "sites"
    sites_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. apps.txt registration
    apps_txt = sites_dir / "apps.txt"
    apps_content = "frappe\nerpnext\nversa_core\nversa_quality\n"
    apps_txt.write_text(apps_content, encoding="utf-8")
    print(f"[OK] Registered installed apps in {apps_txt}")
    
    # 2. common_site_config.json
    common_cfg = {
        "db_host": os.environ.get("DB_HOST", "mariadb"),
        "db_port": int(os.environ.get("MARIADB_PORT", 3306)),
        "redis_cache": f"redis://{os.environ.get('REDIS_CACHE_HOST', 'redis-cache')}:6379",
        "redis_queue": f"redis://{os.environ.get('REDIS_QUEUE_HOST', 'redis-queue')}:6379",
        "developer_mode": 1
    }
    (sites_dir / "common_site_config.json").write_text(json.dumps(common_cfg, indent=2), encoding="utf-8")
    print(f"[OK] Created common_site_config.json")
    
    # 3. Tenant Site Provisioning
    tenants = [
        ("versa-dev.local", "versa_dev_db", "dev_secret_key_12345"),
        ("versa-tenant-a.local", "versa_tenant_a_db", "tenant_a_secret_key_78901"),
        ("versa-tenant-b.local", "versa_tenant_b_db", "tenant_b_secret_key_34567")
    ]
    
    for site_name, db_name, enc_key in tenants:
        site_dir = sites_dir / site_name
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "private" / "files").mkdir(parents=True, exist_ok=True)
        (site_dir / "private" / "backups").mkdir(parents=True, exist_ok=True)
        (site_dir / "public" / "files").mkdir(parents=True, exist_ok=True)
        
        site_cfg = {
            "db_name": db_name,
            "db_user": db_name,
            "db_password": f"pwd_{db_name}",
            "encryption_key": enc_key,
            "installed_apps": ["frappe", "erpnext", "versa_core", "versa_quality"]
        }
        (site_dir / "site_config.json").write_text(json.dumps(site_cfg, indent=2), encoding="utf-8")
        print(f"[OK] Provisioned site '{site_name}' -> Database: '{db_name}'")

        
    print("=" * 70)
    print("TENANT PROVISIONING COMPLETED SUCCESSFULLY")
    print("=" * 70)
    return True

if __name__ == "__main__":
    bench_dir = Path("/home/frappe/frappe-bench")
    if not bench_dir.exists():
        bench_dir = Path(__file__).resolve().parent.parent.parent / "bench"
    success = bootstrap_tenants(bench_dir)
    sys.exit(0 if success else 1)
