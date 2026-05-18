"""Tests for the Korean compliance module and the cross-jurisdiction registry."""

import json

import pytest

from aigis.compliance import ComplianceItem
from aigis.compliance_kr import (
    _build_kr_compliance_items,
    get_compliance_report,
    get_compliance_summary,
)
from aigis.compliance_registry import (
    Jurisdiction,
    get_compliance_report as registry_report,
    get_compliance_summary as registry_summary,
    list_jurisdictions,
)

EXPECTED_REGULATIONS = {
    "개인정보보호법 (PIPA)",
    "신용정보법",
    "정보통신망법",
    "금융분야 AI 가이드라인 (금융위)",
    "전자금융감독규정",
    "ISMS-P 인증기준",
}

VALID_STATUSES = {"covered", "partial", "not_covered", "user_responsibility"}


class TestKoreanComplianceItems:
    def test_all_items_are_compliance_item_instances(self):
        for item in _build_kr_compliance_items():
            assert isinstance(item, ComplianceItem)

    def test_all_required_regulations_present(self):
        regulations = {item.regulation for item in _build_kr_compliance_items()}
        assert EXPECTED_REGULATIONS.issubset(regulations), (
            f"missing regulations: {EXPECTED_REGULATIONS - regulations}"
        )

    def test_each_regulation_has_minimum_five_items(self):
        items = _build_kr_compliance_items()
        for reg in EXPECTED_REGULATIONS:
            count = sum(1 for i in items if i.regulation == reg)
            assert count >= 5, f"{reg} has only {count} items, expected ≥ 5"

    def test_requirement_ids_are_unique(self):
        ids = [item.requirement_id for item in _build_kr_compliance_items()]
        assert len(ids) == len(set(ids)), "duplicate requirement_id in Korean items"

    def test_statuses_are_valid(self):
        for item in _build_kr_compliance_items():
            assert item.status in VALID_STATUSES, (
                f"{item.requirement_id} has invalid status {item.status!r}"
            )

    def test_required_id_prefixes(self):
        """Each regulation uses its own ID prefix so IDs are self-describing."""
        prefix_map = {
            "PIPA-PII-": "개인정보보호법 (PIPA)",
            "CRED-": "신용정보법",
            "ITNA-": "정보통신망법",
            "FSC-AI-": "금융분야 AI 가이드라인 (금융위)",
            "EFR-": "전자금융감독규정",
            "ISMS-P-": "ISMS-P 인증기준",
        }
        for item in _build_kr_compliance_items():
            for prefix, expected_reg in prefix_map.items():
                if item.requirement_id.startswith(prefix):
                    assert item.regulation == expected_reg, (
                        f"{item.requirement_id} has prefix {prefix} but regulation "
                        f"{item.regulation!r}, expected {expected_reg!r}"
                    )
                    break


class TestKoreanComplianceReport:
    def test_report_shape(self):
        report = get_compliance_report()
        assert isinstance(report, list)
        assert len(report) >= 50
        for entry in report:
            assert {
                "regulation",
                "requirement_id",
                "requirement",
                "description",
                "aigis_feature",
                "status",
                "notes",
            }.issubset(entry.keys())

    def test_report_json_serializable(self):
        report = get_compliance_report()
        json.dumps(report, ensure_ascii=False)  # must not raise


class TestKoreanComplianceSummary:
    def test_summary_shape(self):
        summary = get_compliance_summary()
        assert set(summary.keys()) == {
            "total_requirements",
            "covered",
            "partial",
            "not_covered",
            "user_responsibility",
            "coverage_rate",
            "by_regulation",
        }

    def test_status_counts_sum_to_total(self):
        s = get_compliance_summary()
        assert (
            s["covered"] + s["partial"] + s["not_covered"] + s["user_responsibility"]
        ) == s["total_requirements"]

    def test_coverage_rate_within_expected_range(self):
        s = get_compliance_summary()
        # 60% lower bound is the plan target; cap at 100.
        assert 60.0 <= s["coverage_rate"] <= 100.0

    def test_by_regulation_groups_match(self):
        s = get_compliance_summary()
        assert set(s["by_regulation"].keys()) == EXPECTED_REGULATIONS


class TestComplianceRegistry:
    def test_list_jurisdictions(self):
        assert list_jurisdictions() == ["jp", "kr"]

    @pytest.mark.parametrize("juris", ["jp", "kr", "all"])
    def test_report_dispatch(self, juris: Jurisdiction):
        report = registry_report(juris)
        assert isinstance(report, list)
        assert report  # non-empty

    def test_all_is_union(self):
        jp = registry_report("jp")
        kr = registry_report("kr")
        all_items = registry_report("all")
        assert len(all_items) == len(jp) + len(kr)

    def test_summary_dispatch_kr_matches_module(self):
        from_registry = registry_summary("kr")
        from_module = get_compliance_summary()
        assert from_registry == from_module

    def test_summary_all_recomputes(self):
        s = registry_summary("all")
        jp = registry_summary("jp")
        kr = registry_summary("kr")
        assert s["total_requirements"] == jp["total_requirements"] + kr["total_requirements"]
        assert s["covered"] == jp["covered"] + kr["covered"]
        # Both jurisdictions surface in the grouped view.
        assert "개인정보보호법 (PIPA)" in s["by_regulation"]

    def test_unknown_jurisdiction_raises(self):
        with pytest.raises(ValueError):
            registry_report("eu")  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            registry_summary("eu")  # type: ignore[arg-type]


class TestCLIIntegration:
    def test_pipa_pii_03_present(self):
        """PIPA-PII-03 (자동화의사결정 대응권) is the headline 2024 amendment —
        must always be in the report."""
        ids = {item["requirement_id"] for item in get_compliance_report()}
        assert "PIPA-PII-03" in ids

    def test_cli_compliance_kr_json(self, capsys):
        from aigis.cli import main

        rc = main(["compliance", "--jurisdiction", "kr", "--json"])
        assert rc == 0
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["jurisdiction"] == "kr"
        assert payload["summary"]["total_requirements"] >= 50
        ids = {it["requirement_id"] for it in payload["items"]}
        assert "PIPA-PII-03" in ids
        assert "FSC-AI-15" in ids
