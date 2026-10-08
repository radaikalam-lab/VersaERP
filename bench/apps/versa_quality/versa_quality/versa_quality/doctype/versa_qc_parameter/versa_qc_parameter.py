"""
Controller for Versa QC Parameter (Child Table DocType ENT-034).
Defines parameter limits, test methods, severity, and sampling requirements.
"""

try:
    from frappe.model.document import Document
except ImportError:
    class Document:
        pass


class VersaQCParameter(Document):
    def __init__(self, *args, **kwargs):
        self.doctype = "Versa QC Parameter"
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
