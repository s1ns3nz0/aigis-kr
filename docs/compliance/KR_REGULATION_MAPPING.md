# Aigis — 한국 규제 매핑 (Korea Regulation Mapping)

> Last updated: 2026-05-18
> Aigis version: v1.1.0
> Source-of-truth: [`aigis/compliance_kr.py`](../../aigis/compliance_kr.py)
> CLI: `aig compliance --jurisdiction kr` / `aig compliance --jurisdiction kr --json`

이 문서는 Aigis가 한국 데이터·금융·정보보호 규제와 어떻게 정렬되는지 정리한 매핑입니다. 항목의 단일 진실원(single source of truth)은 [`aigis/compliance_kr.py`](../../aigis/compliance_kr.py)이고, 본 문서는 그 데이터를 읽기 쉽게 풀어쓴 동반 문서입니다.

## 한눈에 보는 커버리지

| 규제 | 항목 수 | covered | partial | user_responsibility |
|------|:------:|:-------:|:-------:|:-------------------:|
| 개인정보보호법 (PIPA)            | 12 | 5 | 4 | 3 |
| 신용정보법                       | 8  | 4 | 4 | 0 |
| 정보통신망법                     | 6  | 3 | 2 | 1 |
| 금융분야 AI 가이드라인 (금융위)  | 15 | 8 | 5 | 2 |
| 전자금융감독규정                 | 5  | 3 | 1 | 1 |
| ISMS-P 인증기준                  | 7  | 5 | 1 | 1 |
| **합계**                         | **53** | **28** | **17** | **8** |

**Coverage rate (covered + partial × 0.5) / total = 68.9%**

> `not_covered` 항목은 0개입니다. 의도적으로 사용자(시스템 운영자) 책임으로 분리한 항목은 `user_responsibility`(8개)로 분류했습니다.

---

## 1. 개인정보보호법 (PIPA) — 12 항목

> 근거: 「개인정보 보호법」 (2024년 3월 시행 개정안 포함), 개인정보보호위원회 고시 2023-6호 「개인정보의 안전성 확보조치 기준」

핵심 신설 조항:

- **PIPA-PII-03**: 자동화된 결정에 대한 정보주체의 권리 (제37조의2) — 2024년 신설. AI 결정 거부권·설명요구권. Aigis는 Activity Stream으로 의사결정 근거(triggered_rules, risk_score) 추적하여 설명요구 대응 지원.
- **PIPA-PII-06**: 개인정보 국외이전 (제28조의8) — 2024년 신설. 보호위 적정성 결정 도입. Aigis Policy Engine으로 한국 PII 검출 시 국외 LLM 송신 차단 정책 가능.
- **PIPA-PII-12**: 고유식별정보 처리 제한 (제24조) — 주민등록번호·여권·운전면허·외국인등록번호. Aigis 백엔드 detector에 모두 구현됨 (`pii_ko_rrn`, `pii_ko_passport`, `pii_ko_driver_license`, `pii_ko_foreign_reg`).

`user_responsibility`로 분류한 3건: 정보주체 권리 응답 프로세스(제35-37조), 처리방침 게시(제30조), 손해배상 책임보험(제39조의7).

## 2. 신용정보법 — 8 항목

> 근거: 「신용정보의 이용 및 보호에 관한 법률」 (2020년 데이터 3법 개정 포함)

핵심 매핑:

- **CRED-04**: 개인신용정보 전송요구권(마이데이터, 제33조의2) — 마이데이터 API 트래픽 감사 로깅.
- **CRED-05**: 자동화평가 결과 설명·이의제기권(제36조의2) — PIPA-PII-03과 같이 의사결정 근거 추적 인프라.
- **CRED-06**: 누설 통지·신고(제39조의4) — 1만명 이상 누설 시 5일 내 금감원·금융위 신고. Aigis alerts 로그로 사고 범위 산정 데이터 제공.

## 3. 정보통신망법 — 6 항목

> 근거: 「정보통신망 이용촉진 및 정보보호 등에 관한 법률」

2020년 데이터 3법 개정으로 개인정보 관련 조항은 PIPA로 상당 부분 이관되었으나, **침해사고 대응(제48조의3)**, **ISMS 인증(제47조)**, **본인확인기관(제23조의2~3)**, **청소년 보호(제42조의2)** 등은 망법 고유 영역으로 남음.

## 4. 금융분야 AI 가이드라인 (금융위) — 15 항목

> 근거: 「금융분야 AI 가이드라인」 (금융위원회 2021년 7월 발표, 2024년 행정지도 강화)

이 가이드라인은 **법적 구속력은 약하나 감독상 기준** 성격이며, 특히 신용평가·대출심사·보험인수·자산운용 등 금융 의사결정에 AI를 도입할 때 핵심 점검표 역할을 합니다.

Aigis가 직접 대응(covered)하는 영역:

- **FSC-AI-02** 모형 위험관리(검증·테스트) — `aig benchmark` + `aig redteam` + `aig adversarial-loop`
- **FSC-AI-03** 모형 모니터링 — `aig monitor` 대시보드
- **FSC-AI-06** 책임성(의사결정자 식별) — 감사 로그 user_id·session·agent_type·department
- **FSC-AI-07** 인적개입(중요 결정에 인간 검토) — Human-in-the-Loop 큐, SLA 타임아웃
- **FSC-AI-10** 보안(모델 도난·역공학 방지) — 시스템 프롬프트 추출 패턴(`pi_ko_system_prompt` 등)
- **FSC-AI-11** 외부 위탁 평가 — 외부 LLM 호출 감지·로깅
- **FSC-AI-14** 감독당국 보고 — `aig report --format markdown` 자동 보고서
- **FSC-AI-15** 기록 보존(최소 5년) — `aig maintenance --retention-days 1825`

부분 대응(partial) 5건은 학습데이터 품질 관리, 설명가능성, 차별 방지 등 **모델 자체의 책임 영역**으로, Aigis는 보조 가시화·증적 역할입니다.

## 5. 전자금융감독규정 — 5 항목

> 근거: 「전자금융감독규정」 (금융감독원)

- **EFR-03** 전자금융사고 보고(제73조) — 영업일 익일까지. Aigis alerts + 자동 보고서.
- **EFR-05** 외부 전산자원 이용(제14조의2) — 클라우드/제3자 AI. Aigis Policy Engine으로 사전 평가 없는 엔드포인트 차단.
- **EFR-02** 망분리(제15조) — 인프라 요건이라 Aigis 직접 대응 불가. 단 Aigis 자체는 **zero-dependency · offline 동작** 가능하므로 망분리 환경에서 운영 가능.

## 6. ISMS-P 인증기준 — 7 항목 (AI 관련 통제 중심)

> 근거: 「정보보호 및 개인정보보호 관리체계(ISMS-P) 인증기준」 (KISA, 2023년 개정)

전체 102개 통제항목 중 AI 시스템에 직접 적용되는 통제 분야(2.6~2.12) 7개를 매핑.

- **ISMS-P-2.6** 접근 통제 — Policy Engine
- **ISMS-P-2.8** 개발보안 — `aig benchmark` + `aig redteam`, pre-commit hook
- **ISMS-P-2.10** 시스템·서비스 보안관리 — 64+ 침입 탐지 패턴(한국어 4개 포함)
- **ISMS-P-2.11** 사고 예방·대응 — alerts + Slack/Webhook + adversarial-loop 분기별 보안훈련

암호 통제(2.7)는 인프라 책임으로 `user_responsibility` 분류.

---

## 한계와 책임 분담

Aigis가 직접 해결하지 않는 영역은 다음과 같이 분류했습니다:

| 분류 | 의미 | 예 |
|------|------|----|
| `covered` | Aigis 기능으로 직접 대응 | LLM 경로상 PII 차단, HITL 큐, 감사 로그 |
| `partial` | Aigis 기능이 일부 대응, 추가 도구·정책 필요 | 가명처리(외부 알고리즘 필요), 설명가능성(모델 책임) |
| `user_responsibility` | 인프라·조직·계약 요건이라 Aigis 범위 밖 | CISO 지정, 보험 가입, 망분리, 처리방침 게시 |
| `not_covered` | 의도적으로 비대응 표시 (현재 0건) | 해당 없음 |

**금융 컴플라이언스 도입 가이드**: PR1(이 문서) → PR2(`policy_templates/kr_*.yaml`) → PR3(추가 한국 금융 PII 패턴) 순으로 통합하면 ISMS-P 인증 심사와 금융위 행정지도 점검 시 즉시 제출 가능한 기술적 통제 증적 세트가 구성됩니다.

---

## CLI 사용 예

```bash
# 한국 규제만 요약
aig compliance --jurisdiction kr

# 한국 규제 전체 항목 JSON (감사 자료, BI 도구 입력 등)
aig compliance --jurisdiction kr --json > kr_compliance.json

# 일본+한국 합쳐서 보기 (다국가 운영 조직용)
aig compliance --jurisdiction all
```

CI/CD에 통합 시:

```bash
# 커버리지가 일정 수준 이하로 떨어지면 빌드 실패
COV=$(aig compliance --jurisdiction kr --json | jq '.summary.coverage_rate')
test "$(echo "$COV >= 65" | bc -l)" -eq 1 || exit 1
```

---

## 변경 이력

- 2026-05-18 — 초기 작성. 53개 항목 (PIPA 12 / 신용정보법 8 / 망법 6 / 금융위 AI 15 / 전자금융감독규정 5 / ISMS-P 7).
