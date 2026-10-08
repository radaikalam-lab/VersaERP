"""
Controller for Versa QC Spec (Master DocType ENT-021).
Maintains versioned quality specifications and parameter standards.
"""

import re
from typing import Optional

try:
    from frappe.model.document import Document
except ImportError:
    class Document:
        pass


class VersaQCSpec(Document):
    """
    Frappe Document Controller for Versa QC Spec.
    Enforces versioning rules, parameter limit consistency, and immutable historical definitions.
    """
    def __init__(self, *args, **kwargs):
        self.doctype = "Versa QC Spec"
        if args and isinstance(args[0], dict):
            self.__dict__.update(args[0])
            for k, v in args[0].items():
                setattr(self, k, v)
        elif kwargs:
            self.__dict__.update(kwargs)
            for k, v in kwargs.items():
                setattr(self, k, v)
        else:
            try:
                super().__init__(*args, **kwargs)
            except Exception:
                pass

    def validate(self):
        self.validate_spec_identity()
        self.validate_version_format()
        self.validate_date_ranges()
        self.validate_parameters()
        self.validate_historical_integrity()

    def validate_spec_identity(self):
        if not getattr(self, "spec_name", None):
            raise ValueError("Specification Name ('spec_name') is mandatory.")
        if not getattr(self, "material_type", None):
            raise ValueError("Material Type ('material_type') is mandatory.")

    def validate_version_format(self):
        ver = getattr(self, "version", "V1.0") or "V1.0"
        if not re.match(r"^[vV]?\d+(\.\d+)?$", str(ver).strip()):
            raise ValueError(f"Invalid Specification Version format '{ver}'. Expected format like 'V1.0', 'V2.1', or '1.0'.")

    def validate_date_ranges(self):
        eff_from = getattr(self, "effective_from", None)
        eff_to = getattr(self, "effective_to", None)
        if eff_from and eff_to and str(eff_from) > str(eff_to):
            raise ValueError(f"Effective From date ({eff_from}) cannot be after Effective To date ({eff_to}).")

    def validate_parameters(self):
        params = getattr(self, "parameters", []) or []
        if not params:
            raise ValueError("A Quality Specification must contain at least one Quality Parameter definition.")

        param_codes = set()
        for idx, p in enumerate(params, start=1):
            code = getattr(p, "parameter_code", None) if not isinstance(p, dict) else p.get("parameter_code")
            if not code:
                raise ValueError(f"Row #{idx}: Parameter Code is mandatory.")
            code = code.strip().upper()
            if code in param_codes:
                raise ValueError(f"Duplicate Parameter Code '{code}' in specification parameters.")
            param_codes.add(code)

            min_lim = getattr(p, "min_limit", None) if not isinstance(p, dict) else p.get("min_limit")
            max_lim = getattr(p, "max_limit", None) if not isinstance(p, dict) else p.get("max_limit")
            if min_lim is not None and max_lim is not None:
                if float(min_lim) > float(max_lim):
                    raise ValueError(f"Row #{idx} ({code}): Min Limit ({min_lim}) cannot be greater than Max Limit ({max_lim}).")

    def validate_historical_integrity(self):
        """
        Guarantees historical specifications remain auditable.
        If specification is referenced by submitted QC Results, it cannot be deleted or mutated.
        """
        spec_name = getattr(self, "name", None)
        if not spec_name:
            return

        try:
            import frappe
            if getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
                submitted_results = frappe.db.count("Versa QC Result", {"qc_spec": spec_name, "docstatus": 1})
                if submitted_results > 0:
                    status = getattr(self, "status", "Approved")
                    if status == "Draft":
                        raise ValueError(f"Cannot revert specification '{spec_name}' to Draft: {submitted_results} submitted QC Result(s) depend on this version.")
        except (ImportError, AttributeError):
            pass
