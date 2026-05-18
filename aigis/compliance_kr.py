"""Korea AI Governance compliance checker.

Maps Aigis capabilities to specific requirements from:
  - 개인정보보호법 (PIPA, 2024년 3월 시행 개정안 포함)
  - 개인정보의 안전성 확보조치 기준 (개인정보보호위원회 고시 2023-6호)
  - 신용정보의 이용 및 보호에 관한 법률 (신용정보법)
  - 정보통신망 이용촉진 및 정보보호 등에 관한 법률 (망법)
  - 금융분야 AI 가이드라인 (금융위원회, 2021년 7월 / 2024년 강화)
  - 전자금융감독규정 (금융감독원)
  - 정보보호 및 개인정보보호 관리체계(ISMS-P) 인증기준 (2023년 개정)

References:
  - 법령정보센터 (law.go.kr) 원문 인용
  - 개인정보보호위원회 가이드라인 (pipc.go.kr)
  - 금융위원회 보도자료 (fsc.go.kr)
  - KISA ISMS-P 인증기준 안내서

Usage:
    from aigis.compliance_kr import get_compliance_report, get_compliance_summary

    report = get_compliance_report()
    for item in report:
        print(f"[{item['status']}] {item['requirement']}")
"""

from aigis.compliance import ComplianceItem


def get_compliance_report() -> list[dict]:
    """Generate Korean regulation compliance report.

    Returns a list of compliance items showing how Aigis maps to each
    Korean AI/data regulatory requirement.
    """
    items = _build_kr_compliance_items()
    return [
        {
            "regulation": item.regulation,
            "requirement_id": item.requirement_id,
            "requirement": item.requirement,
            "description": item.description,
            "aigis_feature": item.aigis_feature,
            "status": item.status,
            "notes": item.notes,
        }
        for item in items
    ]


def get_compliance_summary() -> dict:
    """Get a summary of Korean regulation coverage."""
    items = _build_kr_compliance_items()
    total = len(items)
    covered = sum(1 for i in items if i.status == "covered")
    partial = sum(1 for i in items if i.status == "partial")
    not_covered = sum(1 for i in items if i.status == "not_covered")
    user_resp = sum(1 for i in items if i.status == "user_responsibility")

    return {
        "total_requirements": total,
        "covered": covered,
        "partial": partial,
        "not_covered": not_covered,
        "user_responsibility": user_resp,
        "coverage_rate": round(((covered + partial * 0.5) / total) * 100, 1) if total else 0,
        "by_regulation": _group_by_regulation(items),
    }


def _group_by_regulation(items: list[ComplianceItem]) -> dict:
    groups: dict[str, dict] = {}
    for item in items:
        if item.regulation not in groups:
            groups[item.regulation] = {"total": 0, "covered": 0, "partial": 0, "not_covered": 0}
        groups[item.regulation]["total"] += 1
        if item.status in ("covered", "partial", "not_covered"):
            groups[item.regulation][item.status] += 1
    return groups


def _build_kr_compliance_items() -> list[ComplianceItem]:
    return [
        # ================================================================
        # 개인정보보호법 (PIPA) — 2024년 3월 시행 개정안 포함
        # ================================================================
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-01",
            requirement="개인정보의 안전성 확보조치 (제29조)",
            description="개인정보처리자는 개인정보가 분실·도난·유출·위조·변조·훼손되지 않도록 "
            "기술적·관리적·물리적 안전조치를 강구해야 한다. 세부 기준은 개인정보보호위원회 "
            "고시 2023-6호 「개인정보의 안전성 확보조치 기준」으로 정함.",
            aigis_feature="입력 PII 패턴 15개 + 한국 PII 패턴 3개(주민등록번호, 휴대폰, "
            "사업자등록번호)로 LLM 송신 전 검출 및 자동 sanitize(). 감사 로그로 안전조치 "
            "운영 증적 확보.",
            status="covered",
            notes="고시 2023-6호 제7조(개인정보의 암호화), 제8조(접속기록의 보관·점검)는 "
            "사용자(시스템 운영자) 책임. Aigis는 LLM 경로상의 PII 노출 차단을 담당.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-02",
            requirement="가명정보의 처리 (제28조의2~제28조의7)",
            description="통계·과학적 연구·공익적 기록보존 목적의 가명처리 허용. 가명정보를 "
            "다른 정보와 결합하여 특정 개인을 알아보는 행위 금지 (제28조의5).",
            aigis_feature="주민등록번호·휴대폰·사업자등록번호 정규식 매칭으로 가명처리 누락분 "
            "탐지. Output filter로 LLM 응답에 가명 해제(재식별) 시도 차단 가능.",
            status="partial",
            notes="가명처리 알고리즘 자체(k-익명성, 차분 프라이버시 등)는 외부 도구 책임. "
            "Aigis는 재식별 방지 보조 역할.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-03",
            requirement="자동화된 결정에 대한 정보주체의 권리 (제37조의2)",
            description="2024년 3월 신설. 완전히 자동화된 시스템(인공지능 포함)의 결정이 "
            "정보주체의 권리·의무에 중대한 영향을 미치는 경우, 정보주체는 해당 결정을 "
            "거부하거나 설명을 요구할 수 있음.",
            aigis_feature="Activity Stream에 모든 AI 의사결정의 입력·출력·근거 패턴을 기록. "
            "거부/설명 요구 발생 시 감사 로그에서 의사결정 근거 추적 가능. "
            "Human-in-the-Loop 큐로 중대 결정에 인간 개입 강제.",
            status="covered",
            notes="설명 요구 응답은 사용자(서비스 제공자) 책임. Aigis는 설명에 필요한 "
            "기술적 근거(어떤 입력/패턴이 어떤 점수로 평가되었는지)를 제공.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-04",
            requirement="정보주체의 권리 (제35조~제37조)",
            description="열람·정정·삭제·처리정지 요구권. 개인정보처리자는 10일 이내 조치.",
            aigis_feature="감사 로그에 정보주체별 처리 이력 기록(세션/사용자 식별자 기준).",
            status="user_responsibility",
            notes="권리 행사 응답 프로세스는 사용자 책임. Aigis는 이력 조회 인프라만 제공.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-05",
            requirement="개인정보 처리업무의 위탁 (제26조)",
            description="처리위탁 시 위탁자는 수탁자에 대한 관리·감독 의무. 위탁업무 내용과 "
            "수탁자를 공개해야 함.",
            aigis_feature="외부 LLM(OpenAI/Anthropic/Google 등)으로의 데이터 송신을 감지·로깅. "
            "Policy Engine으로 특정 모델/엔드포인트로의 위탁 차단 가능.",
            status="covered",
            notes="수탁자(LLM 제공사) 계약 관리는 사용자 책임.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-06",
            requirement="개인정보의 국외이전 (제28조의8)",
            description="2024년 3월 개정. 국외이전 시 정보주체 동의 또는 법령/조약/적정성 "
            "결정 등의 근거 필요. 보호위원회 적정성 결정(EU와 유사) 도입.",
            aigis_feature="외부 LLM 호출 엔드포인트의 국적/리전 식별 후 차단/경고 가능 "
            "(Policy Engine YAML 규칙). 한국 PII 검출 시 국외 LLM 송신 차단 패턴 제공.",
            status="partial",
            notes="LLM 제공사의 데이터 처리 지역(리전) 식별은 사용자가 설정 시 가능.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-07",
            requirement="민감정보의 처리 제한 (제23조)",
            description="사상·신념, 노동조합·정당의 가입·탈퇴, 정치적 견해, 건강, 성생활 등에 "
            "관한 정보 및 유전정보·범죄경력자료는 별도 동의 또는 법령 근거 필요.",
            aigis_feature="민감정보 키워드 패턴 검출(건강·종교·정치 관련 표현). 출력 필터로 "
            "LLM이 민감정보 추론 결과를 응답에 포함시키는 패턴 탐지.",
            status="partial",
            notes="민감정보 분류는 맥락 의존적이므로 사용자 정책(custom_rules)으로 "
            "업종별 보강 권장.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-08",
            requirement="개인정보 처리방침의 수립 및 공개 (제30조)",
            description="처리목적, 처리 및 보유 기간, 제3자 제공, 위탁, 정보주체 권리·행사방법, "
            "안전성 확보조치 등을 처리방침에 명시·공개.",
            aigis_feature="컴플라이언스 리포트로 안전성 확보조치 현황 자동 생성 (처리방침 "
            "「안전조치」 항목에 활용 가능).",
            status="user_responsibility",
            notes="처리방침 작성·게시는 사용자 책임.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-09",
            requirement="개인정보 유출 등의 통지·신고 (제34조)",
            description="유출 사실을 알게 된 때에는 지체 없이(72시간 이내) 정보주체에 통지 및 "
            "1천명 이상 유출 시 보호위원회·KISA에 신고.",
            aigis_feature="LLM 응답으로 PII 노출 감지 시 즉시 alerts 로그 기록 + Slack/Webhook "
            "실시간 알림. 사고 시점·범위 산정에 필요한 감사 이력 보존.",
            status="covered",
            notes="법정 통지·신고는 사용자 책임. Aigis는 사고 탐지 및 증적만 제공.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-10",
            requirement="손해배상 책임의 이행을 위한 조치 (제39조의7)",
            description="매출액·이용자수 일정 규모 이상 사업자는 손해배상 책임이행 보험 "
            "가입 또는 준비금 적립 의무.",
            aigis_feature="해당 없음 — 보험·재무 조치는 Aigis 범위 밖.",
            status="user_responsibility",
            notes="단, 사고 발생 시 책임 입증을 위한 감사 로그 보존은 Aigis가 지원.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-11",
            requirement="개인정보 영향평가 (제33조)",
            description="공공기관이 일정 규모 이상 개인정보파일을 운용·변경할 때 영향평가 "
            "수행 의무. 민간도 권고.",
            aigis_feature="AI 도입에 따른 PII 처리 흐름을 컴플라이언스 리포트로 가시화. "
            "탐지 패턴 카탈로그를 영향평가 입력 자료로 활용 가능.",
            status="partial",
            notes="공식 영향평가서 작성은 외부 컨설팅 또는 사용자 책임.",
        ),
        ComplianceItem(
            regulation="개인정보보호법 (PIPA)",
            requirement_id="PIPA-PII-12",
            requirement="고유식별정보의 처리 제한 (제24조)",
            description="주민등록번호·여권번호·운전면허번호·외국인등록번호는 법령에 구체적 "
            "근거가 있는 경우에만 처리 가능. 인터넷 회원가입 시 주민등록번호 수집·이용 금지.",
            aigis_feature="주민등록번호(pii_ko_rrn)·여권(pii_ko_passport)·운전면허"
            "(pii_ko_driver_license)·외국인등록번호(pii_ko_foreign_reg) 패턴으로 LLM 송수신 "
            "차단. base_score 60-75로 CRITICAL/HIGH 분류.",
            status="covered",
            notes="여권/운전면허/외국인등록번호 패턴은 PR3에서 추가됨.",
        ),
        # ================================================================
        # 신용정보의 이용 및 보호에 관한 법률 (신용정보법)
        # ================================================================
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-01",
            requirement="개인신용정보의 수집·이용 (제15조)",
            description="개인신용정보 수집·이용 시 정보주체 동의 또는 법령 근거 필요. "
            "신용정보회사 등은 동의 없이 수집·이용 금지 (예외 한정).",
            aigis_feature="신용정보 키워드(신용평점·연체정보·대출잔액·카드한도) 패턴 검출. "
            "Policy Engine으로 동의 없는 신용정보 처리 시도 차단.",
            status="partial",
            notes="동의 관리 시스템은 사용자(금융기관) 책임.",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-02",
            requirement="가명처리·익명처리 (제40조의2)",
            description="2020년 데이터 3법 신설. 가명처리한 개인신용정보는 통계작성·연구 등 "
            "목적으로 활용 가능. 결합전문기관을 통한 결합 절차.",
            aigis_feature="가명 신용정보 결합 결과의 재식별 시도 탐지 (예: 「위 정보로 누구인지 "
            "맞춰봐」 패턴).",
            status="partial",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-03",
            requirement="신용정보의 기술적·물리적·관리적 보안대책 (제19조)",
            description="신용정보회사 등은 신용정보 누설·분실·변경·훼손 방지를 위한 보안대책 "
            "수립·시행 의무. 시행령 제17조의6 세부 기준.",
            aigis_feature="입출력 PII/신용정보 패턴 차단 + 감사 로그로 보안대책 운영 증적 확보. "
            "ISMS-P 통제항목과 매핑.",
            status="covered",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-04",
            requirement="개인신용정보 전송요구권 (제33조의2)",
            description="2020년 신설(마이데이터). 정보주체는 본인의 개인신용정보를 신용정보회사 "
            "등이 본인 또는 제3자(마이데이터사업자)에게 전송할 것을 요구할 수 있음.",
            aigis_feature="마이데이터 API 호출 트래픽 감사 로깅. 전송 대상·범위 변조 시도 "
            "탐지(Policy Engine YAML 규칙).",
            status="partial",
            notes="마이데이터 표준 API 구현은 사용자 책임.",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-05",
            requirement="자동화평가 결과에 대한 설명 및 이의제기권 (제36조의2)",
            description="2020년 신설. 신용평가 등 자동화된 의사결정에 대해 정보주체는 결과의 "
            "설명·근거 요구 및 이의제기 가능.",
            aigis_feature="신용평가 모델 출력에 대한 입력/판단 근거를 감사 로그로 저장. "
            "Activity Stream의 risk_score·triggered_rules 필드로 판단 근거 추적.",
            status="covered",
            notes="설명 응답서 작성은 사용자 책임. PIPA-PII-03과 중첩.",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-06",
            requirement="개인신용정보 누설 통지 및 신고 (제39조의4)",
            description="누설 시 정보주체에 지체 없이 통지, 1만명 이상 누설 시 금감원·금융위 "
            "신고 (5일 이내).",
            aigis_feature="신용정보 노출 감지 시 즉시 alerts + 통지/신고에 필요한 사고 범위 "
            "산정 데이터 제공.",
            status="covered",
            notes="법정 통지·신고는 사용자 책임.",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-07",
            requirement="개인신용정보 처리위탁 (제17조)",
            description="처리위탁 시 위탁자는 수탁자 관리·감독 의무. 수탁자는 위탁받은 업무 "
            "외 신용정보 이용·제3자 제공 금지.",
            aigis_feature="외부 AI 서비스(LLM 제공사) 호출을 감사 로그로 추적. Policy Engine "
            "으로 비인가 수탁자 차단.",
            status="covered",
        ),
        ComplianceItem(
            regulation="신용정보법",
            requirement_id="CRED-08",
            requirement="신용정보의 파기 (제20조의2)",
            description="신용정보 보유기간 경과·처리목적 달성 시 지체 없이 파기. 5년 이내 "
            "분리보관 가능.",
            aigis_feature="감사 로그 자동 회전·압축(aig maintenance --retention-days). "
            "보유기간 정책에 따라 LLM 송수신 캐시 만료 강제.",
            status="partial",
            notes="원천 신용정보 DB 파기는 사용자 책임. Aigis는 LLM 경로상의 로그만 관리.",
        ),
        # ================================================================
        # 정보통신망법 (정보통신망 이용촉진 및 정보보호 등에 관한 법률)
        # ================================================================
        ComplianceItem(
            regulation="정보통신망법",
            requirement_id="ITNA-01",
            requirement="개인정보의 기술적·관리적 보호조치 (제28조)",
            description="정보통신서비스 제공자는 개인정보가 분실·도난·누출·변조·훼손되지 "
            "않도록 기술적·관리적 보호조치 수립·시행 의무.",
            aigis_feature="입출력 PII 패턴 차단 + 감사 로그. PIPA와 중첩되는 영역에 대해 "
            "동일 메커니즘으로 대응.",
            status="covered",
            notes="2020년 데이터 3법 개정으로 PIPA로 상당 부분 일원화됨.",
        ),
        ComplianceItem(
            regulation="정보통신망법",
            requirement_id="ITNA-02",
            requirement="정보보호 최고책임자 지정 (제45조의3)",
            description="일정 규모 이상 정보통신서비스 제공자는 CISO 지정·신고 의무.",
            aigis_feature="해당 없음 — 조직 인사 요건.",
            status="user_responsibility",
        ),
        ComplianceItem(
            regulation="정보통신망법",
            requirement_id="ITNA-03",
            requirement="정보보호 관리체계 인증 (제47조) — ISMS",
            description="매출액·이용자수 일정 규모 이상 정보통신서비스 제공자는 ISMS 인증 "
            "의무. ISMS-P 통제항목과 연계.",
            aigis_feature="ISMS-P 인증기준 통제항목과 Aigis 기능 매핑 제공 "
            "(ISMS-P-2.6~2.12 참조).",
            status="partial",
            notes="실제 인증 심사는 KISA·인증기관 책임.",
        ),
        ComplianceItem(
            regulation="정보통신망법",
            requirement_id="ITNA-04",
            requirement="침해사고 대응 (제48조의3)",
            description="침해사고 발생 시 KISA에 신고 (24시간 이내). 사고 원인·피해 범위·"
            "조치 내역 등 보고.",
            aigis_feature="LLM 보안 사고(프롬프트 인젝션·PII 유출) 발생 시 alerts 로그 + "
            "사고 원인·범위 산정 데이터.",
            status="covered",
        ),
        ComplianceItem(
            regulation="정보통신망법",
            requirement_id="ITNA-05",
            requirement="본인확인기관 (제23조의2~3)",
            description="주민등록번호 사용 제한, 본인확인기관을 통한 대체수단(i-PIN 등) 사용.",
            aigis_feature="주민등록번호 입력 시도 즉시 차단(pii_ko_rrn).",
            status="covered",
        ),
        ComplianceItem(
            regulation="정보통신망법",
            requirement_id="ITNA-06",
            requirement="청소년 보호 (제42조의2)",
            description="청소년 유해정보 차단 의무. AI 생성 콘텐츠도 적용.",
            aigis_feature="유해 콘텐츠 생성 요청 탐지 패턴 (PR5 한국어 PI 패턴 확장 시 강화).",
            status="partial",
        ),
        # ================================================================
        # 금융분야 AI 가이드라인 (금융위원회 2021/2024)
        # ================================================================
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-01",
            requirement="데이터 적정성 — 학습데이터 품질·편향 관리",
            description="AI 학습데이터의 품질·대표성·편향 관리. 차별 변수(성별·연령·지역 등) "
            "직접 사용 금지 및 간접 차별 모니터링.",
            aigis_feature="학습데이터 자체 검증은 외부 도구 책임. Aigis는 추론 시점에 보호변수 "
            "유출 패턴 탐지.",
            status="partial",
            notes="금융위 행정지도 — 법적 구속력보다 감독상 기준 성격.",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-02",
            requirement="AI 모형 위험관리 — 검증·테스트",
            description="모형 개발·운영·변경 단계별 위험평가. 백테스팅·스트레스테스트 수행.",
            aigis_feature="aig benchmark + aig redteam으로 자동화 적대적 테스트. "
            "adversarial-loop로 attack-defend-improve 사이클.",
            status="covered",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-03",
            requirement="AI 모형 모니터링 — 운영 중 성능 추적",
            description="운영 중 모델 드리프트·성능 저하·이상 행동 지속 모니터링.",
            aigis_feature="aig monitor 대시보드로 24시간 침해 시도·차단율·ASR 트렌드 추적. "
            "OWASP LLM Top 10 카테고리별 스코어카드.",
            status="covered",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-04",
            requirement="설명가능성 — 거절 사유 등 고객 설명",
            description="대출 거절·보험 가입 거절·신용평가 등에 대해 고객에게 합리적 설명 제공.",
            aigis_feature="Aigis 차단/리뷰 결정에 대한 remediation_hint(한국어) 제공. "
            "triggered_rules 리스트로 어떤 패턴이 작동했는지 명시.",
            status="partial",
            notes="금융 의사결정 자체의 설명은 모델 책임. Aigis는 보안 차단 결정만 설명.",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-05",
            requirement="차별 방지 — 보호변수 모니터링",
            description="성별·연령·지역·장애 등 보호변수에 의한 직간접 차별 모니터링.",
            aigis_feature="민감속성 키워드 패턴 + 출력 필터로 차별적 결정 사유 노출 차단.",
            status="partial",
            notes="공정성 메트릭(Demographic Parity 등) 측정은 외부 도구 필요.",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-06",
            requirement="책임성 — 의사결정자 식별",
            description="AI 의사결정에 대한 책임자(부서) 명확화. 「AI가 결정했다」 책임회피 금지.",
            aigis_feature="감사 로그에 user_id·session·agent_type·department 기록으로 책임자 "
            "역추적 가능.",
            status="covered",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-07",
            requirement="인적개입 — 중요 의사결정에 인간 검토",
            description="중요 금융 의사결정(고액 대출·중대 신용평가)은 인간 검토 단계 필수.",
            aigis_feature="Human-in-the-Loop 큐. Medium/High 리스크는 자동으로 큐에 적재. "
            "SLA 타임아웃 + 폴백 정책. Policy Engine으로 금융 의사결정 액션을 review 강제.",
            status="covered",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-08",
            requirement="모형 위험관리위원회 — 거버넌스 조직",
            description="이사회·CRO 산하 AI 모형 위험관리 거버넌스 체계 구축.",
            aigis_feature="컴플라이언스 리포트로 위원회 보고자료 자동 생성.",
            status="user_responsibility",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-09",
            requirement="데이터 거버넌스 — 출처·계보 관리",
            description="학습·운영 데이터의 출처·가공이력·접근권한 관리.",
            aigis_feature="scan_rag_context()로 RAG 검색 결과 출처 추적. Activity Stream "
            "delegation_chain으로 데이터 흐름 가시화.",
            status="partial",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-10",
            requirement="보안 — 모형 도난·역공학 방지",
            description="모델 추출 공격(Model Extraction), 멤버십 추론 공격(Membership "
            "Inference) 등에 대한 방어.",
            aigis_feature="시스템 프롬프트 추출 패턴(pi_ko_system_prompt 등) + 출력 PII "
            "패턴으로 모델 정보 유출 차단. 비정상 다량 쿼리 패턴 탐지.",
            status="covered",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-11",
            requirement="외부 위탁 — 제3자 AI 서비스 평가",
            description="외부 AI(클라우드 LLM 등) 위탁 시 보안·컴플라이언스 평가. 위탁계약·"
            "감독 의무.",
            aigis_feature="외부 LLM 호출 감지·로깅 + 한국 PII 검출 시 국외 LLM 차단 정책 "
            "(kr_finance.yaml).",
            status="covered",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-12",
            requirement="소비자 보호 — 약관·고지",
            description="AI 기반 서비스 이용 시 AI 사용 사실·범위·한계를 약관에 명시·고지.",
            aigis_feature="해당 없음 — 약관 작성은 사용자 책임.",
            status="user_responsibility",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-13",
            requirement="운영리스크 — 시스템 장애 대응",
            description="AI 시스템 장애 시 폴백·BCP 계획.",
            aigis_feature="Aigis 자체 장애 시 fail-open/fail-closed 정책 선택 가능 "
            "(Policy Engine).",
            status="partial",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-14",
            requirement="감독당국 보고 — 사고/중대 변경",
            description="AI 관련 중대 사고·모델 중대 변경은 금감원 보고.",
            aigis_feature="alerts 로그 + 사고 보고서 자동 생성 (aig report --format markdown).",
            status="covered",
            notes="실제 보고는 사용자 책임.",
        ),
        ComplianceItem(
            regulation="금융분야 AI 가이드라인 (금융위)",
            requirement_id="FSC-AI-15",
            requirement="기록 보존 — 모형/판단 근거 보관",
            description="AI 의사결정의 입력·출력·판단 근거를 일정 기간(최소 5년) 보존.",
            aigis_feature="감사 로그 100% 기록. aig maintenance --retention-days 1825로 5년 "
            "보존 정책 설정 가능. CSV/Excel 내보내기로 외부 백업 지원.",
            status="covered",
        ),
        # ================================================================
        # 전자금융감독규정 (금융감독원)
        # ================================================================
        ComplianceItem(
            regulation="전자금융감독규정",
            requirement_id="EFR-01",
            requirement="정보처리시스템 보호조치 (제13조)",
            description="전자금융업자·금융회사는 정보처리시스템 보호를 위한 기술적·물리적·"
            "관리적 보호조치 의무.",
            aigis_feature="LLM 경로상의 보안 통제(입력 필터·출력 필터·정책 엔진) 제공. "
            "감사 로그로 보호조치 운영 증적.",
            status="covered",
        ),
        ComplianceItem(
            regulation="전자금융감독규정",
            requirement_id="EFR-02",
            requirement="망분리 (제15조)",
            description="내부망과 외부망의 물리적·논리적 분리. 인터넷 PC와 업무 PC 분리.",
            aigis_feature="해당 없음 — 네트워크 인프라 요건. 단, Aigis는 zero-dependency·"
            "self-hosted 동작으로 망분리 환경에서도 운영 가능.",
            status="user_responsibility",
            notes="Aigis는 인터넷 미연결 환경에서 정상 동작 (offline mode).",
        ),
        ComplianceItem(
            regulation="전자금융감독규정",
            requirement_id="EFR-03",
            requirement="전자금융사고 보고 (제73조)",
            description="전자금융사고 발생 인지 후 즉시 금감원장에 보고 (영업일 익일까지). "
            "사고원인·피해규모·대응조치 보고서 작성.",
            aigis_feature="LLM 보안 사고 alerts 로그 + 자동 사고 보고서 생성 "
            "(aig report --format markdown).",
            status="covered",
        ),
        ComplianceItem(
            regulation="전자금융감독규정",
            requirement_id="EFR-04",
            requirement="백업 및 복구 (제23조)",
            description="중요 정보·시스템의 백업 및 재해복구 체계 구축.",
            aigis_feature="감사 로그 자동 회전·압축·아카이브. 글로벌 집계로 다중 프로젝트 "
            "백업 중앙화 가능.",
            status="partial",
        ),
        ComplianceItem(
            regulation="전자금융감독규정",
            requirement_id="EFR-05",
            requirement="외부 전산자원 이용 (제14조의2) — 클라우드·제3자 AI",
            description="클라우드·외부 AI 서비스 이용 시 사전 평가·계약·감독 의무. "
            "중요업무 클라우드 전환 시 금감원 사전 보고.",
            aigis_feature="외부 LLM 호출 시 자동 감지 + Policy Engine으로 사전 평가 없는 "
            "엔드포인트 차단. 감사 로그로 외부자원 이용 이력 추적.",
            status="covered",
        ),
        # ================================================================
        # ISMS-P 인증기준 (정보보호 및 개인정보보호 관리체계, 2023년 개정)
        # — AI 관련 통제항목 중심
        # ================================================================
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.6",
            requirement="접근 통제 — AI 시스템 접근권한 (2.6.1~2.6.7)",
            description="사용자·시스템 계정 관리, 접근권한 부여·변경·말소, 인증·승인.",
            aigis_feature="Policy Engine으로 사용자/부서/자율성 레벨별 접근 정책 설정. "
            "audit log로 접근 이력 추적.",
            status="covered",
        ),
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.7",
            requirement="암호 통제 — 학습데이터·모델 암호화 (2.7.1~2.7.2)",
            description="중요정보의 저장·전송 시 암호화. 암호키 관리.",
            aigis_feature="해당 없음 — 저장·전송 암호화는 시스템 인프라 책임. 단, Aigis 감사 "
            "로그 자체는 SHA-256 무결성 해시 보장.",
            status="user_responsibility",
        ),
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.8",
            requirement="정보시스템 도입 및 개발보안 — AI 모델 개발 시 보안 검증 (2.8.1~2.8.6)",
            description="시스템 개발·도입 시 보안 요구사항 정의·구현·시험. 외주 개발 보안.",
            aigis_feature="aig benchmark + aig redteam으로 AI 모델 보안 시험. CI/CD 연계 "
            "(.pre-commit-hooks.yaml) 가능.",
            status="covered",
        ),
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.9",
            requirement="시스템 및 서비스 운영관리 — AI 모델 변경관리 (2.9.1~2.9.7)",
            description="변경관리, 성능 모니터링, 백업, 로그관리, 시각 동기화, 정보자산 변경.",
            aigis_feature="aig monitor 실시간 운영 가시화. 감사 로그 자동 회전·압축.",
            status="covered",
        ),
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.10",
            requirement="시스템 및 서비스 보안관리 — 침입탐지·패치 (2.10.1~2.10.9)",
            description="보안시스템 운영, 클라우드 보안, 공개서버 보안, 전자거래·핀테크 보안, "
            "정보전송 보안, 업무용 단말기 보안, 보조저장매체 관리, 패치관리, 악성코드 통제.",
            aigis_feature="LLM 트래픽 침입 탐지(64+ 패턴, 한국어 4개 PI 포함). 패턴 업데이트는 "
            "SDK 버전업으로 배포.",
            status="covered",
        ),
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.11",
            requirement="사고 예방 및 대응 — AI 보안 사고 (2.11.1~2.11.5)",
            description="사고 예방·대응 체계, 취약점 점검, 이상행위 분석, 사고 대응훈련, 사고 "
            "대응 및 복구.",
            aigis_feature="alerts 로그 + Slack/Webhook 알림 + 자동 보고서 생성. "
            "adversarial-loop로 분기별 보안훈련 자동화.",
            status="covered",
        ),
        ComplianceItem(
            regulation="ISMS-P 인증기준",
            requirement_id="ISMS-P-2.12",
            requirement="재해복구 — AI 서비스 BCP (2.12.1~2.12.2)",
            description="재해·재난 대비 IT 재해복구 체계, 시험 및 유지관리.",
            aigis_feature="Aigis fail-open/fail-closed 정책으로 장애 시 안전한 폴백.",
            status="partial",
        ),
    ]
