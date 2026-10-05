"""보고서 생성 단계 (STEP 11).

- 분석 대상(추천 후보)과 분석 제외 대상을 분리해서 보여준다.
- **분석 제외 공고는 '추천 채용공고' 섹션에 절대 넣지 않는다** — 요약이 있어도 별도의
  '[참고] Gemini 요약 결과' 섹션에만 넣고 "추천 아님"을 명시한다.
"""
import os
from typing import Dict, Optional

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


def build_report_markdown(
    full_df: pd.DataFrame,
    analysis_df: pd.DataFrame,
    dry_run: bool,
    generated_at: str,
) -> str:
    total = len(full_df)
    excluded = int(full_df["excluded_from_analysis"].sum()) if "excluded_from_analysis" in full_df.columns else 0
    analysis_count = len(analysis_df)

    mode_note = (
        "**이 보고서는 dry-run(외부 호출·발송 없이 저장된 응답으로 검증) 모드로 생성되었습니다.**"
        if dry_run else
        "이 보고서는 실제(live) 실행으로 생성되었습니다."
    )

    parts = [
        f"# 주간 AX 채용공고 리포트 ({generated_at[:10]})",
        "",
        f"> {mode_note}",
        "",
        "## 1. 분석 현황 요약",
        "",
        "| 구분 | 건수 | 설명 |",
        "|---|---|---|",
        f"| 전체 레코드 | {total}건 | `data/processed/`의 수동 입력 레코드 전체 |",
        f"| 분석 대상(추천 후보) | **{analysis_count}건** | `excluded_from_analysis=False`인 레코드만 |",
        f"| 분석 제외 | {excluded}건 | 사용자 결정으로 제외됨(AI 업무 없음을 뜻하지 않음) |",
        "",
        "## 2. 이번 주 추천 채용공고",
        "",
    ]

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

    parts += ["", "## 3. [참고] Gemini 요약 결과 — 추천 공고 아님", ""]

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
            parts.append("")

    parts += [
        "",
        "## 4. 데이터 출처와 한계",
        "",
        "- LinkedIn: robots.txt가 일반 크롤러를 전면 차단해 자동 수집이 불가능함을 확인했습니다. "
        "현재 데이터는 사용자 수동 입력(`collection_method=manual_copy`)입니다.",
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
