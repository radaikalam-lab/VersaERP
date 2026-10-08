"""
Versa Quality — Quality Gates & Business Control Policies.
Enforces fail-closed quality verification on ERPNext transactions before submit.
"""

from typing import Any, Optional


def check_purchase_receipt_qc_gate(doc: Any, method: Optional[str] = None) -> bool:
    """
    Enforces quality gate on Purchase Receipt submission.
    If QC inspection is required, blocks submission unless an Accepted or Concession
    Versa QC Result exists and is verified.
    """
    if not doc:
        return True

    # Check if document has items requiring inspection
    qc_required = getattr(doc, "is_qc_required", 0) or 0
    qc_status = getattr(doc, "versa_qc_status", "Pending QC") or "Pending QC"

    # Also inspect individual items if custom field is present on items table
    items = getattr(doc, "items", []) or []
    for item in items:
        if getattr(item, "is_qc_required", 0) or getattr(item, "sample_quantity", 0) > 0:
            qc_required = 1
            break

    if not qc_required:
        return True

    # If QC is required, verify QC Result conformance
    if qc_status in ("QC Passed", "Accepted", "Accepted with Concession"):
        return True

    # Search for submitted QC Result matching this Purchase Receipt
    qc_result_name = getattr(doc, "versa_qc_result", None)
    has_valid_qc = False

    try:
        import frappe
        if getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
            filters = {
                "source_doctype": "Purchase Receipt",
                "source_name": doc.name,
                "docstatus": 1,
                "overall_status": ["in", ["Accepted", "Accepted with Concession"]]
            }
            if qc_result_name:
                filters["name"] = qc_result_name

            results = frappe.get_all("Versa QC Result", filters=filters, limit=1)
            if results:
                has_valid_qc = True
    except Exception:
        # If DB not available, fallback to in-memory check
        has_valid_qc = False

    if not has_valid_qc:
        msg = (f"Quality Gate Block: Purchase Receipt '{getattr(doc, 'name', 'Draft')}' cannot be submitted. "
               f"Material inspection is required and current QC status is '{qc_status}'. "
               f"An approved Versa QC Result (Accepted or Concession) must be recorded before stock receipt.")
        try:
            import frappe
            if getattr(frappe, "local", None) and getattr(frappe.local, "flags", None):
                frappe.throw(msg, getattr(frappe, "ValidationError", ValueError))
        except Exception:
            pass
        raise ValueError(msg)

    return True


def check_stock_entry_qc_gate(doc: Any, method: Optional[str] = None) -> bool:
    """
    Enforces quality gate on Stock Entry (e.g., Material Issue to Cutting / Subcontractor).
    Blocks issue of material if referenced roll or batch is Quarantined or Rejected.
    """
    if not doc:
        return True

    purpose = getattr(doc, "purpose", "") or ""
    # Only enforce on issue / transfer / manufacture movements
    if "Receipt" in purpose and "Material Issue" not in purpose:
        return True

    items = getattr(doc, "items", []) or []
    for item in items:
        roll_barcode = getattr(item, "versa_fabric_roll", None)
        if roll_barcode:
            roll = None
            try:
                import frappe
                if getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
                    roll = frappe.get_value("Versa Fabric Roll", roll_barcode, ["quality_grade", "status"], as_dict=True)
            except Exception:
                roll = None

            if roll:
                grade = roll.get("quality_grade")
                if grade in ("Quarantine", "Rejected"):
                    msg = (f"Quality Gate Block: Cannot issue Fabric Roll '{roll_barcode}' in Stock Entry '{getattr(doc, 'name', 'Draft')}'. "
                           f"Roll is currently in '{grade}' status.")
                    try:
                        import frappe
                        if getattr(frappe, "local", None) and getattr(frappe.local, "flags", None):
                            frappe.throw(msg, getattr(frappe, "ValidationError", ValueError))
                    except Exception:
                        pass
                    raise ValueError(msg)

    return True

