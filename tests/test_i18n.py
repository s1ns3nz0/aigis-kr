"""Tests for aigis/i18n.py — message translation, language detection, header parsing."""

import os

import pytest

from aigis.i18n import (
    MESSAGES,
    _DEFAULT,
    _SUPPORTED,
    _normalize_lang,
    detect_lang,
    parse_accept_language,
    t,
)


# ---------------------------------------------------------------------------
# _normalize_lang
# ---------------------------------------------------------------------------
class TestNormalizeLang:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("en", "en"),
            ("ja", "ja"),
            ("ko", "ko"),
            ("EN", "en"),
            ("ko-KR", "ko"),
            ("ko_KR", "ko"),
            ("ko_KR.UTF-8", "ko"),
            ("ja-JP", "ja"),
        ],
    )
    def test_supported(self, value, expected):
        assert _normalize_lang(value) == expected

    @pytest.mark.parametrize("value", [None, "", "fr", "zh", "de-DE", "  "])
    def test_unsupported_returns_none(self, value):
        assert _normalize_lang(value) is None


# ---------------------------------------------------------------------------
# detect_lang — priority: arg > AIGIS_LANG > LC_ALL > LANG > default
# ---------------------------------------------------------------------------
class TestDetectLang:
    def test_explicit_arg_wins(self, monkeypatch):
        monkeypatch.setenv("AIGIS_LANG", "ja")
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        assert detect_lang("ko") == "ko"

    def test_aigis_lang_env(self, monkeypatch):
        monkeypatch.setenv("AIGIS_LANG", "ko")
        monkeypatch.delenv("LANG", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        assert detect_lang() == "ko"

    def test_lc_all_env(self, monkeypatch):
        monkeypatch.delenv("AIGIS_LANG", raising=False)
        monkeypatch.setenv("LC_ALL", "ko_KR.UTF-8")
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        assert detect_lang() == "ko"

    def test_lang_env(self, monkeypatch):
        monkeypatch.delenv("AIGIS_LANG", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.setenv("LANG", "ja_JP.UTF-8")
        assert detect_lang() == "ja"

    def test_default_when_nothing_set(self, monkeypatch):
        for var in ("AIGIS_LANG", "LC_ALL", "LANG"):
            monkeypatch.delenv(var, raising=False)
        assert detect_lang() == _DEFAULT == "en"

    def test_unknown_env_falls_through(self, monkeypatch):
        monkeypatch.setenv("AIGIS_LANG", "fr")
        monkeypatch.setenv("LANG", "ko_KR.UTF-8")
        # AIGIS_LANG is invalid so LANG should win.
        assert detect_lang() == "ko"


# ---------------------------------------------------------------------------
# t() — message lookup, fallback, formatting
# ---------------------------------------------------------------------------
class TestTranslate:
    def test_korean_lookup(self):
        msg = t("server.error.missing_body", "ko")
        assert "본문" in msg  # 한국어 키워드

    def test_japanese_lookup(self):
        msg = t("server.error.missing_body", "ja")
        assert "リクエストボディ" in msg

    def test_english_lookup(self):
        assert t("server.error.missing_body", "en") == "missing body"

    def test_fallback_to_english_when_lang_missing(self):
        # Manually inject a key without ko translation.
        MESSAGES["__test_partial__"] = {"en": "english only", "ja": "日本語のみ"}
        try:
            assert t("__test_partial__", "ko") == "english only"
        finally:
            del MESSAGES["__test_partial__"]

    def test_unknown_key_returns_key(self):
        assert t("nonexistent.key.foo", "ko") == "nonexistent.key.foo"

    def test_format_kwargs(self):
        msg = t("server.error.invalid_json", "ko", detail="line 1")
        assert "line 1" in msg
        assert "JSON" in msg

    def test_format_missing_arg_is_safe(self):
        # Forgetting to pass the format arg returns the raw template without crashing.
        msg = t("server.error.unknown_path", "ko")
        # No exception; template returned as-is.
        assert isinstance(msg, str)


# ---------------------------------------------------------------------------
# parse_accept_language
# ---------------------------------------------------------------------------
class TestParseAcceptLanguage:
    def test_simple_supported(self):
        assert parse_accept_language("ko") == "ko"
        assert parse_accept_language("ja") == "ja"
        assert parse_accept_language("en") == "en"

    def test_region_subtag(self):
        assert parse_accept_language("ko-KR") == "ko"
        assert parse_accept_language("ja-JP") == "ja"

    def test_q_value_ranking(self):
        # ko has higher q than en → ko wins.
        assert parse_accept_language("en;q=0.5,ko;q=0.9") == "ko"

    def test_unknown_language_skipped(self):
        # fr is not supported → fall through to en.
        assert parse_accept_language("fr,en") == "fr" or parse_accept_language("fr,en") == "en"
        # Concretely: fr returns None from _normalize_lang, en is supported.
        assert parse_accept_language("fr,en") == "en"

    def test_all_unknown_returns_none(self):
        assert parse_accept_language("fr,de,zh") is None

    def test_none_input(self):
        assert parse_accept_language(None) is None
        assert parse_accept_language("") is None

    def test_chrome_style_header(self):
        # Realistic Korean Chrome browser header.
        assert parse_accept_language("ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7") == "ko"


# ---------------------------------------------------------------------------
# Sanity — every key has English source-of-truth
# ---------------------------------------------------------------------------
class TestMessagesIntegrity:
    def test_every_key_has_english(self):
        missing = [k for k, v in MESSAGES.items() if "en" not in v]
        assert missing == [], f"keys missing English source-of-truth: {missing}"

    def test_supported_lang_codes(self):
        assert _SUPPORTED == ("en", "ja", "ko")

    def test_no_empty_translations(self):
        for key, entry in MESSAGES.items():
            for lang, text in entry.items():
                assert text, f"empty translation for {key}/{lang}"


# ---------------------------------------------------------------------------
# CLI integration — `aig compliance` honors AIGIS_LANG
# ---------------------------------------------------------------------------
class TestCLIComplianceKoreanOutput:
    def test_compliance_kr_in_korean(self, monkeypatch, capsys):
        from aigis.cli import main

        monkeypatch.setenv("AIGIS_LANG", "ko")
        rc = main(["compliance", "--jurisdiction", "kr"])
        assert rc == 0
        out = capsys.readouterr().out
        # 한글 핵심 라벨 노출 확인
        assert "한국" in out  # header label
        assert "커버리지" in out
        assert "규제별" in out

    def test_compliance_in_japanese(self, monkeypatch, capsys):
        from aigis.cli import main

        monkeypatch.setenv("AIGIS_LANG", "ja")
        rc = main(["compliance", "--jurisdiction", "jp"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "日本" in out
        assert "カバレッジ" in out

    def test_compliance_in_english_default(self, monkeypatch, capsys):
        from aigis.cli import main

        for var in ("AIGIS_LANG", "LC_ALL", "LANG"):
            monkeypatch.delenv(var, raising=False)
        rc = main(["compliance", "--jurisdiction", "all"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "All jurisdictions" in out
        assert "Coverage rate" in out

    def test_json_output_unaffected_by_lang(self, monkeypatch, capsys):
        """JSON output is a machine API; should stay English regardless of locale."""
        import json as _json

        from aigis.cli import main

        monkeypatch.setenv("AIGIS_LANG", "ko")
        rc = main(["compliance", "--jurisdiction", "kr", "--json"])
        assert rc == 0
        payload = _json.loads(capsys.readouterr().out)
        # Item field names stay English in the JSON contract.
        assert payload["jurisdiction"] == "kr"
        assert "summary" in payload
        assert "items" in payload
