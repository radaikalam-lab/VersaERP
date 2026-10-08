"""
Controller for Versa Approval Rule (Configuration DocType ENT-039).
"""

try:
    from frappe.model.document import Document
except ImportError:
    class Document:
        pass


class VersaApprovalRule(Document):
    """
    Frappe Document Controller for Versa Approval Rule.
    Validates amount ranges and non-overlapping active threshold configurations.
    """
    def __init__(self, *args, **kwargs):
        self.doctype = "Versa Approval Rule"
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
        self.validate_amount_range()
        self.validate_no_overlap()

    def validate_amount_range(self):
        min_amt = getattr(self, "min_amount", 0.0) or 0.0
        if min_amt < 0.0:
            raise ValueError(f"Minimum amount ({min_amt}) cannot be negative.")
        max_amt = getattr(self, "max_amount", None)
        if max_amt is not None and max_amt > 0.0 and max_amt < min_amt:
            raise ValueError(f"Maximum amount ({max_amt}) cannot be less than Minimum amount ({min_amt}).")

    def validate_no_overlap(self, existing_rules=None):
        """
        Validates that active approval rules for the same (document_type, company, business_unit)
        do not have overlapping amount ranges.
        """
        is_active = getattr(self, "is_active", 1)
        if not is_active:
            return

        doc_type = getattr(self, "document_type", None)
        if not doc_type:
            return

        rule_company = getattr(self, "company", None)
        rule_bu = getattr(self, "business_unit", None)
        rule_name = getattr(self, "name", None)

        self_min = getattr(self, "min_amount", 0.0) or 0.0
        self_max = getattr(self, "max_amount", None)
        if self_max == 0.0:
            self_max = None

        if existing_rules is None:
            try:
                import frappe
                if getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
                    filters = {
                        "document_type": doc_type,
                        "is_active": 1,
                    }
                    if rule_name:
                        filters["name"] = ["!=", rule_name]
                    if rule_company:
                        filters["company"] = rule_company
                    if rule_bu:
                        filters["business_unit"] = rule_bu

                    existing_rules = frappe.get_all(
                        "Versa Approval Rule",
                        filters=filters,
                        fields=["name", "document_type", "company", "business_unit", "min_amount", "max_amount", "is_active"]
                    )
            except Exception:
                existing_rules = []

        if existing_rules:
            for rule in existing_rules:
                if isinstance(rule, dict):
                    r_name = rule.get("name")
                    r_dt = rule.get("document_type")
                    r_comp = rule.get("company")
                    r_bu = rule.get("business_unit")
                    r_active = rule.get("is_active", 1)
                    r_min = rule.get("min_amount", 0.0) or 0.0
                    r_max = rule.get("max_amount", None)
                else:
                    r_name = getattr(rule, "name", None)
                    r_dt = getattr(rule, "document_type", None)
                    r_comp = getattr(rule, "company", None)
                    r_bu = getattr(rule, "business_unit", None)
                    r_active = getattr(rule, "is_active", 1)
                    r_min = getattr(rule, "min_amount", 0.0) or 0.0
                    r_max = getattr(rule, "max_amount", None)

                if rule_name and r_name == rule_name:
                    continue
                if not r_active:
                    continue
                if r_dt != doc_type:
                    continue
                if r_comp != rule_company:
                    continue
                if r_bu != rule_bu:
                    continue

                if r_max == 0.0:
                    r_max = None

                # Range overlap check between [self_min, self_max] and [r_min, r_max]
                overlap = True
                if self_max is not None and self_max <= r_min:
                    overlap = False
                if r_max is not None and r_max <= self_min:
                    overlap = False

                if overlap:
                    msg = (f"Approval rule conflict: Range [{self_min}, {self_max if self_max is not None else 'open'}] "
                           f"overlaps with existing rule '{r_name or 'unnamed'}' [{r_min}, {r_max if r_max is not None else 'open'}].")
                    try:
                        import frappe
                        if hasattr(frappe, "throw"):
                            frappe.throw(msg, frappe.ValidationError)
                    except (ImportError, AttributeError):
                        pass
                    raise ValueError(msg)
