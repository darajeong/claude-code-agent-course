"""분석 단계 — 분석 대상 필터링, 기본 통계, URL 기준 신규 판별.

STEP 07(신규 판별)·STEP 08(제외 기준 적용) 로직을 함수로 옮긴 것이다.
"""
import os
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
