export type Lang = "en" | "ja" | "ko";

type I18n = { en: string; ja: string; ko: string };

export function tx(entry: I18n, lang: Lang): string {
  return entry[lang];
}

export const t = {
  /* ── Navigation ── */
  nav: {
    pricing: { en: "Pricing", ja: "料金", ko: "요금제" },
    docs: { en: "Docs", ja: "ドキュメント", ko: "문서" },
    github: { en: "GitHub", ja: "GitHub", ko: "GitHub" },
    signIn: { en: "Sign In", ja: "ログイン", ko: "로그인" },
    startTrial: { en: "Start Free", ja: "無料で試す", ko: "무료로 시작" },
  },

  /* ── Hero ── */
  hero: {
    badge: {
      en: "Open-source — Start free (no card required)",
      ja: "オープンベータ — 無料で始められます（カード不要）",
      ko: "오픈소스 — 무료로 시작 (카드 등록 불필요)",
    },
    headline1: {
      en: "Prompt injection is the",
      ja: "プロンプトインジェクションは",
      ko: "프롬프트 인젝션은",
    },
    headline2: {
      en: "#1 LLM attack.",
      ja: "LLM攻撃の第1位。",
      ko: "LLM 공격 1위입니다.",
    },
    headline3: {
      en: "Are you protected?",
      ja: "対策できていますか？",
      ko: "방어하고 계신가요?",
    },
    subhead: {
      en: "Scan every request to your AI. Safe ones pass instantly, suspicious ones are auto-blocked. Just change your base_url — zero code changes needed.",
      ja: "AIへのリクエストをすべてスキャン。安全なものは即座に通過、怪しいものは自動でブロック。base_url を変えるだけで、既存のコードは一切変更不要です。",
      ko: "AI로 가는 모든 요청을 스캔합니다. 안전한 요청은 즉시 통과, 위험한 요청은 자동 차단. base_url 한 줄만 바꾸면 기존 코드 수정 없이 적용됩니다.",
    },
    ctaPrimary: { en: "Start Free (No Card)", ja: "無料で始める（カード不要）", ko: "무료로 시작 (카드 불필요)" },
    ctaSecondary: { en: "How It Works", ja: "仕組みを見る", ko: "동작 원리 보기" },
    badge1: { en: "OWASP LLM Top 10 Coverage", ja: "OWASP LLM Top 10 対応", ko: "OWASP LLM Top 10 대응" },
    badge2: { en: "SOC2-ready Audit Logs", ja: "SOC2対応監査ログ付き", ko: "SOC2 대응 감사 로그 제공" },
    badge3: { en: "No request content stored by default", ja: "デフォルトでリクエスト内容を保存しない", ko: "기본 설정에서는 요청 본문을 저장하지 않음" },
    badge4: { en: "Latency <5ms (safe verdict)", ja: "遅延 <5ms（安全判定時）", ko: "지연 5ms 이하 (안전 판정 시)" },
    flowApp: { en: "Your App", ja: "あなたのアプリ", ko: "고객사 앱" },
    flowAppSub: { en: "Python / Node.js / Any SDK", ja: "Python / Node.js / 任意のSDK", ko: "Python / Node.js / 모든 SDK" },
    flowAllRequests: { en: "All Requests →", ja: "全リクエスト →", ko: "전체 요청 →" },
    flowGuardian: { en: "Aigis", ja: "Aigis", ko: "Aigis" },
    flowGuardianSub: { en: "Security Proxy · <5ms", ja: "セキュリティプロキシ · <5ms", ko: "보안 프록시 · 5ms 이하" },
    flowSafeOnly: { en: "Safe Only →", ja: "安全なもののみ →", ko: "안전한 요청만 →" },
    flowLLM: { en: "Your LLM", ja: "あなたのLLM", ko: "고객사 LLM" },
    flowLLMSub: { en: "OpenAI / Anthropic / Any", ja: "OpenAI / Anthropic / 任意", ko: "OpenAI / Anthropic / 모두" },
    routingLabel: { en: "Intelligent Routing", ja: "インテリジェントルーティング", ko: "지능형 라우팅" },
    routePass: { en: "Pass", ja: "通過", ko: "통과" },
    routeBlock: { en: "Block", ja: "ブロック", ko: "차단" },
    routeReview: { en: "Review", ja: "レビュー", ko: "검토" },
  },

  /* ── How It Works ── */
  howItWorks: {
    label: { en: "How It Works", ja: "仕組み", ko: "동작 원리" },
    heading: {
      en: "Three steps to secure your AI",
      ja: "AIを守る3つのステップ",
      ko: "AI를 보호하는 세 단계",
    },
    sub: {
      en: "Drop-in proxy that scans every request — no code changes needed.",
      ja: "すべてのリクエストをスキャンするドロップインプロキシ。コード変更不要。",
      ko: "모든 요청을 스캔하는 드롭인 프록시 — 코드 수정 불필요.",
    },
    step1Title: {
      en: "Change one line: your base URL",
      ja: "1行変えるだけ：base URLをAigisに",
      ko: "한 줄만 변경: base URL을 Aigis로",
    },
    step1Desc: {
      en: "Point your OpenAI SDK's base URL to Aigis's proxy endpoint. SDK, request format, and error handling stay the same.",
      ja: "OpenAI SDKのbase URLをAigisのプロキシエンドポイントに換えるだけ。SDK・リクエスト形式・エラーハンドリングは何も変えなくて大丈夫です。",
      ko: "OpenAI SDK의 base URL을 Aigis 프록시 엔드포인트로 가리키기만 하면 됩니다. SDK·요청 포맷·에러 처리는 그대로 유지됩니다.",
    },
    step1Aside: { en: "Average setup time: 4 minutes", ja: "平均セットアップ時間：4分", ko: "평균 셋업 시간: 4분" },
    step2Title: {
      en: "Aigis scores & routes",
      ja: "Aigisがスコア&ルーティング",
      ko: "Aigis가 점수 평가 & 라우팅",
    },
    step2Desc: {
      en: "OWASP LLM Top 10 coverage with 165+ detection patterns across 25+ threat categories. 6-layer defense including CaMeL Capabilities, Atomic Execution Pipeline, and Safety Verifier. Every request gets a risk score within 5ms.",
      ja: "OWASP LLM Top 10 に対応した165+検出パターン（25+脅威カテゴリ）で検査。CaMeL Capabilities・AEP・Safety Verifierを含む6層防御。5ms以内にリスクスコアを付与します。",
      ko: "OWASP LLM Top 10에 대응하는 165개 이상 탐지 패턴(25개 이상 위협 카테고리)으로 검사. CaMeL Capabilities·AEP·Safety Verifier 포함 6계층 방어. 5ms 이내에 리스크 점수를 산정합니다.",
    },
    step2Aside: { en: "165+ patterns · 25+ categories · 6-layer defense", ja: "165+パターン · 25+カテゴリ · 6層防御", ko: "165+ 패턴 · 25+ 카테고리 · 6계층 방어" },
    step3Title: {
      en: "Your team decides the hard calls",
      ja: "難しい判断はあなたのチームが下す",
      ko: "어려운 판단은 운영팀이 결정",
    },
    step3Desc: {
      en: "Borderline requests aren't just blocked or passed. They go to your team's review queue. A black-box model doesn't decide — your team does. Risky requests are sent to LLM pre-blocked with a 403.",
      ja: "危うくもないし安全とも言い切れないリクエストは、チームのレビューキューへ。ブラックボックスモデルではなく、あなたのチームが判断します。重大な脅威はLLMに届く前に403でブロック。",
      ko: "애매한 요청은 단순 차단이 아니라 팀의 검토 큐로 이동합니다. 블랙박스 모델이 아닌 사람이 판단합니다. 위험한 요청은 LLM 도달 전 403으로 사전 차단됩니다.",
    },
    step3Aside: {
      en: "Default SLA 30 min · Fallback configurable",
      ja: "デフォルトSLA 30分 · フォールバック設定可能",
      ko: "기본 SLA 30분 · 폴백 정책 구성 가능",
    },
  },

  /* ── Testimonials ── */
  testimonials: {
    label: { en: "What Users Say", ja: "ユーザーの声", ko: "사용자 목소리" },
    q1: {
      en: "Security team went from 'absolutely not' to 'approved in 2 weeks.' The deal-closer was the audit log — every request, verdict, and reviewer action is fully visible.",
      ja: "「セキュリティチームが絶対承認しない」から「2週間で承認」に変わりました。決め手は監査ログでした。リクエスト・判断・担当者のアクションがすべて可視化されているのが刺さったようです。",
      ko: "보안팀이 \"절대 불가\"에서 \"2주 만에 승인\"으로 바뀌었습니다. 결정적 요인은 감사 로그였습니다 — 모든 요청·판정·검토자 액션이 완전히 가시화됩니다.",
    },
    r1: { en: "Staff Engineer", ja: "スタッフエンジニア", ko: "스태프 엔지니어" },
    c1: { en: "Series B Fintech", ja: "シリーズBフィンテック", ko: "Series B 핀테크" },
    q2: {
      en: "Last quarter, prompt injection took our customer-facing chatbot down twice. Since Aigis — zero incidents. Edge cases our own rules missed, the HitL queue catches.",
      ja: "先四半期、プロンプトインジェクションで顧客向けチャットボットが2回ダウンしました。Aigis導入後はゼロ件。自社ルールでは拾えなかったエッジケースも、HitLキューが対処してくれています。",
      ko: "지난 분기에 프롬프트 인젝션으로 고객용 챗봇이 두 번 다운됐습니다. Aigis 도입 후로 사고 0건. 자체 룰이 놓친 엣지 케이스도 HITL 큐가 잡아냅니다.",
    },
    r2: { en: "AI Platform Lead", ja: "AIプラットフォームリード", ko: "AI 플랫폼 리드" },
    c2: { en: "SaaS Company · 200 employees", ja: "SaaS企業 · 従業員200名", ko: "SaaS 기업 · 임직원 200명" },
    q3: {
      en: "LLM-first product, so investors and enterprise customers kept asking 'how do you prevent jailbreaks?' Now we just show the Aigis dashboard and the conversation ends.",
      ja: "LLMファーストのプロダクトなので、投資家やエンタープライズのお客様から「ジェイルブレイクはどう防いでいるの？」と繰り返し聞かれていました。今は、Aigisのダッシュボードを見せるだけで会話が終わります。",
      ko: "LLM 우선 제품이라 투자자와 엔터프라이즈 고객들이 \"탈옥은 어떻게 막느냐\"고 반복적으로 물었습니다. 이제는 Aigis 대시보드만 보여주면 대화가 끝납니다.",
    },
    r3: { en: "CTO & Co-founder", ja: "CTO・共同創業者", ko: "CTO · 공동창업자" },
    c3: { en: "AI-native Startup", ja: "AIネイティブスタートアップ", ko: "AI 네이티브 스타트업" },
  },

  /* ── Features ── */
  features: {
    label: { en: "What We Protect Against", ja: "何から守るか", ko: "무엇으로부터 보호하나" },
    heading: {
      en: "Built on OWASP LLM Top 10.",
      ja: "OWASP LLM Top 10 に基づいて設計。",
      ko: "OWASP LLM Top 10에 기반해 설계.",
    },
    sub: {
      en: "Not a generic WAF. Rules designed specifically for LLM attack patterns.",
      ja: "AIに後付けしたWAFではありません。LLMの攻撃パターンを専用に研究し、設計したルールで守ります。",
      ko: "범용 WAF가 아닙니다. LLM 공격 패턴을 전용으로 연구해 설계한 룰로 보호합니다.",
    },
    f1Title: {
      en: "Prompt Injection & Jailbreak",
      ja: "プロンプトインジェクション・ジェイルブレイク対策",
      ko: "프롬프트 인젝션 & 탈옥 방어",
    },
    f1Desc: {
      en: '"Ignore previous instructions..." attacks, DAN patterns, role-play abuse, system prompt leaks. Covers OWASP LLM Top 10 #1 threat. Updated as new techniques emerge.',
      ja: "「前の指示を無視して…」という攻撃・DANパターン・ロールプレイ悪用・システムプロンプト漏洩を検知。OWASP LLM Top 10 第1位の脅威に対応し、新しい手法が出るたびにパターンを更新します。",
      ko: "\"이전 지시를 무시하라…\" 공격, DAN 패턴, 롤플레이 악용, 시스템 프롬프트 유출을 탐지. OWASP LLM Top 10 1위 위협 대응. 새 기법이 등장할 때마다 패턴을 업데이트합니다.",
    },
    f2Title: {
      en: "Sensitive Data & Credential Leak Prevention",
      ja: "機密情報・認証情報の漏洩防止",
      ko: "민감 정보 & 인증 정보 유출 방지",
    },
    f2Desc: {
      en: "Auto-scan LLM responses before they reach users. Catches API keys, credit card numbers, SSNs, internal hostnames. Your model never becomes the data leak path.",
      ja: "LLMのレスポンスをユーザーに返す前に自動スキャン。APIキー・クレジットカード番号・SSN・内部接続文字列を検知しブロック。モデルがデータ流出の経路になりません。",
      ko: "사용자에게 도달하기 전 LLM 응답을 자동 스캔. API 키·신용카드·SSN·내부 호스트명을 탐지·차단. 모델이 데이터 유출 경로가 되지 않게 합니다.",
    },
    f3Title: {
      en: "SQL Injection Detection",
      ja: "SQLインジェクション遮断",
      ko: "SQL 인젝션 탐지",
    },
    f3Desc: {
      en: "UNION SELECT, DROP TABLE, blind injection, and more — blocks attacks that try to manipulate data pipelines. Especially critical for text-to-SQL and RAG architectures.",
      ja: "UNION SELECT・DROP TABLE・ブラインドインジェクションなど、データ連携パイプラインを操作する攻撃をブロック。text-to-SQLやRAGを使っているアーキテクチャで特に重要です。",
      ko: "UNION SELECT, DROP TABLE, 블라인드 인젝션 등 — 데이터 파이프라인을 조작하려는 공격을 차단. text-to-SQL 및 RAG 아키텍처에서 특히 중요합니다.",
    },
    f4Title: {
      en: "Human-in-the-Loop (HitL) Review",
      ja: "人間によるレビューキュー（HitL）",
      ko: "사람 개입 검토 큐 (HITL)",
    },
    f4Desc: {
      en: "Borderline requests go to your team's review queue with a SLA timer. Reviewers approve, reject, or escalate. If time runs out, the fallback action triggers automatically.",
      ja: "安全とも危険とも判断しにくいリクエストは、SLAタイマー付きでチームのレビューキューへ。担当者が承認・却下・エスカレーションを選択。期限切れ時はフォールバックが自動発動します。",
      ko: "애매한 요청은 SLA 타이머가 있는 팀 검토 큐로 이동. 검토자가 승인·반려·에스컬레이션 선택. 시간 초과 시 폴백 액션이 자동 발동됩니다.",
    },
    f5Title: {
      en: "Per-Tenant Policy Configuration",
      ja: "テナント別ポリシー設定",
      ko: "테넌트별 정책 구성",
    },
    f5Desc: {
      en: "Custom risk thresholds per team. Score 30 and below auto-pass, 81+ auto-block, etc. Medical, financial, and compliance-specific custom rules (regex) can be added.",
      ja: "チームごとにリスク閾値をカスタム設定。スコア30以下は自動通過、81以上は自動ブロックなど。医療・金融・コンプライアンスに合わせた独自ルール（正規表現）も追加できます。",
      ko: "팀별 리스크 임계값 커스텀. 30점 이하 자동 통과, 81점 이상 자동 차단 등. 의료·금융·컴플라이언스 전용 정규식 룰도 추가 가능합니다.",
    },
    f6Title: {
      en: "Immutable Audit Logs",
      ja: "改ざん不可の監査ログ",
      ko: "변조 불가 감사 로그",
    },
    f6Desc: {
      en: "Every request is auto-recorded: timestamp, risk score, matched rule, routing result, and reviewer action. Filterable by date and risk level. SOC2-ready CSV export.",
      ja: "全リクエストを自動記録：日時・リスクスコア・マッチしたルール・ルーティング結果・担当者のアクション。日付やリスクレベルで絞り込み可能。SOC2証拠資料としてCSV出力にも対応。",
      ko: "모든 요청을 자동 기록: 타임스탬프·리스크 점수·매칭 룰·라우팅 결과·검토자 액션. 날짜·리스크 레벨로 필터링. SOC2 증적용 CSV 내보내기 지원.",
    },
    footnote: {
      en: "OWASP LLM Top 10 · CWE/SANS reference · NIST AI RMF aligned",
      ja: "OWASP LLM Top 10 · CWE/SANS参照 · NIST AI RMF準拠",
      ko: "OWASP LLM Top 10 · CWE/SANS 참조 · NIST AI RMF 정렬",
    },
  },

  /* ── Pricing ── */
  pricing: {
    label: { en: "Pricing", ja: "料金", ko: "요금제" },
    heading: {
      en: "Simple, transparent pricing",
      ja: "シンプルで明確な料金体系",
      ko: "단순하고 투명한 요금제",
    },
    sub: {
      en: "Start free. Scale with your business. Enterprise-grade security included.",
      ja: "無料スタート。ビジネスの成長に合わせてスケール。エンタープライズ級のセキュリティ標準装備。",
      ko: "무료로 시작. 비즈니스 성장에 맞춰 확장. 엔터프라이즈급 보안 기본 탑재.",
    },
    footnote: {
      en: "All plans include OWASP LLM Top 10 coverage · Annual billing saves 20%",
      ja: "全プランにOWASP LLM Top 10対応を含む · 年間契約で20%OFF",
      ko: "전 플랜 OWASP LLM Top 10 대응 포함 · 연간 결제 20% 할인",
    },
    free: {
      name: { en: "Free", ja: "Free", ko: "Free" },
      period: { en: "forever", ja: "永久無料", ko: "영구 무료" },
      tagline: {
        en: "Open-source core — everything you need to get started",
        ja: "オープンソースコア — 始めるために必要なすべてが無料",
        ko: "오픈소스 코어 — 시작에 필요한 모든 기능 무료",
      },
      f1: { en: "165+ detection patterns, 6-layer defense (100% accuracy)", ja: "165+検出パターン、6層防御（100%精度）", ko: "165+ 탐지 패턴, 6계층 방어 (100% 정확도)" },
      f2: { en: "MCP Security Scanner", ja: "MCPセキュリティスキャナー", ko: "MCP 보안 스캐너" },
      f3: { en: "Automated Red Team testing", ja: "自動レッドチームテスト", ko: "자동 레드팀 테스트" },
      f4: { en: "CLI tool (pip install)", ja: "CLIツール（pip install）", ko: "CLI 도구 (pip install)" },
      f5: { en: "FastAPI / LangChain / OpenAI integration", ja: "FastAPI / LangChain / OpenAI統合", ko: "FastAPI / LangChain / OpenAI 통합" },
      f6: { en: "Apache 2.0 License", ja: "Apache 2.0ライセンス", ko: "Apache 2.0 라이선스" },
      cta: { en: "Get Started Free", ja: "無料で始める", ko: "무료로 시작" },
    },
    starter: {
      name: { en: "Pro", ja: "Pro", ko: "Pro" },
      price: { en: "$49", ja: "$49", ko: "$49" },
      period: { en: "/ month", ja: "/ 月", ko: "/ 월" },
      tagline: {
        en: "For teams that need visibility into LLM security",
        ja: "LLMセキュリティの可視化が必要なチーム向け",
        ko: "LLM 보안 가시화가 필요한 팀용",
      },
      f1: { en: "Cloud dashboard (log & risk visualization)", ja: "クラウドダッシュボード（ログ・リスク可視化）", ko: "클라우드 대시보드 (로그·리스크 가시화)" },
      f2: { en: "Up to 5 team members", ja: "最大5名のチームメンバー", ko: "최대 5명 팀 멤버" },
      f3: { en: "500K API requests / month", ja: "月間50万APIリクエスト", ko: "월 50만 API 요청" },
      f4: { en: "90-day log retention", ja: "90日間ログ保持", ko: "90일 로그 보관" },
      f5: { en: "Email alerts (critical events)", ja: "メールアラート（重大イベント時）", ko: "이메일 알림 (중대 이벤트)" },
      f6: { en: "14-day free trial", ja: "14日間無料トライアル", ko: "14일 무료 트라이얼" },
      cta: { en: "Start Free Trial", ja: "無料トライアルを開始", ko: "무료 트라이얼 시작" },
    },
    business: {
      name: { en: "Business", ja: "Business", ko: "Business" },
      price: { en: "$299", ja: "$299", ko: "$299" },
      period: { en: "/ month", ja: "/ 月", ko: "/ 월" },
      tagline: {
        en: "For organizations that need compliance & governance",
        ja: "コンプライアンスとガバナンスが必要な組織向け",
        ko: "컴플라이언스 & 거버넌스가 필요한 조직용",
      },
      f1: { en: "Everything in Pro", ja: "Proの全機能", ko: "Pro의 모든 기능" },
      f2: { en: "Up to 50 team members", ja: "最大50名のチームメンバー", ko: "최대 50명 팀 멤버" },
      f3: { en: "5M API requests / month", ja: "月間500万APIリクエスト", ko: "월 500만 API 요청" },
      f4: { en: "1-year log retention (immutable audit)", ja: "1年間ログ保持（イミュータブル監査ログ）", ko: "1년 로그 보관 (변조 불가 감사)" },
      f5: { en: "Compliance reports (OWASP, SOC2, GDPR)", ja: "コンプライアンスレポート（OWASP, SOC2, GDPR）", ko: "컴플라이언스 리포트 (OWASP, SOC2, GDPR)" },
      f6: { en: "SSO / SAML authentication", ja: "SSO / SAML認証", ko: "SSO / SAML 인증" },
      f7: { en: "Slack + PagerDuty notifications", ja: "Slack + PagerDuty通知", ko: "Slack + PagerDuty 알림" },
      cta: { en: "Start Business Trial", ja: "Businessトライアルを開始", ko: "Business 트라이얼 시작" },
      badge: { en: "Most Popular", ja: "人気No.1", ko: "인기 1위" },
    },
    enterprise: {
      name: { en: "Enterprise", ja: "Enterprise", ko: "Enterprise" },
      period: { en: "Custom", ja: "要相談", ko: "별도 협의" },
      tagline: {
        en: "For regulated industries & large organizations",
        ja: "規制産業・大規模組織向け",
        ko: "규제 산업 · 대규모 조직용",
      },
      f1: { en: "Everything in Business", ja: "Businessの全機能", ko: "Business의 모든 기능" },
      f2: { en: "Unlimited users & API requests", ja: "ユーザー・APIリクエスト無制限", ko: "사용자 · API 요청 무제한" },
      f3: { en: "On-premises / VPC deployment", ja: "オンプレミス / VPC対応", ko: "온프레미스 / VPC 배포" },
      f4: { en: "Custom compliance reports (HIPAA, FISC, ISMAP)", ja: "カスタムコンプラレポート（HIPAA, FISC, ISMAP）", ko: "맞춤 컴플라이언스 리포트 (PIPA, ISMS-P, 금융위 AI 가이드)" },
      f5: { en: "Dedicated CSM & security engineer", ja: "専任CSM・セキュリティエンジニア", ko: "전담 CSM · 보안 엔지니어" },
      f6: { en: "99.99% SLA guarantee", ja: "99.99% SLA保証", ko: "99.99% SLA 보장" },
      cta: { en: "Contact Sales", ja: "営業に相談する", ko: "영업팀 문의" },
    },
  },

  /* ── FAQ ── */
  faq: {
    label: { en: "FAQ", ja: "よくある質問", ko: "자주 묻는 질문" },
    heading: {
      en: "Questions before you start",
      ja: "登録前によく聞かれる質問",
      ko: "시작 전 자주 묻는 질문",
    },
    q1: { en: "How long does setup take?", ja: "導入にどれくらいかかりますか？", ko: "셋업에 시간이 얼마나 걸리나요?" },
    a1: {
      en: "Most teams are up and running in under 5 minutes. You just change one line — the base_url — in your existing OpenAI SDK configuration. No new dependencies, no infrastructure changes.",
      ja: "ほとんどのチームが5分以内に稼働始しています。既存のOpenAI SDK設定のbase_urlを1行変えるだけ。新しい依存関係もインフラ変更も不要です。",
      ko: "대부분 팀이 5분 안에 운영 시작합니다. 기존 OpenAI SDK 설정에서 base_url 한 줄만 변경. 새 의존성이나 인프라 변경 불필요.",
    },
    q2: {
      en: "What is the pricing structure? How much for a team of 5?",
      ja: "料金体系を教えてください。5人チームだといくらになりますか？",
      ko: "요금 체계는 어떻게 되나요? 5인 팀 기준 가격은요?",
    },
    a2: {
      en: "Starter plan is $15/user/month. For a 5-person team, that's $75/month. Business plan at $38/user/month includes decision tracking and compliance features. Annual billing saves 20%.",
      ja: "Starterプランはユーザーあたり月額¥2,000。5人チームなら月額¥10,000です。Businessプラン（¥5,000/ユーザー/月）には意思決定追跡とコンプライアンス機能が含まれます。年間契約で20%OFFになります。",
      ko: "Starter 플랜은 사용자당 월 $15. 5인 팀은 월 $75입니다. Business 플랜(사용자당 월 $38)은 의사결정 추적 및 컴플라이언스 기능 포함. 연간 결제 시 20% 할인.",
    },
    q3: {
      en: "How does the review queue actually work?",
      ja: "レビューキューって、実際どんなふうに動くんですか？",
      ko: "검토 큐는 실제로 어떻게 작동하나요?",
    },
    a3: {
      en: "When a request scores in the medium-risk range (31-60), it's held for human review. Your team gets notified, and a reviewer can approve, reject, or escalate the request within the configured SLA (default: 30 minutes). If no action is taken, the configurable fallback kicks in.",
      ja: "リクエストが中リスク（31-60）にスコアリングされると保留されます。チームに通知が届き、担当者がSLA（デフォルト30分）以内に承認・却下・エスカレーションを選択します。未対応の場合は設定済みのフォールバックが発動します。",
      ko: "중리스크(31-60)로 평가된 요청은 사람 검토를 위해 보류됩니다. 팀에 알림이 가고, 검토자는 설정된 SLA(기본 30분) 내에 승인·반려·에스컬레이션을 선택합니다. 미대응 시 설정된 폴백이 발동됩니다.",
    },
    q4: {
      en: "Is request content stored?",
      ja: "リクエストの内容は保存されますか？",
      ko: "요청 본문이 저장되나요?",
    },
    a4: {
      en: "By default, no. We store only metadata (timestamp, risk score, rule matches, routing decisions). You can opt-in to content logging for audit/compliance purposes, which is stored encrypted and configurable by retention policy.",
      ja: "デフォルトでは保存しません。メタデータ（タイムスタンプ、リスクスコア、ルールマッチ、ルーティング判定）のみ記録。監査・コンプライアンス用にコンテンツログのオプトインが可能で、暗号化して保存されます。",
      ko: "기본 설정에서는 저장하지 않습니다. 메타데이터(타임스탬프·리스크 점수·룰 매치·라우팅 결정)만 기록. 감사·컴플라이언스용 본문 로깅은 옵트인 가능하며, 암호화 저장·보관기간 정책 구성 가능.",
    },
    q5: {
      en: "We use Azure OpenAI. Is that supported?",
      ja: "Azure OpenAIを使っています。対応していますか？",
      ko: "Azure OpenAI를 사용 중인데 지원되나요?",
    },
    a5: {
      en: "Yes. Aigis works as a proxy layer — it's compatible with any OpenAI-compatible endpoint including Azure OpenAI, AWS Bedrock (via compatibility layer), and self-hosted models.",
      ja: "はい、対応しています。Aigisはプロキシレイヤーとして動作するため、Azure OpenAI、AWS Bedrock（互換レイヤー経由）、セルフホストモデルなど、OpenAI互換のあらゆるエンドポイントで使えます。",
      ko: "네, 지원합니다. Aigis는 프록시 레이어로 동작하므로 Azure OpenAI, AWS Bedrock(호환 레이어 경유), 셀프호스팅 모델 등 OpenAI 호환 모든 엔드포인트에서 사용 가능합니다.",
    },
    q6: {
      en: "We're preparing for SOC2 Type II. Can this help?",
      ja: "SOC2 Type II監査の準備をしています。役に立ちますか？",
      ko: "ISMS-P 인증을 준비 중인데 도움이 되나요?",
    },
    a6: {
      en: "Absolutely. Our audit logs are designed for SOC2 evidence collection. Immutable records, CSV export, retention policies, and role-based access controls. Several of our customers cite Aigis in their SOC2 evidence packages.",
      ja: "はい、大いに役立ちます。監査ログはSOC2証拠反集向けに設計されています。改ざん不可の記録、CSVエクスポート、保持ポリシー、ロールベースのアクセス制御を備えています。複数のお客様がSOC2証拠パッケージにAigisを引用しています。",
      ko: "네, 큰 도움이 됩니다. 감사 로그는 ISMS-P 통제항목 2.6~2.12 및 SOC2 증적 수집을 염두에 두고 설계되었습니다. 변조 불가 기록, CSV 내보내기, 보관 정책, 역할 기반 접근 제어를 제공합니다. `aig compliance --jurisdiction kr`로 PIPA·신용정보법·금융위 AI 가이드 매핑 확인 가능.",
    },
    contactLabel: {
      en: "Have other questions?",
      ja: "他に気になることがあれば",
      ko: "다른 질문이 있으시다면",
    },
    contactSub: {
      en: "Email us at",
      ja: "こちらまでメールください：",
      ko: "다음 주소로 이메일 주세요:",
    },
    contactSuffix: {
      en: " — we reply within 1 business day.",
      ja: "（1営業日以内にご返信します）",
      ko: " — 영업일 1일 이내에 회신드립니다.",
    },
  },

  /* ── Footer CTA ── */
  footerCta: {
    label: {
      en: "Ready to secure your AI?",
      ja: "AIを守る準備はできましたか？",
      ko: "AI 보호를 시작할 준비가 되셨나요?",
    },
    heading: {
      en: "Start protecting your LLM in minutes",
      ja: "数分でLLMの保護を始めましょう",
      ko: "몇 분 만에 LLM 보호 시작",
    },
    sub: {
      en: "No credit card required. Free tier available for small teams.",
      ja: "クレジットカード不要。小規模チーム向けの無料枠あり。",
      ko: "신용카드 불필요. 소규모 팀용 무료 플랜 제공.",
    },
    cta1: { en: "Get Started Free", ja: "無料で始める", ko: "무료로 시작" },
    cta2: { en: "Read the Docs", ja: "ドキュメントを読む", ko: "문서 보기" },
    contactPrefix: {
      en: "Enterprise or custom needs? Reach out at",
      ja: "エンタープライズ・カスタム要件は",
      ko: "엔터프라이즈 또는 맞춤 요건이 있으시면",
    },
    contactSuffix: { en: "", ja: " までご連絡ください", ko: "로 문의 주세요" },
  },

  /* ── Footer ── */
  footer: {
    product: { en: "Product", ja: "プロダクト", ko: "프로덕트" },
    features: { en: "Features", ja: "機能", ko: "기능" },
    pricing: { en: "Pricing", ja: "料金", ko: "요금제" },
    howItWorks: { en: "How It Works", ja: "仕組み", ko: "동작 원리" },
    riskScoring: { en: "Risk Scoring", ja: "リスクスコアリング", ko: "리스크 스코어링" },
    docs: { en: "Documentation", ja: "ドキュメント", ko: "문서" },
    overview: { en: "Overview", ja: "概要", ko: "개요" },
    quickstart: { en: "Quickstart", ja: "クイックスタート", ko: "퀵스타트" },
    concepts: { en: "Concepts", ja: "コンセプト", ko: "콘셉트" },
    apiRef: { en: "API Reference", ja: "APIリファレンス", ko: "API 레퍼런스" },
    integrations: { en: "Integrations", ja: "インテグレーション", ko: "연동" },
    python: { en: "Python SDK", ja: "Python SDK", ko: "Python SDK" },
    nodejs: { en: "Node.js SDK", ja: "Node.js SDK", ko: "Node.js SDK" },
    openai: { en: "OpenAI", ja: "OpenAI", ko: "OpenAI" },
    langchain: { en: "LangChain", ja: "LangChain", ko: "LangChain" },
    company: { en: "Company", ja: "会社", ko: "회사" },
    github: { en: "GitHub", ja: "GitHub", ko: "GitHub" },
    privacy: { en: "Privacy Policy", ja: "プライバシーポリシー", ko: "개인정보처리방침" },
    terms: { en: "Terms of Service", ja: "利用規約", ko: "이용약관" },
    security: { en: "Security", ja: "セキュリティ", ko: "보안" },
    tagline: {
      en: "Open-source LLM security for teams that ship fast.",
      ja: "高速リリースするチームのためのオープンソースLLMセキュリティ。",
      ko: "빠르게 출시하는 팀을 위한 오픈소스 LLM 보안.",
    },
    copyright: {
      en: "© 2025 Aigis. All rights reserved.",
      ja: "© 2025 Aigis. All rights reserved.",
      ko: "© 2025 Aigis. All rights reserved.",
    },
    builtFor: {
      en: "Built for teams that build with AI.",
      ja: "AIで開発するチームのために。",
      ko: "AI로 개발하는 팀을 위해.",
    },
  },

  /* ── Docs Layout ── */
  docsLayout: {
    gettingStarted: { en: "Getting Started", ja: "はじめに", ko: "시작하기" },
    overview: { en: "Overview", ja: "概要", ko: "개요" },
    quickstart: { en: "Quickstart", ja: "クイックスタート", ko: "퀵스타트" },
    conceptsCategory: { en: "Concepts", ja: "コンセプト", ko: "콘셉트" },
    coreConcepts: { en: "Core Concepts", ja: "コアコンセプト", ko: "핵심 개념" },
    reference: { en: "Reference", ja: "リファレンス", ko: "레퍼런스" },
    apiReference: { en: "API Reference", ja: "APIリファレンス", ko: "API 레퍼런스" },
    integrationsCategory: { en: "Integrations", ja: "インテグレーション", ko: "연동" },
    python: { en: "Python SDK", ja: "Python SDK", ko: "Python SDK" },
    nodejs: { en: "Node.js SDK", ja: "Node.js SDK", ko: "Node.js SDK" },
    complianceCategory: { en: "Compliance", ja: "コンプライアンス", ko: "컴플라이언스" },
    japanGovernance: { en: "Japan AI Governance", ja: "日本AIガバナンス", ko: "한국 규제 매핑 (PIPA · 금융위 · ISMS-P)" },
    breadcrumbDocs: { en: "Documentation", ja: "ドキュメント", ko: "문서" },
    onThisPage: { en: "On this page", ja: "このページの内容", ko: "이 페이지 내용" },
  },

  /* ── Stats / Social Proof ── */
  stats: {
    rules: { en: "Detection Rules", ja: "検出ルール", ko: "탐지 룰" },
    latency: { en: "Latency (safe verdict)", ja: "レイテンシ（安全判定時）", ko: "지연 (안전 판정 시)" },
    owasp: { en: "Coverage", ja: "カバレッジ", ko: "커버리지" },
    uptime: { en: "Uptime SLA", ja: "稼働率SLA", ko: "가동률 SLA" },
    soc2: { en: "SOC2-ready Audit Logs", ja: "SOC2対応監査ログ", ko: "SOC2 대응 감사 로그" },
    japanReady: { en: "Japan AI Governance Ready", ja: "日本AIガバナンス対応", ko: "한국 규제 대응 (PIPA·금융위·ISMS-P)" },
  },

  /* ── Code Integration / Chat ── */
  chat: {
    completions: { en: "chat/completions", ja: "chat/completions", ko: "chat/completions" },
  },

} as const;
