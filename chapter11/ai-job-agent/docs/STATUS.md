# STATUS — 현재 진행 현황

> **매번 작업 시작 시 가장 먼저 읽는 문서입니다.** 이 문서만 읽고도 "다음에 뭘 해야 하는지"가 보여야 합니다.
> 읽기 순서는 [README.md](./README.md) 참고. 전체 사양은 [SPEC.md](./SPEC.md), 실행 상세는 [GUIDE.md](./GUIDE.md).

## 마지막 갱신

- 시각: 2026-10-05 (한국시간 기준으로 기록 — 정확한 시·분은 기록하지 않음, 날짜 단위로만 관리)
- 갱신한 이: Claude Code — **잡코리아 알림을 실제로 시험 발송하고(Slack·Gmail 둘 다 실제 성공), 채널별
  중복 발송 방지 이력 체계를 구현했으며, 금요일 09:10 KST 예약(schedule)을 활성화했다.** (이전의
  Greenhouse 구현·3건 시험 발송·잡코리아 전환 경위는 아래 각 섹션과 `docs/WORK_LOG.md`에 상세 기록됨 —
  여기서는 가장 최근 변경만 요약한다.)
  - `src/analyze.py`에 **채널별(Slack/Gmail) 알림 이력 관리**를 새로 추가:
    `load_jobkorea_notification_history`/`annotate_notification_pending`/
    `update_jobkorea_notification_history`. "신규(첫 발견)"과 "이 채널로 아직 성공 발송한 적 없음"을
    분리해, 한 채널만 실패해도 그 채널에만 다음에 다시 보낼 수 있게 했다(성공한 채널에는 중복 발송 안 함).
  - `src/notify.py`: 예외가 밖으로 새지 않도록 Slack/Gmail 전송을 `try/except`로 감싸고, `is_success()`
    헬퍼로 성공 여부를 일관되게 판단하도록 변경.
  - `main.py`: 채널별로 "발송 대상 없음"이면 실제 호출 자체를 건너뛰고, 성공/실패를 각각 기록하며,
    `--live`일 때만 이력 파일(`history_jobkorea_ai_ax.csv`)을 갱신하도록 재구성.
  - **실제 `--live` 실행 결과(2026-10-05)**: 잡코리아 'AI 엔지니어' 검색 목록 25건 중 제목 스크리닝
    통과 11건 전부 신규 → **Slack 실제 발송 성공(200/ok), Gmail 실제 발송 성공(sent)** → 이력 파일에
    11건 전부 `slack_notified_at`/`gmail_notified_at` 기록됨. 직후 dry-run 재실행으로 같은 11건이
    두 채널 모두 "발송 대상 0건"으로 정확히 걸러짐을 확인(중복 방지 검증 완료).
  - `.github/workflows/ai-job-agent-weekly-report.yml`의 **`schedule` 트리거를 주석 해제해 활성화**
    (매주 금요일 00:10 UTC = 09:10 KST). `GEMINI_API_KEY`는 필수 Secrets 검증에서 제외(잡코리아 트랙은
    Gemini 불필요). **main 반영 PR이 merge되기 전까지는 실제로 동작하지 않는다.**

## 경로 상태 (가장 중요)

| 항목 | 값 | 근거 |
|---|---|---|
| **최종 프로젝트 루트 확정 여부** | **확정: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`** | 사용자 결정(이번 세션) |
| 새 Python 환경(.venv)이 있는 경로 | `C:\dev\claude-code-agent-course\chapter11\ai-job-agent` | 이번 로컬 확인(이번 세션에서 생성·검증) |
| 과거 환경(.venv)이 있던 경로 — 보존만 함, 더 이상 사용 안 함 | `C:\dev\claude-code-agent-course\chapter11\ax-job-agent` | 이번 로컬 확인. 삭제하지 않고 그대로 둠 |

→ 경로 불일치는 해결되었습니다. 이제 `<PROJECT_ROOT>` = `chapter11/ai-job-agent`로 모든 문서를 읽습니다.
과거 `ax-job-agent`는 참고용으로만 남아 있으며, 이후 작업은 전부 `ai-job-agent`에서 진행합니다.

## 브랜치 / 저장소

- 저장소 루트: `C:\dev\claude-code-agent-course`
- 현재 Git 브랜치: `ax-job-agent` (이번 로컬 확인, `git status` 결과 작업 트리 clean)
- 저장소 루트에 `AGENTS.md`/`CLAUDE.md` 없음(이번 로컬 확인). `chapter06`/`chapter07`의 `starter/CLAUDE.md`는
  각 챕터 실습용이며 이 프로젝트와 무관.
- `chapter11` 아래에는 `ax-job-agent`(내용물: `.venv`만 존재)만 있었고, `ai-job-agent`는 이번 세션 전까지 존재하지 않았음.

## 수집 대상 사이트 (중요 — 아직 미확정)

| 사이트 | 상태 | 근거 |
|---|---|---|
| **잡코리아** | 접근 허용 확인 + 실제 공고 10건 수집 검증 **완료** | 에이전트 직접 실행(STEP 02~05). `User-agent: *`가 `/Search/` 등을 막지 않음, 실제 HTTP 응답으로 확인 |
| **LinkedIn** | 접근 **불가 확인**(robots.txt 전면 차단) — 실제 페이지 요청은 보내지 않음 | 에이전트 직접 실행(robots.txt GET 1회 + `urllib.robotparser` 형식 검증). `User-agent: *` → `Disallow: /`(사이트 전체). "화이트리스트 신청 필요" 안내 명시됨(`whitelist-crawl@linkedin.com`) |

- 잡코리아 STEP 02~05의 실행 기록·데이터는 **그대로 보존**되어 있습니다(Notebook에서 삭제·수정하지 않음).
- LinkedIn 작업계획에 사용자가 지정한 검색어 `'AI 엔지니어'`와 URL
  (`https://www.linkedin.com/jobs/search-results/?currentJobId=4416185086&keywords=ai%20%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4&origin=SEMANTIC_SEARCH_LANDING_PAGE`)은
  Notebook `STEP 03-LI-A`에 기록되어 있습니다. **지역(location)은 URL에 없어 "미확인"으로 남겨둠.**
- **최종적으로 어느 사이트를 정식 수집 대상으로 쓸지는 아직 확정되지 않았습니다.** 다음 중 하나를 사용자가 선택해야
  합니다: (1) 잡코리아로 계속 진행, (2) LinkedIn 화이트리스트 신청 등 공식 경로 모색 후 재시도, (3) 사용자가 직접
  공고 텍스트/CSV를 제공하는 수동 입력 방식(Notebook의 "접근이 제한될 경우의 대안" 참고).

### LinkedIn 수동 입력 1건 (2026-10-04) — 자동 수집 아님

- 사용자가 LinkedIn 화면에서 **직접 복사한** 공고 1건(쿠팡 "CS Specialist (데이터 분석 & AI)")을 정리했습니다.
  **웹 요청 없이** 진행했으며, `collection_method = "manual_copy"`로 데이터에 명시해 **자동 수집 성공이 아님**을
  구분해 두었습니다.
- 저장 파일:
  - 원본 보존: `data/raw/linkedin_manual_4469459251.md`
  - 구조화 데이터(14개 컬럼, 1행): `data/processed/linkedin_manual_4469459251.csv` (UTF-8 BOM, `utf-8-sig`)
- `posted_date`/`closing_date`는 사용자 제공값이 "미상"이라 결측(NaN)으로 저장(임의 채움 없음). `collected_at`은
  저장 실행 시각(`2026-10-04T17:52:13+09:00`, 한국 표준시)이며 공고 등록일이 아닙니다.
- ⚠️ **직무 적합성 검토 필요**: `search_keyword = 'AI 엔지니어'`는 사용자가 이 공고를 **찾아낸 검색어**일 뿐,
  이 공고가 실제 "AI 엔지니어" 직무라는 판정이 아닙니다. 공고 제목은 "CS Specialist(데이터 분석 & AI)"로, 이 공고가
  프로젝트가 찾는 직무에 적합한지는 **검토 필요** 상태로 남겨두었습니다.
- 처리 중 발견한 오류(수정 완료): 코드를 처음 실행했을 때 Jupyter 커널의 작업 디렉터리가 `ai-job-agent`가 아니라
  `ai-job-agent/notebooks`여서, 상대경로로 지정한 저장 위치가 `ai-job-agent/notebooks/data/processed/`라는 잘못된
  곳에 생성되었습니다. 즉시 발견해 그 결과물을 삭제하고, 코드가 작업 디렉터리를 확인해 올바른 상위 폴더
  (`ai-job-agent/data/processed/`)에 저장하도록 수정한 뒤 재실행해 올바른 위치를 확인했습니다.

### 대상 선정 — 쿠팡 공고 분석 제외 (2026-10-04, 사용자 결정)

- **쿠팡 공고를 이번 'AI 엔지니어' 분석 대상에서 제외했습니다.** 이는 **사용자의 대상 선정 결정**이며, 이 공고에
  AI 관련 업무가 없다는 판정이 아닙니다. 원본(`data/raw/...md`)과 기존 14개 컬럼 값은 전혀 바꾸지 않았고,
  `excluded_from_analysis=True`, `exclusion_reason`(사유 전문), `exclusion_decided_at`(결정 시각) 3개 컬럼만
  추가했습니다.

### [방향 전환] STEP 09~10은 LinkedIn 쿠팡 공고로 진행 — 전체 원문 보완 (2026-10-04)

- **사용자 결정: STEP 09~10(Gemini 요약 시험)을 잡코리아가 아니라 LinkedIn 쿠팡 공고로 진행합니다.** 이번
  시험에서 잡코리아 데이터는 사용하지 않았습니다(잡코리아 관련 셀/파일 전혀 미접촉).
- 사용자가 같은 공고(`job_url` 동일)를 LinkedIn에서 다시 열어 **전체 본문을 그대로 복사해 전달**했습니다.
  - 원본: `data/raw/linkedin_manual_4469459251.md`에 "2차 확인 — 전체 원문(가공 없음)" 섹션으로 **추가**
    보존(기존 1차 내용 삭제 없음).
  - 구조화 데이터: 기존 레코드를 **보완**(20→28개 컬럼), **새 행을 추가하지 않음**(여전히 1행, 중복 없음).
  - `job_description`/`qualifications`/`preferred_qualifications`를 사용자 원문 그대로 갱신.
  - `excluded_from_analysis=True`, `is_new=True` — **보완 전/후 변경 없음**(추천 대상이나 신규 공고로 바뀌지
    않음, 실제 실행 결과로 재확인).
- **LinkedIn 화면 표시 요소는 해석하지 않고 원문 그대로만 보존**:
  - `posted_date_display_raw = "1주 전"` — `posted_date`는 계속 결측(NaN), 등록일로 변환하지 않음.
  - `apply_click_display_raw = "지원을 클릭한 사람 27"` — 지원자 수로 해석하지 않음.
  - `skill_match_excluded_note` — "보유기술 매치 1/10"은 열람자 개인화 정보라 분석/Gemini 입력 어디에도
    포함하지 않았다는 사실만 메모.
  - `work_arrangement="재택·대면 혼합근무"`, `employment_type="정규직"` — 실제 공고 속성으로 판단해 구조화 보존.
- **Gemini 시험용 입력(`gemini_test_input`, 898자)** 을 별도 컬럼으로 만들었습니다. 직무 소개·업무 내용·자격
  요건·우대 사항만 포함하고, 위 금지 항목은 포함하지 않습니다.

### LinkedIn 수동 입력 트랙 — STEP 06~08 진행 결과 (2026-10-04)

**잡코리아 STEP 02~05와는 완전히 분리된 별도 파일만 사용했습니다** (`data/processed/linkedin_manual_4469459251.csv`,
`data/processed/history_linkedin_manual.csv`). 아래는 전부 에이전트가 `ai-job-agent`의 `.venv`로 직접 실행한
실제 결과입니다(코드 실행 오류 0건, 전수 확인).

- **STEP 06 (정제)**: 결측 — `posted_date`/`closing_date`만 1건(전체), 나머지 16개 컬럼 결측 0건. `job_url` 기준
  중복 0건. 텍스트 컬럼 12개 전부 공백 이슈 없음(확인 후 `strip()` 적용). 정제 후 18개 컬럼(`cleaned_at` 추가),
  1행 유지.
- **STEP 07 (URL 기준 신규 판별)**: `is_new_by_url()` 함수 구현. **검증(메모리상에서만, 실제 이력 파일 미사용)**:
  최초 실행 → 신규 1/1, 동일 입력 재실행 → 신규 0/1(멱등성 확인), 새 URL(검증용 가짜 값, 저장 안 됨) 추가 →
  신규 1/2(가짜 값만 신규로 정확히 구분). **실제 적용**: 운영 이력 파일이 이전에 없었으므로(처리 전 0건) 쿠팡
  공고가 `is_new=True`로 판정됨 — **이 컬럼은 `excluded_from_analysis`와 완전히 독립적으로 관리됩니다.** 운영
  이력 파일을 신규 생성(`history_linkedin_manual.csv`, 1건).
- **STEP 08 (제외 기준 적용 분석 대상 건수)**: 전체 1건, 제외 1건, **분석 대상 0건**. "수집 실패가 아니라 선정
  제외 때문"이라는 설명과 함께 출력. 회사/지역/경력별 집계는 전부 빈 결과(`Series([], ...)`)를 오류 없이
  반환함을 확인. **부족한 실제 공고를 합성 데이터로 채우지 않았습니다.**
- 최종 CSV 컬럼 수(STEP 08 시점): 20개(기존 14 + 제외 3 + 정제 1 + 신규판별 2).
- **참고(2026-10-04 추가)**: 이후 STEP 09~10 준비 과정에서 Gemini 시험용 컬럼 8개가 추가되어 현재 28개
  컬럼입니다(아래 "[방향 전환]" 섹션 참고). **`excluded_from_analysis`는 여전히 `True`이므로 STEP 08의
  "분석 대상 0건" 결론 자체는 바뀌지 않습니다** — Gemini 시험은 STEP08의 정식 "분석 대상" 필터를 우회한
  **별도 시험 입력**(`gemini_test_input`)을 사용합니다.

## 사용 중인 에이전트

- Claude Code CLI: 로컬 설치 확인됨, 버전 `2.1.289` (이번 로컬 확인: `claude --version`)
- Codex CLI: 이번 로컬 확인에서 PATH상 발견되지 않음(`which codex` 실패) → 실제 투입 전 별도 설치/로그인 확인 필요
- 이번 세션 작업 주체: Claude Code (문서 작성)

## 현재 STEP

**STEP 02~05 — 실행·기록 완료, 사용자 최종 확인 대기.** 이번 세션에서 STEP 02(데이터 명세)~STEP 05(DataFrame 생성)를
하나의 작업 묶음으로 진행했습니다. CODING_RULES.md의 "작업계획 → 실제 코드 → 실행 결과 해석" 3개 셀 패턴으로
`notebooks/ax_job_pipeline.ipynb`에 6개 블록(STEP02, 03-A, 03-B, 04-A, 04-B, 05)을 추가했고, **`ai-job-agent`의 `.venv`
커널로 `jupyter nbconvert --execute`를 통해 실제로 전부 실행**해 진짜 출력을 Notebook에 기록했습니다(에이전트가 직접
실행 — 사용자가 VS Code에서 다시 실행한 것은 아직 아님).

핵심 결과:
- robots.txt의 `User-agent: *` 규칙상 `/Search/` 경로는 금지되어 있지 않음을 확인(STEP 03-A).
- 검색어 'AI'로 검색 결과 페이지 1회 접근 성공(상태 200), 응답에 실제 공고 상세 링크 28개 존재 확인(STEP 03-B).
- 공고 1건 필드 추출 검증 성공(STEP 04-A), 실제 공고 10건 수집 — **합성 샘플이 아닌 실제 데이터**(STEP 04-B,
  `IS_SYNTHETIC_SAMPLE: False`).
- DataFrame 생성 완료 — 컬럼 9개 SPEC 일치, 행 수 10, `posted_date`/`closing_date`만 전부 결측(목록 페이지에 없는
  정보라 임의로 채우지 않음 — 의도된 결과)(STEP 05).

⚠️ **참고(사용자 확인 필요)**: jobkorea.co.kr의 robots.txt에 특정 AI 어시스턴트 봇 이름(ClaudeBot 등)을 구체적으로
언급하는, 일반적인 robots.txt에서 보기 드문 상세한 주석이 포함되어 있었습니다. 에이전트는 이를 지시로 취급하지 않고
`User-agent: *` 구간의 기술적 규칙만 사실로 반영했습니다. 자세한 원문은 Notebook STEP 03-A 셀 참고.

**다음 STEP은 STEP 06 (전처리·중복 제거)이지만, 사용자 지시에 따라 아직 시작하지 않았습니다.**

**추가로 이번 세션에서 LinkedIn 접근 가능성 확인(미검증 단계)을 수행했습니다.** 결과: LinkedIn robots.txt가
일반 크롤러 전체를 차단(`Disallow: /`)하고 있어, **실제 페이지 요청은 보내지 않았습니다**(사용자 지시에 따라
허용되지 않으면 요청하지 않음). 잡코리아 STEP 02~05 기록은 전혀 손대지 않고 그대로 보존했습니다. 자세한 내용은
위 "수집 대상 사이트" 표와 Notebook `STEP 03-LI-A/B` 참고.

**추가로 이번 세션에서 LinkedIn 수동 입력 트랙의 STEP 06~08을 진행했습니다**(잡코리아 트랙과는 완전히 분리된
별도 파일만 사용). 쿠팡 공고를 사용자 결정으로 분석 대상에서 제외(원본·사유 보존) → STEP 06 정제(결측/공백/중복
확인, 이상 없음) → STEP 07 URL 기준 신규 판별 구현+검증(멱등성 확인) 및 실제 적용(운영 이력 파일 신규 생성,
`is_new=True`) → STEP 08 제외 기준 적용 결과 **분석 대상 0건**(수집 실패 아님, 합성 데이터로 채우지 않음)까지
전부 에이전트가 직접 실행해 확인했습니다. 자세한 내용은 위 "LinkedIn 수동 입력 트랙 — STEP 06~08 진행 결과"
참고. **STEP 09(Gemini 연동) 이후는 시작하지 않았습니다.**

**[최신] 사용자가 STEP 09(Gemini 연동)를 잡코리아 데이터로 진행하기로 결정했습니다.** 이에 따라 이번 세션에서
다음을 수행했습니다(Gemini API는 호출하지 않음, LinkedIn 데이터/이력은 전혀 접근하지 않음):

- **STEP 09 사전 준비-A (잡코리아 10건 후보 선정)**: 기존 추출 로직으로 10건을 다시 확인해 회사명·제목·URL
  표를 만들고, 제목 기반으로 관련성을 분류했습니다. **결과: '후보(명확)' 0건, '검토 필요' 10건.** 제목에 'AI'가
  들어간 공고는 대한상공회의소 1건뿐이지만 "교육생 모집" 공고라 특정 엔지니어 직무로 단정할 수 없어 역시
  '검토 필요'로 분류했습니다. 과장하지 않고 있는 그대로(0건) 보고합니다.
- **STEP 09 사전 준비-B (Gemini 연동 준비 상태 점검)**: `google-generativeai`/`google-genai` SDK 모두 미설치,
  `.env` 없음(이번에 `.env.example`만 생성), `GEMINI_API_KEY` 환경변수 미설정을 확인했습니다. 추가로 현재
  잡코리아 10건 데이터에는 **공고 본문(상세 설명·자격요건)이 없어** Gemini 요약에 아직 입력이 부족함을
  확인했습니다 — 사용자가 공고를 선택하면 상세 페이지를 먼저 가져와야 합니다.
- **이 두 점검은 Notebook 메인 커널(`jupyter nbconvert --execute`로 전체 재실행)을 통하지 않고, 같은
  `ai-job-agent`의 `.venv`로 별도 실행한 결과를 그대로 Notebook에 옮겨 적었습니다** — 전체 재실행 시 LinkedIn
  STEP 07-B의 `is_new`/운영 이력이 바뀌는 것을 막기 위한 의도적 선택입니다. 실제로 LinkedIn 관련 파일
  (`linkedin_manual_4469459251.csv`, `history_linkedin_manual.csv`)은 수정 시각이 이번 세션에서 전혀 바뀌지
  않았음을 확인했습니다.

**[최신] 사용자가 10건 중 9번(한국투자증권 "FY2026 한국투자증권 IT/디지털 경력직 공개채용")을 선택해 상세
페이지를 확보했습니다(STEP 09 사전 준비-C).** 상태 코드 200, 응답 길이 149,517자를 확인했고, "모집요강"
(모집분야=홈페이지 지원, 모집인원, 고용형태=계약직, 급여, 근무지)과 "지원자격"(경력 2년이상, 대졸이상, 스킬
미기재) 구조화 태그는 추출했습니다. **그러나 자유서술형 "주요업무" 텍스트 블록은 jobkorea 페이지 자체에
존재하지 않았습니다**(모집분야가 "홈페이지 지원"으로 되어 있어, 실제 직무 상세는 회사 자체 채용 홈페이지에
있는 것으로 보입니다). 즉 **이 공고는 현재 Gemini로 의미 있게 "요약"할 자유 텍스트 본문이 사실상 없습니다**
— 조건 메타데이터만 있을 뿐입니다. 이 점검도 LinkedIn 관련 셀을 건드리지 않기 위해 같은 `.venv`로 별도
실행한 결과를 옮겨 적었습니다(파일 수정 시각 불변 재확인함). **Gemini API는 이번에도 호출하지 않았습니다.**

**[최신] 사용자가 7번(안랩 "[안랩] 2026년 10월 신입/경력 채용")으로 다시 확인을 요청해 상세 페이지를
재확인했습니다(STEP 09 사전 준비-D).** 결과는 9번과 **동일한 패턴**입니다 — 상태 200, 모집분야 "홈페이지
지원", 경력(신입·경력/직무별 상이), 학력(대졸이상), 우대조건(장애인·취업보호대상자·유관업무 경험자·보훈대상자·
관련 자격증 보유자 — 직무 기술 우대사항은 아님), 접수기간(2026.10.02~2026.10.11)은 확보했으나, **"주요업무"
자유 서술 텍스트와 직무 관련 자격요건/우대사항은 이 페이지에 없습니다.** 추측해서 채우지 않았습니다. 이번에도
LinkedIn 관련 파일은 전혀 건드리지 않았습니다(수정 시각 재확인).

이번 묶음 작업(STEP 02~05), LinkedIn 확인 작업, 그리고 이번 STEP 09 사전 준비(A/B/C/D) 결과 모두에 대한 사용자
확인을 먼저 받습니다. 9번과 7번 공고 모두 jobkorea에 상세 본문이 없다는 공통 제약이 확인되어, 사용자의 다음
결정이 필요합니다(아래 "다음 작업" 참고).

**[최신, 방향 전환] 사용자가 잡코리아 9/7번 대신 LinkedIn 쿠팡 공고로 STEP 09~10을 진행하기로 결정했습니다.**
사용자가 공고 전체 원문을 직접 복사해 전달했고, 다음을 수행했습니다(잡코리아는 이번 시험에 사용하지 않음):

- 기존 LinkedIn 레코드(1행)를 **보완**(20→28개 컬럼, 중복 행 추가 없음), 전체 원문은 `data/raw/...md`에 추가
  보존. `excluded_from_analysis=True`/`is_new=True` **변경 없음**(실제 재확인).
- "1주 전"/"지원을 클릭한 사람 27"/"보유기술 매치 1/10"은 해석하지 않고 원문만 보존하거나(앞 둘) 분석·Gemini
  입력에서 완전히 제외(뒤 하나)했습니다. `gemini_test_input`(898자) 컬럼을 별도로 만들었습니다.
- 공식 문서(`ai.google.dev/gemini-api/docs/quickstart`)를 확인해 SDK `google-genai`, 초기화
  `genai.Client()`, 모델 `gemini-3.8-flash`를 확인했고, `pip install -U google-genai`로 **SDK를 설치**했습니다.
- `.env` 파일과 `GEMINI_API_KEY` 환경변수가 **아직 없어**, 사용자 지시에 따라 **여기서 멈추고** `.env` 작성
  방법을 안내했습니다. **Gemini API는 호출하지 않았습니다.** STEP 10(사용자 검증)은 호출 자체가 없어 여전히
  "확인 대기" 상태입니다.

**[최신] 사용자가 `.env`에 `GEMINI_API_KEY`를 입력했습니다.** 키 로드 확인(길이만 확인, 값 미노출) 후,
`gemini_test_input`(898자)과 모델 `gemini-3.8-flash`로 `client.models.generate_content()`를 **3회 시도**했으나
**매번 `google.genai.errors.ServerError: 503 UNAVAILABLE`**("This model is currently experiencing high demand")
로 실패했습니다. 이는 우리 쪽 설정(키·모델명·입력)이 아니라 **Google 서버 측의 일시적 과부하**로 보입니다(인증
오류나 "모델 없음" 오류가 아니라 503이었음). **3회 모두 응답을 받지 못해 CSV에 아무 것도 기록하지 않았고,
`excluded_from_analysis`/`is_new`는 실행 전과 동일하게 변경되지 않았습니다**(호출 코드가 `to_csv` 이전에
실패해 저장 자체가 일어나지 않음). 사용자가 요청한 "1회 호출"을 아직 성공적으로 완료하지 못한 상태이며,
재시도 방법(나중에 재시도 / 다른 모델명 시도)을 사용자가 결정해야 합니다.

**[최신] 사용자 지시에 따라 같은 키·같은 모델로 1회만 재시도 — 성공했습니다.** SDK 자체 재시도만 두고 에이전트
쪽에서 추가 반복 루프는 만들지 않았습니다. 응답을 JSON으로 파싱해 5개 항목(주요 업무/필수 요건/우대 사항/
명시된 기술/직무 유형)을 모두 받았고, `gemini_model`/`gemini_response_raw`/`gemini_called_at`을
`linkedin_manual_4469459251.csv`에 저장했습니다(28→31개 컬럼, 행 수 1 유지). **호출 전/후
`excluded_from_analysis=True`, `is_new=True` 변경 없음을 재확인했습니다.** 원문과 대조한 결과 **누락·과도한
해석(원문에 없는 내용 추가)은 발견되지 않았습니다** — 다만 "주요 업무/필수 요건/우대 사항"은 원문 bullet을
거의 그대로 이어붙인 수준이라 진짜 "요약"(재구성)인지는 추가 검증이 필요합니다. 상세 비교표는 아래
"Gemini 응답 vs 원문 비교" 참고. **STEP 10(사용자 검증)은 여전히 "확인 대기" 상태로 남겨둡니다** — 에이전트의
비교는 1차 참고용입니다.

### Gemini 응답 vs 원문 비교 — 수정판 (2026-10-04, `gemini-3.8-flash`, 추가 API 호출 없이 교정)

> ⚠️ **교정 사항**: 아래 표는 사용자 피드백을 반영해 수정했습니다. 최초 비교표에서 "직무 유형=정규직"이라고
> 적었던 것은 실제로는 **고용형태**였습니다(Gemini 응답의 `직무_유형` 필드 값이 `employment_type` 컬럼
> 값과 완전히 동일했음 — 확인 완료). **추가 Gemini 호출 없이**, 본문(공고 제목·직무 소개)을 근거로 "직무
> 유형"을 새로 정리하고 "고용형태"와 별도 행으로 분리했습니다.

| 항목 | 내용 | 원문 근거 | 판정 |
|---|---|---|---|
| 주요 업무 | SQL 데이터 추출/분석/시각화, 생성형 AI 기반 CS 효율화, LLM 업무 자동화, AI Agent·RAG 프로세스 개선, AI 솔루션 성과 분석 | 원문 "업무 내용" 5개 bullet과 **거의 동일한 문구** | 일치(누락·추가 없음). 요약이라기보다 원문 재인용에 가까움 |
| 필수 요건 | SQL 2년↑, 데이터 구조화, 개발 조직 협업, LLM 활용 경험, 커뮤니케이션 역량 | 원문 "자격 요건" 5개 bullet과 **거의 동일한 문구** | 일치(누락·추가 없음) |
| 우대 사항 | 로그·이벤트 분석, AI Agent·Retriever, n8n/Zapier, JavaScript/Python | 원문 "우대 사항" 4개 bullet과 **거의 동일한 문구** | 일치(누락·추가 없음) |
| 명시된 기술 | SQL, LLM(OpenAI·Claude·Gemini), AI Agent, RAG, n8n, Zapier, JavaScript, Python | 모두 원문에 실제로 등장하는 용어 | 일치 — 원문에 없는 기술 추가 없음 |
| **직무 유형 (교정됨)** | **CS 운영 데이터 분석·AI 자동화** | 공고 제목("CS Specialist (데이터 분석 & AI)")·직무 소개 문단 근거, 사용자 확인 하에 정리 | 본문 기반 — Gemini의 원래 답과 다름(아래 참고) |
| **고용형태 (분리됨)** | 정규직 | LinkedIn 원문의 "[정규직]" 태그 | Gemini가 "직무_유형"으로 답했던 값 — 실제로는 이 항목이었음 |

- **누락**: 발견되지 않음(5개 핵심 항목 모두 원문 내용을 포함).
- **과도한 해석(hallucination)**: 발견되지 않음(원문에 없는 회사명·기술·조건이 추가되지 않았음).
- **한계**: "주요 업무/필수 요건/우대 사항"은 원문 bullet을 거의 그대로 이어붙여, 압축·재구성의 정도가
  낮습니다. "직무 유형"은 Gemini가 제대로 답하지 못해(고용형태와 혼동) 사람이 직접 교정했습니다.

### STEP 11 — Gemini 연동 시험판 보고서

- 저장 경로: `reports/step11_gemini_test_report_2026-10-04.md` (2,389자)
- 구성: (1) 분석 현황 요약(0건 vs 1건 표), (2) 이번 주 추천 채용공고 **0건**, (3) [참고] Gemini 연동 시험
  결과 — **추천 공고 아님**(쿠팡 공고, URL·직무 유형·고용형태·근무형태·주요 업무·필수 요건·우대 사항·명시된
  기술 전부 포함), (4) 데이터 출처와 한계.
- **제외된 쿠팡 공고는 "추천 채용공고" 섹션에 전혀 포함되지 않았고**, 별도의 "[참고]" 섹션에만 "추천 아님"
  문구와 함께 들어갑니다.
- 작성 중 발견한 형식 버그(수정 완료): "우대 사항" 등 원문 항목 자체에 "/"가 포함된 경우("n8n / Zapier",
  "Java script / Python")가 있어, 자동 불릿 분리 시 항목이 잘못 쪼개지는 문제를 발견하고 즉시 고쳤다(항목을
  억지로 쪼개지 않고 한 문단으로 유지).

## 완료 / 부분 확인 / 미확인 / 대기 — 근거 포함

| 항목 | 상태 | 근거 |
|---|---|---|
| GitHub 계정/Fork/원격 연결(origin=Fork, upstream=원본) | 완료로 간주 | 사용자 보고(대화) — 이번 세션에서 로컬 재확인은 하지 않음 |
| `ax-job-agent` 브랜치 생성 | 완료 | 사용자 보고(대화) + 이번 로컬 확인(`git branch --show-current` = `ax-job-agent`) |
| `chapter11/ax-job-agent` 폴더 생성 | 완료 | 사용자 보고(대화) + 이번 로컬 확인 |
| `ax-job-agent`에 `.venv` 생성 | 완료 | 사용자 보고(대화) + 이번 로컬 확인(`.venv/Scripts/python.exe` 존재) |
| 가상환경 Python 버전 3.14.6 | 완료 | 사용자 보고(대화)와 이번 로컬 확인 일치 |
| pandas/requests/beautifulsoup4/jupyter/python-dotenv 설치 | 완료 | 사용자 보고(설치 명령 실행) + 이번 로컬 확인(`pip list`, import 테스트 성공) |
| VS Code Python 인터프리터 선택 (ax-job-agent 쪽, 과거) | 부분 확인(참고용, 더 이상 사용 안 함) | 사용자 보고(대화)만 있음. `ai-job-agent`로 루트가 바뀌었으므로 이 확인은 더 이상 유효하지 않음 |
| VS Code Python 인터프리터/Notebook 커널 선택 (ai-job-agent 쪽, 신규) | **완료** | 사용자 보고 — Notebook 셀이 `ai-job-agent\.venv`에서 실제로 실행되어 올바른 `sys.executable`을 출력함으로써 간접 확인됨 |
| `notebooks/ax_job_pipeline.ipynb` 파일 작성(목적/완료조건 Markdown, 환경확인 Code 셀 2개, 기록용 빈 Markdown) | 완료 | 이번 로컬 확인: JSON 구조 파싱 성공, 셀 4개(markdown/code/code/markdown) 순서 확인 |
| Notebook 커널 선택 및 셀 실행(sys.executable 경로·import 성공 확인) | **완료** | **사용자 보고(직접 실행 결과)**: `sys.executable`이 `ai-job-agent\.venv\Scripts\python.exe`와 일치, `pandas 3.0.6`/`requests 2.34.2`/`beautifulsoup4 4.15.0` 오류 없이 출력, `dotenv`도 같은 `.venv`에서 정상 import. Notebook 마지막 Markdown 셀에 기록됨 |
| `chapter11/ai-job-agent`에 `.venv` 생성 | **완료** | 이번 로컬 확인: `python -m venv .venv` 실행 → `.venv/Scripts/python.exe` 생성 확인 |
| `ai-job-agent` 가상환경 Python 버전 | **완료** | 이번 로컬 확인: `python --version` → `3.14.6` (ax-job-agent와 동일) |
| `ai-job-agent`에 pandas/requests/beautifulsoup4/jupyter/python-dotenv 설치 | **완료** | 이번 로컬 확인: `pip list`에서 `pandas 3.0.6`, `requests 2.34.2`, `beautifulsoup4 4.15.0`, `python-dotenv 1.2.4`, jupyter/ipykernel/notebook 계열 확인 |
| `ai-job-agent` venv에서 패키지 import 검증 | **완료** | 이번 로컬 확인: `import pandas, requests, bs4, dotenv` 성공, `sys.executable`이 `ai-job-agent\.venv\Scripts\python.exe`를 가리킴을 확인 |
| STEP 02 — 9개 컬럼 명세(의미/필수여부/결측기준) 표 | **완료** | 에이전트가 `.venv`로 직접 실행 — 9행 표 정상 출력, 오류 없음 |
| STEP 03-A — robots.txt 확인 | **완료** | 에이전트가 `.venv`로 직접 실행 — status 200, `User-agent: *`에 `/Search/` 미차단 확인. ⚠️ robots.txt 내 이례적 서술은 사용자 확인 필요(위 "현재 STEP" 참고) |
| STEP 03-B — 검색 결과 페이지 접근 테스트('AI') | **완료** | 에이전트가 `.venv`로 직접 실행 — status 200, 응답에 실제 공고 상세 링크 28개 확인(상태코드만으로 판단하지 않음) |
| STEP 04-A — 공고 1건 필드 추출 검증 | **완료** | 에이전트가 `.venv`로 직접 실행 — company_name/job_title/job_url 정상 추출 확인 |
| STEP 04-B — 공고 10건 수집 | **완료** | 에이전트가 `.venv`로 직접 실행 — **실제 데이터 10건**(`IS_SYNTHETIC_SAMPLE: False`), 샘플 아님 |
| STEP 05 — DataFrame 생성 | **완료** | 에이전트가 `.venv`로 직접 실행 — shape(10,9), 컬럼 SPEC 9개와 일치, posted_date/closing_date만 전부 결측(의도된 결과) |
| 위 STEP 02~05 결과에 대한 **사용자 직접 확인/재실행** | **미확인 — 사용자 확인 대기** | 에이전트가 직접 실행한 결과이며, 사용자가 VS Code에서 다시 열어 확인한 것은 아직 아님 |
| LinkedIn robots.txt 확인(일반 크롤러 접근 가능 여부) | **완료(접근 불가로 확인)** | 에이전트가 `.venv`로 직접 실행 — `User-agent: *`가 `Disallow: /`, `can_fetch` 전부 False |
| LinkedIn 실제 페이지 요청(상태 코드/Content-Type/공고 포함 여부) | **미수행(의도적 — 정책상 차단)** | robots.txt 차단 확인 후 사용자 지시에 따라 요청 자체를 보내지 않음. 상태 코드 등은 확인된 바 없음 |
| LinkedIn을 정식 수집 대상으로 쓸지 여부 | **미확정 — 사용자 결정 필요** | 사용자가 다음 3가지 중 선택: 잡코리아 유지 / LinkedIn 화이트리스트 신청 후 재시도 / 수동 입력 |
| LinkedIn 공고 1건 수동 입력 정리(쿠팡 CS Specialist) | **완료(수동 입력, 자동 수집 아님)** | 에이전트가 `.venv`로 직접 실행, 웹 요청 없음. `data/raw/linkedin_manual_4469459251.md` + `data/processed/linkedin_manual_4469459251.csv`(14컬럼, 1행) 생성·검증 완료 |
| 위 LinkedIn 수동 입력 공고의 **직무 적합성("AI 엔지니어" 관련 여부)** | **사용자 결정 — 이번 분석 대상에서 제외** | 사용자의 대상 선정 결정(2026-10-04). AI 관련 업무가 없다는 판정이 아님. `exclusion_reason`에 사유 전문 기록 |
| LinkedIn 트랙 STEP 06 — 정제(결측/공백/URL중복) | **완료** | 에이전트가 `.venv`로 직접 실행 — 결측은 posted_date/closing_date만(의도됨), 중복 0건, 공백 이슈 0건 |
| LinkedIn 트랙 STEP 07 — URL 기준 신규 판별(구현+검증+실적용) | **완료** | 에이전트가 `.venv`로 직접 실행 — 검증 3시나리오(최초1/재실행0/신규추가1) 전부 메모리상에서 통과, 실제 적용 시 운영 이력 파일 신규 생성(1건), `is_new`와 `excluded_from_analysis` 독립 관리 확인 |
| LinkedIn 트랙 STEP 08 — 제외 기준 적용 분석 대상 건수 | **완료(0건)** | 에이전트가 `.venv`로 직접 실행 — 전체 1건 중 제외 1건, 분석 대상 0건. "수집 실패 아님" 명시, 집계 코드 오류 없음, 합성 데이터로 채우지 않음 |
| STEP 09 대상 데이터 결정(1차) | 완료 — 잡코리아로 시도(이후 변경됨) | 사용자 결정(2026-10-04) |
| STEP 09 사전 준비-A — 잡코리아 10건 후보 선정(제목 기반) | **완료** | 에이전트가 `.venv`로 별도 실행 — '후보(명확)' 0건, '검토 필요' 10건. 있는 그대로 보고(과장 없음) |
| STEP 09 사전 준비-B — Gemini 연동 준비 상태 점검 | **완료(미준비 확인)** | 에이전트가 `.venv`로 별도 실행 — SDK 미설치, `.env` 없음(`.env.example`만 생성), API 키 미설정, 입력 데이터(본문 텍스트) 부족 확인. 키 값 미노출 |
| 사용자의 9번 공고(한국투자증권) 선택 | **완료** | 사용자 결정(2026-10-04) |
| STEP 09 사전 준비-C — 9번 공고 상세 페이지 확보 | **완료(본문 텍스트 없음으로 확인)** | 에이전트가 `.venv`로 별도 실행(1회 GET, status 200) — 모집요강/지원자격 메타데이터는 확보, **자유서술형 '주요업무' 텍스트는 jobkorea 페이지에 없음**(모집분야="홈페이지 지원") |
| Gemini 실제 API 호출(STEP 09 본작업) | **미수행(의도적)** | 9번 공고에 요약할 본문이 부족함이 확인되어, 호출 전 사용자 결정 대기 중(다른 공고 선택 / 메타데이터만으로 시험 / 회사 홈페이지 내용 수동 제공 중 택1) |
| 사용자의 7번 공고(안랩) 재선택 | **완료** | 사용자 결정(2026-10-04) |
| STEP 09 사전 준비-D — 7번 공고 상세 페이지 재확인 | **완료(9번과 동일하게 본문 텍스트 없음)** | 에이전트가 `.venv`로 별도 실행(1회 GET, status 200) — 모집분야="홈페이지 지원", 우대조건(일반 우대만 있고 직무 우대 없음), 접수기간 확보. **'주요업무' 자유 텍스트 없음, 외부 지원 링크도 정적 HTML에 없음** — 추측하지 않음 |
| STEP 09 대상 데이터 결정(2차, 최종) | **완료 — LinkedIn 쿠팡 공고로 변경** | 사용자 결정(2026-10-04). 잡코리아는 이번 시험에 미사용 |
| LinkedIn 레코드 보완(전체 원문 반영) | **완료(중복 없음, 결정 불변)** | 에이전트가 `.venv`로 직접 실행 — 20→28컬럼, 1행 유지, `excluded_from_analysis`/`is_new` 변경 없음 확인. "1주 전"/"지원 클릭 27"은 원문 보존만, "보유기술 매치"는 완전 제외 |
| `gemini_test_input` 생성(Gemini 시험용 입력) | **완료** | 898자. 직무 소개·업무 내용·자격 요건·우대 사항만 포함, LinkedIn 개인화/UI 요소 제외 |
| Gemini SDK/모델 공식 문서 확인 | **완료** | WebFetch로 `ai.google.dev/gemini-api/docs/quickstart` 확인 — SDK `google-genai`, `genai.Client()`, 모델 `gemini-3.8-flash` |
| Gemini SDK 설치 | **완료** | `pip install -U google-genai` 실행, 설치 확인(`google-genai 2.28.0`) |
| `.env`/`GEMINI_API_KEY` 준비 | **완료** | 사용자가 `.env`에 입력(2026-10-04). 로드 확인(키 길이만 확인, 값 미노출) |
| Gemini 실제 API 호출(1차, 3회) | 실패(503 UNAVAILABLE) | `google.genai.errors.ServerError`("high demand"). 인증/모델명 오류 아님. 응답 없어 CSV 미변경 |
| Gemini 실제 API 호출(2차, 1회 재시도) | **성공** | 에이전트가 `.venv`로 직접 실행 — JSON 파싱 성공, 5개 항목 모두 수신. 추가 반복 루프 없이 단일 호출 |
| 호출이 기존 결정에 미친 영향 | **없음 — 확인됨** | 호출 전/후 `excluded_from_analysis=True`/`is_new=True` 동일(재확인함) |
| Gemini 응답-원문 대조(누락/과도한 해석 점검) | **완료 — 이상 없음(에이전트 1차 점검)** | 5개 항목 모두 원문 근거 있음, 원문에 없는 내용 추가 없음. "요약"보다 "원문 bullet 재인용"에 가까운 한계는 있음 |
| 직무 유형/고용형태 분리 교정 | **완료(추가 API 호출 없음)** | 에이전트가 `.venv`로 직접 실행 — Gemini의 `직무_유형` 값이 `employment_type`과 동일함을 확인 후, 본문 근거로 `job_type_corrected` 신설·분리 |
| STEP 10 사용자 검증 | **확인 대기(수정판 기준)** | 에이전트의 비교는 참고용 — 사용자 최종 확인 필요 |
| Gemini 연동/검증(STEP 09~10) | **STEP 09 완료(호출+대조+교정), STEP 10 확인 대기** | — |
| STEP 11 — Markdown 보고서 생성(Gemini 시험판) | **완료** | 에이전트가 `.venv`로 직접 실행 — `reports/step11_gemini_test_report_2026-10-04.md` 생성. 분석 대상 0건/시험 1건 구분, 제외 공고는 추천 섹션에 미포함, URL·업무·요건·우대·기술 전부 포함 |
| STEP 12 — Slack Incoming Webhook 연결 시험 | **완료(사용자 채널 수신 확인됨)** | 에이전트 실행(200/ok) + **사용자가 테스트 채널에서 실제 메시지 수신을 직접 확인**(2026-10-05) |
| STEP 13 — Gmail 연결 시험 | **완료(사용자 수신함 확인됨)** | 에이전트 실행(SMTP 예외 없음) + **사용자가 수신함에서 실제 메일 수신을 직접 확인**(2026-10-05) |
| STEP 14 — 함수화·모듈 분리(`src/*.py`) | **완료** | `collect.py`/`clean.py`/`analyze.py`/`summarize.py`/`report.py`/`notify.py` 작성, 구문 검사 통과 |
| STEP 15 — `main.py` 통합 | **완료(dry-run 기본값)** | `python main.py`(인자 없음) 실행 성공, `returncode 0`. `--live` 플래그로 실제 호출 전환 가능(이번엔 미실행) |
| STEP 16 — 로컬 전체 실행 검증(재현성) | **완료(dry-run 기준)** | 에이전트가 `.venv`로 직접 2회 연속 실행 — 타임스탬프 제외 출력 완전 동일(`True`), 신규 0건 재현 확인 |
| STEP 14~16 — **사용자 직접 실행 확인** | **완료** | **사용자가 직접 `python main.py` 실행 → 오류 없이 종료, 생성된 보고서에서 dry-run 표시·"전체 1건·추천 대상 0건" 직접 확인(2026-10-05)** |
| `--live` 모드(실제 Gemini 호출 + Slack/Gmail 발송) | **미실행 — 검증 안 됨** | 이번 작업에서 의도적으로 실행하지 않음(사용자 지시). 완료로 표시하지 않음 |
| 보고서/Slack/Gmail(STEP 11~13) | STEP 11 완료(시험판) / STEP 12 완료(사용자 확인됨) / STEP 13 시험 성공(사용자 수신 확인 대기) | — |
| 함수화/main.py/로컬 전체 실행(STEP 14~16) | **완료(사용자 직접 실행 확인됨)** | 위 행 참고 |
| GitHub Actions workflow 파일 작성(STEP 17~18 준비) | **완료** | `.github/workflows/ai-job-agent-weekly-report.yml` 신규 작성(저장소 루트). `workflow_dispatch`만 활성화, `schedule`은 주석 처리(사용자 일정 확인 전) |
| GitHub Actions 실제 실행(수동 workflow_dispatch, dry-run) | **완료** | **사용자가 Actions 탭에서 직접 수동 실행 → Success(초록 체크)로 종료, Artifact 보고서 다운로드 → "전체 1건·추천 대상 0건" 직접 확인(2026-10-05)** |
| GitHub Actions 주간 스케줄(schedule 트리거) | **보류 — 다시 비활성화(주석 처리)됨** | `cron: "10 0 * * 5"`(매주 금요일 09:10 KST)로 설정했다가, 같은 날 **사용자가 잡코리아 자동 수집 가능성 검증을 먼저 하기로 결정**해 다시 주석 처리함(2026-10-05). 희망 일정·관련 코드는 그대로 보존. main PR은 merge하지 않음 |
| live 실행 전 GitHub Secrets 5개 검증(발송 전 실패) | **완료(로직 추가 + 더미값 시뮬레이션 검증)** | 5개 중 하나라도 비어 있으면 `::error::`로 변수 "이름만" 표시 후 `exit 1`. 실제 Secrets 값으로는 미검증(GitHub 환경에서만 확인 가능) |
| Claude Code 로컬 준비 상태 | 완료 | 이번 로컬 확인(`claude --version` → 2.1.289) |
| Codex 로컬 준비 상태 | **미확인** | 이번 로컬 확인에서 PATH상 미발견. 로그인 여부 등은 추가 확인 필요 |

## 막힌 사항

- 없음. (이전에 있던 ax/ai 경로 불일치는 `ai-job-agent`로 확정하면서 해결됨)

## 다음 작업 (1개)

**사용자가 main 반영용 PR을 리뷰하고 merge할지 결정한다.** PR이 merge되어야 `schedule`(금요일 09:10
KST)이 기본 브랜치(main)에서 실제로 동작하기 시작한다. 그 전까지는 금요일이 되어도 자동 실행되지
않는다. merge 전에 GitHub Secrets 4개(SLACK_WEBHOOK_URL/GMAIL_ADDRESS/GMAIL_APP_PASSWORD/
GMAIL_TO_ADDRESS)가 저장소에 등록되어 있어야 schedule 실행이 실패하지 않는다(아래 "GitHub Secrets
등록 확인" 참고).
- **Gemini 재시도·검토 필요 3건·Greenhouse 관련 결정은 더 이상 의미가 없다** — Greenhouse 트랙 자체가
  중단되었기 때문이다(`main.py`가 더 이상 호출하지 않음, 코드는 `src/*.py`에 참고용으로만 남아 있음).
- 쿠팡(LinkedIn) 레코드: `excluded_from_analysis=True` 그대로, 잡코리아 목록 수집과도 완전히 분리됨.
- STEP 18(주간 자동 스케줄)은 **일정 설정 완료 + dry-run/실제 전송 양쪽 검증 완료**지만, **실제
  schedule 트리거를 통한 자동 실행은 아직 한 번도 없었다**(merge 전이므로 당연함) — SPEC.md §11의
  "최소 1회 이상 스케줄된 실행이 실제로 동작함을 확인" 조건은 merge 후 첫 금요일에만 확인 가능하다.

- 함께 남아 있는 확인 사항(별도): STEP 10(Gemini 비교표/`reports/step11_gemini_test_report_2026-10-04.md`)도
  아직 "확인 대기" 상태다.
- STEP 17은 완료되었다(아래 "STEP 17 — 실제 GitHub Actions 실행 결과" 참고). STEP 18은 **merge + 첫
  실제 스케줄 실행 확인 전까지는 완료로 표시하지 않는다.**

## 잡코리아 알림 실제 시험 발송 + 채널별 중복 방지 + 예약 활성화 (2026-10-05, 실제 Slack·Gmail 발송 성공)

### 실제 발송 결과

- **Slack: 성공** — 상태 코드 200, 응답 본문 "ok".
- **Gmail: 성공** — SMTP 세션 정상 종료.
- 발송 내용: 잡코리아 신규 AI·AX 공고 11건(회사·제목·링크, 본문 분석·AI 요약 없음) — 전부 이번이
  처음 발견된 공고였고 두 채널 모두에 처음 발송됨.

### 채널별 중복 발송 방지 이력 체계 (신규 구현)

- `data/processed/history_jobkorea_ai_ax.csv`에 공고별로 `first_seen_at`/`slack_notified_at`/
  `gmail_notified_at`을 따로 기록한다. **"성공"했을 때만** 그 채널의 타임스탬프를 채운다 — 실패했거나
  시도하지 않았으면 그 채널 칸은 비워 둔 채로, 다음 실행에서도 그 채널에는 여전히 "보낼 후보"로 남는다.
- 검증: 실제 발송 직후 dry-run으로 재실행 — 같은 11건이 "Slack 발송 대상 0건, Gmail 발송 대상 0건"으로
  정확히 걸러짐을 확인(중복 방지 동작 확인). 두 채널이 서로 다른 성공 여부를 가질 수 있는 상황(한쪽만
  실패)은 실제로 재현하지 않았고 코드 로직으로만 보장된다(설계상 "채널별 완전히 독립적으로 판단" 구조).
- 발송 실패 시 자동 재발송은 하지 않는다 — `src/notify.py`가 예외를 잡아 `{"status": "error", ...}`로
  돌려주고, `main.py`는 그 결과를 로그로 남긴 뒤 다음 단계(이력 갱신)로 넘어갈 뿐 재시도 루프가 없다.

### 예약(schedule) 활성화

- `.github/workflows/ai-job-agent-weekly-report.yml`의 `schedule: cron: "10 0 * * 5"`(매주 금요일
  09:10 KST) **주석을 해제해 활성화했다.** `workflow_dispatch`는 그대로 유지(수동 실행도 여전히 가능).
- **merge되지 않은 브랜치에서는 schedule이 동작하지 않는다** — main 반영 PR이 merge되어야 실제로
  매주 돌아간다.

### GitHub Secrets 등록 확인

- `gh` CLI와 `GITHUB_TOKEN`이 이 환경에 없어 **에이전트가 직접 등록 여부를 확인할 수 없다.**
- 사용자가 직접 확인/등록할 위치: 저장소(`github.com/darajeong/claude-code-agent-course`) →
  **Settings → Secrets and variables → Actions** → 아래 4개 이름이 보이는지 확인(이름만 보이고
  값은 절대 표시되지 않음 — 이는 GitHub 자체의 정상적인 보안 동작이다):
  - `SLACK_WEBHOOK_URL`
  - `GMAIL_ADDRESS`
  - `GMAIL_APP_PASSWORD`
  - `GMAIL_TO_ADDRESS`
  - (`GEMINI_API_KEY`는 선택 사항 — 없어도 schedule 실행은 실패하지 않는다.)
- 없으면 **New repository secret**으로 위 이름 그대로 추가(로컬 `.env`에 이미 저장한 실제 값 사용).

### 완료 근거

사용자가 요청한 항목(실제 1회씩 발송/채널별 성공 기록/성공 채널 중복 방지/실패 시 재발송 금지/
예약 설정 포함 커밋·푸시·PR 준비/Secrets 확인 또는 위치 안내/merge 보류) 중 **merge는 하지 않았고**,
나머지는 전부 실행·확인했다. (2026-10-05, 최종 목표 재확정 — Greenhouse 중단, 구현+dry-run 검증 완료)

- 배경: 3건 시험 발송에서 Gemini 3건 전부 실패한 직후, 사용자가 "Gemini 재시도와 Greenhouse 작업은
  중단"을 지시하고 최종 목표를 재확정: **"잡코리아 신규 AI·AX 공고(회사·제목·링크)를 매주 금요일
  09:10 KST에 Slack·Gmail로 수신, 본문 분석과 AI 요약은 제외."** "앞서 확인한 잡코리아 이용 조건을
  기준으로 목록 자동 수집이 가능한지 결론을 내리고, 가능하면 목록 수집·중복 알림 방지·전송·GitHub
  이력 유지까지 구현해 dry-run 검증, 불가능하면 우회하지 말고 막히는 조건과 잡코리아 자체 알림
  대안을 알릴 것"을 지시. 추가 실제 발송 금지, 예약 계속 보류.

### 가능성 결론

**"가능"** — 단, 이번에 실제로 구현한 좁은 범위(**검색 결과 목록 페이지 1개만, 주 1회, 키워드 1개,
상세 페이지 미방문, 개인 Slack/Gmail 알림만, 공개 재배포 없음**)에 한정된다. 근거:

| 근거 | 내용 |
|---|---|
| robots.txt(`User-agent: *`) | `/Search/`를 Disallow 하지 않음 — 같은 날 재확인(과거 결론 재사용 안 함) |
| 이용약관 제19조④ | "회사 사전동의 없는 복사·재배포 금지" — 문언상 "회원"에게 적용되는 계약 조항, 익명 자동 요청은 그 계약 당사자가 아님(일반적 해석) |
| 판례(2016/2017, 참고용) | 모두 "경쟁 서비스를 위해 DB 상당 부분을 체계적으로 복제·재배포"한 사안 — 이번 설계(주 1회, 목록 1페이지 중 일부 메타데이터만, 개인 알림용, 재배포 없음)는 그 핵심 요건에 해당하지 않는다고 판단 |
| 기술적 풍선 최소화 | 상세 페이지는 전혀 방문하지 않음 — 사람이 검색창에 검색어 치고 결과 보는 것과 사실상 동일한 수준 |

**이 결론은 법률 자문이 아니라 에이전트의 실무적 판단이다.** 위 전제(주 1회·목록 1페이지·키워드 1개·
상세 미방문·비공개 개인 알림)를 벗어나면(여러 페이지, 여러 키워드, 더 잦은 실행, 공개 재배포 등)
재평가가 필요하다.

### 구현 내역

| 파일 | 변경 |
|---|---|
| `src/collect.py` | `fetch_jobkorea_search_list()` 추가(목록 페이지 1회 GET, 상세 미방문, 회사명은 로고 이미지 `alt` 속성에서 추출). Greenhouse 함수는 그대로 보존(주석으로 "중단됨" 명시). |
| `src/analyze.py` | `screen_jobkorea_candidates()`(제목 기반 1차 스크리닝) 추가. 신규 판별은 **기존 `mark_new_records()`를 그대로 재사용**(새 코드 불필요 — URL 기준 로직이 사이트에 무관하게 일반적으로 작동함). |
| `src/report.py` | `build_jobkorea_section_markdown()` 추가(목록만, 요약 없음). `build_greenhouse_section_markdown()`은 `greenhouse_fetch_results`를 넘기지 않으면 보고서에 아예 나타나지 않도록 변경(레거시 보존, 비활성). |
| `main.py` | `run_greenhouse_track()` 제거, `run_jobkorea_track()` 추가. Slack/Gmail 모두 **보고서 내용 자체**를 전송하도록 통일(로컬 경로 문자열 금지 — 사용자 지시를 정규 파이프라인에도 일반화 적용). |
| `.github/workflows/ai-job-agent-weekly-report.yml` | 이력 커밋 단계에 `history_jobkorea_ai_ax.csv` 추가(파일이 없을 수 있어 존재 확인 후 add). 필수 Secrets 검증에서 `GEMINI_API_KEY` 제외(잡코리아 트랙은 Gemini 불필요). schedule은 그대로 비활성 유지. |

### dry-run 실제 실행 결과

- 잡코리아 검색어 `AI 엔지니어`로 목록 페이지 1회 조회 성공 — 25건. 제목 스크리닝 통과 11건(전부 신규,
  운영 이력 파일이 dry-run에서는 생성되지 않음을 확인). Gemini·Greenhouse 호출 전혀 없음.
- 2회 연속 dry-run 결과 (생성 시각 제외) 완전히 동일 — 재현성 확인.
- `collect.fetch_jobkorea_search_list()`를 극단적으로 짧은 timeout으로 호출해 실패를 강제 재현 —
  `status="error"`로 정확히 반환됨을 확인(수집 실패≠0건 원칙 유지).
- 보고서(`reports/weekly_report_2026-10-05.md`)에 "잡코리아 신규 AI·AX 공고" 섹션이 회사·제목·링크만
  담아 생성됨을 확인(본문·요약 없음).
- 작업 중 로컬 코드 리뷰로 잠재 버그 1건을 실행 전에 미리 발견해 수정: GitHub Actions의 이력 커밋
  스텝에서 `history_jobkorea_ai_ax.csv`가 아직 없을 수 있는데(스크리닝 통과 0건인 주) `git add`가
  존재하지 않는 경로에서 실패해 스텝 전체가 죽는 문제 — 파일 존재 확인 후 add 하도록 수정.

### 완료 근거

사용자가 요청한 항목(이용 조건 기준 결론 제시/가능 시 목록 수집+중복 알림 방지+전송+GitHub 이력 유지
구현+dry-run 검증/우회 금지) 전부 충족. 추가 실제 발송은 하지 않았고 예약도 계속 보류 상태다.

## 3건 시험 발송 (2026-10-05, 실제 Gemini 호출 3건 전부 실패 → 재시도 없이 중단, Slack·Gmail은 실제 발송 성공)

- 배경: 사용자가 "검토 필요 3건은 추천에서 제외하고 별도 목록 유지, 확정 AI·AX 공고 중 서로 다른 직무를
  대표하는 3건을 골라 Gemini로 실제 요약(공고당 1회, 자동 재시도 금지), '3건 시험 발송' 보고서를 만들어
  Slack·Gmail로 각각 1회 실제 발송, Slack에는 경로가 아니라 보고서 내용을 넣을 것, 실패 시 재발송 금지,
  이번 시험이 나머지 공고를 이미 발송한 것으로 기록되지 않게 할 것, 주간 예약은 계속 보류"를 지시.
- **선정한 3건(서로 다른 직무·회사 대표)**: krafton "AX Governance Specialist"(AX 도입·거버넌스, 비개발
  직무), sendbird "Software Engineer, AI Agent"(AI Agent 제품 개발), moloco "Machine Learning Engineer"
  (전통적 AI/ML 엔지니어링). 선정 직전 Greenhouse에서 재조회해 여전히 '포함' 상태임을 재확인했다.
- **Gemini 실제 호출 결과**: **3건 전부 실패** — `google.genai.errors.ServerError: 503 UNAVAILABLE`
  ("This model is currently experiencing high demand"). 2026-10-04 STEP 09 때와 동일한 성격의 일시적
  서버 과부하로 보인다(인증·모델명 오류 아님). **공고당 정확히 1회만 호출했고, 코드 수준에서 자동 재시도
  루프를 만들지 않았다**(사용자 지시 그대로).
- **보고서는 실패를 숨기지 않고 그대로 작성**: `reports/test_send_3jobs_2026-10-05.md`에 3건 모두 "Gemini
  요약 실패"와 에러 메시지를 투명하게 기록했고, "자동 재시도는 하지 않았다"는 문구도 명시했다. 상단에는
  "이 보고서는 28건 중 3건만 다룬 시험 발송이며 나머지 25건은 분석되지 않았다"는 경고 문구를 넣어 전체
  분석으로 오인되지 않도록 했다. 하단에는 '검토 필요' 3건을 "추천에서 제외된 별도 목록"으로 명시했다.
- **Slack·Gmail 실제 발송**: 각각 정확히 1회 — **Slack: 상태 200/본문 "ok"(성공)**, **Gmail: SMTP 세션
  정상 종료(성공)**. Slack에는 `notify.send_slack(webhook_url, 보고서_전체_텍스트, dry_run=False)`로 **보고서
  내용 자체**를 보냈다(로컬 경로 문자열이 아님). **이 발송은 되돌릴 수 없다** — 실제로 "Gemini 요약 실패"가
  표시된 보고서가 사용자의 Slack 채널과 Gmail 수신함에 실제로 전달되었다.
- **"나머지 공고를 이미 보낸 것으로 기록"되지 않도록 한 조치**: 이번 작업은 `main.py`를 실행하지 않고
  별도의 1회성 스크립트(`test_send_3jobs.py`, 프로젝트 코드로 커밋되지 않음 — 스크래치패드에만 존재)로
  수행했다. `greenhouse_jobs.csv`(운영 이력/캐시 파일)는 **이번에도 생성되지 않았다** — 이 파일 자체가
  없으므로 "28건 중 25건이 이미 처리됨"이라는 잘못된 기록이 발생할 여지가 애초에 없다. `history_linkedin_
  manual.csv`도 건드리지 않았다.
- **중단 지점**: 사용자 지시("실패하면 자동 재발송하지 말고 결과를 기록한 뒤 멈춰줘")에 따라, Gemini
  재호출을 시도하지 않고 여기서 멈췄다. **다음 Gemini 재시도는 사용자의 명시적 요청이 있어야 진행한다.**
- 완료 근거: 사용자가 요청한 8개 항목(검토 필요 3건 분리 유지/서로 다른 직무 3건 선정/공고당 1회·재시도
  금지/3건 전용 보고서+전체 28건으로 오인 금지/Slack·Gmail 각 1회 실제 발송/Slack에 내용 전송/실패 시
  재발송 금지하고 결과 기록/나머지 미발송 오기록 방지) 중 Gemini 요약 자체를 제외한 나머지는 전부 충족.
  Gemini 요약은 **3건 모두 실패로 끝났고, 이는 완료가 아니라 "시도했으나 실패 → 사용자 지시대로 중단"**
  이라는 사실 그대로 기록한다.

## Greenhouse 자동 수집 구현 (2026-10-05, `src/collect.py`·`src/analyze.py`·`src/report.py`·`main.py` 연결 — dry-run 검증 완료)

- 배경: 사용자가 "조사한 4개 기업으로 먼저 자동 수집 구현을 진행해달라"고 요청하며, 확정 AI·AX 공고는
  포함, 애매한 건은 '검토 필요'로 별도 표시, 쿠팡은 기존 제외 유지하고 자동 수집과 섞지 말 것, 신규/기존/
  마감 구분, 수집 실패를 0건으로 취급 금지, dry-run에서도 실제 수집은 하되 Gemini/발송/이력 변경은 금지,
  요약 없는 신규 공고는 'AI 요약 미실행'+본문 기반 정보로 표시할 것을 지시.

### 새로 만든/연결한 코드

| 파일 | 추가 내용 |
|---|---|
| `src/collect.py` | `fetch_greenhouse_company()`(회사 1곳, 실패해도 예외 던지지 않고 `status="error"`로 반환), `fetch_greenhouse_jobs()`(4개 기업 순회, 한 곳 실패해도 나머지 계속), `parse_greenhouse_job()`(HTML 본문 추출, 일부 공고의 이중 HTML 이스케이프 보정 포함) |
| `src/analyze.py` | `classify_ai_ax_relevance()` — 2026-10-05 수동 검토 32건을 코드화한 휴리스틱 분류기(포함/검토 필요/제외 + 원문 근거), `screen_greenhouse_candidates()`(제목+한국 근무지 1차 스크리닝), `diff_greenhouse_jobs()`(신규/기존/마감 판정, **수집 실패 기업은 마감 판정에서 제외**) |
| `src/report.py` | `build_greenhouse_section_markdown()` 등 — Greenhouse 전용 섹션(기업별 현황표/신규 포함/기존 포함/검토 필요/마감), LinkedIn 섹션과 완전히 분리 |
| `main.py` | `run_linkedin_track()` + `run_greenhouse_track()` 분리 실행, 두 트랙의 Gemini 호출·보고서·알림을 통합 오케스트레이션 |

### dry-run 실제 실행 결과

- 4개 기업 실제 조회: krafton 53건, daangn 46건, sendbird 8건, moloco 41건(합계 148건) — 전부 성공.
- 제목+한국 근무지 1차 스크리닝 통과 32건 → 자동 분류 **포함 28건 / 검토 필요 3건 / 제외 1건**.
- Gemini 실제 호출 **0건**(dry-run) — 요약 없는 신규 공고는 보고서에 "AI 요약 미실행" + 본문 발췌 +
  포함/검토 이유로 표시됨.
- `greenhouse_jobs.csv`는 dry-run에서 **생성되지 않음**(운영 이력 미변경 확인), `history_linkedin_manual.csv`/
  `linkedin_manual_4469459251.csv` 수정 시각도 실행 전후 불변.
- 같은 dry-run을 2회 연속 실행 → 보고서가 (생성 시각 제외) **완전히 동일**(재현성 확인).
- 보고서: `reports/weekly_report_2026-10-05.md` (새 구조: 1-전체 요약 / 2-Greenhouse 자동 수집(2-1 기업별
  현황 ~ 2-5 마감) / 3-LinkedIn 수동 트랙(기존 로직) / 4-데이터 출처와 한계).

### 발견해 즉시 고친 버그 2건

1. `load_manual_records()`의 glob이 작업 중 만든 백업 CSV(`linkedin_manual_....backup-...csv`)까지
   집어 "레코드 2건 로드"로 오염시킴을 발견 → 백업을 `data/processed/_backups/`로 옮겨 glob에서 제외,
   재확인 결과 정확히 1건만 로드됨.
2. krafton 일부 공고(예: AI Native Full Stack Engineer)의 `content` 필드가 HTML 엔티티로 이중
   이스케이프되어 있어(`&lt;div&gt;...`) 본문 발췌에 HTML 태그가 그대로 섞여 나옴을 발견 → `html.unescape()`
   선적용으로 수정, 재실행 후 깨끗한 텍스트로 확인(분류 결과 자체는 이 버그와 무관 — 핵심 키워드는 태그
   사이에서도 매칭되고 있었음).

### 수집 실패 안전장치 — 단위 테스트로 검증

이번 dry-run에서는 4개 기업이 전부 성공해 실패 경로를 자연 발생시키지 못해, `diff_greenhouse_jobs()`를
가상 이력(실패 기업 1곳 포함)으로 직접 호출하는 별도 테스트를 실행 — **수집 실패 기업의 기존 이력은
'마감'으로 바뀌지 않고 보존되고, 성공한 기업의 사라진 공고만 정확히 '마감' 판정됨**을 확인(assert 통과).

### 2026-10-04 수동 검토(29/2/1) 대비 자동 분류(28/3/1) 차이 — 투명 공개

"[AI Transformation Dept.] Sr. AI DevOps Engineer"가 수동 검토에서는 '포함'(AX 근거가 "팀 소개" 문단에
있었음)이었으나, 자동 분류기는 그 문단을 의도적으로 보지 않아(20여 개 krafton 공고에서 반복되는 "본부
소개" 보일러플레이트까지 걸려 "AI Operation Manager"류 오탐이 재발하는 것을 막기 위함) '검토 필요'로
내렸다. **버그가 아니라 설계된 보수적 동작** — 확신 없는 판정을 '포함'으로 단정하지 않는다는 원칙 그대로다.

- 완료 근거: 사용자가 요청한 7개 항목(확정 포함/애매 검토 필요 분리, 쿠팡 미변경·미혼합, src/collect.py·
  main.py 연결, 신규/기존/마감 구분, 수집 실패≠0건, dry-run 실제 수집+호출·발송·이력변경 금지, AI 요약
  미실행+본문 기반 정보 표시) 전부 실제 실행·단위 테스트로 충족. 예약 활성화는 하지 않음.

- 배경: 대안 수집 경로 조사(아래 섹션) 이후, 사용자가 "AI·ML 엔지니어뿐 아니라 AX(생성형AI/LLM/RAG/AI
  Agent 개발 + AI 도입·업무자동화·운영개선·AI 서비스 기획) 포지션도 원한다"고 범위를 확장. "직무명뿐 아니라
  업무·자격요건 본문으로 판단하고 포함 이유를 보여달라, 단순 키워드 언급만으로 포함하지 말라, 크래프톤은
  첫 검증 기업일 뿐 최종 범위가 한 회사로 제한되는 건 아니다"를 명시.
- Greenhouse에서 **daangn(46건)·sendbird(8건)·moloco(41건)**을 KRAFTON 외 추가로 실제 확인(보드 존재,
  공고 수 확인) — "한 회사 제한" 우려 해소.
- 4개 기업 전체 공고 중 제목+한국 근무지 1차 스크리닝 통과 **32건 전원의 본문을 실제로 읽고** 판정:
  **포함 29건 / 보류(애매) 2건 / 제외 1건.** Notebook `[신규 조사] 수집 대상 범위 확장` 블록에 전체 판정표
  (공고별 본문 인용 근거 포함) 기록.
- **본문 확인으로 판정이 뒤집힌 사례(제목만으론 틀렸을 사례)**:
  - "Game Product Owner"/"Product Owner"(krafton) — 제목만으론 AI 기술직이 아니라 보류했을 것이나, 본문에
    "AI Engineer/Researcher와 협업하여 AI 솔루션 설계", "AI 기술 기반 신규 제품 기획"이 명시되어 **"AI 서비스
    기획"으로 포함 확정**.
  - "AI Operation Manager"(krafton) — 제목은 AX스럽지만, 본문 실제 업무는 "운영계획 수립·리포트", "예산·인사
    리소스 운영", "채용 프로그램 운영", "조직문화 프로그램 기획"뿐인 **순수 행정 운영** — **제외 확정**.
  - 이 두 유형의 대비가 "단순 키워드/제목 매칭이 아니라 본문 기반 판단이 필요하다"는 사용자 지시가 실제로
    유효함을 증명한다.
- **보류(애매) 2건**: krafton "Data Program Manager"(ML 학습데이터 조달/벤더관리 — AI 자체 개발/AX 운영개선
  과는 결이 다름), daangn "Security Engineer(AI Security)"(LLM/에이전트 보안 공격기법 연구 — "개발"도 "AX
  운영개선"도 아닌 제3의 성격). 최종 포함 여부는 사용자 판단 필요.
- **쿠팡(LinkedIn) 레코드 재검토**: `data/processed/linkedin_manual_4469459251.csv`에 `ax_criteria_reviewed_at`,
  `ax_reconsideration_candidate=True`, `ax_reconsideration_reason`(근거: 원문 job_description에 "생성형 AI
  기반 CS 운영 효율화", "LLM을 활용한 업무 자동화", "AI Agent, RAG 등 AI 기술을 활용한 운영 프로세스 개선"이
  이미 명시되어 새 AX 기준에 매우 높은 부합) **3개 컬럼만 추가**. **`excluded_from_analysis`(=True)·
  `exclusion_reason` 등 기존 값은 작업 전후 완전히 동일함을 코드로 확인**(사전 백업:
  `linkedin_manual_4469459251.backup-2026-10-05-pre-ax-review.csv`). **자동으로 제외 결정을 바꾸지 않았다.**
- 완료 근거: 사용자가 요청한 4개 항목(본문 기반 판단+포함 이유 제시/단순 키워드 매칭 금지/다중 기업 검증/
  쿠팡 재검토 후보 표시만 하고 기존 결정 불변) 전부 실제 실행 결과로 충족. 기존 수집 코드 교체·Gemini 호출·
  발송·예약 변경은 하지 않음.

## 대안 수집 경로 조사 (2026-10-05, 공식 API·자동 수집 허용 기업 채용 페이지 비교 — 완료, 전략 결정은 사용자 보류)

## 대안 수집 경로 조사 (2026-10-05, 공식 API·자동 수집 허용 기업 채용 페이지 비교 — 완료, 전략 결정은 사용자 보류)

- 배경: 잡코리아 자동 수집 가능성 검증(아래 섹션) 이후, 사용자가 "수동 입력으로 돌아가지 말고 다른 수집
  경로를 조사해달라"고 결정. 목표는 매주 새 AI 엔지니어 공고 자동 수집·분석·발송.
- 에이전트가 `ai-job-agent`의 `.venv`로 직접 실행(requests, 공개 API만 호출 — 가입·키 발급이 필요한 곳은
  실제 호출하지 않음) + WebSearch/WebFetch로 공식 문서 확인. LinkedIn·잡코리아 파일은 전혀 접촉하지 않음
  (파일 수정 시각 불변 재확인). Notebook `[신규 조사] 대안 수집 경로 조사` 블록(3셀)에 전체 기록.

| 항목 | 워크넷(Work24) OpenAPI | 사람인(Saramin) OpenAPI | **Greenhouse Job Board API**(예: KRAFTON) |
|---|---|---|---|
| 근거 | [data.go.kr](https://www.data.go.kr/data/3038225/openapi.do?recommendDataYn=Y) | [oapi.saramin.co.kr](https://oapi.saramin.co.kr/introduce) | [docs.greenhouse.io](https://docs.greenhouse.io/job-board.html) |
| 가입/인증 | 공공데이터포털 가입+활용신청(자동승인 표기)+키 발급 | 이용신청+승인+access-key 발급 | **불필요**(공개 API) |
| 비용 | 무료 | 명시 안 됨("베타") | 무료 |
| 재사용 조건 | **공공저작물 제4유형: 출처표시+상업적 이용금지+변경금지** | 출처 표기 요구만 확인 | 명시된 제한 없음 |
| 업무/자격요건 제공 | 문서상 미확인(실호출 전까지 불확실) | **응답에 없음**(URL로 재방문 필요 — 잡코리아와 같은 문제로 회귀) | **제공됨**(`content=true`) |
| 실제 호출 검증 | **미검증**(키 미발급) | **미검증**(키 미발급) | **검증 완료** |
| 커버리지 | 한국 채용시장 전체(이론상) | 한국 채용시장 전체(이론상) | **Greenhouse를 쓰는 기업만**(전수 조사 안 함) |

- **Greenhouse 실제 검증**: `boards-api.greenhouse.io/v1/boards/krafton/jobs?content=true` 실제 호출 —
  전체 공고 53건 중 제목에 'AI'+'Engineer' 포함 공고 **7건**(전부 서울 근무) 확인. 2건의 상세 본문을 실제로
  수집해 "필수요건"·"우대요건"·담당 업무 섹션이 **전부 실제 텍스트로 존재**함을 확인(8,779자/15,242자).
  이미지 아님, 차단 없음.
- **단정하지 않은 사항**: 워크넷의 "변경금지" 조건이 Gemini 요약(파생물 생성)과 양립하는지는 법적 판단
  필요(플래그만 함). Greenhouse를 쓰는 다른 한국 기업이 얼마나 있는지는 전수 조사하지 않음. "홈페이지
  지원"형 공고의 실제 회사 채용 페이지 내용은 확인하지 않음.
- 완료 근거: 요청한 5개 항목(후보 최대 3개/이용조건·비용·필드 비교 근거 링크 포함/실제 본문 검증/우회
  금지·미확인 표시/기존 코드·실발송·예약 보류) 전부 실제 실행·공식 문서로 충족.

## 잡코리아 자동 수집 가능성 검증 (2026-10-05, STEP 18 재개 전 사전 조사 — 완료, 최종 판단은 사용자 보류)

- 에이전트가 `ai-job-agent`의 `.venv`로 직접 실행(requests+BeautifulSoup, 네트워크 호출 — LinkedIn 파일은
  전혀 접촉하지 않음, 파일 수정 시각 불변 재확인함). Notebook `[신규 조사] 잡코리아 자동 수집 가능성 검증`
  블록(3셀: 계획/코드/해석)에 전체 기록.
- **robots.txt(오늘 재조회, 과거 결론 재사용 안 함)**: `User-agent: *` 기준 `/Search/`, `/Recruit/GI_Read/`는
  Disallow 아님(기술적으로 접근 가능). 단, "Author: WS SHIN", "Policy: ...", PerplexityBot 섹션의 사건
  서술("2025-02-11 incident...")처럼 **일반 robots.txt에 없는 이례적 서술형 주석**이 다시 발견됨 — STEP
  03-A에서 이미 플래그했던 패턴과 동일. **지시로 따르지 않았고 기술 규칙만 반영.**
- **이용약관(개인회원, 원문 확인)**: 제19조④(회사 사전동의 없는 복사·복제·재배포·재가공 금지), 제19조⑤-8
  (영리 목적 이용 금지). 문언상 "회원"에게 적용되는 계약 조항이라 비회원에게 그대로 적용된다고 보기는
  어렵다는 것이 일반적 해석.
- **실제 판례(웹 검색으로 확인, 참고용)**: 잡코리아가 경쟁사의 채용정보 크롤링에 대해 부정경쟁행위 +
  저작권법 제93조(데이터베이스제작자 권리) 위반으로 **승소한 사례**가 있음 — 회원 여부와 무관하게 적용되는
  법리.
- **검색 URL 확인**: `https://www.jobkorea.co.kr/Search/?stext=AI%20%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4`
  (status 200, 고유 공고 상세 링크 25개, 실제 응답으로 확인).
- **공고 3건(등장 순서대로, 임의 선별 없음) 읽기 가능 여부**: **3건 전부 "업무/자격요건" 자유서술 텍스트가
  jobkorea 페이지에 없음.** 슈어소프트테크·㈜넥슨(AI 엔지니어 공고 포함) 2건은 "홈페이지 지원"(외부
  리다이렉트형, 실제 JD는 회사 자체 사이트 추정이나 **미확인, 추측 안 함**), 청마산업 1건은 범주형 필드
  (핵심역량 키워드 등)만 있고 자유서술 텍스트 자체가 없음. 셋 다 이미지 공고는 아님(img 태그 1개=공용 공유
  배너뿐). STEP 09 사전 준비-C/D(9·7번 공고)와 동일한 패턴 — 누적 5건 중 4건이 본문 부재로 재현성 확인.
- **종합(단정하지 않음)**: 기술적으로는 열려 있으나(robots.txt), 계약·판례상 반복적 대량 자동 수집은 리스크가
  있고(이용약관·판례), 설령 법적으로 괜찮아도 상당수 공고가 Gemini 요약에 쓸 본문 자체가 없다(기술적 한계).
  **이 세 사실을 있는 그대로 전달하며, "해도 된다/안 된다"는 결론은 에이전트가 내리지 않는다.**

## STEP 18 — 주간 자동 스케줄 (2026-10-05 설정 → 2026-10-05 사용자 지시로 보류, 잡코리아 자동 수집 검증 선행 예정)

> ⚠️ **현재 상태: 보류(on hold).** 아래는 설정했던 내용과 그 직후 보류를 결정하게 된 경위를 그대로 남긴
> 기록이다. **schedule은 다시 주석 처리되어 비활성 상태**이고, **main 반영용 PR은 merge하지 않았다.**
> 사용자가 "잡코리아 자동 수집 가능성을 먼저 검증한 뒤 예약 설정을 이어가겠다"고 결정했기 때문이다.

### 희망 일정 (보류 중에도 그대로 보존)

매주 금요일 오전 9시 10분(한국 시간, KST=UTC+9) → UTC로는 금요일 00:10 → cron 표현식 `10 0 * * 5`
(분=10, 시=0, 요일=5(금)). workflow 파일에도 같은 값을 주석으로 남겨뒀다 — 재개 시 주석만 해제하면 된다.

### workflow 변경 내역 (`'.github/workflows/ai-job-agent-weekly-report.yml'`)

| 요구사항 | 반영 방법 |
|---|---|
| schedule cron 설정 | `schedule: - cron: "10 0 * * 5"` 추가(주석 해제 아니라 아예 다시 작성 — 기존 예시 cron이 아니라 요청받은 값으로). |
| schedule 이벤트에서는 항상 live | 새 단계 "실행 모드 결정"(`id: mode`)에서 `github.event_name == 'schedule'`이면 무조건 `live=true`로 판정하고, `workflow_dispatch`는 기존처럼 `live` 입력값을 따르도록 분리했다. 이후 모든 단계는 `inputs.live`가 아니라 이 단계의 출력(`steps.mode.outputs.live`)을 본다. |
| 수동 실행은 기존처럼 기본 dry-run 유지 | `workflow_dispatch`의 `live` 입력 기본값은 그대로 `false` — 변경 없음. |
| Secrets 5개 없으면 발송 전 명확히 실패 | 새 단계 "GitHub Secrets 5개 검증"을 파이프라인 실행 **직전**에 추가. `live=true`일 때만 동작하며, 5개 변수 중 비어 있는 것이 있으면 `::error::` 로 **이름만** 나열하고(`GEMINI_API_KEY`처럼 변수명만, 값은 전혀 출력하지 않음) `exit 1`로 실패시켜, 실제 Gemini 호출/Slack·Gmail 발송 자체가 시도되지 않도록 막는다. |
| LinkedIn 입력은 계속 수동, GitHub 반영 데이터로 실행 | workflow 파일 최상단 주석에 "새로 크롤링하지 않고, 이 시점에 저장소(main)에 반영되어 있는 `data/processed/`의 레코드만 읽는다. 새 공고를 포함하려면 로컬에서 수동 입력 → 커밋 → main 반영이 먼저 필요하다"고 명시했다. |
| 실행 간 신규판별 이력 유지 | 기존 "운영 이력 파일 커밋" 단계를 그대로 유지하되, 조건을 `inputs.live == true`에서 `steps.mode.outputs.live == 'true'`로 바꿔 schedule 실행에서도 동작하도록 했다(기존에는 schedule이 없었으므로 이 조건이 schedule에서 평가될 일이 없었다). `history_linkedin_manual.csv` 변경 사항이 있으면 커밋 후 같은 브랜치(스케줄의 경우 `main`)로 `git push`해, 다음 실행이 이전 실행의 이력을 그대로 이어받는다. |

### 로컬 검증 결과

- YAML 파싱: `yaml.safe_load`로 전체 파일 재검증 — 문법 오류 없음, `schedule: [{'cron': '10 0 * * 5'}]`로 정확히 반영됨을 확인. 8개 스텝(체크아웃/모드결정/Python설치/의존성설치/Secrets검증/파이프라인실행/아티팩트업로드/이력커밋) 구조 확인.
- Secrets 검증 단계 로직: 더미 값으로 bash에서 직접 시뮬레이션 — (a) 5개 중 1개(`GEMINI_API_KEY`)를 비워두면 `MISSING: GEMINI_API_KEY` 출력 후 `exit 1`(실패) 확인, (b) 5개 모두 채우면 `ALL SET` 출력 후 `exit 0`(통과) 확인. 값 자체는 더미 문자열(`"x"`)만 사용했고 실제 Secrets 값은 어디에도 사용하지 않았다.
- **실제 GitHub 환경에서의 schedule 트리거 동작, live 파이프라인 실행, Secrets 검증 실패/통과, 이력 커밋·push는 전혀 실행하지 않았다** — 로컬에서 재현 불가능한 부분이며, merge 후 실제 예약 실행에서만 확인 가능하다.

### 알아둘 점 (완료 판정에 영향)

- **schedule은 기본 브랜치(main)에서만 동작한다.** 지금 이 파일은 `ax-job-agent` 브랜치에 커밋했고, main으로
  가는 PR을 준비했다(아래 PR 링크). **PR이 merge되기 전까지는 금요일이 되어도 자동 실행되지 않는다.**
- live 경로(`python main.py --live`, Gemini 실제 호출, Slack/Gmail 실제 발송, 이력 파일 커밋·push)는 **GitHub
  환경에서 단 한 번도 실행된 적이 없다** — 이번이 설정된 첫 기회이며, 첫 금요일 실행이 사실상 최초 live 종단
  간(end-to-end) 검증이 된다.
- `permissions: contents: write`가 schedule 실행에도 동일하게 적용되는지(이력 파일 push 성공 여부)는 실제
  실행에서만 확인 가능하다.

### 보류 결정 (2026-10-05, 같은 날 — 위 설정 직후)

- **사용자가 STEP 18 예약 활성화를 보류하기로 결정했다**: "먼저 잡코리아 자동 수집 가능성을 검증한 뒤
  예약 설정을 이어가겠다."
- 이에 따라 조치한 것:
  - workflow의 `schedule:` 블록을 다시 **주석 처리**해 비활성화(`on:`에는 더 이상 `schedule` 키가 없음 —
    `yaml.safe_load`로 재확인). 희망 일정(`10 0 * * 5`)은 주석으로 그대로 보존.
  - main 반영용 PR은 **merge하지 않음**(애초에 merge한 적도 없음 — 계속 미병합 상태 유지).
  - 실행 모드 결정/Secrets 검증/이력 커밋 로직(코드 자체)은 **삭제하지 않고 그대로 보존** — schedule 트리거가
    없으므로 어차피 발동하지 않으며, 나중에 주석만 해제하면 바로 다시 쓸 수 있다.
- **STEP 18은 "보류(on hold)"로 분류한다** — "미완료"보다 한 단계 더 명확한 상태 표시다: 사용자가 스스로
  일시 중단을 결정한 것이지, 실행이 실패했거나 준비가 안 된 것이 아니다.
- 다음 재개 조건: 사용자가 잡코리아 자동 수집 가능성 검증을 마치고 다시 요청하면, 보존해 둔 cron 값
  그대로 `schedule:` 주석을 해제하고 PR 리뷰·merge를 진행한다.

## STEP 17 — 실제 GitHub Actions 실행 결과 (2026-10-05, 완료)

- **사용자가 GitHub Actions 탭에서 workflow를 직접 수동 실행(`workflow_dispatch`, `live` 입력 없이 =
  dry-run)했고, 실행이 Success(초록 체크)로 종료됨을 확인했다.**
- **사용자가 생성된 Artifact(`weekly-report`)를 직접 다운로드해 보고서 내용을 확인**했고, "전체 1건·추천
  대상 0건"으로 — 로컬 dry-run(STEP 14~16)과 **동일한 결과**임을 확인했다.
- 이로써 SPEC.md §11의 STEP 17 완료 조건("GitHub Actions 수동 실행이 성공하고 ... 확인") 중 **수동 실행 성공
  + 결과 확인** 부분이 충족되었다. (이력 파일 복원 확인은 `live` 실행 시에만 해당하는 조건이며, 이번은
  dry-run 실행이었으므로 해당 사항 없음 — dry-run은 애초에 이력 파일을 변경하지 않도록 설계되어 있다.)
- **STEP 17을 완료로 확정한다.**
- 추가로 수행한 것 없음 — 이번에도 실제 Gemini 호출/Slack·Gmail 발송은 일어나지 않았다(dry-run이었으므로).
- **STEP 18(주간 자동 스케줄)은 사용자 지시에 따라 여전히 미설정 상태로 유지한다.** `schedule:`은 계속
  주석 처리된 채로 남아 있으며, 사용자가 원하는 요일·시간을 알려줄 때까지 손대지 않는다.

## STEP 17~18 — GitHub Actions 준비 (2026-10-05, workflow 파일 작성 + 로컬 검증 — 과거 기록, 아래 참고)

> ⚠️ 이 섹션은 **실제 GitHub 실행 전**에 작성한 준비 기록입니다. 실제 실행 결과는 위 "STEP 17 — 실제 GitHub
> Actions 실행 결과" 섹션이 최신입니다. 이 섹션은 작업 이력 보존을 위해 그대로 남겨둡니다.

### 이번에 만든 파일

- `C:\dev\claude-code-agent-course\.github\workflows\ai-job-agent-weekly-report.yml` (저장소 **루트** 기준
  경로 — `chapter11/` 아래가 아님. GitHub Actions는 workflow 파일이 저장소 루트의 `.github/workflows/`에
  있어야만 인식한다). 기존 3개 workflow(`fast-track-smoke.yml`, `resource-policy-guard.yml`,
  `resource-smoke.yml`)는 전혀 건드리지 않았다.
- `chapter11/ai-job-agent/requirements.txt` — 현재 `.venv`에 실제로 설치된 버전으로 고정
  (`pandas==3.0.6`, `requests==2.34.2`, `beautifulsoup4==4.15.0`, `python-dotenv==1.2.4`, `google-genai==2.28.0`).

### workflow 설계 — 요구사항 반영 내역

| 요구사항 | 반영 방법 |
|---|---|
| 기본 검증은 외부 호출·발송 없는 dry-run | 트리거는 `workflow_dispatch`뿐이고, `live` 입력(boolean, 기본값 `false`)이 `true`일 때만 `python main.py --live`를, 아니면 `python main.py`(dry-run)를 실행한다. |
| LinkedIn 공고 입력은 계속 수동임을 명시 | workflow 파일 상단 주석에 "LinkedIn에서 새로 크롤링하지 않으며, `data/processed/`에 이미 저장된 수동 입력 레코드만 사용한다"고 명시했다. |
| `.env`/비밀값 커밋 금지, GitHub Secrets 사용 | workflow의 `env:`에서 `${{ secrets.GEMINI_API_KEY }}` 등 5개를 참조한다. `.env` 파일 자체는 `.gitignore`에 이미 등록되어 있어 커밋 대상이 아니다. |
| 필요한 workflow·의존성 작성 | 위 2개 파일. |
| 가능한 로컬 검증 | 아래 "로컬 검증 결과" 참고. |
| 자동 스케줄은 사용자 확인 전 설정 금지 | `schedule:` 블록 전체를 주석 처리해 두었다(비활성 상태). cron 예시(`매주 월요일 09:00 KST`)만 주석으로 남겼다. |
| push·실제 발송 금지 | 이번 세션에서 `git push`를 실행하지 않았다(로컬에만 파일 존재, `git status`에 `??`로 표시됨). Slack/Gmail/Gemini 실제 호출도 하지 않았다. |

### 로컬 검증 결과 (GitHub 인프라를 실제로 호출하지 않고 확인 가능한 범위)

- YAML 문법: `python -c "import yaml; yaml.safe_load(open(...))"` 으로 파싱 성공 확인(문법 오류 없음).
- CI와 동일한 명령 시뮬레이션: 저장소 루트에서 `chapter11/ai-job-agent` 디렉터리로 이동한 뒤, 기존
  `.venv`로 `pip install -r requirements.txt`(이미 설치된 버전과 동일하므로 "Requirement already satisfied")
  → `python main.py`(dry-run) 실행 → `returncode 0`, STEP 16에서 이미 검증한 것과 동일한 로그 패턴 확인.
  (CI 전용 `ubuntu-latest` 러너 자체는 로컬에서 재현 불가능 — 이는 실제 GitHub 실행에서만 확인 가능하다.)
- **실제 GitHub Actions 실행 자체는 수행하지 않았다** — `git push`를 하지 않았으므로 원격 저장소에 이
  workflow 파일이 아직 존재하지 않고, Actions 탭에서 실행된 적도 없다.

### 알아둘 점 (완료 판정에 영향)

- `python-version: "3.14"`는 로컬 `.venv`(3.14.6)와 맞췄지만, GitHub가 제공하는 `ubuntu-latest` 러너에
  3.14가 바로 없을 수 있다. **실제 실행에서 이 단계가 실패하면 "3.12" 등으로 낮춰야 한다** — 이것도 실제
  GitHub 실행을 통해서만 확인 가능하므로, STEP 17을 완료로 표시하지 않는 이유 중 하나다.
- `permissions: contents: write`와 "운영 이력 파일 커밋" 단계는 `live=true`일 때만 동작하도록 만들어
  두었지만, 이 역시 실제로 실행해 본 적은 없다.

### 사용자가 GitHub에서 할 일 (초보자 기준, 클릭 순서)

**1. GitHub Secrets 등록** (저장소 Settings에서, 한 번만 하면 됨)
1. 브라우저에서 포크한 저장소(`github.com/<사용자계정>/claude-code-agent-course`)로 이동.
2. 상단 탭에서 **Settings** 클릭(저장소 소유자만 보임 — 안 보이면 포크 저장소인지, 본인이 소유자인지 확인).
3. 왼쪽 메뉴에서 **Secrets and variables** → **Actions** 클릭.
4. **New repository secret** 버튼을 5번 눌러 아래 5개를 각각 등록(Name은 정확히 아래대로, Value는 `.env`에
   저장한 실제 값):
   - `GEMINI_API_KEY`
   - `SLACK_WEBHOOK_URL`
   - `GMAIL_ADDRESS`
   - `GMAIL_APP_PASSWORD`
   - `GMAIL_TO_ADDRESS`
5. (처음에는 dry-run만 확인할 목적이라면, 사실 이 5개는 당장 없어도 workflow가 실패하지 않는다 — dry-run은
   이 값들을 쓰지 않기 때문이다. 다만 나중에 `live` 실행을 해볼 계획이라면 미리 등록해 두는 것을 권장한다.)

**2. 이 workflow 파일을 저장소에 반영(push)** — **이번 세션에서는 하지 않았으므로, 사용자가 직접 커밋/푸시를
승인해야 한다.** (다음에 "push 해줘"라고 요청하면 그때 진행한다.)

**3. Actions 탭에서 수동 실행**
1. 저장소 상단 탭에서 **Actions** 클릭.
2. 왼쪽 목록에서 **"ai-job-agent weekly report (chapter11)"** 클릭.
3. 오른쪽 **Run workflow** 드롭다운 버튼 클릭.
4. 브랜치 선택(workflow 파일이 존재하는 브랜치 — 예: `ax-job-agent` 또는 push한 브랜치), `live` 입력은
   처음엔 **체크하지 않은 상태(false, dry-run)** 로 두고 **Run workflow** 클릭.
5. 잠시 후 실행 목록에 새 줄이 생기고, 초록 체크(성공) 또는 빨간 X(실패)가 뜬다. 클릭하면 각 단계의 로그를
   볼 수 있다.
6. 성공하면 맨 아래 **Artifacts** 항목에서 `weekly-report`를 다운로드해 보고서 내용을 확인할 수 있다.

**4. (선택, 나중에) 실제 알림까지 확인하고 싶다면**
- 위와 동일하게 Run workflow를 누르되, 이번엔 `live` 입력을 **체크(true)** 한다. 이 경우 실제로 Gemini가
  호출되고 Slack/Gmail로 실제 메시지가 발송된다 — Secrets가 모두 등록되어 있어야 한다.

**⚠️ 반드시 지켜야 할 것**: 위 3번(Actions 탭에서 실제 수동 실행이 성공하는 것)을 사용자가 직접 확인하기
전에는, STEP 17을 완료로 표시하지 않는다. STEP 18(주간 자동 실행)은 사용자가 원하는 요일·시간을 알려주고,
그 일정으로 최소 1회 이상 실제 스케줄 실행이 동작하는 것까지 확인해야 완료로 표시한다.

### Slack/Gmail 연결 준비 안내 (최초 작성 — Slack은 이후 완료됨, Gmail 세부 내용은 아래 "STEP 13 준비" 섹션이 최신)

> 이 섹션은 최초 작성 당시(STEP 12 착수 전) 안내입니다. **Slack은 이후 STEP 12에서 실제로 완료되었고**,
> Gmail의 정확한 절차는 아래(위쪽) "STEP 13 준비 — Gmail 연결에 필요한 사항" 섹션에 공식 문서 확인 후
> 더 구체적으로 다시 정리했습니다. 이 섹션은 기록 보존을 위해 남겨둡니다.

사용자가 미리 준비할 것(비밀값은 여기 채팅에 올리지 않고 로컬 `.env`에 직접 입력):

- **Slack** (택1):
  - Incoming Webhook(간단): Slack 워크스페이스에 Webhook 앱 추가 → `.env`에 `SLACK_WEBHOOK_URL` 입력.
  - Bot Token(세밀한 제어 필요 시): Slack App 생성 + Bot Token 발급, 채널 초대 → `.env`에
    `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID` 입력.
- **Gmail**: 2단계 인증 활성화 후 앱 비밀번호 발급 → `.env`에 `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`,
  `GMAIL_TO_ADDRESS`(받을 주소) 입력.
- 변수명은 `.env.example`에 이미 추가해 두었습니다(값은 비어 있음). **정확한 인증 방식·변수 구성은 STEP 12~13
  착수 시 각 서비스 공식 문서로 다시 확인할 예정**이며, 지금 적은 이름은 예시입니다.

### STEP 12 — Slack Incoming Webhook 연결 시험 결과 (2026-10-05, 성공)

- 사용자가 공식 문서(`docs.slack.dev/messaging/sending-messages-using-incoming-webhooks`) 절차대로 앱 생성 →
  Incoming Webhooks 활성화 → 테스트 채널 선택 → Webhook 발급까지 완료하고, `.env`(프로젝트 루트)에
  `SLACK_WEBHOOK_URL`을 저장했습니다.
- 에이전트가 `python-dotenv`로 `.env`를 **명시적 경로**(`.../ai-job-agent/.env`)로 로드해 값이 실제로
  읽히는지 확인했습니다(로드 여부만 True/False로 확인, **값은 출력하지 않음**). URL이
  `https://hooks.slack.com/services/`로 시작하는 정상 형식임도 확인했습니다(형식만 확인, 값 미노출).
- **"채용정보 파이프라인 연결 테스트" 메시지를 정확히 1회** `requests.post`로 전송했습니다. 응답:
  **상태 코드 200, 본문 "ok"**(Slack의 표준 성공 응답).
- **사용자가 테스트 채널에서 실제 메시지 수신을 직접 확인했습니다(2026-10-05).** → **STEP 12 완료.**
- 추가 메시지는 보내지 않았습니다(정확히 1회로 중단).

### STEP 13 준비 — Gmail 연결에 필요한 사항 (2026-10-05 최초 안내 — 이후 아래에서 실제로 시험 완료)

공식 문서(`support.google.com/mail/answer/185833`, Google 앱 비밀번호 도움말)를 확인했습니다. 요지:

- **2단계 인증(2-Step Verification)이 반드시 먼저 켜져 있어야** 앱 비밀번호를 발급받을 수 있습니다.
- 앱 비밀번호 발급 페이지: `https://myaccount.google.com/apppasswords`
- 발급받은 16자리 앱 비밀번호로 `smtplib`에서 `smtp.gmail.com:587` + `starttls()` + `login()`하는 방식이
  공식적으로 안내되어 있습니다.
- 사용자가 준비할 것(비밀값은 채팅에 올리지 않고 `.env`에 직접 입력):
  1. 보낼 Gmail 계정의 2단계 인증 활성화(이미 되어 있으면 생략)
  2. `myaccount.google.com/apppasswords`에서 앱 비밀번호 발급(16자리)
  3. `.env`에 다음 3개 변수 입력(이미 `.env.example`에 이름만 있음):
     - `GMAIL_ADDRESS` — 보내는 Gmail 주소
     - `GMAIL_APP_PASSWORD` — 방금 발급받은 16자리 앱 비밀번호
     - `GMAIL_TO_ADDRESS` — 받을 주소(테스트용으로 본인 주소 권장)

### STEP 13 — Gmail 연결 시험 결과 (2026-10-05, 성공)

- 사용자가 위 준비사항(2단계 인증, 앱 비밀번호 발급)을 완료하고 `.env`에 3개 변수를 저장했습니다.
- 에이전트가 `python-dotenv`로 `.env`를 **명시적 경로**로 로드해 `GMAIL_ADDRESS`/`GMAIL_APP_PASSWORD`/
  `GMAIL_TO_ADDRESS` 3개 모두 로드됨을 확인했습니다(값은 출력하지 않음).
- `GMAIL_TO_ADDRESS`로 제목 **"채용정보 파이프라인 이메일 연결 테스트"** 메일을 `smtplib`로 **정확히 1회**
  발송했습니다(`smtp.gmail.com:587` + `starttls()` + `login()` + `sendmail()`). **SMTP 세션이 예외 없이
  정상 종료되어 전송 성공으로 기록했습니다.** 실패 시 자동 재발송하지 않도록 `try/except`로 구현했으나,
  이번에는 예외가 발생하지 않았습니다.
- **사용자 추가 확인 필요**: SMTP 성공은 "Gmail 서버가 메일을 접수했다"는 뜻입니다. `GMAIL_TO_ADDRESS`의
  받은편지함(스팸함 포함)에 실제로 도착했는지는 **사용자가 직접 확인**해야 최종 완료로 볼 수 있습니다.
- 추가 메일은 보내지 않았습니다(정확히 1회로 중단).
- **사용자가 수신함에서 실제 메일 수신을 직접 확인했습니다(2026-10-05).** → **STEP 13 완료.**

### STEP 14~16 — 함수화·main.py 통합·로컬 전체 실행 검증 (2026-10-05, dry-run 기준 완료)

**git 상태 확인**: 작업 전후로 `git status`를 확인했습니다 — `chapter11/`은 여전히 전체가 미추적(untracked)
상태라 커밋된 베이스라인과의 `git diff`는 의미가 없었고(비교 대상이 없음), 대신 이번에 새로 생긴/바뀐
파일 목록을 직접 확인해 의도한 범위(`chapter11/ai-job-agent/` 내부)만 바뀌었음을 확인했습니다. 커밋은
하지 않았습니다(요청받지 않음).

**새로 만든 파일**:
- `src/collect.py`, `src/clean.py`, `src/analyze.py`, `src/summarize.py`, `src/report.py`, `src/notify.py`,
  `src/__init__.py`
- `main.py` (프로젝트 루트)

**검증 결과(실제 실행, `.venv`로 직접 실행)**:
- `python main.py`(인자 없음 = dry-run) 1회 실행 → `returncode 0`, 수집 1건 → 정제 1건 → 신규 0건(운영
  이력 미변경) → 분석 대상 **0건**(제외 1건, "추천" 섹션에 미포함 확인) → Gemini 호출 **0건**(캐시된 응답
  재사용) → 보고서 저장(`reports/weekly_report_2026-10-05.md`) → Slack/Gmail 둘 다 `dry_run: True`(실제
  전송 없음).
- **같은 실행을 2회 연속**해서 타임스탬프를 제외한 출력이 완전히 동일함을 확인(`True`) — "같은 입력이면
  신규 0건이 재현된다"는 요구사항을 실행 결과로 검증.
- 작업 중 발견해 즉시 고친 버그: 검증 스크립트의 `subprocess.run(..., text=True)`에 인코딩을 지정하지
  않아 한글 출력이 Windows 기본 코드페이지(cp949)로 깨지는 문제 → `encoding="utf-8"` 추가로 해결.
- 데이터 안전성 재확인: `data/processed/linkedin_manual_4469459251.csv`와
  `data/processed/history_linkedin_manual.csv`의 파일 수정 시각이 dry-run 실행 전후로 **변경되지
  않았음**을 확인(= dry-run이 기존 데이터·이력을 건드리지 않음).

**⚠️ 검증하지 못한 것(완료로 표시하지 않음)**:
- `--live` 모드(실제 Gemini API 호출, 실제 Slack/Gmail 발송)는 **이번 작업에서 실행하지 않았다** — 사용자
  지시("Gemini 실제 호출이나 Slack·Gmail 발송을 하지 마")에 따른 것이며, 코드는 작성했지만 동작은 미검증 상태다.
- `main.py`의 `--live` 경로 중 "분석 대상인데 캐시된 응답이 없는 새 레코드"에 대한 실시간 Gemini 호출 분기도
  미검증이다(현재 유일한 레코드는 이미 캐시된 응답이 있어 이 분기 자체가 실행되지 않았다).

<details>
<summary>참고: 잡코리아 9·7번 공고 조사 이력(현재는 사용하지 않음 — STEP 09가 LinkedIn으로 변경됨)</summary>

사용자가 잡코리아 STEP 09를 LinkedIn으로 전환하기 전, 9번(한국투자증권)과 7번(안랩) 공고를 각각 확인했으나
둘 다 jobkorea 페이지에 "주요업무" 자유서술 텍스트가 없음(모집분야="홈페이지 지원")을 확인한 바 있다. 이
조사 자체는 유효한 기록이지만, 현재 진행 방향과는 무관하다.
</details>

- Notebook 재열람 시 저장 충돌 방지(중요): 에이전트가 `notebooks/ax_job_pipeline.ipynb`를 디스크에서 직접
  여러 차례 수정했습니다. 이미 열려 있는 탭이 있다면 `Ctrl+W`로 닫을 때 **"저장 안 함/Don't Save"** 를 선택한
  뒤, 탐색기에서 다시 클릭해 새로 여세요. 커널은 "Python (ai-job-agent)"를 선택합니다.
- 확인할 것: "[수동 입력 보완] STEP 09~10" 블록(쿠팡 레코드 보완 결과)과 "STEP 09 — Gemini 연동 준비 상태
  재점검" 블록(SDK/모델/키 상태).

## STEP 01~18 진행표 (잡코리아 트랙 기준)

> 아래 표는 **잡코리아 트랙**의 진행 상태입니다. **LinkedIn 수동 입력 트랙**의 STEP 06~08은 별도로 진행되어
> 완료되었습니다 — 위 "LinkedIn 수동 입력 트랙 — STEP 06~08 진행 결과" 섹션 참고(파일도 서로 다름: 잡코리아는
> 이 표의 STEP 06 미착수, LinkedIn은 `linkedin_manual_4469459251.csv`/`history_linkedin_manual.csv`로 이미 완료).

| STEP | 내용 | 상태 |
|---|---|---|
| 준비 | ax/ai 경로 확정 | **완료** (`ai-job-agent`로 확정) |
| 01 | 개발환경 확인 | **완료** (venv·패키지 설치·Notebook 작성·셀 실행 확인 모두 사용자 실행 결과로 확인됨) |
| 02 | 수집 데이터 명세 재확인 | **완료**(에이전트 직접 실행, 사용자 확인 대기) |
| 03 | 채용공고 페이지 접근 테스트(robots.txt + 검색페이지) | **완료**(에이전트 직접 실행, 사용자 확인 대기) |
| 04 | 소량 데이터 수집(실제 데이터 10건) | **완료**(에이전트 직접 실행, 사용자 확인 대기) |
| 05 | DataFrame 생성 | **완료**(에이전트 직접 실행, 사용자 확인 대기) |
| 06 | 전처리·중복 제거 (잡코리아 데이터) | 대기 (⚠️ STEP 09를 먼저 진행하기로 사용자가 결정 — 아래 참고. LinkedIn 트랙은 별도로 완료됨) |
| 07 | 신규 공고 판별 (잡코리아 데이터) | 대기 (LinkedIn 트랙은 별도로 완료됨) |
| 08 | 기본 분석·관련 공고 필터링 (잡코리아 데이터) | 대기 (LinkedIn 트랙은 별도로 완료됨 — 분석 대상 0건) |
| 09 | Gemini API 연동 | **완료(LinkedIn 쿠팡 공고 1건 시험 호출 성공, `gemini-3.8-flash`)** |
| 10 | Gemini 결과 검증 | **확인 대기(수정판 비교표 기준)** — 에이전트 1차 대조 완료, 사용자 최종 확인 필요 |
| 11 | Markdown 보고서 생성 | **완료(시험판)** — `reports/step11_gemini_test_report_2026-10-04.md` |
| 12 | Slack 발송 | **완료** — 1회 발송(응답 200/ok) + 사용자가 테스트 채널에서 실제 수신 확인(2026-10-05) |
| 13 | Gmail 발송 | **완료** — 1회 발송(SMTP 예외 없음) + 사용자가 수신함에서 실제 수신 확인(2026-10-05) |
| 14 | 함수화·모듈 분리 | **완료** — `src/{collect,clean,analyze,summarize,report,notify}.py` |
| 15 | main.py 통합 | **완료(dry-run 기본값)** — `python main.py` 실행 성공 |
| 16 | 로컬 전체 실행 검증 | **완료(dry-run, 재현성 확인)** — `--live` 모드는 미실행·미검증 |
| 17 | GitHub Actions 수동 실행 | **완료** — 사용자가 Actions 탭에서 수동 dry-run 실행 → Success, Artifact 보고서로 "전체 1건·추천 대상 0건" 확인(2026-10-05) |
| 18 | GitHub Actions 주간 실행 | **schedule 활성화 완료 + 실제 발송 1회 검증(수동)**, **merge 전이라 완료 아님** — 금요일 09:10 KST cron 켜짐, PR 준비됨(미병합). main 반영 + 첫 실제 스케줄 실행 확인 후 완료로 갱신 예정 |

> ⚠️ **STEP 순서 예외(사용자 명시적 결정)**: 잡코리아 트랙의 STEP 06~08(정제/신규판별/분석 필터링)을 아직 거치지
> 않은 채로, STEP 09(Gemini 연동)를 기존 10건 원본 데이터로 먼저 시험해 보기로 했습니다. 이는 Gemini 연동 자체가
> 되는지 빠르게 확인하려는 의도적 선택이며, 정식 파이프라인에서는 STEP 06~08을 먼저 마치는 순서를 따릅니다.
