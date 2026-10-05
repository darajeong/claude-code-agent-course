"""Gemini 요약 단계.

- 실제 API 호출(call_gemini)은 `--live` 모드에서만 쓴다.
- dry-run에서는 get_cached_summary()로 이미 저장된 응답(gemini_response_raw)만 재사용한다 —
  추가 API 호출을 하지 않고도 보고서 생성까지 전체 흐름을 검증하기 위함이다.
- 요약 항목은 주요 업무/필수 요건/우대 사항/명시된 기술/직무 유형 5가지로 고정한다(STEP 09~10에서 확정).
"""
import json
from typing import Optional

import pandas as pd

MODEL_NAME = "gemini-3.8-flash"  # STEP 09에서 공식 문서로 확인한 모델명 (ai.google.dev/gemini-api, 2026-10-04 기준)


def build_prompt(job_text: str) -> str:
    return (
        "아래는 채용공고 본문입니다. 다음 다섯 항목을 각각 추출해 정리해 주세요: "
        "주요 업무, 필수 요건, 우대 사항, 명시된 기술, 직무 유형.\n\n"
        "규칙:\n"
        "- 반드시 아래 입력 텍스트에 실제로 쓰여 있는 내용만 사용하세요. 추측하지 마세요.\n"
        "- 입력에 명시되지 않은 항목은 \"명시되지 않음\"이라고 쓰세요.\n"
        "- 다른 설명 없이 아래 JSON 형식으로만 답하세요:\n"
        '{"주요_업무": "...", "필수_요건": "...", "우대_사항": "...", "명시된_기술": "...", "직무_유형": "..."}\n\n'
        "[입력]\n" + job_text
    )


def parse_gemini_json(response_text: str) -> dict:
    """```json ... ``` 코드펜스가 있으면 제거하고 JSON으로 파싱한다."""
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    return json.loads(cleaned)


def call_gemini(prompt: str, model: str = MODEL_NAME):
    """실제 Gemini API 호출. `--live` 모드에서만 호출된다(이 함수 자체는 이번 작업에서 실행하지 않음)."""
    from google import genai  # 지연 import: dry-run 경로에서는 SDK가 없어도 동작하게 하기 위함

    client = genai.Client()
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text


def get_cached_summary(row: pd.Series) -> Optional[dict]:
    """CSV에 이미 저장된 `gemini_response_raw`를 재사용해 요약 dict를 만든다.
    저장된 응답이 없으면 None을 반환한다(= 이 레코드는 아직 요약된 적 없음, dry-run에서는 건너뜀)."""
    raw = row.get("gemini_response_raw")
    if raw is None or (isinstance(raw, float)):  # NaN(float)이면 저장된 응답 없음
        return None
    parsed = parse_gemini_json(raw)
    job_type = row.get("job_type_corrected") or parsed.get("직무_유형")
    return {
        "주요_업무": parsed.get("주요_업무"),
        "필수_요건": parsed.get("필수_요건"),
        "우대_사항": parsed.get("우대_사항"),
        "명시된_기술": parsed.get("명시된_기술"),
        "직무_유형": job_type,
        "고용형태": row.get("employment_type"),
        "model": row.get("gemini_model"),
        "called_at": row.get("gemini_called_at"),
        "source": "cached",
    }
