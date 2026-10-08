app_name = "versa_quality"
app_title = "Versa Quality"
app_publisher = "Versa ERP Platform Team"
app_description = "Textile QA/QC, Versioned Specifications, Multi-Point Measurements & Quality Gates"
app_email = "quality@versaerp.com"
app_license = "Proprietary"

# Document Events
# ---------------
doc_events = {
    "Purchase Receipt": {
        "before_submit": "versa_quality.events.purchase_receipt.check_qc_conformance"
    },
    "Stock Entry": {
        "before_submit": "versa_quality.events.stock_entry.validate_qc_status"
    },
    "Versa QC Result": {
        "validate": "versa_quality.permissions.check_quality_company_isolation"
    }
}

# Permission Query Conditions
# ---------------------------
# Enforces multi-company isolation on quality documents
permission_query_conditions = {
    "Versa QC Result": "versa_quality.permissions.get_permission_query_conditions_quality_result",
    "Versa QC Spec": "versa_quality.permissions.get_permission_query_conditions_quality_spec"
}

# Fixtures
# --------
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Versa Quality"]]
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "Versa Quality"]]
    }
]
