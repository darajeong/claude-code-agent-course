# WORK_LOG — 작업 기록

> 세션마다 기록을 **추가**합니다. 이전 기록은 삭제하지 않습니다. 최신 기록이 맨 아래로 가도록 추가하세요.

## 초기 진행 요약 (이번 문서 작성 이전, 대화 기준 — 로컬 미확인 포함)

사용자와 GPT Web의 대화에서 확인된 내용(로컬에서 직접 확인한 것은 아래 "세션 기록"의 2026-10-04 항목 참고):

- GitHub 계정 `darajeong`, Fork `darajeong/claude-code-agent-course`, 원본 `GilbertMoon/claude-code-agent-course`.
- 로컬 Clone 위치: `C:\dev\claude-code-agent-course`, VS Code로 열어 작업.
- `origin` = Fork, `upstream` = 강의 원본 저장소로 연결.
- `ax-job-agent` 브랜치 생성(`git branch`에서 `*` 확인).
- `chapter11/ax-job-agent` 폴더 생성(`pwd`로 확인).
- 해당 폴더에서 `python -m venv .venv` 실행, `Test-Path .venv\Scripts\python.exe` → `True`.
- 가상환경 활성화 후 `(.venv)` 프롬프트 확인.
- `python --version` → `Python 3.14.6`.
- `where.exe python` 첫 경로 → `C:\dev\claude-code-agent-course\chapter11\ax-job-agent\.venv\Scripts\python.exe`.
- pip 업그레이드 + `pandas, requests, beautifulsoup4, jupyter, python-dotenv` 설치 명령 실행, 설치 목록 확인.
- VS Code Python 인터프리터 선택 완료라고 사용자 보고.
- **Notebook 생성·커널 선택·셀 실행·실제 수집·Gemini·Slack·Gmail·main.py·Actions 실행 결과는 대화에서 확인되지 않음.**

## 이번 문서 작성 세션의 실제 변경 사항

- 날짜: 2026-10-04
- 담당 에이전트: Claude Code
- 생성한 파일(모두 신규):
  - `chapter11/ai-job-agent/docs/README.md`
  - `chapter11/ai-job-agent/docs/SPEC.md`
  - `chapter11/ai-job-agent/docs/GUIDE.md`
  - `chapter11/ai-job-agent/docs/STATUS.md`
  - `chapter11/ai-job-agent/docs/SESSION_START.md`
  - `chapter11/ai-job-agent/docs/AGENT_HANDOFF.md`
  - `chapter11/ai-job-agent/docs/WORK_LOG.md` (이 파일)
  - `chapter11/ai-job-agent/CLAUDE.md`
  - `chapter11/ai-job-agent/AGENTS.md`
- 코드/Notebook/main.py/.venv는 생성하지 않음(요청 범위 밖).
- `chapter11/ax-job-agent`의 기존 `.venv`는 이동·삭제·복제하지 않음(그대로 둠).
- 이번 세션에서 로컬로 직접 확인한 사실(읽기/버전 확인/목록 조회만 수행, 프로그램 실행 없음):
  - 저장소 루트 `C:\dev\claude-code-agent-course`, 브랜치 `ax-job-agent`, `git status` clean.
  - `chapter11/ax-job-agent`에는 `.venv`만 존재(그 외 파일 없음), `chapter11/ai-job-agent`는 이번 세션 전 미존재.
  - `ax-job-agent/.venv`: `python --version` → `3.14.6`. `pip list`에서 `pandas 3.0.6`, `requests 2.34.2`,
    `beautifulsoup4 4.15.0`, `python-dotenv 1.2.4`, jupyter/ipykernel/notebook/jupyterlab 계열 확인.
  - `import pandas, requests, bs4, dotenv` 실행 → 성공(버전 출력 확인).
  - 저장소 루트 및 `chapter11` 어디에도 `AGENTS.md`/`CLAUDE.md`/`.vscode` 설정 없음(이번 생성 전 기준).
  - `claude --version` → `2.1.289`(설치 확인). `which codex` → 미발견.
  - `chapter11` 관련 Git 커밋 이력 없음(ax-job-agent 내용은 `.venv` 외 없고, `.venv`는 자체 `.gitignore`로 무시됨).

## 세션 기록

### 2026-10-04 세션 (경로 확정 + ai-job-agent 가상환경 생성)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: 준비 단계(ax/ai 경로 확정)
- 목표: 사용자 지시에 따라 `ai-job-agent`를 최종 프로젝트 루트로 확정하고, 새 가상환경을 만들어 필수 패키지를 설치·검증한다.
  기존 `ax-job-agent`는 보존하고, Notebook은 만들지 않는다.
- 수정 파일:
  - 신규 생성: `chapter11/ai-job-agent/.venv/` (가상환경 전체)
  - 갱신: `chapter11/ai-job-agent/docs/STATUS.md`, `chapter11/ai-job-agent/docs/README.md`, 이 파일(`WORK_LOG.md`)
  - 변경 없음: `chapter11/ax-job-agent`(그대로 보존, 손대지 않음)
- 실행 명령·셀 (PowerShell 동등 명령, 실제로는 Bash로 실행):
  ```
  "C:\Users\dara0\AppData\Local\Programs\Python\Python314\python.exe" -m venv .venv   # ai-job-agent 폴더에서 실행
  .\.venv\Scripts\python.exe -m pip install --upgrade pip
  .\.venv\Scripts\python.exe -m pip install pandas requests beautifulsoup4 jupyter python-dotenv
  .\.venv\Scripts\python.exe --version
  .\.venv\Scripts\python.exe -m pip list
  .\.venv\Scripts\python.exe -c "import sys, pandas, requests, bs4, dotenv; print(sys.executable, pandas.__version__, requests.__version__, bs4.__version__)"
  ```
- 실제 결과:
  - venv 생성 확인: `.venv\Scripts\python.exe` 생성됨.
  - pip 업그레이드: `pip 26.1.2` → `26.2.1`.
  - 패키지 설치 성공: `pandas 3.0.6`, `requests 2.34.2`, `beautifulsoup4 4.15.0`, `python-dotenv 1.2.4`, `jupyter 1.1.1`,
    `ipykernel 7.4.0`, `notebook 7.6.3` 등 설치 완료(에러 없음).
  - `python --version` → `Python 3.14.6` (ax-job-agent와 동일 버전).
  - import 테스트 성공: `sys.executable` = `C:\dev\claude-code-agent-course\chapter11\ai-job-agent\.venv\Scripts\python.exe`,
    `pandas 3.0.6`, `requests 2.34.2`, `bs4 4.15.0` 출력 확인.
- 사용자 확인: 아직 없음 — VS Code 인터프리터 선택과 실제 Notebook 셀 실행은 사용자가 직접 해야 함(다음 작업).
- 결과 해석: `ai-job-agent` 쪽 Python 환경이 `ax-job-agent`와 동등한 버전·패키지 구성으로 독립적으로 준비되었다.
  단, 이는 PowerShell/CLI 레벨 검증이며 VS Code/Notebook 레벨(인터프리터 선택, 커널 선택)은 아직 검증되지 않았다.
- 오류·미확인 사항: VS Code 인터프리터 선택 미확인(사용자 수행 필요). Notebook 커널 선택·셀 실행 미확인(Notebook 자체를
  이번 세션에서 만들지 않음 — 요청 범위 밖).
- 완료 근거: GUIDE.md "준비 단계"의 완료 조건("최종 루트 한 곳에 docs와 정상 동작하는 .venv가 함께 존재") 충족 확인.
  STEP 01의 완료 조건(Notebook에서 사용자가 직접 실행해 확인)은 아직 미충족.
- 다음 작업: VS Code에서 `ai-job-agent\.venv\Scripts\python.exe`를 인터프리터로 선택(사용자 직접) → 이후
  `notebooks/01_env_check.ipynb` 생성 및 셀 실행 검증(STATUS.md "다음 작업" 참고).

### 2026-10-04 세션 (STEP 01 환경 확인용 Notebook 작성)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 01(개발환경 확인) — venv/패키지는 이전 세션에서 준비 완료, Notebook만 미작성 상태였음
- 목표: STEP 01의 환경 확인용 Notebook `notebooks/ax_job_pipeline.ipynb`를 작성한다. 크롤링·API·알림 코드는
  작성하지 않는다. 파일 생성만으로 STEP 완료 표시하지 않는다.
- 수정 파일:
  - 신규 생성: `chapter11/ai-job-agent/notebooks/ax_job_pipeline.ipynb`
  - 갱신: `chapter11/ai-job-agent/docs/STATUS.md`, 이 파일(`WORK_LOG.md`)
  - 기존 파일 없음(보존할 기존 Notebook 없었음 — `notebooks/` 폴더 자체가 이번에 처음 생성됨)
- 실행 명령·셀: Notebook 파일 작성 후 `./.venv/Scripts/python.exe -c "import json; json.load(...)"`로 JSON 구조만
  파싱 검증(셀 개수 4, 순서 markdown/code/code/markdown 확인). **Notebook 내부의 코드 셀 자체는 이번 세션에서
  실행하지 않았음**(에이전트가 실행하는 것이 아니라 사용자가 직접 실행해야 하는 항목).
- 실제 결과: Notebook 파일이 유효한 nbformat 4 JSON으로 생성됨. 셀 구성 — ①목적/완료조건 Markdown, ②Python
  버전/`sys.executable`/OS 출력 Code, ③pandas/requests/bs4/dotenv import+버전 출력 Code, ④실행 결과 기록용 빈 Markdown.
- 사용자 확인: 아직 없음 — 셀 실행과 결과 확인은 사용자 몫(다음 작업).
- 결과 해석: 해당 없음(아직 아무도 실행하지 않았으므로 해석할 출력이 없음).
- 오류·미확인 사항: Notebook 셀 실행 결과(특히 `sys.executable` 경로 일치 여부, import 성공 여부)가 전부 미확인.
- 완료 근거: 이번 세션은 "Notebook 작성"만이 목표였으므로 그 범위 내에서는 완료(파일 존재 + JSON 유효성 확인).
  STEP 01 자체의 완료 조건(GUIDE.md STEP 01 참고: 사용자가 직접 실행해 출력 확인)은 **아직 미충족** — STATUS.md에도
  "사용자 실행 대기"로 명시함.
- 다음 작업: 사용자가 VS Code에서 `notebooks/ax_job_pipeline.ipynb`를 열어 커널을 `ai-job-agent\.venv`로 선택하고
  셀 1·2를 직접 실행 → 결과를 Notebook 마지막 Markdown 셀과 STATUS.md에 기록.

### 2026-10-04 세션 (STEP 01 완료 처리, STEP 02로 전환)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 01(개발환경 확인) — Notebook 작성 완료, 셀 실행은 사용자 대기 상태였음
- 목표: 사용자가 직접 실행한 Notebook 셀 결과를 받아 Notebook 기록란·STATUS.md·WORK_LOG.md에 반영하고, STEP 01을
  완료로 표시하며 다음 작업을 STEP 02로 갱신한다(STEP 02 구현은 시작하지 않음).
- 수정 파일:
  - `chapter11/ai-job-agent/notebooks/ax_job_pipeline.ipynb` — 마지막 Markdown 셀(실행 결과 기록란)을 실제 결과로 채움
  - `chapter11/ai-job-agent/docs/STATUS.md` — STEP 01을 완료로, 완료/미확인 표 갱신, "다음 작업"을 STEP 02로 변경,
    진행표 갱신
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀: 에이전트는 코드를 실행하지 않음. **사용자가 직접** Notebook 셀 1(Python 버전/`sys.executable`/OS)과
  셀 2(pandas/requests/bs4/dotenv import) 실행.
- 실제 결과 (사용자 보고):
  - 셀 1: `sys.executable` = `C:\dev\claude-code-agent-course\chapter11\ai-job-agent\.venv\Scripts\python.exe`
  - 셀 2: `pandas 3.0.6`, `requests 2.34.2`, `beautifulsoup4 4.15.0` 오류 없이 출력, `dotenv`도 같은 `.venv`에서
    오류 없이 import됨
- 사용자 확인: 사용자가 직접 셀을 실행하고 위 결과를 보고함(에이전트가 대신 실행한 것이 아님).
- 결과 해석: Notebook 커널이 `ai-job-agent\.venv`를 정상적으로 사용 중이며, 설치된 4개 패키지가 모두 이 환경에서
  정상 import된다. VS Code 인터프리터/Notebook 커널 선택이 의도한 대로 동작함이 간접 확인됨.
- 오류·미확인 사항: 없음(이번 STEP 범위 내). STEP 02 이후(실제 사이트 구조, 수집 로직 등)는 모두 미착수.
- 완료 근거: GUIDE.md STEP 01의 완료 조건("사용자가 직접 실행해서 `sys.executable` 경로 일치 + 패키지 버전 출력 확인")을
  사용자 보고 기준으로 충족. STATUS.md "진행표"에서 STEP 01을 완료로 갱신함.
- 다음 작업: STEP 02(수집 데이터 명세 재확인) — 잡코리아 검색 결과 페이지를 사람이 직접 열어 9개 컬럼의 실제 위치를
  메모하는 작업부터 시작(STATUS.md "다음 작업" 참고). 이번 세션에서는 이 작업 지정만 했고 실제 열람·메모는
  아직 수행하지 않음.

### 2026-10-04 세션 (STEP 02~05 묶음 진행: 데이터 명세 → robots.txt/접근 테스트 → 실제 데이터 10건 수집 → DataFrame)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 02 (STEP 01은 이미 완료되어 재검증하지 않음 — 사용자 지시)
- 목표: STEP 02~05를 CODING_RULES.md의 "작업계획→실제 코드→실행 결과 해석" 3개 셀 패턴으로 Notebook에 추가하고,
  `ai-job-agent`의 `.venv`로 직접 실행해 진짜 결과를 기록한다. Gemini/Slack/Gmail 호출 없음. STEP 06 이후는 시작하지 않는다.
- 수정 파일:
  - `chapter11/ai-job-agent/CLAUDE.md`, `AGENTS.md` — "작업 시작 전 docs/CODING_RULES.md를 읽는다" 안내 추가(기존 내용 보존)
  - `chapter11/ai-job-agent/notebooks/ax_job_pipeline.backup-2026-10-04-step01.ipynb` — 수정 전 백업(신규 생성)
  - `chapter11/ai-job-agent/notebooks/ax_job_pipeline.ipynb` — STEP02, 03-A, 03-B, 04-A, 04-B, 05 블록(총 18개 셀) 추가,
    kernelspec을 `ai-job-agent`로 교정, 전체 실행해 실제 출력 기록. 기존 STEP 01 셀(0~3번)은 손대지 않음(내용 보존)
  - `docs/STATUS.md`, 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행):
  ```
  jupyter nbconvert --to notebook --execute --inplace notebooks/ax_job_pipeline.ipynb --ExecutePreprocessor.kernel_name=ai-job-agent
  ```
  (주의: 커널명을 명시하지 않고 1차 실행했을 때 전역 "python3" 커널(= 과거 `ax-job-agent`의 venv)로 잘못 실행된 것을
  경고 메시지로 발견해 즉시 재실행함. 최종적으로는 `ai-job-agent` 커널로 실행되었음을 Notebook 내 `sys.executable`
  출력으로 재확인함 — STATUS.md 근거 참고.)
- 실제 결과(요약 — 상세는 Notebook 각 블록의 해석 셀 참고):
  - STEP 02: 9개 컬럼 명세 표 정상 출력.
  - STEP 03-A: robots.txt status 200, `User-agent: *`에서 `/Search/` 미차단 확인. **robots.txt에 특정 AI 봇 이름을
    구체적으로 언급하는 이례적 서술 발견 — 지시로 취급하지 않고 기술 규칙만 반영, 사용자에게 플래그함.**
  - STEP 03-B: 검색어 'AI' 검색 결과 페이지 status 200, 응답에 실제 공고 상세 링크 28개 확인.
  - STEP 04-A: 공고 1건 필드 추출 검증 성공(company_name/job_title/job_url 정상).
  - STEP 04-B: **실제 데이터** 10건 수집(`IS_SYNTHETIC_SAMPLE: False`) — 샘플 전환 없음(접근 정상이었으므로).
  - STEP 05: DataFrame shape (10, 9), 컬럼 SPEC 9개와 일치, `posted_date`/`closing_date`만 전부 결측(목록 페이지에
    없는 정보라 임의로 채우지 않은 의도된 결과), 나머지 7개 컬럼 결측 0건.
- 사용자 확인: 아직 없음 — 이번 실행은 에이전트가 `.venv`로 직접 실행한 것이며, 사용자가 VS Code에서 Notebook을
  다시 열어 확인하는 것이 다음 작업(STATUS.md 참고).
- 결과 해석: STEP 02~05에서 목표한 "실제 데이터로 소량 수집 + DataFrame 생성"이 전부 성공했고, 접근 제한이 없어
  샘플 데이터 전환이 필요 없었다. 날짜 컬럼 결측은 설계대로이며 오류가 아니다.
- 오류·미확인 사항:
  - 코드 실행 오류 없음(error output 0건, 전수 확인).
  - robots.txt의 이례적 서술(특정 AI 봇 이름 언급)에 대한 최종 해석과, 사이트 이용약관 전체 검토는 사람의 몫으로 남겨둠.
  - 사용자의 Notebook 직접 재확인은 아직 이루어지지 않음.
- 완료 근거: GUIDE.md STEP 02~05 완료 조건을 에이전트 직접 실행 결과로 충족(출력 캡처는 STATUS.md "완료/미확인" 표 참고).
  단, "사용자 직접 확인"은 이 프로젝트의 통상적인 완료 기준이므로 그 전까지는 "사용자 확인 대기" 상태로 별도 표기.
- 다음 작업: 사용자가 Notebook을 다시 열어 STEP 02~05 결과를 확인(저장 충돌 회피 절차는 STATUS.md "다음 작업" 참고) →
  확인 후 STEP 06(전처리·중복 제거) 착수.

### 2026-10-04 세션 (LinkedIn 접근 가능성 확인 — jobkorea 기록은 보존)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 03 상당(접근 가능성 확인), 단 대상 사이트를 잡코리아 → LinkedIn으로 변경
- 목표: 수집 대상을 LinkedIn으로 바꾸는 가능성만 확인한다. robots.txt/이용정책을 먼저 확인하고, 허용되지 않으면
  요청하지 않는다. 잡코리아 STEP 02~05 기록은 보존하고, LinkedIn은 별도 미검증 단계로 기록한다. STEP 06 이후는
  시작하지 않는다.
- 수정 파일:
  - `chapter11/ai-job-agent/notebooks/ax_job_pipeline.backup-2026-10-04-step02to05.ipynb` — 수정 전 백업(신규)
  - `chapter11/ai-job-agent/notebooks/ax_job_pipeline.ipynb` — `[대상 변경]` 안내, STEP 03-LI-A(작업계획+URL 설명),
    STEP 03-LI-A 코드/해석, STEP 03-LI-B(결정 로직)+코드/해석, "접근 제한 시 대안" 안내 추가(총 7개 셀). 기존
    STEP 01~05 셀은 삭제·수정하지 않음(단, Notebook 전체 재실행의 부작용으로 STEP 03-B/04-A 해석 셀의 실시간
    수치·타임스탬프만 최신 값으로 소폭 보정함 — 결론/완료판정은 변경 없음)
  - `docs/SPEC.md` 1장(대상 변경 경고), 2장(사이트 확정 이력 표), 7장(robots.txt 우선 확인 원칙 일반화)
  - `docs/STATUS.md`(수집 대상 사이트 섹션 신설, 현재 STEP/증거표/다음 작업 갱신)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행):
  ```
  jupyter nbconvert --to notebook --execute --inplace notebooks/ax_job_pipeline.ipynb --ExecutePreprocessor.kernel_name=ai-job-agent
  ```
- 실제 결과:
  - LinkedIn `robots.txt`: status 200, length 120190. `urllib.robotparser.can_fetch("*", ...)` → 대상 URL/검색
    경로/사이트 루트 **전부 False**. 끝부분 일반 규칙이 `User-agent: *` / `Disallow: /` + "화이트리스트 신청
    안내(whitelist-crawl@linkedin.com)".
  - 판단: `PROCEED_WITH_LIVE_REQUEST = False` → **LinkedIn 채용 페이지에 실제 HTTP 요청을 보내지 않음.** 상태
    코드/Content-Type/공고 포함 여부는 확인되지 않음(의도적 미수행).
  - 코드 실행 오류 0건(전수 확인).
  - 부작용: Notebook 전체 재실행으로 잡코리아 STEP 03-B 응답의 실시간 수치(검색결과 총건수 14,286→14,290)와
    `collected_at` 타임스탬프가 바뀜 — 사이트의 실시간 특성 + 전체 재실행의 자연스러운 결과이며, 결론(접근 가능,
    실제 데이터 10건 등)에는 영향 없음. 해당 해석 셀 2곳의 수치만 최신값으로 보정.
- 사용자 확인: 아직 없음 — 이번 실행도 에이전트가 직접 수행한 것이며, 최종 수집 대상 사이트 결정은 사용자 몫.
- 결과 해석: 잡코리아는 기술적으로 접근 가능함이 이미 검증되어 있고, LinkedIn은 robots.txt 전면 차단으로 이
  방식(익명 자동 요청)으로는 접근 불가능하다는 것이 명확히 확인되었다. 우회 시도는 하지 않았다.
- 오류·미확인 사항:
  - LinkedIn 실제 페이지의 상태 코드/Content-Type/공고 포함 여부는 미확인(정책상 요청을 보내지 않았기 때문).
  - LinkedIn 공식 이용약관(User Agreement) 전문은 사람이 직접 확인하지 않음(robots.txt만 기계적으로 확인).
- 완료 근거: 이번 작업 목표는 "접근 가능성 확인"이었고, robots.txt 기반으로 명확한 차단 근거를 확보했으므로 목표
  자체는 달성. 단, "LinkedIn에서 실제로 수집 가능한지"는 여전히 미확정(차단되어 있으므로 사실상 불가로 결론).
- 다음 작업: 사용자가 Notebook의 jobkorea(STEP 02~05) + LinkedIn(STEP 03-LI-A/B) 결과를 모두 확인한 뒤, 최종
  수집 대상(잡코리아 유지 / LinkedIn 화이트리스트 신청 / 수동 입력)을 결정 → STATUS.md 갱신 → STEP 06 착수.

### 2026-10-04 세션 (LinkedIn 공고 1건 수동 입력 정리 — 웹 요청 없음)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: 수동 입력(자동 수집 STEP 03~05와 별개) — LinkedIn이 robots.txt로 차단되어 있어 사용자가 직접 복사한
  공고 1건을 정리
- 목표: 사용자가 대화로 전달한 LinkedIn 공고 1건(쿠팡 CS Specialist)을 (1) 원본 그대로 `data/raw/`에 보존,
  (2) 14개 컬럼 1행 DataFrame으로 만들어 `data/processed/`에 UTF-8 CSV로 저장. 웹 요청 없이 진행. 잡코리아 데이터와
  섞지 않음. 자동 수집 성공으로 표시하지 않음.
- 수정 파일:
  - 신규: `data/raw/linkedin_manual_4469459251.md`(원본 Markdown), `data/processed/linkedin_manual_4469459251.csv`
    (구조화 데이터)
  - `notebooks/ax_job_pipeline.backup-2026-10-04-linkedin-access-check.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "[수동 입력] LinkedIn 공고 1건" 블록(계획/코드/해석 3셀) 추가. 기존 셀은
    삭제하지 않음
  - `docs/STATUS.md`(LinkedIn 수동 입력 섹션 신설, 증거표 2행 추가, 다음 작업에 직무 적합성 검토 추가)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, 네트워크 요청 없음):
  ```
  jupyter nbconvert --to notebook --execute --inplace notebooks/ax_job_pipeline.ipynb --ExecutePreprocessor.kernel_name=ai-job-agent
  ```
- 실제 결과:
  - 1차 실행에서 **경로 오류 발견**: Jupyter 커널의 작업 디렉터리가 `ai-job-agent/notebooks`였기 때문에 상대경로
    `"data/processed"`가 `ai-job-agent/notebooks/data/processed/`에 잘못 저장됨(`data/raw`와 다른 위치). 즉시
    발견해 그 결과물(`notebooks/data/`)을 삭제하고, 코드를 작업 디렉터리 이름이 `"notebooks"`인지 확인해 상위
    폴더 기준으로 저장하도록 수정 후 재실행.
  - 2차 실행(수정 후) 결과: 컬럼 14개, 행 1개, `collection_method: manual_copy` 출력 확인. `posted_date`/
    `closing_date`는 `None`(결측 유지), `collected_at = 2026-10-04T17:52:13.397533+09:00`(실행 시각, 한국
    표준시). CSV가 `C:\dev\claude-code-agent-course\chapter11\ai-job-agent\data\processed\linkedin_manual_4469459251.csv`에
    저장됨(`os.path.exists` True로 확인).
  - `pandas.read_csv`로 저장된 CSV를 다시 읽어 shape (1, 14), 14개 컬럼명, 한글 텍스트(회사명·업무내용 등)가 깨지지
    않고 정상 복원됨을 재확인.
  - 코드 실행 오류 0건(전수 확인).
- 사용자 확인: 아직 없음 — 에이전트가 직접 실행·검증한 결과이며, 사용자의 직무 적합성 최종 판단은 아직 없음.
- 결과 해석: 사용자가 제공한 공고 1건이 손실 없이 원본(Markdown)과 구조화 데이터(CSV) 두 형태로 보존되었고,
  "자동 수집이 아니라 수동 입력"이라는 사실이 `collection_method` 컬럼으로 데이터에 명시적으로 남았다.
- 오류·미확인 사항:
  - 저장 경로 오류 1건 발생 → 발견 즉시 수정·재검증 완료(위 참고).
  - 이 공고(쿠팡 CS Specialist)가 "AI 엔지니어" 관련 채용공고로 적합한지는 **검토 필요** 상태로 남음(사용자 판단
    필요). `search_keyword`는 발견 경로일 뿐 적합성 판정이 아님을 원본 Markdown과 Notebook 해석 셀에 명시함.
- 완료 근거: 요청된 저장 위치(raw/processed)에 파일이 실제로 생성되고 `pandas.read_csv`로 재검증까지 마쳤으므로
  "수동 입력 1건 정리" 작업 자체는 완료. 단, 이 레코드를 파이프라인에 포함할지(직무 적합성)는 미확정.
- 다음 작업: 사용자가 (1) `data/processed/linkedin_manual_4469459251.csv` 내용 확인, (2) 이 공고의 직무 적합성
  판단, (3) 최종 수집 대상 사이트 결정(잡코리아/LinkedIn 화이트리스트/수동 입력) 중 진행 방향을 알려주면 그에
  따라 STATUS.md 갱신 후 다음 STEP으로 진행.

### 2026-10-04 세션 (LinkedIn 수동 입력 트랙 STEP 06~08 — 제외 처리/정제/신규판별/분석 0건)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: LinkedIn 수동 입력 트랙 — 쿠팡 공고 분석 제외 처리 → STEP 06 → STEP 07 → STEP 08 (잡코리아 트랙과
  완전히 분리, 섞지 않음)
- 목표: (1) 쿠팡 공고를 사용자 결정으로 이번 'AI 엔지니어' 분석 대상에서 제외하되 원본·사유 보존, (2) STEP 06
  결측/공백/URL중복 정제, (3) STEP 07 URL 기준 신규 판별 구현 + 검증(최초실행/재실행/새URL) — 검증은 운영 이력을
  변경하지 않고 메모리상에서만 수행, (4) STEP 08 제외 기준 적용 분석 대상 건수 계산(0건이어도 오류 없이, 합성
  데이터로 채우지 않음). Gemini 호출은 하지 않음.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-04-linkedin-manual-entry.ipynb` — 수정 전 백업(신규)
  - `notebooks/ax_job_pipeline.ipynb` — 5개 블록(대상 선정, STEP06, STEP07-A, STEP07-B, STEP08) 총 15개 셀 추가.
    기존 셀(STEP01~05, LinkedIn 접근성 확인, 기존 수동 입력 블록)은 전혀 수정하지 않음
  - `data/processed/linkedin_manual_4469459251.csv` — 14컬럼 → 20컬럼으로 확장(제외 3 + 정제 1 + 신규판별 2).
    기존 14개 컬럼 값은 변경 없음(원본 보존)
  - `data/processed/history_linkedin_manual.csv` — 신규 생성(STEP 07의 실제 운영 이력, 1건)
  - `docs/STATUS.md`(LinkedIn 수동 입력 트랙 결과 섹션 확장, 증거표 3행 추가, 현재 STEP/다음 작업 갱신, STEP
    진행표에 "잡코리아 트랙 기준" 안내 추가)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, 웹 요청 없음):
  ```
  jupyter nbconvert --to notebook --execute --inplace notebooks/ax_job_pipeline.ipynb --ExecutePreprocessor.kernel_name=ai-job-agent
  ```
- 실제 결과:
  - [대상 선정] 컬럼 14→17(`excluded_from_analysis=True`, `exclusion_reason` 전문, `exclusion_decided_at`).
    `job_description` 등 원본 값 불변 확인.
  - [STEP 06] 결측 — posted_date/closing_date만 1건(전체), 나머지 16개 컬럼 0건. `job_url` 중복 0건. 텍스트
    컬럼 12개 공백 이슈 0건. 중복 제거 1행→1행(변화 없음). 컬럼 17→18(`cleaned_at` 추가).
  - [STEP 07-A 검증, 실제 파일 미사용] 최초 실행 신규 1/1, 동일 입력 재실행 신규 0/1(멱등성 확인), 새 URL(검증용
    가짜 값, 미저장) 추가 시 신규 1/2(가짜 값만 신규로 정확히 구분됨).
  - [STEP 07-B 실적용] 운영 이력 파일 처리 전 미존재(0건) → 쿠팡 `is_new=True`(최초 관측) → 이력 파일 신규
    생성(1건). `is_new`가 `excluded_from_analysis`와 독립된 컬럼으로 공존함을 확인. 컬럼 18→20.
  - [STEP 08] 전체 1건, 제외 1건, **분석 대상 0건**. "수집 실패 아님" 메시지 출력. 회사/지역/경력별 집계
    `Series([], ...)`로 오류 없이 빈 결과 반환. 합성 데이터 추가 없음.
  - 코드 실행 오류 0건(전수 확인, `ast.parse`로 삽입 전 구문 검증 + nbconvert 실행 후 error output 전수 스캔).
- 사용자 확인: 아직 없음 — 에이전트가 직접 실행·검증한 결과. 분석 대상 0건 상태에서 다음 진행 방향(공고 추가
  수동 입력 vs 잡코리아로 STEP 09 진행)은 사용자 결정 필요.
- 결과 해석: "신규 여부"와 "직무 적합성(분석 대상 포함 여부)"이 서로 다른 독립 컬럼으로 정확히 분리 관리되었고,
  신규 판별 로직은 멱등성을 포함한 3가지 시나리오에서 모두 올바르게 동작했다. 분석 대상 0건은 데이터 부족이나
  수집 실패가 아니라 사용자의 명시적 제외 결정에 따른 정상적인 결과다.
- 오류·미확인 사항: 없음(이번 범위 내). STEP 09(Gemini) 이후는 전혀 시작하지 않음.
- 완료 근거: STEP 06~08 각각의 완료 조건(결측/중복/공백 출력, 검증 3시나리오 일치, 분석 대상 건수와 "0건" 설명)
  이 모두 실제 실행 출력으로 충족됨.
- 다음 작업: 사용자가 Notebook의 새 5개 블록을 확인하고, (1) 분석 대상 0건 상태에서 공고를 더 수동 입력할지
  또는 잡코리아 데이터로 STEP 09를 진행할지, (2) 최종 수집 대상 사이트(잡코리아/LinkedIn 화이트리스트/수동
  입력)를 결정 → STATUS.md 갱신 → 다음 STEP 진행.

### 2026-10-04 세션 (STEP 09 대상 결정: 잡코리아 — 후보 10건 분류 + Gemini 준비 점검, API 미호출)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 09 사전 준비 (사용자 결정: STEP 09는 잡코리아 데이터로 진행, LinkedIn 트랙은 미접촉)
- 목표: (1) 잡코리아 기존 10건의 회사명/제목/URL 표를 만들고 제목 기반으로 'AI 엔지니어' 관련성이 명확한 후보를
  표시(불명확하면 검토 필요로 유지), (2) Gemini 연동 준비 상태(SDK/　.env/API키/입력데이터 충분성) 점검 — API는
  호출하지 않음, (3) STATUS.md/WORK_LOG.md에 이번 결정 기록. LinkedIn 데이터·이력은 섞거나 변경하지 않음.
- 수정 파일:
  - `.env.example`(신규) — `GEMINI_API_KEY=` 변수명만, 실제 값 없음
  - `.gitignore`(신규) — `.env`, `.venv/`, `__pycache__/` 등 등록
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step06to08.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "[대상 결정] STEP 09는 잡코리아 데이터로 진행" 안내 + 2개 블록(사전
    준비-A 후보선정, 사전 준비-B Gemini 점검) 총 6개 셀 추가. **기존 셀(STEP01~08, LinkedIn 관련 전체)은 전혀
    수정하지 않음 — `jupyter nbconvert`로 전체 재실행하지 않고, 같은 `.venv`로 별도 실행한 결과를 수동으로
    옮겨 적음**(LinkedIn STEP07-B의 `is_new`/운영 이력이 재실행 시 바뀌는 것을 방지하기 위한 의도적 선택)
  - `docs/STATUS.md`(STEP09 진행 상황 섹션 추가, 증거표 4행 추가, 다음 작업 갱신, STEP표에 순서 예외 각주 추가)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 **독립 스크립트**로 직접 실행 — Notebook 커널 경유 아님):
  ```
  python jobkorea_candidate_select.py   # 잡코리아 재조회 + 제목 기반 relevance 분류
  python gemini_readiness_check.py      # SDK/.env/API키/입력데이터 점검 (API 미호출, 키 값 미출력)
  ```
- 실제 결과:
  - 잡코리아 10건 재조회: status 200, 카드 28개 중 상위 10건 추출. `relevance` 분류 결과 — **후보(명확) 0건,
    검토 필요 10건.** 'AI' 단어가 제목에 있는 공고는 대한상공회의소(교육생 모집) 1건뿐이며, 나머지 9건은 제목에
    AI 관련 키워드가 아예 없음(보험영업/부동산중개/마케터/컨설턴트 등 이종 직무).
  - Gemini 준비 점검: `google-generativeai` 미설치, `google-genai` 미설치, `.env` 없음(`.env.example`만 존재),
    `GEMINI_API_KEY` 환경변수 미설정. 잡코리아 10건은 목록 정보(제목/회사/경력/지역)만 있고 상세 본문(설명·자격
    요건)이 없어 Gemini 요약 입력으로 아직 부족함을 확인.
  - LinkedIn 데이터 불변 검증: `data/processed/linkedin_manual_4469459251.csv`, `history_linkedin_manual.csv`의
    파일 수정 시각이 이번 세션 시작 전과 동일함을 `ls -la`로 재확인(= 이번 작업에서 전혀 건드리지 않음).
  - 코드 실행 오류 0건(두 스크립트 모두 정상 종료, `ast.parse`로 노트북 삽입 전 구문 재검증).
- 사용자 확인: 아직 없음 — 사용자가 10건 표를 보고 공고 1건을 선택해야 다음 단계(상세 페이지 확보 → Gemini
  실제 호출)로 진행 가능.
- 결과 해석: 잡코리아 검색어 'AI'는 폭넓게 매칭되어 제목만으로 명확한 'AI 엔지니어' 공고를 가려내기 어렵다는
  것이 실제 데이터로 확인되었다(과장 없이 0건 그대로 보고). Gemini 연동은 SDK·키·입력데이터 3박자가 모두
  아직 준비되지 않은 상태임을 투명하게 기록했다.
- 오류·미확인 사항: 없음(이번 범위 내). STEP 06~08(잡코리아 정식 정제/판별/필터링)은 여전히 미착수 상태로,
  이번 STEP 09 사전 작업은 원본 10건을 그대로 사용한 것임을 STATUS.md에 각주로 명시함.
- 완료 근거: 10건 표와 relevance 분류, Gemini 준비 상태 점검 결과가 모두 실제 실행 출력으로 확인됨. API는
  호출하지 않았고 키 값도 노출하지 않음(요구사항 그대로 충족).
- 다음 작업: 사용자가 10건 중 공고 1건을 선택 → 해당 공고의 상세 페이지(job_url) 내용을 확보하는 단계로 진행
  (아직 미수행) → 사용자가 `.env`에 실제 `GEMINI_API_KEY`를 직접 입력하고 SDK 설치 여부를 알려주면 실제 Gemini
  호출 시험 진행.

### 2026-10-04 세션 (9번 공고 상세 페이지 확보 — 본문 텍스트 없음 확인, Gemini 미호출)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 09 사전 준비-C (사용자가 10건 중 9번 한국투자증권 공고를 선택)
- 목표: 선택된 공고의 상세 페이지(`job_url`)를 1회 GET으로 가져와 "주요 업무"·"자격 요건" 내용을 확보한다.
  Gemini는 호출하지 않는다. LinkedIn 데이터/이력은 접근하지 않는다.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step09prep.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 09 사전 준비-C" 블록(계획/코드/해석 3셀) 추가. 기존 셀은 전혀
    수정하지 않음(이번에도 Notebook 전체 재실행 없이 같은 `.venv`로 별도 실행한 결과를 옮겨 적음)
  - `docs/STATUS.md`(최신 결과 단락, 증거표 2행 추가, 다음 작업을 "본문 부족 문제 해결 방법 결정"으로 갱신)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, 1회 GET):
  ```
  requests.get("https://www.jobkorea.co.kr/Recruit/GI_Read/49983013?...", timeout=10, headers={...})
  ```
- 실제 결과:
  - status 200, 응답 길이 149,517자.
  - 구조화 태그 확보 — 모집요강(모집분야="홈페이지 지원", 모집인원 ○명, 고용형태 계약직, 급여 회사 내규,
    근무지 서울 영등포구 여의도동 한국투자증권빌딩 20층), 지원자격(경력 2년이상·직무별 상이, 학력 대졸이상,
    스킬 미기재).
  - **자유서술형 "주요업무"/"담당업무" 텍스트 블록은 페이지 어디에도 없음(`False`로 확인)** — iframe도 없고
    (`iframe count: 0`), "상세요강" 탭(`TabsTrigger`)은 존재하지만 해당 탭의 실제 본문 콘텐츠는 확인되지 않음.
    모집분야 값이 "홈페이지 지원"인 점으로 미루어, 실제 직무 설명은 회사 자체 채용 홈페이지에 있을 가능성이
    높다고 판단.
  - 코드 실행 오류 없음.
- 사용자 확인: 아직 없음 — 본문 부족 문제를 어떻게 처리할지(메타데이터만으로 시험/다른 공고 재선택/회사
  홈페이지 내용 수동 제공) 사용자 결정 필요.
- 결과 해석: jobkorea의 모든 공고가 상세 설명을 자체 호스팅하는 것은 아니며, 일부 대기업/금융사는 지원
  경로만 연결하고 실제 JD는 자사 사이트에 둔다는 것이 실제 데이터로 확인되었다. STEP 09 사전 준비-B에서
  이미 "본문 텍스트 부족 가능성"을 경고했던 것이 실제로 들어맞은 사례다.
- 오류·미확인 사항: 없음(코드 관점). 단, 이 공고로 Gemini를 의미 있게 테스트하려면 추가 입력(메타데이터뿐이거나
  사용자 수동 제공 텍스트)이 필요하다는 점이 새로 확인된 제약사항이다.
- 완료 근거: 상세 페이지 1회 GET과 구조화 데이터 추출은 완료 조건을 충족(상태 200, 메타데이터 출력). "주요
  업무" 자유 텍스트 확보라는 원래 목적은 데이터 자체의 한계로 완전히 달성하지 못했으며, 이를 꾸미지 않고
  그대로 보고했다.
- 다음 작업: 사용자가 본문 부족 문제 처리 방법을 결정 → 입력 텍스트 확정 → `.env`에 `GEMINI_API_KEY` 입력
  + SDK 설치 → 실제 Gemini 호출 시험.

### 2026-10-04 세션 (7번 안랩 공고 재확인 — 9번과 동일하게 본문 텍스트 없음, 사용자 복사용 URL 안내)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 09 사전 준비-D (사용자가 9번 대신 7번 안랩 공고로 재확인 요청)
- 목표: 7번 안랩 공고의 상세 페이지에서 주요 업무·자격 요건·우대 사항을 확보할 수 있는지 확인하고, 실제
  추출 내용을 보여준다. 본문이 없으면 추측하지 않고 사용자가 직접 열어 복사할 URL을 안내한다. Gemini는
  호출하지 않는다. Notebook 3셀 패턴과 LinkedIn 비접촉 원칙을 유지한다.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step09prepC.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 09 사전 준비-D" 블록(계획/코드/해석 3셀) 추가. 기존 셀 무수정,
    Notebook 전체 재실행 없이 같은 `.venv`로 별도 실행한 결과를 옮겨 적음(LinkedIn 상태 불변 유지)
  - `docs/STATUS.md`(최신 결과 단락, 증거표 2행 추가, 다음 작업에 URL과 선택지 갱신)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, 1회 GET):
  ```
  requests.get("https://www.jobkorea.co.kr/Recruit/GI_Read/50095529?...", timeout=10, headers={...})
  ```
- 실제 결과:
  - status 200, 응답 길이 152,114자.
  - 모집요강: 모집분야 **"홈페이지 지원"**(9번과 동일 패턴), 모집인원 ○명, 고용형태 정규직, 급여 회사 내규,
    근무지 경기 성남시 분당구(안랩) / 경기 과천시(안랩클라우드메이트).
  - 지원자격: 경력 신입·경력(직무별 상이/상세요강 참조), 학력 대졸이상(상세요강 참조), 스킬 값 없음.
  - 우대조건(기본우대): 장애인, 취업보호대상자, 유관업무 경험자(인턴·알바), 보훈대상자, 관련 자격증
    보유자 — **일반 우대 항목일 뿐 직무 관련 기술 우대사항은 아님.**
  - 접수기간: 2026.10.02(금)~2026.10.11(일).
  - **자유서술형 '주요업무' 텍스트: 없음(`False`). 외부(회사 자체) 지원 페이지 링크: 정적 HTML에 없음(`False`).**
  - 추가 조사: `ContentTabs`/`StrategyWrapper` 컴포넌트에 텍스트가 있었으나 이는 "이 기업의 취업 전략"(다른
    지원자들의 합격자소서·면접후기)이며 이 공고 자체의 업무/자격 내용이 아님을 확인하고 제외함(섞어서
    보고하지 않음).
  - 코드 실행 오류 없음.
- 사용자 확인: 아직 없음 — 사용자가 URL을 직접 열어 본문을 복사해 줄지, 메타데이터만으로 시험할지, 다른
  번호를 또 시도할지 결정 필요.
- 결과 해석: 9번(한국투자증권)과 7번(안랩) 모두 "모집분야: 홈페이지 지원" 템플릿으로, jobkorea는 지원
  경로·조건 메타데이터만 갖고 실제 직무 설명은 회사 자체 채용 시스템에 있다는 공통 패턴이 재확인되었다.
  이는 큰 기업/금융사 공고에서 흔한 패턴으로 보이며, 과장하지 않고 두 사례 모두 동일하게 보고했다.
- 오류·미확인 사항: 외부 지원 링크가 실제로는 JS 클릭 후 동적으로 열릴 가능성이 있으나, 정적 HTML 조사
  범위에서는 확인되지 않음(추측하지 않고 "없음"으로만 보고).
- 완료 근거: 1회 GET과 구조화 데이터 추출은 완료 조건 충족(상태 200, 메타데이터 출력). "주요업무" 확보라는
  목적은 데이터 자체의 한계로 달성하지 못했으며, 사용자가 복사할 URL을 정확히 제공했다.
- 다음 작업: 사용자가 (1) URL을 직접 열어 본문 복사·전달 / (2) 메타데이터만으로 Gemini 시험 / (3) 다른 번호
  재시도 중 선택 → 입력 확정 → `.env`/SDK 준비 → 실제 Gemini 호출 시험.

### 2026-10-04 세션 (방향 전환: STEP 09~10을 LinkedIn 쿠팡 공고로 — 레코드 보완 + Gemini SDK/모델 확인, 키 대기)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 09~10 (사용자가 대상을 잡코리아 9·7번에서 LinkedIn 쿠팡 공고로 전환)
- 목표: 사용자가 전달한 쿠팡 공고 전체 원문으로 기존 LinkedIn 레코드를 보완(중복 없이, 제외/신규 판정 유지),
  LinkedIn 화면 전용 요소(1주 전/지원 클릭 27/보유기술 매치)를 규칙대로 처리, Gemini 공식 문서로 SDK/모델
  확인, `.env`/API 키 상태 점검(키 없으면 안내 후 중단), 잡코리아는 미사용. Notebook 3셀 패턴 유지.
- 수정 파일:
  - `data/raw/linkedin_manual_4469459251.md` — "2차 확인(2026-10-04) — 전체 원문(가공 없음)" 섹션 **추가**
    (기존 1차 내용 삭제 없음), 원문 전체 + "해석·사용 금지 항목" 설명 포함
  - `data/processed/linkedin_manual_4469459251.csv` — 20→28컬럼으로 보완(행 수 1 유지, 중복 없음)
  - `.venv`에 `google-genai` SDK 설치(`pip install -U google-genai`)
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step09prepD.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "[수동 입력 보완] STEP 09~10" 블록, "STEP 09 — Gemini 연동 준비 상태
    재점검" 블록(각 3셀, 총 6셀) 추가. 기존 셀(잡코리아·이전 LinkedIn 셀) 무수정, 전체 재실행 없이 같은
    `.venv`로 별도 실행한 결과를 옮겨 적음
  - `docs/STATUS.md`(방향 전환 섹션, 증거표 다수 행 갱신, 다음 작업을 "`.env` 키 입력 대기"로 전면 교체)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행):
  ```
  pip install -U google-genai
  python linkedin_augment.py          # 레코드 보완, gemini_test_input 생성
  python gemini_readiness_check2.py   # SDK/모델/키 상태 점검 (API 미호출)
  ```
  추가로 WebFetch로 `https://ai.google.dev/gemini-api/docs/quickstart` 확인(공식 문서 조회, 코드 실행 아님).
- 실제 결과:
  - 레코드 보완: 20→28컬럼, 1행 유지(중복 없음). `excluded_from_analysis`: True→True(불변). `is_new`:
    True→True(불변). `job_description`/`qualifications`/`preferred_qualifications`를 사용자 원문 그대로 갱신.
    `posted_date_display_raw="1주 전"`, `apply_click_display_raw="지원을 클릭한 사람 27"`(해석 없이 원문만
    보존, `posted_date`는 계속 NaN), `skill_match_excluded_note`(제외 사실 메모, 값 자체는 어디에도 미기록),
    `work_arrangement="재택·대면 혼합근무"`, `employment_type="정규직"` 추가.
  - `gemini_test_input`(898자) 생성 — 직무 소개/업무 내용/자격 요건/우대 사항만 포함, 금지 3항목 미포함(직접
    확인함).
  - 공식 문서 확인: SDK `google-genai`, 초기화 `from google import genai; client = genai.Client()`, 키는
    환경변수 `GEMINI_API_KEY` 자동 인식, 문서상 기본 모델 `gemini-3.8-flash`(WebFetch 요약 결과 — 실제 호출
    시 재확인 권장이라고 명시).
  - SDK 설치 확인: `google-genai 2.28.0` 설치 성공.
  - `.env` 파일 없음, `GEMINI_API_KEY` 환경변수 미설정(값 미노출) — **Gemini API 호출 안 함, 여기서 중단.**
  - LinkedIn 작업 전 과정에서 코드 실행 오류 0건.
- 사용자 확인: 아직 없음 — 사용자가 `.env`에 실제 키를 입력한 뒤 알려줘야 다음(실제 호출) 진행.

### 2026-10-05 세션 (사용자 직접 실행 검증 기록 + STEP 17~18 GitHub Actions 준비)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent` (workflow 파일만 저장소 루트
  `C:\dev\claude-code-agent-course\.github\workflows\`), 브랜치 `ax-job-agent`
- 시작 STEP: STEP 14~16 사용자 검증 반영 → STEP 17~18(GitHub Actions) 준비
- 목표:
  1. 사용자가 직접 `python main.py`를 실행해 오류 없이 종료되고, 보고서에서 dry-run 표시와
     "전체 1건·추천 대상 0건"을 확인했다는 사실을 문서에 기록한다.
  2. GUIDE.md 기준 STEP 17~18을 준비한다 — 기본 검증은 dry-run(외부 호출 없음), LinkedIn 입력은 계속
     수동임을 명시, `.env`/비밀값은 커밋하지 않고 GitHub Secrets 사용, 필요한 workflow·의존성 작성 후
     가능한 로컬 검증 수행, 자동 스케줄은 사용자 확인 전 설정 금지, `git push`나 실제 발송은 하지 않음.
  3. **실제 GitHub 실행을 확인하기 전에는 STEP 17~18을 완료로 표시하지 않는다**(사용자 명시적 지시).
- 수정/생성 파일:
  - 신규: `C:\dev\claude-code-agent-course\.github\workflows\ai-job-agent-weekly-report.yml` (저장소 루트,
    기존 3개 workflow는 무수정)
  - 신규: `chapter11/ai-job-agent/requirements.txt` (현재 `.venv` 설치 버전 그대로 고정)
  - 갱신: `docs/STATUS.md` (STEP14~16 사용자 검증 완료 반영, STEP17~18 준비 내역·완료 전 상태·GitHub 설정
    안내 섹션 신설, 진행표 갱신)
  - 갱신: 이 파일(`WORK_LOG.md`)
  - Notebook(`ax_job_pipeline.ipynb`)은 이번 작업에서 수정하지 않음(STEP 17~18은 CI 설정이라 Notebook
    3셀 패턴 대상이 아니라고 판단 — SPEC/GUIDE에도 STEP 17~18은 코드/설정 작업으로 되어 있음).
- 실행 명령(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, GitHub 인프라는 호출하지 않음):
  ```
  git remote show origin          # 기본 브랜치 확인(main)
  ls .github/workflows/           # 기존 workflow 3개 확인(무수정 대상)
  pip show beautifulsoup4 google-genai pandas python-dotenv requests   # 버전 고정용 조회
  python -c "import yaml; yaml.safe_load(open('.github/workflows/ai-job-agent-weekly-report.yml'))"
  pip install -r requirements.txt   # 이미 설치된 것과 동일 버전인지 확인(전부 "already satisfied")
  python main.py                    # CI와 동일한 dry-run 명령 재확인
  ```
- 실제 결과:
  - `git remote show origin` → 기본 브랜치 `main` 확인. 이번 세션 작업은 전부 `ax-job-agent` 브랜치에만
    존재하며 미커밋(`chapter11/`과 신규 `.github/workflows/ai-job-agent-weekly-report.yml` 둘 다 `??`).
  - 기존 workflow 3개(`fast-track-smoke.yml`, `resource-policy-guard.yml`, `resource-smoke.yml`) 내용은
    읽기만 하고 전혀 수정하지 않음(파일 목록으로 확인).
  - `requirements.txt`에 고정한 버전(`pandas 3.0.6`, `requests 2.34.2`, `beautifulsoup4 4.15.0`,
    `python-dotenv 1.2.4`, `google-genai 2.28.0`)이 실제 `.venv`에 설치된 버전과 **정확히 일치**함을
    `pip install -r requirements.txt` 재실행으로 재확인(전부 "Requirement already satisfied").
  - workflow YAML이 `yaml.safe_load`로 파싱 오류 없이 로드됨을 확인(문법 유효성만 확인 — GitHub Actions
    고유 스키마 검증은 아님).
  - `python main.py`(인자 없음)를 다시 실행해 `returncode 0`, STEP 16에서 기록한 것과 동일한 로그 패턴
    (수집 1건→정제 1건→신규 0건→분석 대상 0건→Gemini 호출 0건→보고서 저장→Slack/Gmail `dry_run: True`)을
    재확인 — CI에서 실행할 명령과 동일한 명령이 로컬에서 그대로 성공함을 검증.
  - **실제 GitHub Actions 실행은 수행하지 않음**(`git push` 없음, Actions 탭 실행 없음) — 사용자 지시에
    따른 의도적 범위 제한.
- 사용자 확인:
  - **STEP 14~16**: 사용자가 `python main.py`를 **본인이 직접** 실행해 오류 없이 종료됨과, 생성된 보고서의
    dry-run 표시·"전체 1건·추천 대상 0건"을 **직접 확인했다고 보고**(2026-10-05). 이는 이전 세션의
    "에이전트가 직접 실행"과는 별개로, 사용자 본인 환경에서의 재현을 의미한다.
  - **STEP 17~18**: 아직 없음 — GitHub Secrets 등록, 실제 workflow_dispatch 실행, 스케줄 일정 확인 모두
    사용자가 수행/결정해야 하는 다음 작업.
- 결과 해석: STEP 14~16은 "에이전트 실행 검증"에 이어 "사용자 본인 실행 검증"까지 더해져 더 높은 확신으로
  완료 처리할 수 있게 되었다. STEP 17~18은 로컬에서 할 수 있는 모든 사전 검증(YAML 문법, 의존성 버전 일치,
  CI와 동일한 명령의 로컬 재현)을 마쳤지만, GitHub Actions 고유의 실행 환경(`ubuntu-latest` 러너, Secrets
  주입, `workflow_dispatch` 트리거 자체의 동작)은 로컬로 재현할 수 없는 영역이므로 실제 실행 확인 전까지는
  "준비 완료"일 뿐 "완료"가 아니다.
- 오류·미확인 사항:
  - `python-version: "3.14"`가 GitHub `ubuntu-latest` 러너에 아직 없을 가능성 — 실제 실행에서만 확인 가능.
  - `permissions: contents: write` + 이력 파일 자동 커밋 단계(`live=true`일 때만 동작)는 전혀 실행해보지
    않음.
  - `schedule:` 트리거는 주석 처리 상태 — 사용자가 원하는 일정을 아직 받지 않음.
- 완료 근거: STEP 14~16은 SPEC.md §11 기준 "사용자 직접 확인"까지 충족되어 완료로 표시. STEP 17~18은
  SPEC.md §11의 "GitHub Actions 수동 실행이 성공하고 이력 파일이 복원됨을 확인" / "주간 스케줄이 최소
  1회 이상 실제로 동작함을 확인" 조건이 **아직 충족되지 않아 완료로 표시하지 않는다**(사용자 명시적 지시).
- 다음 작업: 사용자가 (1) GitHub Secrets 5개 등록, (2) 이 workflow 파일을 포함해 커밋/푸시 승인, (3) Actions
  탭에서 `workflow_dispatch`로 dry-run 수동 실행 성공 확인, (4) 원하는 자동 실행 요일·시간 결정 → 이후
  `schedule:` 주석 해제 + 기본 브랜치 반영 → 최소 1회 스케줄 실행 성공 확인까지 마치면 STEP 17~18을 완료로
  갱신한다. 구체적인 클릭 순서는 `docs/STATUS.md`의 "STEP 17~18 — GitHub Actions 준비" 섹션에 기록함.
- 결과 해석: "별도 Gemini 연동 시험용 입력으로 사용하고 추천 대상이나 신규 공고로 바꾸지 않는다"는 지시가
  `excluded_from_analysis`/`is_new` 불변 확인으로 코드 수준에서 충족됨. LinkedIn 화면 전용 표시를 공고 속성과
  혼동하지 않도록 구분 저장한 것도 실제 파일 내용으로 확인됨.
- 오류·미확인 사항: 없음(코드 관점). `gemini-3.8-flash`라는 모델명은 WebFetch의 AI 요약 결과이므로, 실제 첫
  호출 시 모델명이 정확한지 한 번 더 확인할 필요가 있다고 판단해 다음 세션 메모로 남김.
- 완료 근거: 보완 전/후 컬럼·행 수·불변 컬럼 값이 모두 실제 출력으로 확인되었고, 키 부재로 호출을 멈추라는
  지시를 그대로 따름(호출 코드 자체를 작성하지 않음).
- 다음 작업: 사용자가 `C:\dev\claude-code-agent-course\chapter11\ai-job-agent\.env`에 `GEMINI_API_KEY=...`를
  입력 → 알려주면 `gemini_test_input`과 `gemini-3.8-flash`로 실제 시험 호출 → 원문 대조 비교표 제시 → STEP 10은
  "확인 대기"로 유지.

### 2026-10-04 세션 (Gemini 실제 호출 시도 3회 — 전부 503 서버 과부하로 실패, 데이터 영향 없음)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 09 본작업(Gemini 실제 호출) — 사용자가 `.env`에 키 입력 완료 후 요청
- 목표: 키 값을 출력하지 않고, 준비된 `gemini_test_input`으로 Gemini를 1회 호출해 원문 비교표를 보여준다.
  기존 `excluded_from_analysis`/`is_new` 결정은 유지한다.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step09prepE.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 09 — Gemini 실제 호출 시도" 블록(계획/코드/해석 3셀) 추가
  - `docs/STATUS.md`(호출 시도 결과 단락, 증거표 3행 갱신, 다음 작업을 "재시도 방법 결정"으로 교체)
  - 이 파일(`WORK_LOG.md`)
  - **`data/processed/linkedin_manual_4469459251.csv`는 변경되지 않음**(호출이 저장 전에 실패)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, API 키는 `.env`에서 자동 로드):
  ```
  python gemini_test_call.py   # genai.Client().models.generate_content(model="gemini-3.8-flash", ...)
  ```
  총 3회 실행(1차 결과 확인 후 일시적 오류로 판단해 2회 더 재시도).
- 실제 결과:
  - 호출 전 상태: `excluded_from_analysis: True`, `is_new: True`, `GEMINI_API_KEY` 로드 True(값 미노출,
    길이만 확인: 53자).
  - 3회 모두 동일 오류: `google.genai.errors.ServerError: 503 UNAVAILABLE` —
    "This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try
    again later."
  - 인증 오류(401/403)나 모델 미발견(404)이 아니라 503이므로 키·SDK·모델명 설정 자체는 정상이고 요청이 서버
    까지 도달한 것으로 판단.
  - 예외가 `to_csv` 저장 이전에 발생해 **CSV 파일은 전혀 수정되지 않음** — `excluded_from_analysis`/`is_new`
    포함 모든 기존 값이 그대로 보존됨(재확인함).
  - API 키 값은 어떤 로그·출력·Notebook 셀에도 기록되지 않음(길이만 출력).
- 사용자 확인: 아직 없음 — 재시도 방법(동일 모델 재시도 / 다른 모델명 시도) 결정 필요.
- 결과 해석: 요청받은 "1회 호출"을 시도했으나 Google 서버 측 일시적 가용성 문제로 성공하지 못했다. 코드·설정
  자체의 문제가 아니라고 판단되는 근거(401/404가 아닌 503, 동일 오류 3회 반복)를 명확히 기록했다. 실패를
  성공으로 포장하지 않고, 응답이 없다는 사실과 원인 추정을 그대로 보고했다.
- 오류·미확인 사항: `gemini-3.8-flash` 모델이 일시적으로 과부하 상태인지, 아니면 이 모델 자체가 현재
  불안정한 것인지는 이번 세션에서 확정하지 못함(재시도 또는 다른 모델로 추가 확인 필요).
- 완료 근거: "키 값 미노출"과 "기존 제외/신규 판정 유지" 조건은 충족(저장 자체가 일어나지 않아 자동으로
  충족됨). "Gemini 요약·비교표 제시"라는 핵심 목표는 **미충족** — 솔직하게 미완료로 기록함.
- 다음 작업: 사용자가 재시도 방법(동일 모델 재시도 / 다른 모델명)을 알려주면 `gemini_test_input`으로 재호출
  → 성공 시 원문 대조 비교표 제시 → STEP 10 "확인 대기"로 전환.

### 2026-10-04 세션 (Gemini 1회 재시도 성공 — 원문 대조 완료, STEP 10 확인 대기)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 09 본작업 재시도 (이전 3회 503 실패 후 사용자가 "1회만 재시도, 추가 반복 제한" 지시)
- 목표: 같은 키·모델로 1회만 재시도(SDK 자체 재시도 외 추가 반복 금지). 다시 503이면 멈추고 대체 모델 후보
  확인. 성공하면 요약과 원문 비교표 제시. 키 값은 출력하지 않음.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step09prepF.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 09 — Gemini 실제 호출 재시도 (성공)" 블록(계획/코드/해석 3셀) 추가
  - `data/processed/linkedin_manual_4469459251.csv` — `gemini_model`/`gemini_response_raw`/`gemini_called_at`
    3개 컬럼 추가(28→31컬럼, 행 수 1 유지)
  - `docs/STATUS.md`(성공 결과, "Gemini 응답 vs 원문 비교" 표 신설, 증거표 갱신, 다음 작업을 "STEP 10 확인"으로 교체)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, 단일 호출, 추가 재시도 루프 없음):
  ```
  python gemini_test_call.py   # genai.Client().models.generate_content(model="gemini-3.8-flash", ...), 1회
  ```
- 실제 결과:
  - 호출 성공(503 재발 없음). JSON 파싱 성공. 응답 5개 항목:
    - 주요_업무/필수_요건/우대_사항: 원문 bullet과 거의 동일한 문구로 구성(요약이라기보다 재인용에 가까움).
    - 명시된_기술: "SQL, LLM(OpenAI, Claude, Gemini), AI Agent, RAG, n8n, Zapier, Java script, Python" —
      전부 원문에 실제로 등장하는 용어, 원문에 없는 기술 추가 없음.
    - 직무_유형: "정규직" — 이는 Gemini의 추론이 아니라 프롬프트에 에이전트가 미리 넣어준 "고용형태: 정규직"
      값을 그대로 반영한 것(원출처는 LinkedIn 화면의 "[정규직]" 태그).
  - 원문 대조 결과: **누락 없음, 과도한 해석(hallucination) 없음.**
  - 호출 전/후 `excluded_from_analysis: True`/`is_new: True` — 변경 없음 재확인.
  - 코드 실행 오류 없음. API 키 값은 로그/출력/Notebook 어디에도 기록되지 않음.
- 사용자 확인: 아직 없음 — 비교표는 에이전트의 1차 점검이며, STEP 10(사용자 검증)은 "확인 대기"로 유지.
- 결과 해석: 입력에 없는 정보를 Gemini가 추측해 채우지 않았다는 점에서는 성공적이나, "주요 업무/필수 요건/
  우대 사항" 응답이 원문을 거의 그대로 이어붙인 수준이라 진짜 "요약"(압축·재구성) 품질은 이번 결과만으로
  충분히 검증되지 않았다. 이는 프롬프트가 "추출해 정리"를 요청한 설계상의 결과로 보이며, 더 간결한 요약이
  필요하면 프롬프트 조정이 필요하다는 점을 기록해 둔다.
- 오류·미확인 사항: 이전 3회 실패가 정말 "서버 일시 과부하"였는지(이번 성공으로 간접 뒷받침되지만 확정은
  아님), "명시된 기술"/"직무 유형" 필드가 더 복잡한 공고에서도 안정적으로 동작하는지는 추가 검증 필요.
- 완료 근거: "1회 재시도, 추가 반복 제한", "키 값 미노출", "성공 시 비교표 제시", "기존 제외/신규 판정 유지"
  4가지 요구사항이 모두 실제 실행 결과로 확인됨.
- 다음 작업: 사용자가 비교표를 직접 확인하고 STEP 10을 완료로 전환할지 결정. 이후 보고서(STEP 11)/전송
  (STEP 12~13) 진행 여부는 별도 논의 — 이번 세션에서는 시작하지 않음.

### 2026-10-04 세션 (직무 유형/고용형태 분리 교정 + STEP 11 Gemini 시험판 보고서 생성)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 10 비교표 교정 → STEP 11 보고서 생성
- 목표: (1) 비교표의 "직무 유형=정규직" 오류를 추가 API 호출 없이 교정(직무 유형은 본문 근거로 재정리,
  고용형태는 분리), (2) STEP 11 Markdown 보고서 생성 — 시험임을 명시, 분석대상 0건과 시험 1건 구분, 제외된
  쿠팡 공고를 추천으로 표시하지 않음, URL·업무·요건·우대·기술 포함, (3) Slack/Gmail 계정 준비 안내(비밀값
  요청 없이). Notebook 3셀 패턴 유지, STEP 10은 확인 대기로 유지.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-04-step09success.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 10 (수정)" 블록, "STEP 11" 블록(각 3셀, 총 6셀) 추가. 기존 셀
    무수정
  - `data/processed/linkedin_manual_4469459251.csv` — `job_type_corrected`/`job_type_correction_note`/
    `job_type_corrected_at` 3개 컬럼 추가(31→34컬럼, 행 수 1 유지, **API 호출 없음**)
  - `reports/step11_gemini_test_report_2026-10-04.md`(신규) — Gemini 연동 시험판 보고서
  - `.env.example` — Slack/Gmail 변수명(값 없음) 추가, STEP 12~13용임을 주석으로 명시
  - `docs/STATUS.md`(비교표 수정판 교체, STEP 11 보고서 요약, Slack/Gmail 준비 안내, 증거표·진행표 갱신)
  - 이 파일(`WORK_LOG.md`)
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, **네트워크/API 호출 없음**):
  ```
  python fix_job_type.py            # 기존 gemini_response_raw 재파싱, 직무유형/고용형태 분리
  python generate_step11_report.py  # Markdown 보고서 생성
  ```
- 실제 결과:
  - 교정: Gemini 응답의 `직무_유형`(`"정규직"`)이 `employment_type` 컬럼 값과 **동일함을 확인**(`True`) →
    고용형태를 잘못 답한 것으로 판단. `job_type_corrected = "CS 운영 데이터 분석·AI 자동화"`(공고 제목·직무
    소개 근거)로 신설, `employment_type`은 그대로 유지. 컬럼 31→34. `excluded_from_analysis`/`is_new` 변경 없음.
  - 보고서: 2,389자. "1. 분석 현황 요약"(0건 vs 1건 표) / "2. 추천 채용공고(0건)" / "3. [참고] Gemini 연동
    시험 결과 — 추천 아님"(쿠팡, URL·직무유형·고용형태·근무형태·주요업무·필수요건·우대사항·명시된기술 포함)
    / "4. 데이터 출처와 한계" 4개 섹션 생성 확인.
  - 작업 중 발견·즉시 수정한 버그: 보고서 초안에서 "우대 사항" bullet을 " / " 기준으로 자동 분리하려다,
    원문 항목 자체에 "/"가 포함된 경우("n8n / Zapier", "Java script / Python")가 잘못 쪼개지는 것을 발견 →
    항목을 억지로 쪼개지 않고 한 문단으로 표시하도록 즉시 수정 후 재생성.
  - 코드 실행 오류 없음(두 스크립트 모두).
- 사용자 확인: 아직 없음 — 수정된 비교표와 보고서 내용에 대한 사용자 최종 확인 필요(STEP 10 확인 대기).
- 결과 해석: Gemini가 "직무 유형"과 "고용형태"를 혼동한 것은 프롬프트가 두 개념을 명확히 구분하지 않았기
  때문으로 보이며, 이번처럼 사람이 결과를 검토해 바로잡는 과정이 "AI 응답을 원문과 비교·검증한다"는 프로젝트
  원칙의 실제 적용 사례가 되었다.
- 오류·미확인 사항: "CS 운영 데이터 분석·AI 자동화"라는 직무 유형 문구가 사용자 의도와 정확히 일치하는지는
  사용자 확인 필요.
- 완료 근거: "추가 API 호출 없이 수정", "필수 요건/우대 사항 분리 유지", "보고서 4대 요구사항(시험 명시/0건
  구분/제외 공고 비추천/URL·업무·요건·우대·기술 포함)" 모두 실제 파일 생성 결과로 확인됨.
- 다음 작업: 사용자가 수정된 비교표와 보고서를 확인 → STEP 10을 완료로 전환 → Slack/Gmail 계정·`.env` 준비
  후 STEP 12~13 착수 여부 논의(이번 세션에서는 메시지 미발송).

### 2026-10-05 세션 (STEP 12 — Slack Incoming Webhook 연결 시험 성공, 1회 발송)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 12(Slack 발송) — 사용자가 Webhook 생성 및 `.env` 저장 완료 후 요청
- 목표: `.env`를 `python-dotenv`로 명시적 경로 로드해 `SLACK_WEBHOOK_URL`이 실제로 읽히는지 확인하고,
  "채용정보 파이프라인 연결 테스트" 메시지를 테스트 채널로 **정확히 1회** 발송한다. 키/URL 값은 출력하지
  않는다. 결과를 기록하고 멈춘다.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-05-step12test.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 12 — Slack Incoming Webhook 연결 시험 (1회 발송)" 블록(계획/
    코드/해석 3셀) 추가. 기존 셀 무수정
  - `docs/STATUS.md`(STEP 12 결과 섹션 신설, 증거표·진행표 갱신, 다음 작업을 "Slack 채널 수신 확인"으로 교체)
  - 이 파일(`WORK_LOG.md`)
  - **`.env`는 에이전트가 수정하지 않음**(사용자가 직접 입력한 값을 읽기만 함)
- 직전 세션에서 발견한 사실: 사용자가 "`.env`에 입력 완료했다"고 알린 첫 시도에서 실제로는
  `SLACK_WEBHOOK_URL` 변수가 `.env`에 없었음을 확인(변수명만 확인, 값은 확인 안 함) → 전송하지 않고
  사용자에게 재확인 요청 → 사용자가 다시 추가 후 이번 세션에서 재확인해 존재 확인.
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, **단 1회 POST**):
  ```
  load_dotenv(dotenv_path="<ai-job-agent>/.env")
  requests.post(SLACK_WEBHOOK_URL, json={"text": "채용정보 파이프라인 연결 테스트"})
  ```
- 실제 결과:
  - `.env` 경로: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent\.env`(명시적 경로로 로드).
  - `SLACK_WEBHOOK_URL` 로드 여부: `True`. URL이 `https://hooks.slack.com/services/`로 시작하는 정상 형식임을
    확인(형식만 확인, 값 미노출).
  - 전송 시각 `2026-10-05T14:20:04+09:00`. **응답 상태 코드 200, 응답 본문 "ok"**(Slack 표준 성공 응답).
  - Webhook URL 실제 값은 코드 출력·Notebook·로그 어디에도 기록되지 않음(재확인 완료, `grep`으로 노트북
    파일 내 실제 URL 패턴 부재 확인).
  - 코드 실행 오류 없음. 메시지는 정확히 1회만 발송(반복 없음).
- 사용자 확인: 아직 없음 — **상태 코드 200/ok는 Slack 서버가 요청을 접수했다는 뜻일 뿐, 실제로 테스트
  채널에 메시지가 보이는지는 사용자가 Slack에서 직접 확인해야 한다.**
- 결과 해석: `.env` 로딩, Webhook 형식, 실제 HTTP 전송까지 전 과정이 정상 동작했다. 이전에 "입력 완료"라는
  보고와 실제 파일 상태가 달랐던 사례가 있었으므로, 매번 변수명 존재 여부를 코드로 재확인한 뒤에만 진행하는
  것이 안전하다는 점을 재확인했다.
- 오류·미확인 사항: 실제 채널 수신 여부는 코드로 확인할 수 없는 영역이라 사용자 확인 대기로 남김.
- 완료 근거: "정확히 1회 발송", "키/URL 미노출", "결과 기록 후 중단" 3가지 요구사항이 모두 실제 실행
  결과로 확인됨.
- 다음 작업: 사용자가 Slack 테스트 채널에서 메시지 도착을 직접 확인 → STEP 12 완료로 갱신. (별도로 STEP 10
  Gemini 비교표 확인도 여전히 대기 중.) STEP 13(Gmail)은 이번 세션에서 시작하지 않음.

### 2026-10-05 세션 (STEP 12 완료 확정 + STEP 13 Gmail 준비사항 안내, 공식 문서 확인)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 12 완료 확정 → STEP 13 준비 안내
- 목표: 사용자의 Slack 채널 수신 확인을 반영해 STEP 12를 완료로 기록하고, STEP 13(Gmail) 착수에 필요한
  준비사항을 공식 문서 확인 후 안내한다. 추가 발송은 하지 않는다.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-05-step12confirmed.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 12 — 사용자 확인 완료" 마크다운 셀 1개 추가(코드 실행 없음,
    순수 기록용 — 추가 작업이 없어 불필요한 Code Cell을 만들지 않음)
  - `docs/STATUS.md`(STEP 12를 완료로 갱신, "STEP 13 준비 — Gmail 연결에 필요한 사항" 섹션 신설, 증거표·
    진행표·다음 작업 갱신, 과거 Slack/Gmail 안내 섹션에 "최신 아님" 메모 추가)
  - 이 파일(`WORK_LOG.md`)
  - **메시지 발송·코드 실행 없음**(순수 문서/기록 작업)
- 조사(공식 문서 확인, 코드 실행 아님): `support.google.com/mail/answer/185833`(Google 앱 비밀번호 도움말)을
  확인해 (1) 2단계 인증 필수, (2) 발급 URL `myaccount.google.com/apppasswords`, (3) `smtplib` +
  `smtp.gmail.com:587` + `starttls()` 조합이 공식 안내임을 확인.
- 실제 결과: 사용자가 "Slack 테스트 메시지 수신 확인했다"고 보고 → STEP 12를 **완료**로 확정. Gmail 준비
  안내(2단계 인증 → 앱 비밀번호 발급 → `.env`에 `GMAIL_ADDRESS`/`GMAIL_APP_PASSWORD`/`GMAIL_TO_ADDRESS` 입력)
  전달. 코드 작성·실행·발송 없음.
- 사용자 확인: STEP 12는 사용자 확인으로 완료됨. STEP 13 준비는 사용자가 아직 수행 전.
- 결과 해석: STEP 12는 "에이전트 실행 성공(200/ok)"과 "사용자 채널 수신 확인" 두 조건이 모두 충족되어
  정식으로 완료 처리했다. 이는 프로젝트 원칙("API 호출 성공만으로 완료 판단하지 않음")을 Slack 발송에도
  동일하게 적용한 사례다.
- 오류·미확인 사항: 없음.
- 완료 근거: 사용자의 명시적 수신 확인 보고.
- 다음 작업: 사용자가 Gmail 2단계 인증·앱 비밀번호 발급·`.env` 3개 변수 입력을 완료한 뒤 알려주면, 변수명
  존재 여부만 확인(값 미노출) 후 Slack과 동일하게 1회 시험 발송 진행.

### 2026-10-05 세션 (STEP 13 — Gmail 연결 시험, 1회 발송 성공)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 13(Gmail 발송) — 사용자가 앱 비밀번호 발급 및 `.env` 저장 완료 후 요청
- 목표: 프로젝트 규칙·현재 상태 확인 → `.env`를 `python-dotenv`로 명시적 경로 로드해 Gmail 설정 3개 로드
  확인(비밀번호 미출력) → `GMAIL_TO_ADDRESS`로 제목 "채용정보 파이프라인 이메일 연결 테스트" 메일을 정확히
  1회 발송(실패 시 자동 재발송 금지) → Notebook 3셀 패턴 기록 → STEP 13은 사용자 수신 확인 대기로 표시 후 중단.
  Gemini 호출·Slack 발송은 하지 않음.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-05-step13test.ipynb`(수정 전 백업, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 13 — Gmail 연결 시험 (1회 발송)" 블록(계획/코드/해석 3셀) 추가.
    기존 셀 무수정
  - `docs/STATUS.md`(STEP 13 결과 섹션 추가, 증거표·진행표 갱신, 다음 작업을 "Gmail 수신함 확인"으로 교체,
    STEP 12 요약행 누락 수정)
  - 이 파일(`WORK_LOG.md`)
  - **`.env`는 에이전트가 수정하지 않음**(사용자가 직접 입력한 값을 읽기만 함)
- 작업 전 확인: `docs/CODING_RULES.md`/`docs/STATUS.md`를 다시 확인해 STEP 12가 사용자 확인으로 완료되었고
  STEP 13 준비 안내가 이미 전달된 상태임을 재확인. `.env`에서 `GMAIL_ADDRESS`/`GMAIL_APP_PASSWORD`/
  `GMAIL_TO_ADDRESS` 변수명 존재를 먼저 확인(값은 확인하지 않음).
- 실행 명령·셀(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행, **단 1회 발송, 자동 재시도 없음**):
  ```
  load_dotenv(dotenv_path="<ai-job-agent>/.env")
  smtplib.SMTP("smtp.gmail.com", 587) -> starttls() -> login() -> sendmail()  # try/except, 실패 시 중단만
  ```
- 실제 결과:
  - `.env` 경로: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent\.env`(명시적 경로로 로드).
  - `GMAIL_ADDRESS`/`GMAIL_APP_PASSWORD`/`GMAIL_TO_ADDRESS` 로드 여부 모두 `True`(값 미출력).
  - 전송 시도 시각 `2026-10-05T14:41:55+09:00`. 제목 "채용정보 파이프라인 이메일 연결 테스트".
    **전송 결과: 성공(SMTP 세션 정상 종료, 예외 없음).**
  - Gmail 주소·앱 비밀번호 실제 값은 코드 출력·Notebook 어디에도 기록되지 않음(재확인 완료, `grep`으로
    노트북 내 실제 값 패턴 부재 확인).
  - 코드 실행 오류 없음. 메일은 정확히 1회만 발송(반복 없음, 재시도 로직 자체를 넣지 않음).
- 사용자 확인: 아직 없음 — **SMTP 성공은 "Gmail 서버가 접수했다"는 뜻일 뿐, 실제 수신함(스팸함 포함) 도착
  여부는 사용자가 직접 확인해야 한다.**
- 결과 해석: Slack 때와 동일한 패턴(명시적 `.env` 로드 → 값 미노출 확인 → 1회 발송 → 결과 기록 → 사용자
  확인 대기)을 Gmail에도 일관되게 적용했다. "서버 접수 성공"과 "실제 수신 확인"을 구분해 기록하는 습관을
  계속 유지했다.
- 오류·미확인 사항: 실제 수신함 도착 여부는 코드로 확인할 수 없는 영역이라 사용자 확인 대기로 남김.
- 완료 근거: "정확히 1회 발송", "비밀값 미노출", "실패 시 자동 재발송 없음", "STEP 13을 확인 대기로 표시 후
  중단" 4가지 요구사항이 모두 실제 실행 결과로 확인됨.
- 다음 작업: 사용자가 `GMAIL_TO_ADDRESS` 수신함(스팸함 포함)에서 메일 도착을 직접 확인 → STEP 13 완료로
  갱신. (별도로 STEP 10 Gemini 비교표 확인도 여전히 대기 중.)

### 2026-10-05 세션 (STEP 13 완료 확정 + STEP 14~16: 함수화/main.py 통합/dry-run 재현성 검증)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent`, 브랜치 `ax-job-agent`
- 시작 STEP: STEP 13 완료 확정 → STEP 14(함수화) → STEP 15(main.py 통합) → STEP 16(로컬 전체 실행 검증)
- 목표: 사용자가 Gmail 수신을 확인해 STEP 13을 완료로 기록. 이어서 docs(SPEC/GUIDE/CODING_RULES)와 실제
  코드를 확인한 뒤, 검증된 LinkedIn 수동 입력→정제→Gemini 분석→보고서→Slack/Gmail 전송 흐름을 `src/*.py`
  함수와 `main.py`로 통합. 분석 제외 공고는 추천에서 제외 유지. 기본 실행은 dry-run(외부 호출 없음)으로
  하고 실제 실행 방법은 별도 안내. 저장된 응답/스텁으로 전체 흐름을 검증하고 Gemini 실제 호출·Slack·Gmail
  발송은 하지 않음. git diff 확인, 검증 결과를 문서에 기록. STEP 17~18은 시작하지 않음.
- 수정 파일:
  - `notebooks/ax_job_pipeline.backup-2026-10-05-step12confirmed.ipynb`, `...-step12test.ipynb`,
    `...-step13test.ipynb`, `...-step13confirmed.ipynb`(수정 전 백업들, 신규)
  - `notebooks/ax_job_pipeline.ipynb` — "STEP 13 사용자 확인 완료"(markdown), "STEP 14~15"(3셀),
    "STEP 16"(3셀) 추가. 기존 셀 무수정
  - **신규 생성**: `src/__init__.py`, `src/collect.py`, `src/clean.py`, `src/analyze.py`, `src/summarize.py`,
    `src/report.py`, `src/notify.py`, `main.py`
  - **신규 생성(실행 결과물)**: `reports/weekly_report_2026-10-05.md`(dry-run 산출물)
  - `docs/STATUS.md`(STEP 13 완료 확정, STEP 14~16 결과 섹션 신설 — 검증/미검증 항목 명확히 구분, 증거표·
    진행표 갱신, 다음 작업을 "보고서 확인 + live 전환 여부 결정"으로 교체)
  - 이 파일(`WORK_LOG.md`)
  - **`data/processed/`의 기존 CSV·이력 파일, `.env`는 수정하지 않음**(읽기만 함, 수정 시각 불변 재확인)
- 작업 전 확인: `docs/SPEC.md`(5장 예정 폴더 구조, 7장 기능 요구사항), `docs/CODING_RULES.md`,
  `docs/STATUS.md`를 다시 읽어 현재까지 검증된 로직(STEP 06~13)과 SPEC이 예정한 `src/` 구조를 확인.
- 실행 명령(에이전트가 `ai-job-agent`의 `.venv`로 직접 실행):
  ```
  python -m py_compile main.py src/*.py   # 구문 검사
  python main.py                          # dry-run 1회
  python main.py                          # dry-run 2회째(재현성 비교용)
  ```
- 실제 결과:
  - 구문 검사 통과(`SYNTAX OK`).
  - `python main.py`(dry-run) 2회 연속 실행 — 둘 다 `returncode 0`. 로그: 수집 1건 → 정제 1→1행(중복 0) →
    신규판별 신규 0건(운영 이력 미변경) → 분석 대상(추천 후보) **0건**(제외 1건) → Gemini 호출 **0건**(캐시
    재사용) → 보고서 저장(`reports/weekly_report_2026-10-05.md`) → Slack `{'dry_run': True, ...}` → Gmail
    `{'dry_run': True, ...}`.
  - 타임스탬프를 제외한 1차/2차 출력이 **완전히 동일**함을 코드로 확인(`True`) — 재현성(멱등성) 검증.
  - 생성된 보고서를 직접 열어 확인: "2. 추천 채용공고" 섹션에 쿠팡 공고가 **없고** 0건으로만 표시됨, 쿠팡은
    "3. [참고] Gemini 요약 결과 — 추천 공고 아님" 섹션에만 들어 있음(요구사항대로 분리 확인).
  - 데이터 무결성 재확인: `linkedin_manual_4469459251.csv`, `history_linkedin_manual.csv` 파일 수정 시각이
    dry-run 실행 전후로 변경되지 않음(= 기존 데이터·운영 이력을 건드리지 않음).
  - `git status`(저장소 루트) 확인 — `chapter11/`이 여전히 전체 미추적 상태라 추적 대상과의 `git diff`는
    해당 없음(비교 대상 없음). 새로 생긴 파일 목록을 직접 나열해 의도한 범위(`ai-job-agent/` 내부, 특히
    `src/`, `main.py`, `reports/weekly_report_*.md`)만 바뀌었음을 확인. 커밋은 하지 않음(요청 밖).
  - 작업 중 발견·즉시 수정한 버그: 검증용 `subprocess.run(..., text=True)` 호출에 인코딩을 지정하지 않아
    한글 출력이 Windows cp949로 깨지는 문제 발견 → `encoding="utf-8"` 추가로 해결.
  - **`--live` 모드(실제 Gemini 호출, 실제 Slack/Gmail 발송)는 코드만 작성했고 실행하지 않음 — 미검증 상태로
    문서에 명시.**
- 사용자 확인: STEP 13은 사용자의 수신 확인으로 완료 처리. STEP 14~16(dry-run 기준)은 사용자가 아직
  보고서 내용을 직접 확인하기 전.
- 결과 해석: "분석 제외 공고는 추천에 포함하지 않는다"는 요구사항이 `src/analyze.py`의
  `filter_analysis_targets()`와 `src/report.py`의 섹션 분리 로직으로 코드 수준에서 구조적으로 보장됨을
  실제 생성된 보고서 파일로 확인했다. dry-run이 기존 데이터·이력에 아무 부작용을 남기지 않는다는 것도
  파일 수정 시각으로 재확인했다.
- 오류·미확인 사항: `--live` 경로 전체(실제 Gemini 호출, 실제 알림 발송, "신규이고 캐시 없는 레코드"에 대한
  실시간 요약 생성 분기)는 미검증. 완료로 표시하지 않음.
- 완료 근거: dry-run 2회 실행 모두 오류 없이 끝까지 성공했고, 재현성(출력 동일)과 데이터 무결성(파일 시각
  불변)을 코드로 직접 확인했다. "검증하지 못한 항목(=--live)"은 명확히 분리해 완료로 표시하지 않았다.
- 다음 작업: 사용자가 `reports/weekly_report_2026-10-05.md`를 직접 확인 → `--live` 전환 여부 결정. 그 외
  STEP 10(Gemini 비교표)도 여전히 확인 대기. STEP 17~18(GitHub Actions)은 시작하지 않음.

### 2026-10-05 세션 (STEP 17 — 실제 GitHub Actions 수동 dry-run 실행 결과 기록)

- 담당 에이전트: Claude Code
- 경로·브랜치: `C:\dev\claude-code-agent-course\chapter11\ai-job-agent` (workflow는 저장소 루트
  `.github/workflows/ai-job-agent-weekly-report.yml`), 브랜치 `ax-job-agent`(PR 생성 안내 완료, merge는
  사용자 몫으로 남아 있음)
- 시작 STEP: STEP 17(GitHub Actions 수동 실행) — 직전 세션에서 workflow 파일 push + PR 생성 링크 안내까지
  마친 상태였고, 사용자가 실제로 GitHub에서 workflow를 실행해볼 차례였음
- 목표: 사용자가 보고한 실제 GitHub Actions 실행 결과(Success + Artifact 보고서 내용)를 STATUS.md/WORK_LOG.md에
  정확히 기록하고 STEP 17을 완료로 확정한다. STEP 18(주간 자동 스케줄)은 사용자 지시대로 미설정 상태를
  유지한다. 추가 Gemini 호출이나 Slack/Gmail 발송은 하지 않는다.
- 수정 파일:
  - 갱신: `docs/STATUS.md` — "마지막 갱신" 갱신, 증거표 STEP17/18 행 갱신, "다음 작업"을 STEP 18 하나로
    축소, "STEP 17 — 실제 GitHub Actions 실행 결과" 섹션 신설(완료 기록), 기존 "STEP 17~18 — GitHub Actions
    준비" 섹션은 "과거 기록"임을 알리는 배너를 추가하고 보존, 진행표(STEP 01~18) 17번 행 완료로 갱신
  - 갱신: 이 파일(`WORK_LOG.md`)
  - 코드/workflow/데이터 파일은 이번 작업에서 전혀 수정하지 않음(기록만 갱신)
- 실행 명령: 없음 — 이번 작업은 **사용자가 GitHub Actions UI에서 직접 수행한 실행 결과를 전달받아 문서화**한
  것이며, 에이전트는 어떤 코드도 실행하지 않았고 어떤 API도 호출하지 않았다.
- 실제 결과(사용자 보고):
  - GitHub Actions 탭에서 `workflow_dispatch`로 수동 실행(`live` 입력 없이, 즉 dry-run) → **Success(초록
    체크)로 종료.**
  - **Artifact(`weekly-report`)를 사용자가 직접 다운로드**해 보고서 내용을 확인 → **"전체 1건·추천 대상
    0건"** — 이는 로컬 dry-run(STEP 14~16)에서 에이전트와 사용자가 각각 확인했던 결과와 **정확히 일치**한다.
- 사용자 확인: **이번 세션 전체가 사용자의 직접 실행·확인 보고**다("GitHub Actions 수동 dry-run이 Success로
  끝났고, Artifact 보고서도 내려받아 확인했어. 전체 1건, 추천 대상 0건이야.").
- 결과 해석: 로컬에서만 검증했던 STEP 14~16의 dry-run 결과가, GitHub Actions의 실제 `ubuntu-latest` 실행
  환경에서도 동일하게 재현되었다. 이는 `requirements.txt` 버전 고정과 workflow 설계(의존성 설치 → dry-run
  실행 → 아티팩트 업로드)가 로컬 환경에 특정된 우연이 아니라 실제로 이식 가능함을 보여준다. 이전 세션에서
  우려했던 "`python-version: 3.14`가 `ubuntu-latest`에 없을 수 있다"는 리스크도 이번 Success로 해소되었다
  (실제로 문제없이 실행됨이 확인됨).
- 오류·미확인 사항:
  - `permissions: contents: write` + 이력 파일 자동 커밋 단계는 이번에도 검증되지 않았다(이번은 `live=false`
    dry-run이었으므로 해당 단계 자체가 실행되지 않음 — 조건부 `if: inputs.live == true`로 막혀 있음).
  - `--live` 모드(실제 Gemini 호출 + 실제 Slack/Gmail 발송)는 로컬·GitHub 어디에서도 여전히 미검증 상태다.
  - STEP 18(주간 자동 스케줄 실행)은 **사용자가 명시적으로 "자동 일정 미설정 상태로 유지"를 지시**했으므로
    착수하지 않았다 — `schedule:`은 계속 주석 처리된 채로 남아 있다.
- 완료 근거: SPEC.md §11의 STEP 17 완료 조건 중 "GitHub Actions 수동 실행이 성공하고" 부분은 이번 실제 Success
  실행으로 충족되었고, "확인됨" 부분은 사용자가 Artifact를 직접 열어 "전체 1건·추천 대상 0건"을 확인한 것으로
  충족되었다. (이력 파일 복원 조건은 `live` 실행 전용이라 dry-run인 이번 실행에는 해당하지 않음.) **STEP 17을
  완료로 확정한다.**
- 다음 작업: 사용자가 원하는 주간 자동 실행 요일·시간을 알려주면, workflow 파일의 `schedule:` 주석을 해제하고
  기본 브랜치(`main`) 반영 상태를 재확인한 뒤, 최소 1회 이상의 실제 스케줄 실행이 성공함을 확인해 STEP 18을
  완료로 갱신한다. 그 전까지는 요청하지 않는 한 스케줄을 활성화하지 않는다.

### 2026-10-05 세션 (STEP 18 — 주간 자동 스케줄 workflow 변경 + 로컬 검증 + PR 준비)

- 담당 에이전트: Claude Code
- 경로·브랜치: workflow는 저장소 루트 `.github/workflows/ai-job-agent-weekly-report.yml`, 브랜치
  `ax-job-agent`
- 시작 STEP: STEP 18(GitHub Actions 주간 실행) — STEP 17 완료 직후, 사용자가 구체적 일정(매주 금요일
  09:10 KST)과 live 분기·Secrets 검증 요구사항을 지정
- 목표: workflow에 `schedule: cron: "10 0 * * 5"`를 설정하고, schedule 이벤트에서는 항상 `--live`로 동작,
  `workflow_dispatch`는 기존처럼 기본 dry-run 유지, live 실행 전 GitHub Secrets 5개를 값 노출 없이 검증해
  누락 시 명확히 실패, LinkedIn 입력이 계속 수동이며 GitHub에 반영된 데이터로 실행됨을 문서화, 실행 간
  신규판별 이력이 유지되는 구조를 확인, 문서·workflow를 로컬로 검증한 뒤 커밋·push하고 main 반영용 PR을
  준비한다. 실제 Gemini 호출·Slack/Gmail 발송·schedule 활성화(=merge)는 하지 않는다.
- 수정 파일:
  - `.github/workflows/ai-job-agent-weekly-report.yml` — (1) `schedule: - cron: "10 0 * * 5"` 추가, (2)
    새 단계 "실행 모드 결정"(`id: mode`)으로 `github.event_name == 'schedule'`이면 무조건 live, 아니면
    기존 `inputs.live`를 따르도록 변경, 이후 모든 단계가 `inputs.live` 대신 `steps.mode.outputs.live`를
    보도록 전부 교체, (3) 새 단계 "GitHub Secrets 5개 검증"을 파이프라인 실행 직전에 추가(비어 있는 변수
    "이름만" `::error::`로 표시 후 `exit 1`), (4) 최상단 주석에 schedule 일정·KST 환산·LinkedIn 수동 입력
    원칙·Secrets 요구사항을 추가.
  - 갱신: `docs/STATUS.md` — "마지막 갱신", "다음 작업"(merge 대기 + 첫 실행 확인), 새 섹션 "STEP 18 — 주간
    자동 스케줄 준비"(요청 일정/변경 내역 표/로컬 검증/알아둘 점), 증거표 2행 갱신, 진행표 STEP18 행 갱신.
  - 갱신: 이 파일(`WORK_LOG.md`)
  - `main.py`/`src/*.py`/`requirements.txt`/데이터 파일은 이번 작업에서 수정하지 않음(workflow와 문서만 변경).
- 실행 명령(에이전트가 로컬에서 직접 실행, GitHub 인프라·실제 Secrets는 전혀 사용하지 않음):
  ```
  python -c "import yaml; yaml.safe_load(open('.github/workflows/ai-job-agent-weekly-report.yml'))"
  # Secrets 검증 단계 로직을 더미 값으로 bash에서 그대로 시뮬레이션(실제 변수명 사용, 값은 "x" 등 더미)
  git add <14개 파일 경로> && git commit -m "..." && git push origin ax-job-agent
  ```
- 실제 결과:
  - YAML 파싱 성공. `schedule`이 `[{'cron': '10 0 * * 5'}]`로 정확히 반영됨을 재확인. 8개 스텝(체크아웃→
    모드결정→Python설치→의존성설치→Secrets검증→파이프라인실행→아티팩트업로드→이력커밋) 순서·조건(`if`)
    구조를 다시 파싱해 확인.
  - Secrets 검증 로직 시뮬레이션: 5개 중 `GEMINI_API_KEY`만 빈 값으로 두면 `MISSING: GEMINI_API_KEY` 출력 후
    `exit 1`(실패) — 재현 확인. 5개 모두 채우면 `ALL SET` 출력 후 `exit 0`(통과) — 재현 확인. 실제 GitHub
    Secrets 값은 어디에도 사용하지 않음(더미 문자열만 사용).
  - **schedule 트리거 자체의 실제 동작, live 파이프라인의 실제 실행, Secrets 검증의 실제 통과/실패, 이력
    파일 커밋·push는 GitHub 환경에서 전혀 실행하지 않았다** — merge 후 첫 예약 실행에서만 확인 가능.
- 사용자 확인: 아직 없음 — 이번 세션은 workflow 수정·로컬 검증·커밋/push·PR 준비까지이며, 실제 예약 실행과
  Slack/Gmail 수신 확인은 다음 금요일(또는 사용자가 수동으로 `live=true` 실행을 먼저 시도하는 경우) 이후다.
- 결과 해석: STEP 17에서 이미 GitHub `ubuntu-latest` 환경에서의 dry-run 실행이 실제로 성공함을 확인했으므로,
  이번에 추가한 schedule/live 분기/Secrets 검증 로직은 "같은 환경에서 다른 분기를 타는" 변경이다. 로컬에서
  YAML 구조와 조건문 자체의 정확성은 검증했지만, GitHub Actions 고유의 schedule 트리거 동작과 실제 Secrets
  주입은 로컬로 재현할 수 없는 영역이라 첫 실제 실행 전까지는 "준비 완료"로만 표시한다.
- 오류·미확인 사항:
  - schedule은 기본 브랜치(`main`)에서만 동작 — 지금은 `ax-job-agent`에만 있어 **merge 전까지는 자동
    실행되지 않는다.** main 반영용 PR을 준비했다(아래 "다음 작업" 참고).
  - live 경로(실제 Gemini 호출, 실제 Slack/Gmail 발송, 이력 파일 커밋·push) 자체는 GitHub에서 단 한 번도
    실행된 적 없음 — 첫 금요일 실행이 사실상 최초 end-to-end 검증이 된다.
- 완료 근거: STEP 18의 "준비"(cron 설정, live 분기, Secrets 검증, 문서화, 로컬 검증, 커밋·push·PR 준비)는
  이번 세션에서 모두 충족했다. 그러나 SPEC.md §11 및 사용자의 명시적 지시("첫 예약 실행과 수신 확인 전에는
  STEP 18을 완료로 표시하지 마세요")에 따라, **실제 스케줄 실행 성공 + Slack/Gmail 수신 확인 전까지는 STEP 18을
  완료로 표시하지 않는다.**
- 다음 작업: 사용자가 (1) `main` 반영용 PR을 리뷰 후 merge, (2) 다음 금요일 09:10 KST 예약 실행이 Success로
  끝나는지 Actions 탭에서 확인, (3) Slack 채널과 Gmail 수신함에서 실제로 보고서가 도착했는지 확인 → 이 3가지가
  모두 확인되면 STEP 18을 완료로 갱신한다.

## 다음 세션 기록 양식

```
### YYYY-MM-DD 세션

- 담당 에이전트: (Claude Code / Codex)
- 경로·브랜치: (<PROJECT_ROOT>, 브랜치명)
- 시작 STEP: (STATUS.md 기준)
- 목표: (이번 세션에서 하려던 것)
- 수정 파일: (경로 목록)
- 실행 명령·셀: (실제로 실행한 PowerShell 명령 또는 Notebook 셀)
- 실제 결과: (콘솔/셀 출력 요약 — 추측 금지, 실행 안 했으면 "미실행"이라고 적음)
- 사용자 확인: (사용자가 직접 확인한 것과 그 결과)
- 결과 해석: (출력이 의미하는 바)
- 오류·미확인 사항: (있다면)
- 완료 근거: (GUIDE.md의 완료 조건 중 무엇을 충족했는지)
- 다음 작업: (STATUS.md에도 반영)
```
