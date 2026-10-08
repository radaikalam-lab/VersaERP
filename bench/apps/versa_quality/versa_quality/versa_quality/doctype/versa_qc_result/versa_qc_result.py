"""
Controller for Versa QC Result (Transaction DocType ENT-024).
Orchestrates lab inspection recordings, multi-point reading evaluations,
4-point defect scoring, disposition logic, and quality gates.
"""

from typing import List, Dict, Any, Optional
from versa_quality.evaluator import (
    evaluate_parameter_measurement,
    calculate_4point_defect_score,
    evaluate_overall_disposition
)
from versa_quality.permissions import check_quality_company_isolation

try:
    from frappe.model.document import Document
except ImportError:
    class Document:
        pass


class VersaQCResult(Document):
    """
    Frappe Document Controller for Versa QC Result.
    Submittable transaction providing deterministic evaluation and quality gate evidence.
    """
    def __init__(self, *args, **kwargs):
        self.doctype = "Versa QC Result"
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
        self.validate_mandatory_headers()
        self.validate_company_boundary()
        self.resolve_and_lock_spec()
        self.evaluate_measurements_and_disposition()
        self.validate_concession_signoff()

    def validate_mandatory_headers(self):
        if not getattr(self, "company", None):
            raise ValueError("Company is mandatory for Versa QC Result.")
        if not getattr(self, "qc_spec", None):
            raise ValueError("Quality Specification ('qc_spec') is mandatory.")
        if not getattr(self, "inspection_type", None):
            raise ValueError("Inspection Type ('inspection_type') is mandatory.")
        if not getattr(self, "source_doctype", None):
            raise ValueError("Source DocType is mandatory.")
        if not getattr(self, "source_name", None):
            raise ValueError("Source Name is mandatory.")
        if not getattr(self, "item", None):
            raise ValueError("Item is mandatory.")
        if not getattr(self, "inspected_by", None):
            raise ValueError("Inspected By ('inspected_by') is mandatory.")
        if not getattr(self, "inspection_date", None):
            raise ValueError("Inspection Date is mandatory.")

    def validate_company_boundary(self):
        check_quality_company_isolation(self)

    def resolve_and_lock_spec(self):
        """
        Retrieves specification parameters and locks historical spec_version.
        """
        spec_name = getattr(self, "qc_spec", None)
        if not spec_name:
            return

        try:
            import frappe
            if getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
                spec_doc = frappe.get_doc("Versa QC Spec", spec_name)
                if spec_doc:
                    if not getattr(self, "spec_version", None):
                        self.spec_version = spec_doc.version

                    # If measurements are empty, populate from spec parameters
                    current_measurements = getattr(self, "measurements", []) or []
                    if not current_measurements and getattr(spec_doc, "parameters", None):
                        for p in spec_doc.parameters:
                            self.append("measurements", {
                                "parameter_code": p.parameter_code,
                                "parameter_name": p.parameter_name,
                                "test_method": p.test_method,
                                "severity": p.severity,
                                "target_value": p.target_value,
                                "min_limit": p.min_limit,
                                "max_limit": p.max_limit,
                                "reading_status": "Not Evaluated"
                            })
        except (ImportError, AttributeError):
            pass

    def evaluate_measurements_and_disposition(self):
        """
        Executes deterministic evaluation across all measurement parameters and multi-point readings.
        """
        measurements = getattr(self, "measurements", []) or []
        readings_list = getattr(self, "readings", []) or []

        # Map readings by parameter_code
        readings_by_param: Dict[str, List[float]] = {}
        for r in readings_list:
            pcode = getattr(r, "parameter_code", None) if not isinstance(r, dict) else r.get("parameter_code")
            rval = getattr(r, "reading_value", None) if not isinstance(r, dict) else r.get("reading_value")
            if pcode and rval is not None:
                pcode_upper = str(pcode).strip().upper()
                if pcode_upper not in readings_by_param:
                    readings_by_param[pcode_upper] = []
                readings_by_param[pcode_upper].append(float(rval))

        evaluated_measurements = []
        for m in measurements:
            if isinstance(m, dict):
                pcode = m.get("parameter_code")
                severity = m.get("severity", "Critical")
                min_lim = m.get("min_limit")
                max_lim = m.get("max_limit")
                target = m.get("target_value")
                tol_type = m.get("tolerance_type", "Range")
            else:
                pcode = getattr(m, "parameter_code", None)
                severity = getattr(m, "severity", "Critical")
                min_lim = getattr(m, "min_limit", None)
                max_lim = getattr(m, "max_limit", None)
                target = getattr(m, "target_value", None)
                tol_type = getattr(m, "tolerance_type", "Range")

            if not pcode:
                continue

            pcode_upper = str(pcode).strip().upper()
            observed_readings = readings_by_param.get(pcode_upper, [])

            eval_res = evaluate_parameter_measurement(
                parameter_code=pcode_upper,
                severity=severity,
                min_limit=float(min_lim) if min_lim is not None else None,
                max_limit=float(max_lim) if max_lim is not None else None,
                target_value=str(target) if target is not None else None,
                tolerance_type=tol_type,
                readings=observed_readings
            )
            evaluated_measurements.append(eval_res)

            # Update measurement row in place
            stats = eval_res["stats"]
            if isinstance(m, dict):
                m["reading_count"] = stats["count"]
                m["mean_reading"] = stats["mean"]
                m["min_reading"] = stats["min"]
                m["max_reading"] = stats["max"]
                m["std_dev_reading"] = stats["std_dev"]
                m["reading_status"] = eval_res["status"]
                m["remarks"] = eval_res["reason"]
            else:
                setattr(m, "reading_count", stats["count"])
                setattr(m, "mean_reading", stats["mean"])
                setattr(m, "min_reading", stats["min"])
                setattr(m, "max_reading", stats["max"])
                setattr(m, "std_dev_reading", stats["std_dev"])
                setattr(m, "reading_status", eval_res["status"])
                setattr(m, "remarks", eval_res["reason"])

        # Defect scoring
        defect_score = None
        tot_defects = getattr(self, "total_defect_points", None)
        length_yds = getattr(self, "inspected_length_yds", None)
        width_in = getattr(self, "cuttable_width_inches", None)
        if tot_defects is not None and length_yds and width_in and float(length_yds) > 0 and float(width_in) > 0:
            defect_score, _ = calculate_4point_defect_score(float(tot_defects), float(length_yds), float(width_in))
            self.defect_score_4point = defect_score

        # Disposition determination
        disp = evaluate_overall_disposition(
            evaluated_measurements=evaluated_measurements,
            defect_score=defect_score,
            concession_reason=getattr(self, "concession_reason", None),
            concession_approved_by=getattr(self, "concession_approved_by", None)
        )

        self.overall_status = disp["overall_status"]
        self.evaluation_summary = disp["summary"]

    def validate_concession_signoff(self):
        status = getattr(self, "overall_status", None)
        if status == "Accepted with Concession":
            reason = getattr(self, "concession_reason", None)
            approver = getattr(self, "concession_approved_by", None)
            if not reason or not str(reason).strip():
                raise ValueError("Concession Reason ('concession_reason') is mandatory when overall status is 'Accepted with Concession'.")
            if not approver or not str(approver).strip():
                raise ValueError("Concession Approved By ('concession_approved_by') is mandatory when overall status is 'Accepted with Concession'.")

    def on_submit(self):
        status = getattr(self, "overall_status", None)
        if status in ("Inconclusive", "Quarantine"):
            msg = f"Cannot submit Versa QC Result in '{status}' status. Complete all required measurements first."
            try:
                import frappe
                if getattr(frappe, "local", None) and getattr(frappe.local, "flags", None):
                    frappe.throw(msg, getattr(frappe, "ValidationError", ValueError))
            except Exception:
                pass
            raise ValueError(msg)

        # Sync status to linked source document if applicable
        source_dt = getattr(self, "source_doctype", None)
        source_name = getattr(self, "source_name", None)
        if source_dt and source_name:
            try:
                import frappe
                if getattr(frappe, "local", None) and getattr(frappe.local, "db", None) and frappe.db:
                    if source_dt == "Purchase Receipt" and frappe.db.exists("Purchase Receipt", source_name):
                        qc_stat = "QC Passed" if status == "Accepted" else status
                        frappe.db.set_value("Purchase Receipt", source_name, {
                            "versa_qc_status": qc_stat,
                            "versa_qc_result": self.name
                        })
            except (ImportError, AttributeError):
                pass
