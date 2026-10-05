"""분석 단계 — 분석 대상 필터링, 기본 통계, URL 기준 신규 판별, Greenhouse AI·AX 관련성 판정.

STEP 07(신규 판별)·STEP 08(제외 기준 적용) 로직을 함수로 옮긴 것이다.

2026-10-05 "수집 대상 범위 확장" 작업에서, Greenhouse로 수집한 공고(krafton/daangn/sendbird/moloco)를
AI·AX 관련성에 따라 포함/검토 필요/제외로 판정하는 `classify_ai_ax_relevance()`와, 회사별 수집
성공/실패를 반영해 신규·기존·마감을 구분하는 `diff_greenhouse_jobs()`를 추가했다.
"""
import os
import re
from typing import Optional

import pandas as pd


def filter_analysis_targets(df: pd.DataFrame) -> pd.DataFrame:
    """`excluded_from_analysis`가 True가 아닌 행만 돌려준다 (= '추천' 대상이 될 수 있는 행).

    `excluded_from_analysis` 컬럼 자체가 없으면(과거 포맷 데이터) 전부 분석 대상으로 간주한다.
    """
    if df.empty or "excluded_from_analysis" not in df.columns:
        return df.copy()
    return df[df["excluded_from_analysis"] != True].reset_index(drop=True)  # noqa: E712


def compute_basic_stats(df: pd.DataFrame) -> dict:
    """회사·지역·경력별 건수를 계산한다. 0행이어도 오류 없이 빈 결과를 돌려준다."""
    if df.empty:
        empty = pd.Series(dtype="int64")
        return {"by_company": empty, "by_location": empty, "by_career": empty}
    return {
        "by_company": df["company_name"].value_counts(),
        "by_location": df["location"].value_counts(),
        "by_career": df["career"].value_counts(),
    }


def is_new_by_url(current_df: pd.DataFrame, history_df: pd.DataFrame) -> pd.Series:
    """job_url 기준으로 신규 여부(Bool Series)를 반환한다. history_df에 없는 job_url이면 신규(True)."""
    known_urls = set(history_df["job_url"]) if len(history_df) else set()
    return ~current_df["job_url"].isin(known_urls)


def mark_new_records(
    df: pd.DataFrame,
    history_path: str,
    update_history: bool = False,
    now_iso: Optional[str] = None,
) -> pd.DataFrame:
    """`is_new` 컬럼을 채운 df를 반환한다. `update_history=True`일 때만 운영 이력 파일을 실제로
    갱신한다(dry-run에서는 이력 파일을 건드리지 않기 위해 기본값은 False).
    """
    if df.empty:
        return df.copy()

    if os.path.exists(history_path):
        history_df = pd.read_csv(history_path, encoding="utf-8-sig")
    else:
        history_df = pd.DataFrame(columns=["job_url", "first_seen_at"])

    result = df.copy()
    result["is_new"] = is_new_by_url(result, history_df)

    if update_history:
        import datetime
        stamp = now_iso or datetime.datetime.now().astimezone().isoformat()
        new_rows = result.loc[result["is_new"], ["job_url"]].copy()
        new_rows["first_seen_at"] = stamp
        updated_history = pd.concat([history_df, new_rows], ignore_index=True)
        updated_history.to_csv(history_path, index=False, encoding="utf-8-sig")

    return result


# ======================================================================
# Greenhouse 자동 수집 — AI·AX 관련성 판정 (2026-10-05)
#
# ⚠️ 이 분류기는 2026-10-05에 krafton/daangn/sendbird/moloco의 실제 공고 32건을 사람이 직접 읽고
# 내린 판단(docs/WORK_LOG.md, Notebook "[신규 조사] 수집 대상 범위 확장" 참고)을 규칙으로 코드화한
# **휴리스틱**이다. 완벽한 의미 판단이 아니다 — 애매하면 '포함'으로 단정하지 않고 '검토 필요'로
# 분류하도록 일부러 보수적으로 설계했다(사용자 지시: "단순 키워드 언급만으로 포함하지 마").
# ======================================================================

#: 제목(또는 본문) 1차 스크리닝 — 이 패턴에 전혀 안 걸리면 애초에 AI·AX 후보로도 보지 않는다.
TITLE_SCREEN_PATTERN = re.compile(
    r"\bAI\b|\bML\b|LLM|GPT|RAG|Agent|생성형|자동화|\bAX\b|머신러닝|인공지능|"
    r"Applied Scientist|MLOps|Data Scientist|데이터\s*사이언|프롬프트",
    re.I,
)
KOREA_LOCATION_PATTERN = re.compile(r"seoul|korea|서울|대한민국", re.I)

#: 핵심 — 생성형 AI/LLM/RAG/AI Agent "개발" 업무 근거
_CORE_PATTERNS = [
    re.compile(r"생성형\s*AI"), re.compile(r"\bLLM\b", re.I), re.compile(r"\bMLLM\b", re.I),
    re.compile(r"\bvLLM\b", re.I), re.compile(r"\bRAG\b"), re.compile(r"AI\s*Agent", re.I),
    re.compile(r"에이전트"), re.compile(r"Foundation\s*Model", re.I), re.compile(r"파운데이션\s*모델"),
    re.compile(r"프롬프트\s*(설계|엔지니어링)"), re.compile(r"Prompt\s*Engineering", re.I),
    re.compile(r"언어모델"),
]
#: AX — AI 도입/업무자동화/운영개선/AI 서비스 기획 근거
_AX_PATTERNS = [
    re.compile(r"AI\s*도입"), re.compile(r"업무\s*자동화"), re.compile(r"운영\s*개선"),
    re.compile(r"AI\s*서비스\s*기획"), re.compile(r"\bAX\b"), re.compile(r"AI\s*Transformation", re.I),
    re.compile(r"AI\s*전환"), re.compile(r"AI.{0,6}거버넌스|거버넌스.{0,6}AI"),
    re.compile(r"AI\s*기술\s*기반\s*(신규\s*)?제품"), re.compile(r"AI\s*솔루션\s*설계"),
    re.compile(r"In-game\s*AI\s*기능"),
]
#: 기존(core) — AI/ML 엔지니어 기준(생성형AI 언급이 없어도 모델 개발·서빙 자체면 포함)
_BASELINE_ML_PATTERNS = [
    re.compile(r"머신러닝"), re.compile(r"Machine\s*Learning", re.I), re.compile(r"딥러닝"),
    re.compile(r"모델\s*(학습|서빙|추론)"), re.compile(r"Applied\s*Scientist", re.I),
    re.compile(r"\bML\s*(모델|엔지니어|Engineer)", re.I),
]
#: 보안 캐비앗 — AI/LLM "공격·방어 연구"는 개발도 AX 운영개선도 아닌 제3의 성격이라 검토 필요로 내림
_SECURITY_CAVEAT_PATTERNS = [
    re.compile(r"프롬프트\s*인젝션"), re.compile(r"AI\s*레드\s*팀|레드\s*팀.{0,6}AI", re.I),
    re.compile(r"LLM\s*보안"), re.compile(r"탈옥|jailbreak", re.I),
    re.compile(r"AI\s*에이전트.{0,10}공격|공격.{0,10}AI\s*에이전트"),
]
#: 조달/운영 지원 캐비앗 — AI 모델 학습을 "지원"하나 AI 개발/AX 운영개선 자체는 아닌 경우
_PROCUREMENT_CAVEAT_PATTERNS = [
    re.compile(r"데이터\s*확보"), re.compile(r"벤더\s*관리"), re.compile(r"조달"),
    re.compile(r"컴플라이언스"),
]
#: 일반 행정/운영 — 다른 신호가 전혀 없을 때만 "제외" 확정 근거로 쓴다(이것만으론 포함 여부를 못 정하므로)
_ADMIN_EXCLUDE_PATTERNS = [
    re.compile(r"운영계획\s*수립"), re.compile(r"예산.{0,10}인사"), re.compile(r"채용\s*프로그램\s*운영"),
    re.compile(r"조직문화\s*프로그램"), re.compile(r"사무관리"),
]
#: krafton류 공고에서 "본부 소개(division 비전)"와 "이 포지션의 실제 업무"를 분리하기 위한 헤더.
#: 못 찾으면 전체 본문으로 판단한다(보수적 — 잘못 잘라서 근거를 놓치는 것보다 낫다).
_DUTY_SECTION_HEADERS = ["미션을 소개합니다", "이런 일을 해요", "우리 팀과 함께할 미션"]
#: 담당 업무 구간이 끝나고 "자격요건" 구간이 시작되는 지점 — 여기서부터는 "ML 논문을 읽을 줄 아는 분"
#: 같은 자격요건 문구가 담당 업무로 오인되지 않도록 duty 구간에서 잘라낸다.
_DUTY_SECTION_END_MARKERS = [
    "이런 경험을 가진", "필수요건", "필수 요건", "자격요건", "지원자격", "우대요건", "우대 사항", "우대사항",
]
_DUTY_SECTION_WINDOW = 2000  # 끝 마커를 못 찾았을 때의 상한(안전장치)


def _extract_duty_section(body_text: str) -> str:
    for header in _DUTY_SECTION_HEADERS:
        idx = body_text.find(header)
        if idx == -1:
            continue
        start = idx + len(header)
        window = body_text[start: start + _DUTY_SECTION_WINDOW]
        end = len(window)
        for marker in _DUTY_SECTION_END_MARKERS:
            marker_idx = window.find(marker)
            if marker_idx != -1:
                end = min(end, marker_idx)
        return window[:end].lstrip(" .:。\n\t")
    return body_text


def get_duty_excerpt(body_text: str) -> str:
    """`_extract_duty_section()`의 공개 래퍼 — 보고서 발췌용으로 main.py 등에서 재사용한다."""
    return _extract_duty_section(body_text)


def _first_match_snippet(patterns, text, width=50) -> Optional[str]:
    for pat in patterns:
        m = pat.search(text)
        if m:
            start = max(0, m.start() - width)
            end = min(len(text), m.end() + width)
            return text[start:end].replace("\n", " ").strip()
    return None


def classify_ai_ax_relevance(body_text: str) -> dict:
    """본문(업무+자격요건 위주) 텍스트를 보고 '포함'/'검토 필요'/'제외'와 근거(원문 인용)를 반환한다.

    판정 우선순위(2026-10-05 수동 검토 32건에서 역산):
    1) AI/LLM 관련 업무이지만 보안 공격·방어 연구 성격이면 → 검토 필요(개발도 AX도 아닌 제3 성격)
    2) AX(도입·자동화·운영개선·서비스기획) 근거가 있으면 → 포함
    3) 핵심(생성형AI/LLM/RAG/Agent 개발) 근거가 있으면 → 포함
    4) 기존 AI/ML 엔지니어 근거(모델 개발·서빙)가 있으면 → 포함
    5) 그 외 신호가 전혀 없이 일반 행정/운영 업무만 있으면 → 제외
    6) 데이터 조달/벤더관리처럼 AI를 "지원"만 하는 업무면 → 검토 필요
    7) 위 어디에도 안 걸리면(제목 스크리닝은 통과했으나 본문 근거가 아예 없음) → 검토 필요(안전한 기본값)
    """
    duty_text = _extract_duty_section(body_text)

    core_hit = _first_match_snippet(_CORE_PATTERNS, duty_text)
    ax_hit = _first_match_snippet(_AX_PATTERNS, duty_text)
    ml_hit = _first_match_snippet(_BASELINE_ML_PATTERNS, duty_text)
    security_hit = _first_match_snippet(_SECURITY_CAVEAT_PATTERNS, duty_text)
    admin_hit = _first_match_snippet(_ADMIN_EXCLUDE_PATTERNS, duty_text)
    procurement_hit = _first_match_snippet(_PROCUREMENT_CAVEAT_PATTERNS, duty_text)

    if (core_hit or ax_hit or ml_hit) and security_hit:
        return {
            "status": "검토 필요",
            "reason": f"AI/LLM 관련 업무이나 보안 공격·방어 연구 성격이 강해 '개발'/AX 운영개선으로 "
                      f"단정하기 애매함 — 근거: \"...{security_hit}...\"",
        }
    if ax_hit:
        return {"status": "포함", "reason": f"AX(AI 도입·업무자동화·운영개선·서비스기획) 근거: \"...{ax_hit}...\""}
    if core_hit:
        return {"status": "포함", "reason": f"생성형AI·LLM·RAG·AI Agent 개발 근거: \"...{core_hit}...\""}
    if ml_hit:
        return {"status": "포함", "reason": f"AI·ML 엔지니어링(모델 개발·서빙) 근거: \"...{ml_hit}...\""}
    if admin_hit:
        return {
            "status": "제외",
            "reason": f"제목은 AI 관련이나 본문 실제 업무는 일반 운영·행정으로 확인됨 — 근거: "
                      f"\"...{admin_hit}...\"",
        }
    if procurement_hit:
        return {
            "status": "검토 필요",
            "reason": f"AI 모델 개발을 지원하는 데이터 조달/벤더관리성 업무로 보이나, AI 자체 개발이나 "
                      f"AX 운영개선과는 결이 달라 애매함 — 근거: \"...{procurement_hit}...\"",
        }
    return {
        "status": "검토 필요",
        "reason": "제목 1차 스크리닝은 통과했으나 본문에서 뚜렷한 AI·AX 핵심 업무 근거를 찾지 못함 "
                  "— 사람이 직접 확인 필요(안전한 기본값으로 분류, 임의로 포함/제외하지 않음).",
    }


def screen_greenhouse_candidates(records: list) -> list:
    """`collect.parse_greenhouse_job()`이 만든 레코드 리스트에서, 제목이 AI 관련 키워드에 걸리고
    한국 근무지인 것만 1차로 거른다. 여기서 걸러진 것만 `classify_ai_ax_relevance()`로 정밀 판정한다
    (그렇지 않으면 수백 건의 무관한 공고가 전부 '검토 필요'로 보고서에 쏟아진다)."""
    out = []
    for rec in records:
        if not TITLE_SCREEN_PATTERN.search(rec.get("title", "")):
            continue
        if not KOREA_LOCATION_PATTERN.search(rec.get("location", "")):
            continue
        out.append(rec)
    return out


def diff_greenhouse_jobs(
    classified_records: list,
    successful_companies: set,
    history_df: pd.DataFrame,
    now_iso: str,
) -> pd.DataFrame:
    """이번에 수집·분류된 레코드(`classified_records`)를 기존 이력(`history_df`)과 비교해
    신규/기존/마감을 반영한 전체 DataFrame을 반환한다(디스크에 쓰지는 않음 — 그건 호출하는 쪽의 몫).

    **`successful_companies`에 없는 회사는 '마감 처리 대상에서 제외'한다** — 그 회사는 이번 실행에서
    수집에 실패했으므로, 기존 이력에 있던 그 회사의 공고를 "더 이상 안 보이니 마감"으로 잘못 판정하지
    않기 위함이다(수집 실패를 0건으로 흡수하지 않는다는 원칙).
    """
    if history_df is None or history_df.empty:
        history_df = pd.DataFrame(columns=[
            "company", "job_id", "job_url", "title", "location", "ai_ax_status", "ai_ax_reason",
            "duty_excerpt", "body_len", "first_seen_at", "last_seen_at", "posting_status",
            "closed_detected_at", "gemini_response_raw", "gemini_model", "gemini_called_at",
        ])

    history_df = history_df.copy()
    if "job_id" in history_df.columns:
        history_df["job_id"] = history_df["job_id"].astype(str)

    current_keys = set()
    rows = []
    for rec in classified_records:
        key = (rec["company"], str(rec["job_id"]))
        current_keys.add(key)
        existing = history_df[
            (history_df.get("company") == rec["company"]) & (history_df.get("job_id") == str(rec["job_id"]))
        ] if len(history_df) else history_df.iloc[0:0]

        is_new = not len(existing)
        if len(existing):
            first_seen_at = existing.iloc[0]["first_seen_at"]
            gemini_response_raw = existing.iloc[0].get("gemini_response_raw")
            gemini_model = existing.iloc[0].get("gemini_model")
            gemini_called_at = existing.iloc[0].get("gemini_called_at")
        else:
            first_seen_at = now_iso
            gemini_response_raw = None
            gemini_model = None
            gemini_called_at = None

        rows.append({
            "company": rec["company"],
            "job_id": str(rec["job_id"]),
            "job_url": rec["job_url"],
            "title": rec["title"],
            "location": rec["location"],
            "ai_ax_status": rec["ai_ax_status"],
            "ai_ax_reason": rec["ai_ax_reason"],
            "duty_excerpt": rec.get("duty_excerpt", ""),
            "body_len": rec.get("body_len", 0),
            "first_seen_at": first_seen_at,
            "last_seen_at": now_iso,
            "posting_status": "open",
            "closed_detected_at": None,
            "gemini_response_raw": gemini_response_raw,
            "gemini_model": gemini_model,
            "gemini_called_at": gemini_called_at,
            "_is_new": is_new,
        })

    # 과거 이력 중, "이번에 성공적으로 조회한 회사"인데 더 이상 목록에 없는 공고만 마감으로 반영한다.
    if len(history_df):
        for _, old in history_df.iterrows():
            if old.get("company") not in successful_companies:
                carried = old.to_dict()
                carried["_is_new"] = False  # 이전 실행에서의 '신규' 표시가 이월되지 않도록 초기화
                rows.append(carried)  # 미수집 회사는 이력을 그대로 보존(마감 판정 skip)
                continue
            key = (old.get("company"), str(old.get("job_id")))
            if key in current_keys:
                continue  # 이번에도 살아있음 — 위에서 이미 처리함
            updated = old.to_dict()
            updated["_is_new"] = False
            if updated.get("posting_status") != "closed":
                updated["posting_status"] = "closed"
                updated["closed_detected_at"] = now_iso
            rows.append(updated)

    return pd.DataFrame(rows)


# ======================================================================
# 잡코리아 목록 수집 — 제목 기반 1차 스크리닝 (2026-10-05, 본문 수집·분석 없음)
#
# 사용자 지시: "본문 분석과 AI 요약은 제외" — 그래서 Greenhouse처럼 본문을 읽고 판정하는 분류기는
# 쓰지 않는다. 검색 결과 목록의 **제목에 AI·AX 관련 키워드가 있는지만** 본다. 이 방식은 본문을 봤다면
# 포함했을 공고를 놓칠 수 있다(2026-10-04 STEP 09 사전 준비-A에서 실제로 "검토 필요(명확한 후보 0건)"
# 였던 전례가 있다) — 이 한계는 docs/STATUS.md에 명시했다.
# ======================================================================
JOBKOREA_TITLE_PATTERN = re.compile(
    r"AI|인공지능|머신러닝|딥러닝|LLM|\bAX\b",
    re.I,
)


def screen_jobkorea_candidates(records: list) -> list:
    """`collect.fetch_jobkorea_search_list()`가 돌려준 레코드 중 제목에 AI·AX 키워드가 있는 것만 거른다."""
    return [r for r in records if JOBKOREA_TITLE_PATTERN.search(r.get("job_title") or "")]


# ======================================================================
# 잡코리아 알림 — 채널(Slack/Gmail)별 중복 발송 방지 (2026-10-05)
#
# "신규 공고(첫 발견)"와 "이 채널로 아직 성공적으로 보낸 적 없음"은 서로 다른 개념이다. 예를 들어
# Slack은 성공하고 Gmail은 실패했다면, 다음 실행에서 Slack에는 같은 공고를 다시 보내면 안 되지만
# Gmail에는 (사용자가 다시 시도를 요청했을 때) 여전히 보낼 후보여야 한다. 그래서 채널별로 별도
# 컬럼(`slack_notified_at`/`gmail_notified_at`)을 두고, **"성공"했을 때만** 그 채널의 타임스탬프를
# 채운다 — 실패하거나 아예 시도하지 않았으면 그 채널 컬럼은 계속 비워 둔다(= 여전히 "보낼 후보").
# ======================================================================
JOBKOREA_NOTIFICATION_HISTORY_COLUMNS = [
    "job_url", "company_name", "job_title", "first_seen_at", "slack_notified_at", "gmail_notified_at",
]


def load_jobkorea_notification_history(history_path: str) -> pd.DataFrame:
    if os.path.exists(history_path):
        return pd.read_csv(history_path, encoding="utf-8-sig")
    return pd.DataFrame(columns=JOBKOREA_NOTIFICATION_HISTORY_COLUMNS)


def annotate_notification_pending(candidates_df: pd.DataFrame, history_df: pd.DataFrame) -> pd.DataFrame:
    """현재 스크리닝된 후보(`candidates_df`, `job_url` 포함)에 `is_new`/`slack_pending`/`gmail_pending`을
    채워 돌려준다. 이력에 없는 공고는 당연히 둘 다 pending(True)이다. **파일은 쓰지 않는다** — 실제 전송
    결과를 알고 난 뒤 `update_jobkorea_notification_history()`가 쓴다."""
    result = candidates_df.copy()
    if result.empty:
        result["is_new"] = pd.Series(dtype=bool)
        result["slack_pending"] = pd.Series(dtype=bool)
        result["gmail_pending"] = pd.Series(dtype=bool)
        return result

    if len(history_df) and "job_url" in history_df.columns:
        hist = history_df.set_index("job_url")
    else:
        hist = pd.DataFrame(columns=JOBKOREA_NOTIFICATION_HISTORY_COLUMNS).set_index("job_url")

    def _is_new(url):
        return url not in hist.index

    def _pending(url, col):
        if url not in hist.index:
            return True
        val = hist.loc[url, col]
        return bool(pd.isna(val)) or val in (None, "")

    result["is_new"] = result["job_url"].apply(_is_new)
    result["slack_pending"] = result["job_url"].apply(lambda u: _pending(u, "slack_notified_at"))
    result["gmail_pending"] = result["job_url"].apply(lambda u: _pending(u, "gmail_notified_at"))
    return result


def update_jobkorea_notification_history(
    candidates_df: pd.DataFrame,
    history_df: pd.DataFrame,
    slack_sent_ok: bool,
    gmail_sent_ok: bool,
    now_iso: str,
) -> pd.DataFrame:
    """이번에 스크리닝된 후보 전원을 이력에 반영한다(없으면 추가, `first_seen_at` 기록). **채널별
    타임스탬프는 그 채널이 '이번에 pending이었고 + 실제로 성공했을 때만' 채운다** — 실패했거나
    애초에 이미 성공해 있던 채널은 건드리지 않는다. 디스크에 쓰는 것은 호출하는 쪽의 몫이다(live일 때만).
    """
    if history_df is None or history_df.empty:
        history_df = pd.DataFrame(columns=JOBKOREA_NOTIFICATION_HISTORY_COLUMNS)
    history_df = history_df.copy()
    if "job_url" in history_df.columns:
        hist_index = {url: i for i, url in enumerate(history_df["job_url"])}
    else:
        hist_index = {}

    rows = history_df.to_dict("records")

    for _, cand in candidates_df.iterrows():
        url = cand["job_url"]
        was_slack_pending = bool(cand.get("slack_pending", True))
        was_gmail_pending = bool(cand.get("gmail_pending", True))

        if url in hist_index:
            idx = hist_index[url]
            if slack_sent_ok and was_slack_pending:
                rows[idx]["slack_notified_at"] = now_iso
            if gmail_sent_ok and was_gmail_pending:
                rows[idx]["gmail_notified_at"] = now_iso
        else:
            rows.append({
                "job_url": url,
                "company_name": cand.get("company_name"),
                "job_title": cand.get("job_title"),
                "first_seen_at": now_iso,
                "slack_notified_at": now_iso if (slack_sent_ok and was_slack_pending) else None,
                "gmail_notified_at": now_iso if (gmail_sent_ok and was_gmail_pending) else None,
            })
            hist_index[url] = len(rows) - 1

    return pd.DataFrame(rows, columns=JOBKOREA_NOTIFICATION_HISTORY_COLUMNS)
