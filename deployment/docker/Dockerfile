# VersaERP Canonical Docker Runtime Image
# Based on Python 3.11-slim-bookworm with pinned Frappe v15 & ERPNext v15

FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FRAPPE_VERSION=15.122.0 \
    FRAPPE_COMMIT=b0b5b99a1d9d2cb3d54b32293d3854bf2c15f4a4 \
    ERPNEXT_VERSION=15.122.0 \
    ERPNEXT_COMMIT=bfd8100d42162048248b7b947f2e21fdf7999a91 \
    PATH="/home/frappe/.local/bin:${PATH}"

# Install minimal OS dependencies for Frappe / MariaDB / Git
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    libffi-dev \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Create frappe user
RUN useradd -ms /bin/bash frappe
USER frappe
WORKDIR /home/frappe/frappe-bench

# Install core runtime python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
    werkzeug \
    gunicorn \
    redis \
    pymysql \
    cryptography \
    click \
    jinja2 \
    requests \
    pytz \
    sqlparse

# Create bench directories
RUN mkdir -p apps sites config logs

# Copy apps into image
COPY --chown=frappe:frappe bench/apps /home/frappe/frappe-bench/apps
COPY --chown=frappe:frappe deployment/docker /home/frappe/frappe-bench/deployment/docker

# Install apps in editable mode
RUN pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/frappe && \
    pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/erpnext && \
    pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/versa_core && \
    pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/versa_quality

# Initialize sites configuration
RUN python3 /home/frappe/frappe-bench/deployment/docker/scripts/bootstrap_tenants.py

# Healthcheck definition
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import frappe, erpnext, versa_core, versa_quality; print('VersaERP Runtime Healthy')" || exit 1

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/home/frappe/frappe-bench/deployment/docker/scripts/entrypoint.sh"]

