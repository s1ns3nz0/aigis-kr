"""Compliance registry — dispatch by jurisdiction (jp / kr / all).

Aggregates per-jurisdiction compliance modules so that callers can request
a single combined view without each module having to know about the others.

Existing callers of ``aigis.compliance.get_compliance_summary()`` are
unaffected — that function continues to return the Japan-only view.
For multi-jurisdiction queries, use this module.

Usage:
    from aigis.compliance_registry import get_compliance_report, get_compliance_summary

    jp = get_compliance_report("jp")
    kr = get_compliance_report("kr")
    everything = get_compliance_report("all")

    summary = get_compliance_summary("kr")
    print(summary["coverage_rate"], summary["by_regulation"])
"""

from typing import Literal

Jurisdiction = Literal["jp", "kr", "all"]


def get_compliance_report(jurisdiction: Jurisdiction = "all") -> list[dict]:
    """Return compliance items for the requested jurisdiction.

    "jp"  → Japan (AI事業者ガイドライン, APPI, ...)
    "kr"  → Korea (PIPA, 신용정보법, 금융위 AI, ISMS-P, ...)
    "all" → Both, concatenated (jp first, then kr).
    """
    if jurisdiction == "jp":
        from aigis.compliance import get_compliance_report as _jp

        return _jp()
    if jurisdiction == "kr":
        from aigis.compliance_kr import get_compliance_report as _kr

        return _kr()
    if jurisdiction == "all":
        from aigis.compliance import get_compliance_report as _jp
        from aigis.compliance_kr import get_compliance_report as _kr

        return [*_jp(), *_kr()]
    raise ValueError(f"unknown jurisdiction: {jurisdiction!r} (expected 'jp', 'kr', or 'all')")


def get_compliance_summary(jurisdiction: Jurisdiction = "all") -> dict:
    """Return a coverage summary for the requested jurisdiction.

    For "all", coverage_rate is recomputed across the combined item set —
    not an average of the per-jurisdiction rates.
    """
    if jurisdiction == "jp":
        from aigis.compliance import get_compliance_summary as _jp

        return _jp()
    if jurisdiction == "kr":
        from aigis.compliance_kr import get_compliance_summary as _kr

        return _kr()
    if jurisdiction == "all":
        items = get_compliance_report("all")
        return _summarize(items)
    raise ValueError(f"unknown jurisdiction: {jurisdiction!r} (expected 'jp', 'kr', or 'all')")


def list_jurisdictions() -> list[str]:
    """Return the list of supported jurisdiction codes (excludes 'all')."""
    return ["jp", "kr"]


def _summarize(items: list[dict]) -> dict:
    total = len(items)
    covered = sum(1 for i in items if i["status"] == "covered")
    partial = sum(1 for i in items if i["status"] == "partial")
    not_covered = sum(1 for i in items if i["status"] == "not_covered")
    user_resp = sum(1 for i in items if i["status"] == "user_responsibility")

    groups: dict[str, dict] = {}
    for item in items:
        reg = item["regulation"]
        if reg not in groups:
            groups[reg] = {"total": 0, "covered": 0, "partial": 0, "not_covered": 0}
        groups[reg]["total"] += 1
        if item["status"] in ("covered", "partial", "not_covered"):
            groups[reg][item["status"]] += 1

    return {
        "total_requirements": total,
        "covered": covered,
        "partial": partial,
        "not_covered": not_covered,
        "user_responsibility": user_resp,
        "coverage_rate": round(((covered + partial * 0.5) / total) * 100, 1) if total else 0,
        "by_regulation": groups,
    }
