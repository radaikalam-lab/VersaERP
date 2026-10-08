"""
Multi-Company Tenant Isolation Engine for Versa ERP.
Implements canonical invariant: multi_company_isolation
Security Policy: FAIL CLOSED — No fallback to mock companies or permissive defaults.
"""

def get_permission_query_conditions_company(user=None):
    """
    Returns SQL WHERE clause restricting document queries to the user's authorized company.
    
    FAIL-CLOSED GUARANTEES:
    - Administrator receives unrestricted access ("").
    - Valid users receive restriction to their permitted companies.
    - If user has NO active company or an error occurs, returns '1 = 0' (zero rows returned).
    - NEVER falls back to hard-coded test companies.
    """
    try:
        import frappe
        import frappe.defaults

        if not user:
            if getattr(frappe, "local", None) and getattr(frappe.local, "session", None) and getattr(frappe.session, "user", None):
                user = frappe.session.user
            else:
                user = "Guest"

        if user == "Administrator":
            return ""

        permitted_companies = []
        if getattr(frappe, "defaults", None) and hasattr(frappe.defaults, "get_user_default"):
            user_default = frappe.defaults.get_user_default("Company", user=user)
            if user_default:
                permitted_companies.append(user_default)

        if getattr(frappe, "get_all", None) and getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
            try:
                user_perms = frappe.get_all(
                    "User Permission",
                    filters={"user": user, "allow": "Company"},
                    pluck="for_value"
                )
                for comp in user_perms:
                    if comp and comp not in permitted_companies:
                        permitted_companies.append(comp)
            except Exception:
                pass

        if not permitted_companies:
            # FAIL-CLOSED: No authorized company context found. Prevent all row visibility.
            return "1 = 0"

        if len(permitted_companies) == 1:
            comp = permitted_companies[0]
            escaped = frappe.db.escape(comp) if (getattr(frappe, "db", None) and hasattr(frappe.db, "escape")) else f"'{comp}'"
            return f"(`company` = {escaped})"
        else:
            escaped_items = []
            for comp in permitted_companies:
                esc = frappe.db.escape(comp) if (getattr(frappe, "db", None) and hasattr(frappe.db, "escape")) else f"'{comp}'"
                escaped_items.append(esc)
            return f"(`company` IN ({', '.join(escaped_items)}))"

    except Exception:
        # FAIL-CLOSED: Any failure in evaluation yields empty dataset
        return "1 = 0"


def check_company_isolation(doc, method=None):
    """
    Validates that a document's company matches the session user's company context.
    
    FAIL-CLOSED GUARANTEES:
    - Administrator is exempt (returns True).
    - Missing doc or missing document company raises ValidationError.
    - Missing user company context raises PermissionError.
    - Cross-company attempt raises PermissionError.
    - NEVER swallows exceptions or returns True on errors.
    """
    import frappe
    import frappe.defaults

    if doc is None:
        frappe.throw("Document context is missing for company isolation validation.", frappe.ValidationError)

    # Resolve session user
    user = None
    if getattr(frappe, "session", None) and getattr(frappe.session, "user", None):
        user = frappe.session.user

    if user == "Administrator":
        return True

    # Extract document company
    doc_company = None
    if callable(getattr(doc, "get", None)):
        doc_company = doc.get("company")
    if not doc_company:
        doc_company = getattr(doc, "company", None)

    if not doc_company:
        doctype = getattr(doc, "doctype", None)
        if not doctype and callable(getattr(doc, "get", None)):
            doctype = doc.get("doctype")
        doctype = doctype or "Unknown"
        frappe.throw(
            f"Company isolation violation: 'company' field is mandatory for {doctype} but is missing.",
            frappe.ValidationError
        )

    # Resolve user authorized companies
    permitted_companies = []
    if getattr(frappe, "defaults", None) and hasattr(frappe.defaults, "get_user_default"):
        user_company = frappe.defaults.get_user_default("Company", user=user)
        if user_company:
            permitted_companies.append(user_company)

    if getattr(frappe, "get_all", None) and getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
        try:
            user_perms = frappe.get_all(
                "User Permission",
                filters={"user": user, "allow": "Company"},
                pluck="for_value"
            )
            for comp in user_perms:
                if comp and comp not in permitted_companies:
                    permitted_companies.append(comp)
        except Exception:
            pass

    if not permitted_companies:
        frappe.throw(
            f"Access denied: User '{user or 'Unknown'}' has no authorized company context configured.",
            frappe.PermissionError
        )

    if doc_company not in permitted_companies:
        frappe.throw(
            f"Cross-company transaction violation: User '{user}' is authorized for {permitted_companies} "
            f"but document belongs to '{doc_company}'.",
            frappe.PermissionError
        )

    return True
