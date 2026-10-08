"""
Event handlers for Stock Entry in versa_quality.
"""

from versa_quality.gates import check_stock_entry_qc_gate


def validate_qc_status(doc, method=None):
    """
    Hooked before_submit on Stock Entry.
    """
    return check_stock_entry_qc_gate(doc, method)
