"""
Versa Quality — Multi-Company Isolation & Permission Enforcement.
Implements fail-closed company query conditions and document permissions.
"""

from typing import Optional, Any


def get_user_active_company(user: Optional[str] = None) -> Optional[str]:
    """
    Resolves the active Company for the current session user.
    """
    try:
        import frappe
        if not user:
            user = getattr(frappe.session, "user", None)
        if not user or user == "Administrator":
            return None
        return frappe.defaults.get_user_default("Company", user=user) or frappe.db.get_value("User Permission", {"user": user, "allow": "Company"}, "for_value")
    except Exception:
        return None


def get_permission_query_conditions_quality_result(user: Optional[str] = None) -> str:
    """
    Generates SQL WHERE clause to enforce company isolation on Versa QC Result.
    Fails closed (1 = 0) if user lacks an active company context.
    """
    try:
        import frappe
        if not user:
            user = getattr(frappe.session, "user", None)
        if user == "Administrator":
            return ""
    except Exception:
        pass

    company = get_user_active_company(user)
    if not company:
        # Fail-closed security standard
        return "1 = 0"

    import sqlparse
    safe_company = company.replace("'", "''")
    return f"(`tabVersa QC Result`.`company` = '{safe_company}')"


def get_permission_query_conditions_quality_spec(user: Optional[str] = None) -> str:
    """
    Generates SQL WHERE clause for Versa QC Spec (Shared Masters or Company-scoped Specs).
    """
    try:
        import frappe
        if not user:
            user = getattr(frappe.session, "user", None)
        if user == "Administrator":
            return ""
    except Exception:
        pass

    company = get_user_active_company(user)
    if company:
        safe_company = company.replace("'", "''")
        return f"(`tabVersa QC Spec`.`company` = '{safe_company}' OR `tabVersa QC Spec`.`company` IS NULL OR `tabVersa QC Spec`.`company` = '')"
    else:
        # Only global specs accessible if no active company context
        return "(`tabVersa QC Spec`.`company` IS NULL OR `tabVersa QC Spec`.`company` = '')"


def check_quality_company_isolation(doc: Any, method: Optional[str] = None) -> bool:
    """
    Validates document company boundary against session user context.
    Raises PermissionError on cross-company violation.
    """
    if not doc:
        raise ValueError("Document cannot be None for company isolation verification.")

    doc_company = getattr(doc, "company", None)
    if not doc_company:
        # QC Spec may be global shared master (company is optional)
        if getattr(doc, "doctype", None) == "Versa QC Spec":
            return True
        raise ValueError(f"Document '{getattr(doc, 'name', 'Draft')}' missing mandatory 'company' field.")

    try:
        import frappe
        session_user = getattr(frappe.session, "user", None)
        if session_user == "Administrator":
            return True
    except Exception:
        session_user = None

    user_company = get_user_active_company(session_user)
    if not user_company:
        msg = f"Access Denied: User '{session_user or 'Anonymous'}' has no active Company context configured."
        try:
            import frappe
            if getattr(frappe, "local", None) and getattr(frappe.local, "flags", None):
                frappe.throw(msg, getattr(frappe, "PermissionError", PermissionError))
        except Exception:
            pass
        raise PermissionError(msg)

    if doc_company != user_company:
        msg = (f"Cross-Company Violation: User company '{user_company}' cannot modify or access "
               f"record belonging to '{doc_company}'.")
        try:
            import frappe
            if getattr(frappe, "local", None) and getattr(frappe.local, "flags", None):
                frappe.throw(msg, getattr(frappe, "PermissionError", PermissionError))
        except Exception:
            pass
        raise PermissionError(msg)

    return True

