"""
Event handlers for Purchase Receipt in versa_quality.
"""

from versa_quality.gates import check_purchase_receipt_qc_gate


def check_qc_conformance(doc, method=None):
    """
    Hooked before_submit on Purchase Receipt.
    """
    return check_purchase_receipt_qc_gate(doc, method)
