#!/bin/bash
set -e

echo "===================================================="
echo "VERSA ERP CANONICAL RUNTIME BOOTSTRAP (DOCKER)"
echo "===================================================="

cd /home/frappe/frappe-bench

# Ensure sites directory exists
mkdir -p sites/versa-dev.local sites/versa-tenant-a.local sites/versa-tenant-b.local

# Write apps.txt if missing
if [ ! -f "sites/apps.txt" ]; then
    echo -e "frappe\nerpnext\nversa_core" > sites/apps.txt
fi

# Run custom command if provided
if [ "$#" -gt 0 ]; then
    exec "$@"
fi

# Default fallback: keep container active or run test suite
echo "Versa ERP Docker Backend Ready."
exec python3 -m http.server 8000 --directory /home/frappe/frappe-bench
