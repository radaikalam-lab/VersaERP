import json
import os

model = {
    "schema_version": "1.3.0",
    "model_name": "Versa_ERP_Tiruppur_Canonical_Domain_Model",
    "source_document": "Source/Versa_ERP_Platform_Strategy_Tiruppur.docx",
    "extracted_at": "2026-10-08T12:45:00Z",
    "authoritative_environment": "GraphModel (Design-time Semantic Analysis)",
    "target_platform": "Versa ERP Platform (Frappe / ERPNext Modular Extension)",
    "runtime_dependency": "None (GraphModel is zero-runtime dependency)",
    "classification_taxonomy": [
        "ERPNext_STANDARD",
        "VERSA_EXTENSION",
        "VERSA_TRANSACTION",
        "VERSA_CHILD_TABLE",
        "CONFIGURATION",
        "DERIVED",
        "REFERENCE",
        "OPEN"
    ],
    "provenance_taxonomy": [
        "SOURCE",
        "INFERRED",
        "ASSUMED",
        "DERIVED",
        "OPEN"
    ],
    "invariant_classification_taxonomy": [
        "CANONICAL_INVARIANT",
        "BUSINESS_RULE",
        "WORKFLOW_RULE",
        "DERIVED_METRIC",
        "ASSUMPTION",
        "OPEN"
    ],
    "company_authority_taxonomy": [
        "COMPANY_OWNED",
        "COMPANY_SCOPED_TRANSACTION",
        "SHARED_MASTER",
        "DERIVED_COMPANY_CONTEXT",
        "CONFIGURATION"
    ],
    "reconciliation_summary": {
        "source_business_concepts": 39,
        "domain_entities_total": 39,
        "erpnext_reused_doctypes": 14,
        "versa_master_extensions": 8,
        "versa_transactions": 3,
        "versa_child_tables": 11,
        "reference_taxonomies": 2,
        "configuration_doctypes": 1,
        "configuration_models": 4,
        "derived_analytics_concepts": 6,
        "canonical_relationships_total": 28,
        "invariants_by_classification": {
            "CANONICAL_INVARIANT": 6,
            "BUSINESS_RULE": 3,
            "WORKFLOW_RULE": 2,
            "DERIVED_METRIC": 2,
            "ASSUMPTION": 0,
            "OPEN": 0,
            "TOTAL_INVARIANTS_AND_RULES": 13
        }
    },
    "apps": [
        {"app_name": "versa_core", "purpose": "Governance, dynamic approval matrices, credit policies, business units", "provenance": "SOURCE"},
        {"app_name": "versa_textile", "purpose": "Yarn/Fabric specs, fabric rolls, garment styles, order matrices", "provenance": "SOURCE"},
        {"app_name": "versa_jobwork", "purpose": "Job worker profiles, subcontracting orders, mass balance reconciliation", "provenance": "SOURCE"},
        {"app_name": "versa_quality", "purpose": "Multi-tier QC specs, test parameters, physical measurements, AQL", "provenance": "SOURCE"},
        {"app_name": "versa_export", "purpose": "Cartonization, packing plans, export packing lists", "provenance": "SOURCE"}
    ],
    "entities": [
        # --- 1. ERPNext Standard Reused DocTypes (14) ---
        {
            "name": "Company",
            "classification": "ERPNext_STANDARD",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Legal corporate entity, root of general ledger and financial accounting.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master",
            "app": "erpnext",
            "natural_key": ["company_name"],
            "lifecycle_states": ["Active", "Disabled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company_name", "type": "Data", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "default_currency", "type": "Link", "target": "Currency", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Cost Center",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_OWNED",
            "provenance": "INFERRED",
            "business_purpose": "Business unit / branch / division for budgeting and P&L segregation.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master",
            "app": "erpnext",
            "natural_key": ["cost_center_name", "company"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "cost_center_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Customer",
            "classification": "ERPNext_STANDARD",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Buyer / Brand legal commercial party, credit limit, and receivables account.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master",
            "app": "erpnext",
            "natural_key": ["customer_name"],
            "lifecycle_states": ["Active", "Disabled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "customer_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "customer_group", "type": "Link", "target": "Customer Group", "mandatory": True, "provenance": "SOURCE"},
                {"name": "credit_limit", "type": "Currency", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Supplier",
            "classification": "ERPNext_STANDARD",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Vendor for raw materials, trims, chemicals, and subcontracted services.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master",
            "app": "erpnext",
            "natural_key": ["supplier_name"],
            "lifecycle_states": ["Active", "Disabled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "supplier_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "supplier_group", "type": "Link", "target": "Supplier Group", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Item",
            "classification": "ERPNext_STANDARD",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Base inventory SKU for stock ledger, valuation, billing, and taxation.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master",
            "app": "erpnext",
            "natural_key": ["item_code"],
            "lifecycle_states": ["Active", "Disabled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "item_code", "type": "Data", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "item_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "item_group", "type": "Link", "target": "Item Group", "mandatory": True, "provenance": "SOURCE"},
                {"name": "stock_uom", "type": "Link", "target": "UOM", "mandatory": True, "provenance": "SOURCE"},
                {"name": "is_stock_item", "type": "Check", "default": 1, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Warehouse",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_OWNED",
            "provenance": "SOURCE",
            "business_purpose": "Physical or logical storage location for raw materials, WIP, and finished goods.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master",
            "app": "erpnext",
            "natural_key": ["warehouse_name", "company"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "warehouse_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Batch",
            "classification": "ERPNext_STANDARD",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "ERPNext stock batch tracking inventory lots, manufacturing dates, and supplier batch references.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Master/Traceability",
            "app": "erpnext",
            "natural_key": ["batch_id"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "batch_id", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Sales Order",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Commercial commitment with buyer, holding total values and delivery dates.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "To Deliver and Bill", "To Bill", "To Deliver", "Completed", "Cancelled", "Closed"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "customer", "type": "Link", "target": "Customer", "mandatory": True, "provenance": "SOURCE"},
                {"name": "transaction_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"},
                {"name": "delivery_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"},
                {"name": "grand_total", "type": "Currency", "mandatory": True, "provenance": "SOURCE"},
                {"name": "docstatus", "type": "Int", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Purchase Order",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Commercial purchasing contract issued to raw material vendors.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "To Receive and Bill", "To Bill", "To Receive", "Completed", "Cancelled", "Closed"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "supplier", "type": "Link", "target": "Supplier", "mandatory": True, "provenance": "SOURCE"},
                {"name": "transaction_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"},
                {"name": "grand_total", "type": "Currency", "mandatory": True, "provenance": "SOURCE"},
                {"name": "docstatus", "type": "Int", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Purchase Receipt",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Goods receipt note updating stock ledger and creating batch/roll references.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Submitted", "Cancelled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "supplier", "type": "Link", "target": "Supplier", "mandatory": True, "provenance": "SOURCE"},
                {"name": "posting_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"},
                {"name": "docstatus", "type": "Int", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Delivery Note",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Stock dispatch transaction linked to cartons and shipping containers.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Submitted", "Cancelled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "customer", "type": "Link", "target": "Customer", "mandatory": True, "provenance": "SOURCE"},
                {"name": "posting_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"},
                {"name": "docstatus", "type": "Int", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Purchase Invoice",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Accounts payable invoice for raw materials and job work service charges.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Submitted", "Paid", "Partly Paid", "Unpaid", "Cancelled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "supplier", "type": "Link", "target": "Supplier", "mandatory": True, "provenance": "SOURCE"},
                {"name": "grand_total", "type": "Currency", "mandatory": True, "provenance": "SOURCE"},
                {"name": "outstanding_amount", "type": "Currency", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Sales Invoice",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Accounts receivable billing document with GST / e-Invoicing compliance.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Submitted", "Paid", "Partly Paid", "Unpaid", "Cancelled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "customer", "type": "Link", "target": "Customer", "mandatory": True, "provenance": "SOURCE"},
                {"name": "grand_total", "type": "Currency", "mandatory": True, "provenance": "SOURCE"},
                {"name": "outstanding_amount", "type": "Currency", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Stock Entry",
            "classification": "ERPNext_STANDARD",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Movement of goods for Job Work Issue, Job Work Receipt, and Production Consumption.",
            "runtime_owner": "ERPNext",
            "doctype_type": "Transaction",
            "app": "erpnext",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Submitted", "Cancelled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "purpose", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "posting_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"}
            ]
        },

        # --- 2. Versa Extensions & Master DocTypes (8) ---
        {
            "name": "Versa Material Spec",
            "classification": "VERSA_EXTENSION",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Decouples textile technical specifications from ERPNext stock SKU catalog.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Material Spec",
            "doctype_type": "Master",
            "app": "versa_textile",
            "natural_key": ["item", "specification_version"],
            "lifecycle_states": ["Draft", "Active", "Superseded", "Deprecated"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "specification_version", "type": "Data", "mandatory": True, "default": "V1.0", "provenance": "SOURCE"},
                {"name": "material_type", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "composition", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "is_active", "type": "Check", "default": 1, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Yarn Spec",
            "classification": "VERSA_EXTENSION",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Captures spinning count, ply, process, twist, and mill for yarn procurement.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Yarn Spec",
            "doctype_type": "Master",
            "app": "versa_textile",
            "natural_key": ["material_spec"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "material_spec", "type": "Link", "target": "Versa Material Spec", "mandatory": True, "provenance": "SOURCE"},
                {"name": "yarn_count", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "count_system", "type": "Select", "default": "Ne", "provenance": "INFERRED"},
                {"name": "ply", "type": "Int", "default": 1, "provenance": "SOURCE"},
                {"name": "spinning_process", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "twist_type", "type": "Select", "default": "Z-Twist", "provenance": "INFERRED"},
                {"name": "csp_min", "type": "Float", "provenance": "ASSUMED"},
                {"name": "origin_mill", "type": "Data", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Fabric Spec",
            "classification": "VERSA_EXTENSION",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Defines knit/woven structure, target GSM, width, finishing, shrinkage, and spirality.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Fabric Spec",
            "doctype_type": "Master",
            "app": "versa_textile",
            "natural_key": ["material_spec"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "material_spec", "type": "Link", "target": "Versa Material Spec", "mandatory": True, "provenance": "SOURCE"},
                {"name": "fabric_structure", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "target_gsm", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "gsm_tolerance_pct", "type": "Float", "default": 3.0, "provenance": "INFERRED"},
                {"name": "cuttable_width_inches", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "finish_type", "type": "Select", "default": "Greige", "provenance": "SOURCE"},
                {"name": "shrinkage_length_pct_max", "type": "Float", "default": 5.0, "provenance": "SOURCE"},
                {"name": "shrinkage_width_pct_max", "type": "Float", "default": 5.0, "provenance": "SOURCE"},
                {"name": "spirality_pct_max", "type": "Float", "default": 4.0, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Fabric Roll",
            "classification": "VERSA_EXTENSION",
            "company_authority": "COMPANY_OWNED",
            "provenance": "SOURCE",
            "business_purpose": "Physical unit inventory tracking for fabric rolls with weight, meters, GSM, and defect grades.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Fabric Roll",
            "doctype_type": "Master/Traceability",
            "app": "versa_textile",
            "natural_key": ["roll_barcode"],
            "lifecycle_states": ["In Stock", "Issued to Cutting", "Issued to Job Work", "Consumed", "Scrapped"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "roll_barcode", "type": "Data", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "batch", "type": "Link", "target": "Batch", "mandatory": True, "provenance": "SOURCE"},
                {"name": "roll_no", "type": "Int", "mandatory": True, "provenance": "SOURCE"},
                {"name": "warehouse", "type": "Link", "target": "Warehouse", "mandatory": True, "provenance": "SOURCE"},
                {"name": "net_weight_kg", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "gross_weight_kg", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "length_meters", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "actual_gsm", "type": "Float", "provenance": "SOURCE"},
                {"name": "actual_width_inches", "type": "Float", "provenance": "SOURCE"},
                {"name": "shade", "type": "Link", "target": "Versa Shade", "provenance": "SOURCE"},
                {"name": "quality_grade", "type": "Select", "default": "Quarantine", "provenance": "SOURCE"},
                {"name": "defect_points_4point", "type": "Float", "default": 0.0, "provenance": "INFERRED"},
                {"name": "status", "type": "Select", "default": "In Stock", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Style",
            "classification": "VERSA_EXTENSION",
            "company_authority": "COMPANY_OWNED",
            "provenance": "SOURCE",
            "business_purpose": "Garment product master containing BOM, operations, colourways, and size ranges.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Style",
            "doctype_type": "Master",
            "app": "versa_textile",
            "natural_key": ["company", "buyer_customer", "style_no"],
            "lifecycle_states": ["Development", "Sampling", "Costed", "Approved for Production", "Archived"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "style_no", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "buyer_customer", "type": "Link", "target": "Customer", "mandatory": True, "provenance": "SOURCE"},
                {"name": "brand", "type": "Data", "provenance": "SOURCE"},
                {"name": "season", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "garment_type", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "base_fabric_item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "target_sam_minutes", "type": "Float", "default": 0.0, "provenance": "INFERRED"},
                {"name": "status", "type": "Select", "default": "Development", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Job Worker",
            "classification": "VERSA_EXTENSION",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Subcontractor profile capturing process capabilities, machine gauge/dia, and ratings.",
            "runtime_owner": "Versa Job Work",
            "table_name": "tabVersa Job Worker",
            "doctype_type": "Master/Extension",
            "app": "versa_jobwork",
            "natural_key": ["supplier"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "supplier", "type": "Link", "target": "Supplier", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "machine_count", "type": "Int", "default": 0, "provenance": "INFERRED"},
                {"name": "daily_capacity_kg", "type": "Float", "default": 0.0, "provenance": "ASSUMED"},
                {"name": "standard_loss_tolerance_pct", "type": "Float", "default": 3.0, "provenance": "INFERRED"},
                {"name": "quality_rating", "type": "Float", "default": 5.0, "provenance": "SOURCE"},
                {"name": "compliance_status", "type": "Select", "default": "Compliant", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa QC Spec",
            "classification": "VERSA_EXTENSION",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Versioned inspection specification standard for materials, processes, and garments.",
            "runtime_owner": "Versa Quality",
            "table_name": "tabVersa QC Spec",
            "doctype_type": "Master",
            "app": "versa_quality",
            "natural_key": ["spec_code"],
            "lifecycle_states": ["Active", "Disabled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "spec_code", "type": "Data", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "spec_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "material_type", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "version", "type": "Data", "default": "1.0", "provenance": "SOURCE"},
                {"name": "is_active", "type": "Check", "default": 1, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Carton",
            "classification": "VERSA_EXTENSION",
            "company_authority": "COMPANY_OWNED",
            "provenance": "SOURCE",
            "business_purpose": "Physical carton unit with barcode serialization, dimensions, and weighment.",
            "runtime_owner": "Versa Export",
            "table_name": "tabVersa Carton",
            "doctype_type": "Master/Traceability",
            "app": "versa_export",
            "natural_key": ["carton_barcode"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "packing_plan", "type": "Link", "target": "Versa Packing Plan", "mandatory": True, "provenance": "SOURCE"},
                {"name": "carton_barcode", "type": "Data", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "carton_no", "type": "Int", "mandatory": True, "provenance": "SOURCE"},
                {"name": "length_cm", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "width_cm", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "height_cm", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "gross_weight_kg", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "net_weight_kg", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "total_pcs", "type": "Int", "default": 0, "provenance": "SOURCE"}
            ]
        },

        # --- 3. Versa Transaction DocTypes (3) ---
        {
            "name": "Versa Job Work Order",
            "classification": "VERSA_TRANSACTION",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Subcontract process control document tracking issues, receipts, losses, and settlements.",
            "runtime_owner": "Versa Job Work",
            "table_name": "tabVersa Job Work Order",
            "doctype_type": "Transaction",
            "app": "versa_jobwork",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Issued", "In Progress", "Partially Received", "Completed", "Cancelled", "Closed"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "job_worker", "type": "Link", "target": "Supplier", "mandatory": True, "provenance": "SOURCE"},
                {"name": "process", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "source_doctype", "type": "Select", "provenance": "INFERRED"},
                {"name": "source_name", "type": "Dynamic Link", "provenance": "INFERRED"},
                {"name": "planned_input_qty", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "planned_output_qty", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "uom", "type": "Link", "target": "UOM", "mandatory": True, "provenance": "SOURCE"},
                {"name": "allowed_loss_pct", "type": "Float", "default": 3.0, "provenance": "SOURCE"},
                {"name": "rate_per_unit", "type": "Currency", "mandatory": True, "provenance": "SOURCE"},
                {"name": "billing_basis", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "status", "type": "Select", "default": "Draft", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa QC Result",
            "classification": "VERSA_TRANSACTION",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Inspection transaction recording multi-point physical readings and pass/concession/fail disposition.",
            "runtime_owner": "Versa Quality",
            "table_name": "tabVersa QC Result",
            "doctype_type": "Transaction",
            "app": "versa_quality",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "Submitted", "Cancelled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "qc_spec", "type": "Link", "target": "Versa QC Spec", "mandatory": True, "provenance": "SOURCE"},
                {"name": "inspection_type", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "source_doctype", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "source_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "batch", "type": "Link", "target": "Batch", "provenance": "SOURCE"},
                {"name": "roll_barcode", "type": "Link", "target": "Versa Fabric Roll", "provenance": "SOURCE"},
                {"name": "inspected_by", "type": "Link", "target": "User", "mandatory": True, "provenance": "SOURCE"},
                {"name": "inspection_date", "type": "Date", "mandatory": True, "provenance": "SOURCE"},
                {"name": "sample_size", "type": "Int", "default": 1, "provenance": "INFERRED"},
                {"name": "overall_status", "type": "Select", "default": "Quarantine", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Packing Plan",
            "classification": "VERSA_TRANSACTION",
            "company_authority": "COMPANY_SCOPED_TRANSACTION",
            "provenance": "SOURCE",
            "business_purpose": "Packing plan organizing order ratio allocation and carton breakdown.",
            "runtime_owner": "Versa Export",
            "table_name": "tabVersa Packing Plan",
            "doctype_type": "Transaction",
            "app": "versa_export",
            "synthetic_key": ["name"],
            "lifecycle_states": ["Draft", "In Packing", "Completed", "Dispatched"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "company", "type": "Link", "target": "Company", "mandatory": True, "provenance": "SOURCE"},
                {"name": "sales_order", "type": "Link", "target": "Sales Order", "mandatory": True, "provenance": "SOURCE"},
                {"name": "customer", "type": "Link", "target": "Customer", "mandatory": True, "provenance": "SOURCE"},
                {"name": "packing_type", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "total_planned_cartons", "type": "Int", "default": 0, "provenance": "SOURCE"},
                {"name": "status", "type": "Select", "default": "Draft", "provenance": "SOURCE"}
            ]
        },

        # --- 4. Versa Child Tables (11) ---
        {
            "name": "Versa Style Material",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Component material requirement and consumption per garment piece.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Style Material",
            "doctype_type": "Child Table",
            "app": "versa_textile",
            "parent": "Versa Style",
            "attributes": [
                {"name": "item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "material_type", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "consumption_per_pc", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "uom", "type": "Link", "target": "UOM", "mandatory": True, "provenance": "SOURCE"},
                {"name": "wastage_pct", "type": "Float", "default": 0.0, "provenance": "INFERRED"}
            ]
        },
        {
            "name": "Versa Style Operation",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Sequential routing operations, SAM, and standard piece rates for garment styles.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Style Operation",
            "doctype_type": "Child Table",
            "app": "versa_textile",
            "parent": "Versa Style",
            "attributes": [
                {"name": "operation_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "sequence_no", "type": "Int", "mandatory": True, "provenance": "SOURCE"},
                {"name": "standard_sam", "type": "Float", "default": 0.0, "provenance": "INFERRED"},
                {"name": "subcontractable", "type": "Check", "default": 0, "provenance": "SOURCE"},
                {"name": "default_piece_rate", "type": "Currency", "default": 0.0, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Style Colourway",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Approved colour and shade combinations for the style.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Style Colourway",
            "doctype_type": "Child Table",
            "app": "versa_textile",
            "parent": "Versa Style",
            "attributes": [
                {"name": "colour", "type": "Link", "target": "Versa Colour", "mandatory": True, "provenance": "SOURCE"},
                {"name": "shade", "type": "Link", "target": "Versa Shade", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Style Size",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Size grid definitions and measurement grading charts.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Style Size",
            "doctype_type": "Child Table",
            "app": "versa_textile",
            "parent": "Versa Style",
            "attributes": [
                {"name": "size_code", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "sequence_no", "type": "Int", "mandatory": True, "provenance": "INFERRED"}
            ]
        },
        {
            "name": "Versa Order Matrix",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Colour × Size quantity breakdown grid embedded on Sales Order.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Order Matrix",
            "doctype_type": "Child Table",
            "app": "versa_textile",
            "parent": "Sales Order",
            "attributes": [
                {"name": "style", "type": "Link", "target": "Versa Style", "mandatory": True, "provenance": "SOURCE"},
                {"name": "colour", "type": "Link", "target": "Versa Colour", "mandatory": True, "provenance": "SOURCE"},
                {"name": "shade", "type": "Link", "target": "Versa Shade", "provenance": "SOURCE"},
                {"name": "size_code", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "ordered_qty", "type": "Int", "default": 0, "provenance": "SOURCE"},
                {"name": "confirmed_qty", "type": "Int", "default": 0, "provenance": "SOURCE"},
                {"name": "produced_qty", "type": "Int", "default": 0, "provenance": "SOURCE"},
                {"name": "packed_qty", "type": "Int", "default": 0, "provenance": "SOURCE"},
                {"name": "delivered_qty", "type": "Int", "default": 0, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Job Worker Process",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "INFERRED",
            "business_purpose": "Machine gauge, diameter, and process capability list per Job Worker.",
            "runtime_owner": "Versa Job Work",
            "table_name": "tabVersa Job Worker Process",
            "doctype_type": "Child Table",
            "app": "versa_jobwork",
            "parent": "Versa Job Worker",
            "attributes": [
                {"name": "process_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "machine_specs", "type": "Data", "provenance": "INFERRED"},
                {"name": "loss_tolerance_pct", "type": "Float", "default": 3.0, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Job Work Material",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Raw material lots and rolls issued to Job Worker.",
            "runtime_owner": "Versa Job Work",
            "table_name": "tabVersa Job Work Material",
            "doctype_type": "Child Table",
            "app": "versa_jobwork",
            "parent": "Versa Job Work Order",
            "attributes": [
                {"name": "item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "batch", "type": "Link", "target": "Batch", "provenance": "SOURCE"},
                {"name": "roll_barcode", "type": "Link", "target": "Versa Fabric Roll", "provenance": "SOURCE"},
                {"name": "qty_issued", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "qty_returned", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "uom", "type": "Link", "target": "UOM", "mandatory": True, "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa Job Work Result",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Processed output receipts, mass balance, process loss, and scrap reconciliation.",
            "runtime_owner": "Versa Job Work",
            "table_name": "tabVersa Job Work Result",
            "doctype_type": "Child Table",
            "app": "versa_jobwork",
            "parent": "Versa Job Work Order",
            "attributes": [
                {"name": "output_item", "type": "Link", "target": "Item", "mandatory": True, "provenance": "SOURCE"},
                {"name": "output_batch", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "qty_received", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "process_loss_qty", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "wastage_qty", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "rework_qty", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "rejected_qty", "type": "Float", "default": 0.0, "provenance": "SOURCE"},
                {"name": "unaccounted_qty", "type": "Float", "default": 0.0, "provenance": "INFERRED"},
                {"name": "quality_status", "type": "Select", "default": "Pending Inspection", "provenance": "SOURCE"}
            ]
        },
        {
            "name": "Versa QC Parameter",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Inspection parameter definition, target values, tolerance limits, and test methods.",
            "runtime_owner": "Versa Quality",
            "table_name": "tabVersa QC Parameter",
            "doctype_type": "Child Table",
            "app": "versa_quality",
            "parent": "Versa QC Spec",
            "attributes": [
                {"name": "parameter_code", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "parameter_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "target_value", "type": "Data", "provenance": "SOURCE"},
                {"name": "lower_limit", "type": "Float", "provenance": "SOURCE"},
                {"name": "upper_limit", "type": "Float", "provenance": "SOURCE"},
                {"name": "uom", "type": "Link", "target": "UOM", "provenance": "SOURCE"},
                {"name": "test_method", "type": "Data", "provenance": "SOURCE"},
                {"name": "is_mandatory", "type": "Check", "default": 1, "provenance": "INFERRED"}
            ]
        },
        {
            "name": "Versa QC Measurement",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Actual recorded test reading and parameter pass/fail evaluation.",
            "runtime_owner": "Versa Quality",
            "table_name": "tabVersa QC Measurement",
            "doctype_type": "Child Table",
            "app": "versa_quality",
            "parent": "Versa QC Result",
            "attributes": [
                {"name": "parameter_code", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "reading_value", "type": "Float", "mandatory": True, "provenance": "SOURCE"},
                {"name": "status", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "remarks", "type": "Data", "provenance": "INFERRED"}
            ]
        },
        {
            "name": "Versa Carton Item",
            "classification": "VERSA_CHILD_TABLE",
            "company_authority": "DERIVED_COMPANY_CONTEXT",
            "provenance": "SOURCE",
            "business_purpose": "Garment style, colour, size, and pieces breakdown packed in a specific carton.",
            "runtime_owner": "Versa Export",
            "table_name": "tabVersa Carton Item",
            "doctype_type": "Child Table",
            "app": "versa_export",
            "parent": "Versa Carton",
            "attributes": [
                {"name": "style", "type": "Link", "target": "Versa Style", "mandatory": True, "provenance": "SOURCE"},
                {"name": "colour", "type": "Link", "target": "Versa Colour", "mandatory": True, "provenance": "SOURCE"},
                {"name": "size_code", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "qty", "type": "Int", "default": 0, "provenance": "SOURCE"}
            ]
        },

        # --- 5. Reference / Taxonomy DocTypes (2) ---
        {
            "name": "Versa Colour",
            "classification": "REFERENCE",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Controlled standard colour library for styles, fabric, and yarn.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Colour",
            "doctype_type": "Master",
            "app": "versa_textile",
            "natural_key": ["colour_code"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "colour_code", "type": "Data", "mandatory": True, "unique": True, "provenance": "SOURCE"},
                {"name": "colour_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "colour_family", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "pantone_ref", "type": "Data", "provenance": "INFERRED"}
            ]
        },
        {
            "name": "Versa Shade",
            "classification": "REFERENCE",
            "company_authority": "SHARED_MASTER",
            "provenance": "SOURCE",
            "business_purpose": "Production shade variations and lab dip approvals attached to colour codes.",
            "runtime_owner": "Versa Textile",
            "table_name": "tabVersa Shade",
            "doctype_type": "Master",
            "app": "versa_textile",
            "natural_key": ["colour", "shade_code"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "colour", "type": "Link", "target": "Versa Colour", "mandatory": True, "provenance": "SOURCE"},
                {"name": "shade_code", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "shade_name", "type": "Data", "mandatory": True, "provenance": "SOURCE"},
                {"name": "lab_dip_no", "type": "Data", "provenance": "INFERRED"}
            ]
        },

        # --- 6. Configuration DocType (1) ---
        {
            "name": "Versa Approval Rule",
            "classification": "CONFIGURATION",
            "company_authority": "CONFIGURATION",
            "provenance": "SOURCE",
            "business_purpose": "Multi-tier dynamic approval bands based on amount, business unit, and item group.",
            "runtime_owner": "Versa Core",
            "table_name": "tabVersa Approval Rule",
            "doctype_type": "Configuration",
            "app": "versa_core",
            "natural_key": ["document_type", "business_unit", "min_amount"],
            "lifecycle_states": ["Active", "Disabled"],
            "attributes": [
                {"name": "name", "type": "Data", "primary_key": True, "provenance": "SOURCE"},
                {"name": "document_type", "type": "Select", "mandatory": True, "provenance": "SOURCE"},
                {"name": "min_amount", "type": "Currency", "mandatory": True, "provenance": "SOURCE"},
                {"name": "max_amount", "type": "Currency", "provenance": "SOURCE"},
                {"name": "approver_role", "type": "Link", "target": "Role", "mandatory": True, "provenance": "SOURCE"},
                {"name": "business_unit", "type": "Link", "target": "Cost Center", "provenance": "INFERRED"},
                {"name": "is_active", "type": "Check", "default": 1, "provenance": "SOURCE"}
            ]
        }
    ],
    "relationships": [
        {"id": "REL-001", "source": "Cost Center", "target": "Company", "cardinality": "Many-to-One", "foreign_key": "company", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-002", "source": "Warehouse", "target": "Company", "cardinality": "Many-to-One", "foreign_key": "company", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-003", "source": "Batch", "target": "Item", "cardinality": "Many-to-One", "foreign_key": "item", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-004", "source": "Sales Order", "target": "Customer", "cardinality": "Many-to-One", "foreign_key": "customer", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-005", "source": "Purchase Order", "target": "Supplier", "cardinality": "Many-to-One", "foreign_key": "supplier", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-006", "source": "Purchase Receipt", "target": "Supplier", "cardinality": "Many-to-One", "foreign_key": "supplier", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-007", "source": "Delivery Note", "target": "Customer", "cardinality": "Many-to-One", "foreign_key": "customer", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-008", "source": "Purchase Invoice", "target": "Supplier", "cardinality": "Many-to-One", "foreign_key": "supplier", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-009", "source": "Sales Invoice", "target": "Customer", "cardinality": "Many-to-One", "foreign_key": "customer", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-010", "source": "Stock Entry", "target": "Warehouse", "cardinality": "Many-to-One", "foreign_key": "to_warehouse", "type": "ERPNext Standard", "provenance": "SOURCE"},
        {"id": "REL-011", "source": "Versa Material Spec", "target": "Item", "cardinality": "Many-to-One", "foreign_key": "item", "type": "ERPNext Binding", "provenance": "SOURCE"},
        {"id": "REL-012", "source": "Versa Yarn Spec", "target": "Versa Material Spec", "cardinality": "One-to-One", "foreign_key": "material_spec", "type": "Domain Extension", "provenance": "SOURCE"},
        {"id": "REL-013", "source": "Versa Fabric Spec", "target": "Versa Material Spec", "cardinality": "One-to-One", "foreign_key": "material_spec", "type": "Domain Extension", "provenance": "SOURCE"},
        {"id": "REL-014", "source": "Versa Shade", "target": "Versa Colour", "cardinality": "Many-to-One", "foreign_key": "colour", "type": "Taxonomy", "provenance": "SOURCE"},
        {"id": "REL-015", "source": "Versa Fabric Roll", "target": "Item", "cardinality": "Many-to-One", "foreign_key": "item", "type": "Physical Inventory", "provenance": "SOURCE"},
        {"id": "REL-016", "source": "Versa Fabric Roll", "target": "Batch", "cardinality": "Many-to-One", "foreign_key": "batch", "type": "Traceability", "provenance": "SOURCE"},
        {"id": "REL-017", "source": "Versa Fabric Roll", "target": "Warehouse", "cardinality": "Many-to-One", "foreign_key": "warehouse", "type": "Location Linkage", "provenance": "SOURCE"},
        {"id": "REL-018", "source": "Versa Fabric Roll", "target": "Versa Shade", "cardinality": "Many-to-One", "foreign_key": "shade", "type": "Taxonomy Linkage", "provenance": "SOURCE"},
        {"id": "REL-019", "source": "Versa Style", "target": "Customer", "cardinality": "Many-to-One", "foreign_key": "buyer_customer", "type": "Commercial Linkage", "provenance": "SOURCE"},
        {"id": "REL-020", "source": "Versa Style", "target": "Item", "cardinality": "Many-to-One", "foreign_key": "base_fabric_item", "type": "Engineering Linkage", "provenance": "SOURCE"},
        {"id": "REL-021", "source": "Versa Order Matrix", "target": "Sales Order", "cardinality": "Many-to-One", "foreign_key": "parent", "type": "Child Table", "provenance": "SOURCE"},
        {"id": "REL-022", "source": "Versa Order Matrix", "target": "Versa Style", "cardinality": "Many-to-One", "foreign_key": "style", "type": "Domain Reference", "provenance": "SOURCE"},
        {"id": "REL-023", "source": "Versa Job Worker", "target": "Supplier", "cardinality": "One-to-One", "foreign_key": "supplier", "type": "Master Extension", "provenance": "SOURCE"},
        {"id": "REL-024", "source": "Versa Job Work Order", "target": "Supplier", "cardinality": "Many-to-One", "foreign_key": "job_worker", "type": "Subcontracting", "provenance": "SOURCE"},
        {"id": "REL-025", "source": "Versa QC Result", "target": "Versa QC Spec", "cardinality": "Many-to-One", "foreign_key": "qc_spec", "type": "Quality Standard", "provenance": "SOURCE"},
        {"id": "REL-026", "source": "Versa QC Result", "target": "Item", "cardinality": "Many-to-One", "foreign_key": "item", "type": "Quality Inspection Target", "provenance": "SOURCE"},
        {"id": "REL-027", "source": "Versa Packing Plan", "target": "Sales Order", "cardinality": "Many-to-One", "foreign_key": "sales_order", "type": "Commercial Fulfillment", "provenance": "SOURCE"},
        {"id": "REL-028", "source": "Versa Carton", "target": "Versa Packing Plan", "cardinality": "Many-to-One", "foreign_key": "packing_plan", "type": "Logistics Packing", "provenance": "SOURCE"}
    ],
    "invariants": {
        # --- 1. Canonical Invariants (6) ---
        "job_work_mass_balance": {
            "name": "Job Work Mass Balance Conservation",
            "classification": "CANONICAL_INVARIANT",
            "owner": "versa_jobwork",
            "formula": "Issued_Weight == Converted_Output_Weight + Process_Loss + Scrap + Returned_Unprocessed + Unaccounted_Weight",
            "tolerance": "Configurable per process in Versa Process Loss Tolerance Setting (Default <= 0.1% scale calibration limit)",
            "provenance": "SOURCE",
            "enforcement": "Hard block on Job Work Order closure if unaccounted loss exceeds configured tolerance"
        },
        "order_matrix_conservation": {
            "name": "Order Matrix Line Item Quantity Conservation",
            "classification": "CANONICAL_INVARIANT",
            "owner": "versa_textile",
            "formula": "For each (Sales_Order, Style, Colour, Shade, Size, UOM): Sum(OrderMatrix.ordered_qty) == Sum(SalesOrderItem.qty)",
            "scope": "Exact tuple identity: (Sales Order, Style, Colour, Shade, Size, UOM)",
            "provenance": "SOURCE",
            "enforcement": "Server-side before_save hook validation on Sales Order"
        },
        "carton_packing_conservation": {
            "name": "Carton Packing Piece Conservation",
            "classification": "CANONICAL_INVARIANT",
            "owner": "versa_export",
            "formula": "Sum(CartonItem.qty for (c, s)) == Packed_Qty(c, s) <= Ordered_Qty(c, s) * (1 + Shipment_Over_Tolerance_Pct)",
            "scope": "Per Style, Colour, Size across all Cartons in Packing Plan",
            "provenance": "SOURCE",
            "enforcement": "Validation hook on Versa Packing Plan submit"
        },
        "fabric_roll_dual_uom_conservation": {
            "name": "Fabric Roll Dual-UOM Mass Conservation",
            "classification": "CANONICAL_INVARIANT",
            "owner": "versa_textile",
            "formula": "Weight_kg == (Length_m * Width_m * GSM) / 1000 +/- GSM_Tolerance_Pct",
            "scope": "Per Fabric Roll physical inspection and receipt",
            "sampling_protocol": "DEFERRED / OPEN (Lab sampling locations and relaxed width methods deferred to Phase 0 discovery)",
            "provenance": "INFERRED",
            "enforcement": "Validates roll physical consistency on Purchase Receipt and In-house Knitting GRN"
        },
        "quality_gate_enforcement": {
            "name": "Quality Gate Quarantine Issuance Block",
            "classification": "CANONICAL_INVARIANT",
            "owner": "versa_quality",
            "rule": "Stock entities marked Quarantine or Rejected cannot be issued to Production Cutting or Shipped without formal QA Head Concession override",
            "provenance": "SOURCE",
            "enforcement": "Server-side before_submit hook on Stock Entry and Delivery Note"
        },
        "multi_company_isolation": {
            "name": "Multi-Company Data Segregation Invariant",
            "classification": "CANONICAL_INVARIANT",
            "owner": "versa_core",
            "rule": "Every transactional document and company-owned master must carry a mandatory non-null Company foreign key",
            "provenance": "SOURCE",
            "enforcement": "Frappe permission_query_conditions and validate hook"
        },

        # --- 2. Business Rules (3) ---
        "job_work_excess_loss_penalty": {
            "name": "Job Work Excess Loss Financial Penalty",
            "classification": "BUSINESS_RULE",
            "owner": "versa_jobwork",
            "formula": "Excess_Loss = max(0, Actual_Loss - (Issued_Qty * Allowed_Loss_Pct)); Debit_Amount = Excess_Loss * Material_Cost_Per_Kg",
            "provenance": "SOURCE",
            "enforcement": "Automated debit note generation against Job Worker settlement Purchase Invoice"
        },
        "three_way_matching": {
            "name": "Procurement 3-Way Matching Rule",
            "classification": "BUSINESS_RULE",
            "owner": "erpnext",
            "formula": "Invoice_Qty <= Accepted_Receipt_Qty and Invoice_Rate <= PO_Rate * (1 + Price_Tolerance_Pct)",
            "provenance": "SOURCE",
            "enforcement": "Standard ERPNext purchase invoice submission check"
        },
        "dispatch_invoice_reconciliation": {
            "name": "Delivery to Cumulative Invoice Reconciliation Rule",
            "classification": "BUSINESS_RULE",
            "owner": "erpnext",
            "formula": "Cumulative_Invoiced_Qty <= Accepted_Delivered_Qty - Returned_Qty; Total_Invoiced_Amount == Delivered_Net_Value +/- Adjustments",
            "scope": "Permits partial invoicing, multi-invoice schedules, and debit/credit note adjustments",
            "provenance": "SOURCE",
            "enforcement": "Standard ERPNext sales billing and revenue recognition validation"
        },

        # --- 3. Workflow Rules (2) ---
        "production_cutting_allowance": {
            "name": "Production Cutting Allowance Allocation",
            "classification": "WORKFLOW_RULE",
            "owner": "versa_textile",
            "formula": "Cutting_Plan_Qty(c, s) = Ordered_Qty(c, s) * (1 + Cutting_Allowance_Pct)",
            "provenance": "INFERRED",
            "enforcement": "Auto-calculation in cutting batch generation"
        },
        "order_fulfillment_closure": {
            "name": "Order Fulfillment Closure Tolerance",
            "classification": "WORKFLOW_RULE",
            "owner": "versa_textile",
            "formula": "Delivered_Qty >= Ordered_Qty * (1 - Short_Shipment_Tolerance_Pct)",
            "provenance": "INFERRED",
            "enforcement": "Evaluates Sales Order completion status on final delivery"
        },

        # --- 4. Derived Metrics (2) ---
        "astm_d5430_4point_defect_scoring": {
            "name": "Fabric Defect 4-Point Density Calculation",
            "classification": "DERIVED_METRIC",
            "owner": "versa_quality",
            "formula": "Defect_Score = (Total_Defect_Points * 3600) / (Inspected_Length_yds * Cuttable_Width_inches)",
            "provenance": "INFERRED",
            "enforcement": "Auto-calculated on Versa Fabric Roll and QC Result submit"
        },
        "supplier_otif_scoring": {
            "name": "Supplier On-Time In-Full Metric",
            "classification": "DERIVED_METRIC",
            "owner": "versa_core",
            "formula": "OTIF_Score = (On_Time_In_Full_Receipts / Total_Receipts) * 100",
            "provenance": "SOURCE",
            "enforcement": "Calculated dynamically in supplier performance dashboard"
        }
    },
    "open_questions_reference": "versa_analysis/validation/VERSA_OPEN_QUESTIONS.md",
    "assumptions_reference": "versa_analysis/validation/VERSA_ASSUMPTION_REGISTER.md"
}

os.makedirs('versa_analysis/output', exist_ok=True)
with open('versa_analysis/output/versa_domain_model.json', 'w', encoding='utf-8') as f:
    json.dump(model, f, indent=2)

print('Wrote updated canonical JSON model (v1.3.0) to versa_analysis/output/versa_domain_model.json')
