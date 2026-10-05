"""보고서 생성 단계 (STEP 11, 2026-10-05 잡코리아 목록 섹션 추가 / Greenhouse 섹션은 중단·레거시화).

- 분석 대상(추천 후보)과 분석 제외 대상을 분리해서 보여준다.
- **분석 제외 공고는 '추천 채용공고' 섹션에 절대 넣지 않는다** — 요약이 있어도 별도의
  '[참고] Gemini 요약 결과' 섹션에만 넣고 "추천 아님"을 명시한다.
- **잡코리아 신규 AI·AX 공고 목록은 LinkedIn 수동 입력 트랙과 완전히 분리된 섹션에만 넣는다** —
  두 트랙을 같은 표/같은 목록에 절대 섞지 않는다. 본문 분석·Gemini 요약은 하지 않는다(목록만).
- Greenhouse 섹션(`build_greenhouse_section_markdown`)은 2026-10-05 사용자 지시로 중단되었다 —
  `main.py`가 `greenhouse_fetch_results`를 넘기지 않으면 보고서에 아예 나타나지 않는다(코드는 보존).
"""
import os
from typing import Dict, List, Optional

import pandas as pd

from . import summarize


def _job_block(row: pd.Series, summary: dict) -> str:
    lines = [
        f"- **회사**: {row.get('company_name')}",
        f"- **공고 제목**: {row.get('job_title')}",
        f"- **원문 URL**: {row.get('job_url')}",
        f"- **수집 방식**: {row.get('collection_method')}",
    ]
    if summary:
        lines.append(f"- **직무 유형**: {summary.get('직무_유형')}")
        if summary.get("고용형태"):
            lines.append(f"- **고용형태**: {summary.get('고용형태')}")
    lines.append("")
    if summary:
        lines.append("**주요 업무**")
        lines.append(f"- {summary.get('주요_업무')}")
        lines.append("")
        lines.append("**필수 요건**")
        lines.append(f"- {summary.get('필수_요건')}")
        lines.append("")
        lines.append("**우대 사항**")
        lines.append(f"- {summary.get('우대_사항')}")
        lines.append("")
        lines.append("**명시된 기술**")
        lines.append(str(summary.get("명시된_기술")))
        lines.append("")
        lines.append(f"> Gemini 모델: `{summary.get('model')}` / 호출 시각: `{summary.get('called_at')}`"
                      f" / 출처: {summary.get('source')}")
    else:
        lines.append("_(Gemini 요약 없음 — 캐시된 응답이 없어 dry-run에서는 생성하지 않음)_")
    return "\n".join(lines)


def _greenhouse_job_block(row: pd.Series) -> str:
    summary = summarize.get_cached_summary(row)
    lines = [
        f"- **회사**: {row.get('company')}",
        f"- **공고 제목**: {row.get('title')}",
        f"- **근무지**: {row.get('location')}",
        f"- **원문 URL**: {row.get('job_url')}",
        f"- **판정 상태**: {row.get('ai_ax_status')}",
        f"- **포함/검토 이유**: {row.get('ai_ax_reason')}",
        "",
    ]
    if summary:
        lines.append(f"> Gemini 요약 (모델: `{summary.get('model')}`, 호출: `{summary.get('called_at')}`)")
        lines.append(f"- 주요 업무: {summary.get('주요_업무')}")
        lines.append(f"- 필수 요건: {summary.get('필수_요건')}")
        lines.append(f"- 우대 사항: {summary.get('우대_사항')}")
    else:
        excerpt = (row.get("duty_excerpt") or "").strip()
        if len(excerpt) > 600:
            excerpt = excerpt[:600] + " ...(이하 생략, 원문 URL 참고)"
        lines.append("> **AI 요약 미실행** — 아직 Gemini로 요약된 적 없는 공고입니다(dry-run이거나, "
                     "live 모드에서도 최초 수집이라 아직 호출 전일 수 있습니다). 대신 본문 발췌와 "
                     "포함 판정 근거를 아래에 보여드립니다.")
        lines.append("")
        lines.append("**본문 발췌(업무/자격요건 추정 구간)**")
        lines.append(f"> {excerpt if excerpt else '(본문을 추출하지 못함)'}")
    return "\n".join(lines)


def _greenhouse_company_status_table(fetch_results: List[dict], greenhouse_df: pd.DataFrame) -> List[str]:
    lines = ["| 기업 | 수집 상태 | 신규 | 기존(계속 열림) | 마감 | 포함 | 검토 필요 | 제외 |",
             "|---|---|---|---|---|---|---|---|"]
    for fr in fetch_results:
        company = fr["company"]
        if fr["status"] != "ok":
            lines.append(f"| {company} | **수집 실패**({fr.get('error')}) | - | - | - | - | - | - |"
                         )
            continue
        sub = greenhouse_df[greenhouse_df["company"] == company] if len(greenhouse_df) else greenhouse_df
        new_count = int((sub.get("_is_new") == True).sum()) if "_is_new" in sub.columns else 0  # noqa: E712
        open_existing = int(((sub.get("posting_status") == "open") & (sub.get("_is_new") != True)).sum()) if len(sub) else 0  # noqa: E712
        closed_count = int((sub.get("posting_status") == "closed").sum()) if len(sub) else 0
        included = int(((sub.get("ai_ax_status") == "포함") & (sub.get("posting_status") == "open")).sum()) if len(sub) else 0
        review = int(((sub.get("ai_ax_status") == "검토 필요") & (sub.get("posting_status") == "open")).sum()) if len(sub) else 0
        excluded = int(((sub.get("ai_ax_status") == "제외") & (sub.get("posting_status") == "open")).sum()) if len(sub) else 0
        lines.append(
            f"| {company} | 성공 | {new_count} | {open_existing} | {closed_count} | "
            f"{included} | {review} | {excluded} |"
        )
    return lines


def build_jobkorea_section_markdown(new_df: pd.DataFrame, fetch_result: Optional[dict]) -> List[str]:
    """잡코리아 신규 AI·AX 공고 섹션 — **목록(회사·제목·링크)만**, 본문 분석·Gemini 요약 없음.

    2026-10-05 사용자 지시: "본문 분석과 AI 요약은 제외". 그래서 이 섹션은 의도적으로 매우 단순하다.
    """
    parts = ["## 2. 잡코리아 신규 AI·AX 공고 (목록만 — 본문 분석·AI 요약 없음)", ""]
    fetch_result = fetch_result or {}
    if fetch_result.get("status") != "ok":
        parts.append(
            f"⚠️ **이번 실행에서 수집 실패** — {fetch_result.get('error')} "
            f"(0건이 아니라 '확인하지 못함'입니다. 운영 이력은 이번 실행에서 변경하지 않았습니다.)"
        )
        parts.append("")
        return parts

    parts.append(f"- 검색어: `{fetch_result.get('keyword')}`")
    parts.append(f"- 검색 URL: {fetch_result.get('search_url')}")
    parts.append(
        "- 방식: 검색 결과 **목록 페이지만** 1회 조회(상세 페이지 방문 없음), 제목에 AI·AX 키워드가 "
        "있는 공고만 추림. 제목만으로 판단하므로 실제로 관련 있는 공고를 놓칠 수 있습니다(아래 "
        "'데이터 출처와 한계' 참고)."
    )
    parts.append("")

    if new_df is None or new_df.empty:
        parts.append("이번 실행에서 새로 발견된(이전에 알려드리지 않은) AI·AX 관련 공고가 없습니다.")
    else:
        for _, row in new_df.iterrows():
            company = row.get("company_name") or "(회사명 확인 필요)"
            parts.append(f"- **{company}** — {row.get('job_title')} — {row.get('job_url')}")
    parts.append("")
    return parts


def build_greenhouse_section_markdown(
    greenhouse_df: pd.DataFrame,
    fetch_results: List[dict],
) -> List[str]:
    """(2026-10-05 중단됨 — main.py에서는 더 이상 호출하지 않음, 참고용으로 보존)
    Greenhouse 자동 수집 결과 섹션(기업별 현황 + 신규 포함 + 검토 필요 + 기존/마감 요약)을 만든다."""
    parts = ["## 5. [레거시, 중단됨] Greenhouse 자동 수집 결과 (krafton/daangn/sendbird/moloco)", ""]

    failed = [fr["company"] for fr in fetch_results if fr["status"] != "ok"]
    if failed:
        parts.append(
            f"⚠️ **이번 실행에서 수집에 실패한 기업: {', '.join(failed)}** — 공고 0건이 아니라 "
            f"'확인하지 못함'입니다. 해당 기업의 기존 이력은 이번 실행에서 변경하지 않았습니다."
        )
        parts.append("")

    parts.append("### 5-1. 기업별 수집 현황")
    parts.append("")
    parts += _greenhouse_company_status_table(fetch_results, greenhouse_df)
    parts.append("")

    open_df = greenhouse_df[greenhouse_df.get("posting_status") == "open"] if len(greenhouse_df) else greenhouse_df
    included_df = open_df[open_df.get("ai_ax_status") == "포함"] if len(open_df) else open_df
    new_included_df = included_df[included_df.get("_is_new") == True] if len(included_df) else included_df  # noqa: E712
    existing_included_df = included_df[included_df.get("_is_new") != True] if len(included_df) else included_df  # noqa: E712
    review_df = open_df[open_df.get("ai_ax_status") == "검토 필요"] if len(open_df) else open_df
    closed_df = greenhouse_df[greenhouse_df.get("posting_status") == "closed"] if len(greenhouse_df) else greenhouse_df

    parts += ["### 5-2. 신규 포함 공고 (이번 실행에서 처음 발견된 AI·AX 관련 공고)", ""]
    if new_included_df.empty:
        parts.append("이번 실행에서 새로 발견된 '포함' 공고가 없습니다.")
    else:
        for _, row in new_included_df.iterrows():
            parts.append(_greenhouse_job_block(row))
            parts.append("")

    parts += ["### 5-3. 기존 포함 공고 (이전 실행에서 이미 보고됨, 계속 열려있음)", ""]
    if existing_included_df.empty:
        parts.append("해당 없음.")
    else:
        for _, row in existing_included_df.iterrows():
            parts.append(f"- [{row.get('company')}] {row.get('title')} ({row.get('location')}) — {row.get('job_url')}")
    parts.append("")

    parts += ["### 5-4. 검토 필요 공고 (사람이 직접 포함 여부를 확인해야 함)", ""]
    if review_df.empty:
        parts.append("해당 없음.")
    else:
        for _, row in review_df.iterrows():
            parts.append(_greenhouse_job_block(row))
            parts.append("")

    parts += ["### 5-5. 마감된 공고 (참고 — 이전엔 있었으나 이번 조회에서 더 이상 보이지 않음)", ""]
    if closed_df.empty:
        parts.append("해당 없음.")
    else:
        for _, row in closed_df.iterrows():
            parts.append(f"- [{row.get('company')}] {row.get('title')} — 마감 감지 시각: {row.get('closed_detected_at')}")
    parts.append("")
    return parts


def build_report_markdown(
    full_df: pd.DataFrame,
    analysis_df: pd.DataFrame,
    dry_run: bool,
    generated_at: str,
    jobkorea_new_df: Optional[pd.DataFrame] = None,
    jobkorea_fetch_result: Optional[dict] = None,
    greenhouse_df: Optional[pd.DataFrame] = None,
    greenhouse_fetch_results: Optional[List[dict]] = None,
) -> str:
    total = len(full_df)
    excluded = int(full_df["excluded_from_analysis"].sum()) if "excluded_from_analysis" in full_df.columns else 0
    analysis_count = len(analysis_df)

    mode_note = (
        "**이 보고서는 dry-run(외부 호출·발송 없이 저장된 응답으로 검증) 모드로 생성되었습니다.**"
        if dry_run else
        "이 보고서는 실제(live) 실행으로 생성되었습니다."
    )

    jobkorea_new_df = jobkorea_new_df if jobkorea_new_df is not None else pd.DataFrame()
    jobkorea_fetch_result = jobkorea_fetch_result or {}
    jk_new_count = len(jobkorea_new_df)
    jk_status = jobkorea_fetch_result.get("status", "미실행")

    greenhouse_df = greenhouse_df if greenhouse_df is not None else pd.DataFrame()
    greenhouse_fetch_results = greenhouse_fetch_results or []
    greenhouse_active = bool(greenhouse_fetch_results)  # 2026-10-05 중단 — main.py가 넘기지 않으면 섹션 자체가 안 나옴

    parts = [
        f"# 주간 AX 채용공고 리포트 ({generated_at[:10]})",
        "",
        f"> {mode_note}",
        "",
        "## 1. 전체 수집 현황 요약",
        "",
        "| 구분 | 건수 | 설명 |",
        "|---|---|---|",
        f"| **잡코리아 — 신규 AI·AX 공고(목록)** | **{jk_new_count}건** | 수집 상태: {jk_status} "
        f"(본문 분석·AI 요약 없음, 회사·제목·링크만) |",
        f"| LinkedIn 수동 입력 — 전체 레코드 | {total}건 | `data/processed/linkedin_manual_*.csv` (자동 수집 아님) |",
        f"| LinkedIn 수동 입력 — 분석 대상 | {analysis_count}건 | `excluded_from_analysis=False`인 레코드만 |",
        f"| LinkedIn 수동 입력 — 분석 제외 | {excluded}건 | 사용자 결정으로 제외됨(AI 업무 없음을 뜻하지 않음) |",
        "",
    ]

    parts += build_jobkorea_section_markdown(jobkorea_new_df, jobkorea_fetch_result)

    parts += ["## 3. LinkedIn 수동 입력 트랙 (잡코리아 자동 수집과 완전히 별도)", ""]
    parts += ["### 3-1. 이번 주 추천 채용공고 (LinkedIn)", ""]

    if analysis_count == 0:
        parts.append(
            "현재 분석 대상에 포함된 채용공고가 없어 추천할 공고가 없습니다. "
            "(수집 실패가 아니라, 제외 결정·파이프라인 미완료에 따른 정상적인 결과입니다.)"
        )
    else:
        for _, row in analysis_df.iterrows():
            summary = summarize.get_cached_summary(row)
            parts.append(_job_block(row, summary))
            parts.append("")

    parts += ["", "### 3-2. [참고] Gemini 요약 결과 — 추천 공고 아님", ""]

    reference_rows = full_df[full_df.get("excluded_from_analysis", False) == True] if total else full_df.iloc[0:0]  # noqa: E712
    reference_rows = reference_rows[reference_rows["gemini_response_raw"].notna()] if "gemini_response_raw" in reference_rows.columns else reference_rows.iloc[0:0]

    if reference_rows.empty:
        parts.append("분석 제외 레코드 중 Gemini 요약이 저장된 건이 없습니다.")
    else:
        parts.append(
            "이 섹션의 공고는 **정식 추천 목록이 아니라**, 분석 대상에서 제외된 레코드에 대한 Gemini "
            "연동 결과를 참고용으로 보여줍니다."
        )
        parts.append("")
        for _, row in reference_rows.iterrows():
            summary = summarize.get_cached_summary(row)
            parts.append(_job_block(row, summary))
            if row.get("ax_reconsideration_candidate") is True:
                parts.append(f"> ⚠️ **AX 재검토 후보**: {row.get('ax_reconsideration_reason')}")
                parts.append(
                    "> 단, 이 표시는 참고용이며 `excluded_from_analysis`는 변경되지 않았습니다 — "
                    "이 공고는 여전히 추천 목록이 아닙니다."
                )
            parts.append("")

    if greenhouse_active:
        parts.append("")
        parts += build_greenhouse_section_markdown(greenhouse_df, greenhouse_fetch_results)

    parts += [
        "",
        "## 4. 데이터 출처와 한계",
        "",
        "- **잡코리아 신규 AI·AX 공고 목록**: 검색 결과 **목록 페이지만** 1회 조회합니다(상세 페이지 "
        "방문 없음 — 본문·자격요건은 수집하지 않습니다, 2026-10-05 사용자 지시). robots.txt(`User-agent: "
        "*`)가 `/Search/`를 막지 않음을 확인했습니다. **제목에 AI·AX 키워드가 있는지만으로 판단**하므로, "
        "본문에는 관련 내용이 있지만 제목에 키워드가 없는 공고는 놓칠 수 있습니다.",
        "- LinkedIn: robots.txt가 일반 크롤러를 전면 차단해 자동 수집이 불가능함을 확인했습니다. "
        "현재 데이터는 사용자 수동 입력(`collection_method=manual_copy`)이며, 잡코리아 자동 수집과는 "
        "파일·이력·분석이 전부 분리되어 있습니다.",
        "- 이 보고서의 건수는 수집 실패가 아니라, 제외 결정·파이프라인 상태에 따른 정상적인 결과입니다.",
        "",
        "---",
        f"생성 시각: {generated_at} (main.py, {'dry-run' if dry_run else 'live'} 모드)",
    ]
    return "\n".join(parts)


def save_report(markdown_text: str, out_dir: str = "reports", filename: Optional[str] = None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    if filename is None:
        import datetime
        filename = f"weekly_report_{datetime.date.today().isoformat()}.md"
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    return path
