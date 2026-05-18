"""Input filter: analyze incoming LLM request messages."""

from __future__ import annotations

from aigis.decoders import normalize_hangul
from aigis.filters.patterns import ALL_INPUT_PATTERNS
from aigis.filters.scorer import run_patterns
from aigis.types import MatchedRule, RiskLevel


def extract_text_from_messages(messages: list[dict]) -> str:
    """Concatenate all message content into a single string for pattern matching."""
    parts: list[str] = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    parts.append(part.get("text", ""))
    return "\n".join(parts)


def _augment_with_hangul_variant(text: str) -> str:
    """Append the NFKC-normalized Hangul variant so jamo-split inputs are scanned.

    Pattern engine uses ``re.search()`` over the full text, so concatenating the
    normalized form lets KOREAN_*_PATTERNS hit even when the original payload
    used separated jamo (e.g. ``ㅇㅣ전 지시 무시`` → ``이전 지시 무시``). The
    normalized form is only appended when it actually differs, keeping
    Latin-only inputs unchanged.
    """
    normalized = normalize_hangul(text)
    if normalized == text:
        return text
    return text + "\n" + normalized


def filter_input(
    text: str,
    custom_rules: list[dict] | None = None,
) -> tuple[int, RiskLevel, list[MatchedRule]]:
    """Run input filter on a plain text string."""
    return run_patterns(_augment_with_hangul_variant(text), ALL_INPUT_PATTERNS, custom_rules)


def filter_messages(
    messages: list[dict],
    custom_rules: list[dict] | None = None,
) -> tuple[int, RiskLevel, list[MatchedRule]]:
    """Run input filter on OpenAI-style messages array."""
    text = extract_text_from_messages(messages)
    return run_patterns(_augment_with_hangul_variant(text), ALL_INPUT_PATTERNS, custom_rules)
