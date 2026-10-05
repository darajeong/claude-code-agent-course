"""정제 단계 — 결측값 확인, 텍스트 공백 제거, job_url 기준 중복 제거.

Notebook STEP 06에서 검증한 로직을 그대로 함수로 옮긴 것이다(날짜를 임의로 채우지 않는 등
SPEC.md 7장의 정제 원칙을 그대로 따른다).
"""
from typing import Tuple

import pandas as pd

TEXT_COLUMNS = [
    "company_name", "job_title", "career", "location", "job_url", "search_keyword",
    "job_description", "qualifications", "preferred_qualifications", "source_site",
    "collection_method",
]


def clean_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """공백 제거 + job_url 기준 중복 제거를 수행하고, (정제된 df, 정제 리포트)를 반환한다.

    정제 리포트에는 정제 전 결측 개수, 중복 제거 전/후 행 수가 들어 있어 main.py에서 로그로
    출력할 수 있다.
    """
    if df.empty:
        return df.copy(), {"missing_counts": {}, "rows_before": 0, "rows_after": 0, "duplicates_removed": 0}

    report = {"missing_counts": df.isna().sum().to_dict()}

    cleaned = df.copy()
    for col in TEXT_COLUMNS:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).where(cleaned[col].notna(), None)
            cleaned[col] = cleaned[col].apply(lambda v: v.strip() if isinstance(v, str) else v)

    rows_before = len(cleaned)
    if "job_url" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["job_url"], keep="first").reset_index(drop=True)
    rows_after = len(cleaned)

    report["rows_before"] = rows_before
    report["rows_after"] = rows_after
    report["duplicates_removed"] = rows_before - rows_after
    return cleaned, report
