"""Aigis i18n — zero-dependency message translation for CLI and HTTP server.

Mirrors the design of ``site/src/lib/translations.ts`` (frontend i18n): a flat
``MESSAGES`` dict keyed by message ID, each value mapping ``Lang`` codes to
the localized string. ``t(key, lang)`` looks up the localized string; missing
translations fall back to the English form so a partially-translated key is
still safe.

Language resolution order (highest priority first):
  1. Explicit ``lang`` argument passed to ``t()``.
  2. ``AIGIS_LANG`` environment variable (``en`` / ``ja`` / ``ko``).
  3. ``LANG`` / ``LC_ALL`` environment variable prefix (e.g. ``ko_KR.UTF-8``).
  4. Default ``en``.

HTTP server callers should additionally honor the ``Accept-Language`` request
header — see ``parse_accept_language()``.
"""

from __future__ import annotations

import os
from typing import Literal

Lang = Literal["en", "ja", "ko"]

_SUPPORTED: tuple[Lang, ...] = ("en", "ja", "ko")
_DEFAULT: Lang = "en"


# Message dictionary. Add new keys here as more user-facing strings get
# wrapped. Keep the keys grouped by surface (server.*, cli.*) for clarity.
# IMPORTANT: ``en`` is the source of truth — every key must have an English
# entry. ``ja`` and ``ko`` may be omitted (fallback to ``en``), but if present
# they should match the English semantics exactly.
MESSAGES: dict[str, dict[Lang, str]] = {
    # ---- HTTP server (aigis/server.py) ----
    "server.error.missing_body": {
        "en": "missing body",
        "ja": "リクエストボディがありません",
        "ko": "요청 본문이 없습니다",
    },
    "server.error.body_too_large": {
        "en": "body too large",
        "ja": "リクエストボディが大きすぎます",
        "ko": "요청 본문이 너무 큽니다",
    },
    "server.error.invalid_json": {
        "en": "invalid JSON: {detail}",
        "ja": "不正な JSON: {detail}",
        "ko": "잘못된 JSON 형식입니다: {detail}",
    },
    "server.error.expected_object": {
        "en": "expected JSON object",
        "ja": "JSON オブジェクトが必要です",
        "ko": "JSON 객체가 필요합니다",
    },
    "server.error.unknown_path": {
        "en": "unknown path: {path}",
        "ja": "未定義のパス: {path}",
        "ko": "알 수 없는 경로입니다: {path}",
    },
    "server.error.text_must_be_string": {
        "en": "text must be string",
        "ja": "text は文字列である必要があります",
        "ko": "text 필드는 문자열이어야 합니다",
    },
    "server.error.messages_must_be_list": {
        "en": "messages must be list",
        "ja": "messages は配列である必要があります",
        "ko": "messages 필드는 배열이어야 합니다",
    },
    # ---- CLI: `aig compliance` ----
    "cli.compliance.header": {
        "en": "Aigis Compliance — {label}",
        "ja": "Aigis コンプライアンス — {label}",
        "ko": "Aigis 컴플라이언스 — {label}",
    },
    "cli.compliance.label.jp": {"en": "Japan", "ja": "日本", "ko": "일본"},
    "cli.compliance.label.kr": {"en": "Korea", "ja": "韓国", "ko": "한국"},
    "cli.compliance.label.all": {
        "en": "All jurisdictions",
        "ja": "全管轄",
        "ko": "전체 관할",
    },
    "cli.compliance.total": {
        "en": "Total requirements",
        "ja": "要件総数",
        "ko": "전체 요건 수",
    },
    "cli.compliance.covered": {
        "en": "Covered",
        "ja": "対応済み",
        "ko": "대응 완료",
    },
    "cli.compliance.partial": {
        "en": "Partial",
        "ja": "部分対応",
        "ko": "부분 대응",
    },
    "cli.compliance.not_covered": {
        "en": "Not covered",
        "ja": "未対応",
        "ko": "미대응",
    },
    "cli.compliance.user_responsibility": {
        "en": "User responsibility",
        "ja": "利用者責任",
        "ko": "사용자 책임",
    },
    "cli.compliance.coverage_rate": {
        "en": "Coverage rate",
        "ja": "カバレッジ",
        "ko": "커버리지",
    },
    "cli.compliance.by_regulation": {
        "en": "By regulation:",
        "ja": "規制ごと:",
        "ko": "규제별:",
    },
    "cli.compliance.tip_json": {
        "en": (
            "Tip: aig compliance --jurisdiction {jurisdiction} --json"
            " for the full item list."
        ),
        "ja": (
            "ヒント: aig compliance --jurisdiction {jurisdiction} --json"
            " で全項目を JSON 出力できます。"
        ),
        "ko": (
            "팁: aig compliance --jurisdiction {jurisdiction} --json"
            " 로 전체 항목을 JSON으로 받아볼 수 있습니다."
        ),
    },
    "cli.compliance.supported": {
        "en": "Supported jurisdictions: {jurisdictions}",
        "ja": "対応管轄: {jurisdictions}",
        "ko": "지원 관할: {jurisdictions}",
    },
}


def _normalize_lang(value: str | None) -> Lang | None:
    """Normalize an arbitrary string to a supported Lang code, or ``None``."""
    if not value:
        return None
    token = value.strip().lower().replace("_", "-")
    # First two letters of an RFC 1766 / BCP 47-ish tag (e.g. "ko-KR" → "ko").
    primary = token.split("-")[0].split(".")[0]
    if primary in _SUPPORTED:
        return primary  # type: ignore[return-value]
    return None


def detect_lang(arg_lang: str | None = None) -> Lang:
    """Resolve the active language using the documented priority order."""
    explicit = _normalize_lang(arg_lang)
    if explicit:
        return explicit
    env = _normalize_lang(os.environ.get("AIGIS_LANG"))
    if env:
        return env
    for var in ("LC_ALL", "LANG"):
        from_env = _normalize_lang(os.environ.get(var))
        if from_env:
            return from_env
    return _DEFAULT


def t(key: str, lang: str | None = None, **kwargs: object) -> str:
    """Look up a localized message.

    ``key`` must exist in ``MESSAGES``. If the requested ``lang`` is not in
    the entry, fall back to the English form. ``kwargs`` are formatted into
    the message with ``str.format()``.

    Unknown keys return the literal key (rather than raising) so a missing
    translation never crashes the caller — but the key shows up in logs as a
    self-describing token to fix later.
    """
    entry = MESSAGES.get(key)
    if entry is None:
        return key
    resolved = detect_lang(lang)
    text = entry.get(resolved) or entry.get(_DEFAULT) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def parse_accept_language(header_value: str | None) -> Lang | None:
    """Pick the highest-priority supported language from an HTTP header.

    Examples accepted:
        ``"ko-KR,ko;q=0.9,en;q=0.8"`` → ``"ko"``
        ``"fr-FR,en;q=0.5"``          → ``"en"``
        ``""`` or ``None``            → ``None``

    Q-values are honored; supported languages always win over q-values when
    tied. Unknown languages are skipped.
    """
    if not header_value:
        return None
    # Build (q, lang) tuples and pick highest q among supported.
    candidates: list[tuple[float, Lang]] = []
    for part in header_value.split(","):
        token = part.strip()
        if not token:
            continue
        q = 1.0
        if ";" in token:
            lang_part, _, q_part = token.partition(";")
            token = lang_part.strip()
            q_part = q_part.strip()
            if q_part.startswith("q="):
                try:
                    q = float(q_part[2:])
                except ValueError:
                    q = 1.0
        lang = _normalize_lang(token)
        if lang is not None:
            candidates.append((q, lang))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[0], reverse=True)
    return candidates[0][1]
