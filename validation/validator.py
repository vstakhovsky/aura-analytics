from typing import Dict, Any, List

REQUIRED_INSIGHT_FIELDS = {"id", "domain", "title", "summary", "confidence", "impact"}
REQUIRED_HYP_FIELDS = {"id", "title", "problem", "domain", "summary"}

def _missing_fields(item: Dict[str, Any], required: set) -> List[str]:
    return sorted([k for k in required if k not in item or item[k] in (None, "", [])])

def validate_report(report: Dict[str, Any]) -> Dict[str, Any]:
    score = {"checks": [], "passed": True}

    # 1) Structure presence
    for key in ["executive_summary", "insights", "hypotheses"]:
        ok = key in report and report[key] not in (None, "", [])
        score["checks"].append({"name": f"has_{key}", "ok": ok})
    # 2) Insights format
    for idx, ins in enumerate(report.get("insights", [])):
        miss = _missing_fields(ins, REQUIRED_INSIGHT_FIELDS)
        ok = len(miss) == 0
        score["checks"].append({"name": f"insight_{idx}_required", "ok": ok, "missing": miss})
    # 3) Hypotheses format
    for idx, hyp in enumerate(report.get("hypotheses", [])):
        miss = _missing_fields(hyp, REQUIRED_HYP_FIELDS)
        ok = len(miss) == 0
        score["checks"].append({"name": f"hypothesis_{idx}_required", "ok": ok, "missing": miss})

    score["passed"] = all(ch["ok"] for ch in score["checks"])
    return score
