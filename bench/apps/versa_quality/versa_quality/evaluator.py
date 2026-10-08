"""
Versa Quality — Deterministic Evaluation Engine.
Provides reproducible statistical tolerance evaluations, multi-point reading
aggregations, ASTM D5430 4-point defect scoring, and disposition determinations.

Zero AI/ML, zero probabilistic heuristics, zero silent fallback approximations.
"""

from typing import List, Dict, Any, Optional, Tuple
import math


def calculate_readings_statistics(readings: List[float]) -> Dict[str, Optional[float]]:
    """
    Computes deterministic statistical metrics across multi-point readings.
    """
    if not readings:
        return {
            "count": 0,
            "mean": None,
            "min": None,
            "max": None,
            "std_dev": None
        }

    valid_readings = [float(r) for r in readings if r is not None and not math.isnan(float(r))]
    n = len(valid_readings)
    if n == 0:
        return {
            "count": 0,
            "mean": None,
            "min": None,
            "max": None,
            "std_dev": None
        }

    mean_val = sum(valid_readings) / n
    min_val = min(valid_readings)
    max_val = max(valid_readings)

    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in valid_readings) / (n - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0.0

    return {
        "count": n,
        "mean": round(mean_val, 4),
        "min": round(min_val, 4),
        "max": round(max_val, 4),
        "std_dev": round(std_dev, 4)
    }


def evaluate_parameter_measurement(
    parameter_code: str,
    severity: str,
    min_limit: Optional[float],
    max_limit: Optional[float],
    target_value: Optional[str],
    tolerance_type: str,
    readings: List[float]
) -> Dict[str, Any]:
    """
    Evaluates observed readings against parameter tolerance limits.
    Returns evaluation dictionary with deterministic status:
    - Pass
    - Fail
    - Inconclusive
    - Not Evaluated
    """
    stats = calculate_readings_statistics(readings)
    if stats["count"] == 0:
        return {
            "parameter_code": parameter_code,
            "severity": severity,
            "stats": stats,
            "status": "Inconclusive",
            "reason": "Missing measurement readings. Cannot determine quality conformance."
        }

    mean_val = stats["mean"]
    tol_type = tolerance_type or "Range"
    status = "Pass"
    reason = "Within acceptable specification limits."

    if tol_type == "Range":
        if min_limit is not None and mean_val < min_limit:
            status = "Fail"
            reason = f"Mean reading ({mean_val}) is below minimum limit ({min_limit})."
        elif max_limit is not None and mean_val > max_limit:
            status = "Fail"
            reason = f"Mean reading ({mean_val}) exceeds maximum limit ({max_limit})."

    elif tol_type == "Minimum":
        if min_limit is not None and mean_val < min_limit:
            status = "Fail"
            reason = f"Mean reading ({mean_val}) is below minimum threshold ({min_limit})."

    elif tol_type == "Maximum":
        if max_limit is not None and mean_val > max_limit:
            status = "Fail"
            reason = f"Mean reading ({mean_val}) exceeds maximum threshold ({max_limit})."

    elif tol_type == "Visual/Pass-Fail":
        # Any reading < 1.0 (0.0 = Fail, 1.0 = Pass) indicates failure
        if any(r < 0.5 for r in readings):
            status = "Fail"
            reason = "Visual or categorical inspection failed on one or more sample points."

    elif tol_type == "Exact":
        try:
            target_num = float(target_value)
            if any(abs(r - target_num) > 1e-5 for r in readings):
                status = "Fail"
                reason = f"Observed reading deviates from exact target value ({target_num})."
        except (ValueError, TypeError):
            # Target is string/categorical
            pass

    return {
        "parameter_code": parameter_code,
        "severity": severity,
        "stats": stats,
        "status": status,
        "reason": reason
    }


def calculate_4point_defect_score(
    total_defect_points: float,
    inspected_length_yds: float,
    cuttable_width_inches: float
) -> Tuple[Optional[float], str]:
    """
    Computes ASTM D5430 4-Point System fabric defect score:
    Points per 100 sq yds = (Total Defect Points * 3600) / (Inspected Length * Cuttable Width)

    Returns:
    - (score, grade)
    Grade A: Score <= 20.0 -> Accepted
    Grade B: 20.0 < Score <= 28.0 -> Concession
    Grade C: Score > 28.0 -> Rejected
    """
    if inspected_length_yds <= 0 or cuttable_width_inches <= 0:
        return None, "Inconclusive"

    score = (total_defect_points * 3600.0) / (inspected_length_yds * cuttable_width_inches)
    score = round(score, 2)

    if score <= 20.0:
        grade = "Grade A"
    elif score <= 28.0:
        grade = "Grade B"
    else:
        grade = "Grade C"

    return score, grade


def evaluate_overall_disposition(
    evaluated_measurements: List[Dict[str, Any]],
    defect_score: Optional[float] = None,
    concession_reason: Optional[str] = None,
    concession_approved_by: Optional[str] = None
) -> Dict[str, Any]:
    """
    Determines overall inspection disposition from evaluated measurements:
    - Accepted
    - Accepted with Concession
    - Quarantine
    - Rejected
    - Inconclusive
    """
    if not evaluated_measurements:
        return {
            "overall_status": "Inconclusive",
            "summary": "No evaluation parameters provided.",
            "critical_fails": 0,
            "major_fails": 0,
            "minor_fails": 0
        }

    critical_fails = []
    major_fails = []
    minor_fails = []
    inconclusives = []

    for m in evaluated_measurements:
        status = m.get("status")
        severity = m.get("severity")
        pcode = m.get("parameter_code", "Unknown")

        if status == "Inconclusive":
            inconclusives.append(pcode)
        elif status == "Fail":
            if severity == "Critical":
                critical_fails.append(pcode)
            elif severity == "Major":
                major_fails.append(pcode)
            else:
                minor_fails.append(pcode)

    if inconclusives:
        return {
            "overall_status": "Inconclusive",
            "summary": f"Inconclusive measurement data on parameters: {', '.join(inconclusives)}",
            "critical_fails": len(critical_fails),
            "major_fails": len(major_fails),
            "minor_fails": len(minor_fails)
        }

    has_concession_signoff = bool(concession_reason and concession_approved_by)

    # Defect score evaluation if present
    defect_rejected = False
    defect_concession = False
    if defect_score is not None:
        if defect_score > 28.0:
            defect_rejected = True
        elif defect_score > 20.0:
            defect_concession = True

    # Critical failures strictly reject unless QA Head concession is fully recorded
    if critical_fails:
        if has_concession_signoff:
            overall_status = "Accepted with Concession"
            summary = (f"Critical parameter deviations ({', '.join(critical_fails)}) accepted under "
                       f"authorized concession by {concession_approved_by}. Reason: {concession_reason}")
        else:
            overall_status = "Rejected"
            summary = f"Critical parameter specification failure on: {', '.join(critical_fails)}."

    elif major_fails or defect_rejected:
        if defect_rejected and not has_concession_signoff:
            overall_status = "Rejected"
            summary = f"4-Point fabric defect score ({defect_score}) exceeds rejection threshold (28.0)."
        elif has_concession_signoff:
            overall_status = "Accepted with Concession"
            summary = (f"Major deviations ({', '.join(major_fails) if major_fails else f'Defect Score {defect_score}'}) "
                       f"accepted under concession by {concession_approved_by}. Reason: {concession_reason}")
        else:
            overall_status = "Rejected"
            summary = f"Major specification failures without authorized concession: {', '.join(major_fails)}."

    elif minor_fails or defect_concession:
        if has_concession_signoff or defect_concession:
            overall_status = "Accepted with Concession"
            summary = f"Minor deviations or Grade B defect score accepted."
        else:
            overall_status = "Accepted"
            summary = f"Passed with non-critical minor advisory notes on: {', '.join(minor_fails)}."

    else:
        overall_status = "Accepted"
        summary = "All quality parameters within standard specification limits."

    return {
        "overall_status": overall_status,
        "summary": summary,
        "critical_fails": len(critical_fails),
        "major_fails": len(major_fails),
        "minor_fails": len(minor_fails)
    }
