# Aigis — Policy Template Hub

Industry-specific YAML policy templates for common deployment scenarios.

## Usage

```bash
# Use any template directly
pip install 'aigis[yaml]'
```

```python
from aigis import Guard

# Use a template from this directory
guard = Guard(policy_file="policy_templates/finance.yaml")

# Or point to your own copy
guard = Guard(policy_file="my_policy.yaml")
```

## Available Templates

| Template | Use Case | Block Threshold |
|----------|----------|-----------------|
| [`finance.yaml`](finance.yaml) | Banking, trading, payment apps | 61 (strict) |
| [`healthcare.yaml`](healthcare.yaml) | Medical records, telehealth | 61 (strict) |
| [`ecommerce.yaml`](ecommerce.yaml) | Online stores, product QA bots | 76 (moderate-strict) |
| [`internal_tools.yaml`](internal_tools.yaml) | Internal company chatbots | 81 (default) |
| [`education.yaml`](education.yaml) | EdTech, student-facing AI | 71 (moderate) |
| [`customer_support.yaml`](customer_support.yaml) | Support bots, helpdesks | 76 (moderate-strict) |
| [`developer_tools.yaml`](developer_tools.yaml) | Code assistants, CI helpers | 86 (permissive) |
| [`eu_ai_act_high_risk.yaml`](eu_ai_act_high_risk.yaml) | EU AI Act Annex III systems (effective 2026-08-02) | 55 (strict) |
| [`gpai_provider.yaml`](gpai_provider.yaml) | EU AI Act Art. 53/55 General-Purpose AI providers | 55 (strict) |
| [`kr_finance.yaml`](kr_finance.yaml) | 한국 금융권 — 신용정보법 · 전자금융감독규정 · 금융위 AI 가이드 | 55 (strict) |
| [`kr_pipa.yaml`](kr_pipa.yaml) | 한국 개인정보보호법(PIPA) 범용 — 모든 산업 | 60 (strict) |
| [`kr_isms_p.yaml`](kr_isms_p.yaml) | ISMS-P 인증 통제(2.6~2.12 AI 관련) | 55 (strict) |

> 한국 규제 매핑 전체는 [`docs/compliance/KR_REGULATION_MAPPING.md`](../docs/compliance/KR_REGULATION_MAPPING.md) 참조.
> `aig compliance --jurisdiction kr`로 53개 한국 규제 항목 매핑을 확인할 수 있습니다.
> 금융사는 `kr_finance` + `kr_pipa` + `kr_isms_p` 조합 사용을 권장합니다.

## Customization

All templates follow this schema:

```yaml
name: my-policy
auto_block_threshold: 75   # Score >= this → blocked
auto_allow_threshold: 25   # Score <= this → always allowed
custom_rules:
  - id: unique_rule_id
    name: Human-readable name
    pattern: "(regex|pattern)"
    score_delta: 50          # Added to base risk score
    enabled: true
```

## Contributing a Template

PRs welcome! To add a new industry template:

1. Copy `internal_tools.yaml` as a starting point
2. Adjust thresholds and add industry-specific `custom_rules`
3. Add a row to the table above
4. Submit a PR with a description of the target use case
