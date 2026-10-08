app_name = "versa_core"
app_title = "Versa Core"
app_publisher = "Versa ERP Platform Team"
app_description = "Core Governance, Approval Matrix & Multi-Company Tenant Isolation"
app_email = "core@versaerp.com"
app_license = "Proprietary"

# Document Events
# ---------------
# Hook on standard ERPNext document events
doc_events = {
    "Purchase Order": {
        "validate": "versa_core.permissions.check_company_isolation",
        "before_submit": "versa_core.approvals.check_approval_permission"
    },
    "Sales Order": {
        "validate": "versa_core.permissions.check_company_isolation",
        "before_submit": "versa_core.approvals.check_approval_permission"
    },
    "Purchase Receipt": {
        "validate": "versa_core.permissions.check_company_isolation",
        "on_submit": "versa_core.analytics.update_supplier_otif"
    },
    "Delivery Note": {
        "validate": "versa_core.permissions.check_company_isolation"
    },
    "Purchase Invoice": {
        "validate": "versa_core.permissions.check_company_isolation"
    },
    "Sales Invoice": {
        "validate": "versa_core.permissions.check_company_isolation"
    },
    "Stock Entry": {
        "validate": "versa_core.permissions.check_company_isolation"
    }
}

# Permission Query Conditions
# ---------------------------
# Enforces multi_company_isolation across company-owned and company-scoped transactions
permission_query_conditions = {
    "Sales Order": "versa_core.permissions.get_permission_query_conditions_company",
    "Purchase Order": "versa_core.permissions.get_permission_query_conditions_company",
    "Purchase Receipt": "versa_core.permissions.get_permission_query_conditions_company",
    "Delivery Note": "versa_core.permissions.get_permission_query_conditions_company",
    "Purchase Invoice": "versa_core.permissions.get_permission_query_conditions_company",
    "Sales Invoice": "versa_core.permissions.get_permission_query_conditions_company",
    "Stock Entry": "versa_core.permissions.get_permission_query_conditions_company",
    "Cost Center": "versa_core.permissions.get_permission_query_conditions_company",
    "Warehouse": "versa_core.permissions.get_permission_query_conditions_company",
}

# Fixtures
# --------
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Versa Core"]]
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "Versa Core"]]
    }
]
