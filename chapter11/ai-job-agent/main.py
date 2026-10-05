"""ai-job-agent 파이프라인 진입점 (STEP 14~16 + 2026-10-05 잡코리아 목록 수집 연결, Greenhouse 트랙 중단).

**최종 목표(2026-10-05 확정)**: 잡코리아의 신규 AI·AX 채용공고(회사·제목·링크)를 매주 금요일
한국 시간 09:10에 Slack·Gmail로 받는다. **본문 분석과 AI 요약은 하지 않는다** — 목록만 다룬다.

두 트랙을 완전히 분리해서 실행합니다(파일·이력·보고서 섹션 모두 분리, 서로 섞지 않습니다):
  1) LinkedIn 수동 입력 트랙 — 기존 로직 그대로(수집은 `data/processed/linkedin_manual_*.csv`를
     읽는 것뿐, 자동 웹 수집이 아님).
  2) 잡코리아 목록 수집 트랙 — 검색 결과 **목록 페이지만** 1회 조회(상세 페이지 방문 없음, 본문·
     Gemini 요약 없음). 제목에 AI·AX 키워드가 있는 공고만 추려 신규 여부를 판별한다.

**(중단됨) Greenhouse 자동 수집 트랙**: 2026-10-05 중 사용자 지시로 중단되었다. `src/collect.py`·
`src/analyze.py`·`src/report.py`의 관련 함수는 삭제하지 않고 남겨뒀지만, 이 파일(`main.py`)에서는
더 이상 호출하지 않는다.

기본 실행(인자 없음)은 **dry-run**입니다 — Slack·Gmail로 실제 메시지를 보내지 않고, 운영 이력 파일
(`history_linkedin_manual.csv`, `history_jobkorea_ai_ax.csv`)도 갱신하지 않습니다. 그러나 잡코리아
목록 수집 자체(HTTP GET 1회)는 dry-run에서도 실제로 수행합니다 — "수집"과 "그 결과를 바탕으로 한
발송/이력 갱신"을 분리하기 위함입니다.

실제로 Slack·Gmail을 보내고 이력을 갱신하려면:
    python main.py --live

(--live 모드에는 `.env`에 SLACK_WEBHOOK_URL / GMAIL_* 가 필요합니다. 잡코리아 트랙은 Gemini를 쓰지
않습니다 — LinkedIn 트랙만 `GEMINI_API_KEY`가 있으면 캐시 없는 레코드에 한해 호출을 시도합니다.)
"""
import argparse
import datetime
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import analyze, clean, collect, notify, report, summarize  # noqa: E402

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LINKEDIN_HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "history_linkedin_manual.csv")
JOBKOREA_HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "history_jobkorea_ai_ax.csv")


def run_linkedin_track(live: bool) -> tuple:
    """LinkedIn 수동 입력 트랙. 반환: (checked_df, analysis_df)."""
    raw_df = collect.load_manual_records(data_dir=os.path.join(PROJECT_ROOT, "data", "processed"))
    print(f"[LinkedIn/수집] 레코드 {len(raw_df)}건 로드")

    clean_df, clean_report = clean.clean_dataframe(raw_df)
    print(f"[LinkedIn/정제] {clean_report.get('rows_before', 0)}행 -> {clean_report.get('rows_after', 0)}행 "
          f"(중복 제거 {clean_report.get('duplicates_removed', 0)}건)")

    checked_df = analyze.mark_new_records(clean_df, LINKEDIN_HISTORY_PATH, update_history=live)
    new_count = int(checked_df["is_new"].sum()) if "is_new" in checked_df.columns and len(checked_df) else 0
    print(f"[LinkedIn/신규판별] 신규 {new_count}건 / 전체 {len(checked_df)}건"
          + ("" if live else " (dry-run: 운영 이력 파일 미변경)"))

    analysis_df = analyze.filter_analysis_targets(checked_df)
    print(f"[LinkedIn/분석] 분석 대상(추천 후보) {len(analysis_df)}건 "
          f"(전체 {len(checked_df)}건 중 제외 {len(checked_df) - len(analysis_df)}건)")

    return checked_df, analysis_df


def run_jobkorea_track(live: bool) -> tuple:
    """잡코리아 목록 수집 트랙. 반환: (annotated_df, slack_due_df, gmail_due_df, fetch_result, history_df).

    **본문 분석·Gemini 요약을 하지 않는다** — 검색 결과 목록 페이지 1회 조회, 제목 기반 1차 스크리닝뿐이다.
    신규 판별은 "URL 기준 전체 신규 여부"가 아니라 **채널(Slack/Gmail)별로 아직 성공적으로 보낸 적
    없는지**를 기준으로 한다(2026-10-05) — 한 채널만 실패했을 때 그 채널에만 다시 보낼 수 있도록 하기
    위함이다. 실제 이력 갱신(파일 쓰기)은 전송 결과를 알고 난 뒤 `run()`에서 한다.
    """
    import pandas as pd

    fetch_result = collect.fetch_jobkorea_search_list()
    empty_cols = ["company_name", "job_title", "job_url", "is_new", "slack_pending", "gmail_pending"]
    if fetch_result["status"] != "ok":
        print(f"[잡코리아/수집] 실패 — {fetch_result['error']} (0건이 아니라 '확인 못함', 기존 이력 유지)")
        empty = pd.DataFrame(columns=empty_cols)
        return empty, empty, empty, fetch_result, analyze.load_jobkorea_notification_history(JOBKOREA_HISTORY_PATH)

    print(f"[잡코리아/수집] 검색어 '{fetch_result['keyword']}' 결과 {len(fetch_result['jobs'])}건 조회 성공 "
          f"(목록 페이지만, 상세 페이지 방문 없음)")

    candidates = analyze.screen_jobkorea_candidates(fetch_result["jobs"])
    print(f"[잡코리아/제목 스크리닝] AI·AX 키워드 포함 {len(candidates)}건 "
          f"(전체 {len(fetch_result['jobs'])}건 중)")

    df = pd.DataFrame(candidates, columns=["company_name", "job_title", "job_url"])
    history_df = analyze.load_jobkorea_notification_history(JOBKOREA_HISTORY_PATH)
    annotated_df = analyze.annotate_notification_pending(df, history_df)

    new_count = int(annotated_df["is_new"].sum()) if len(annotated_df) else 0
    slack_due_df = annotated_df[annotated_df["slack_pending"] == True].reset_index(drop=True) if len(annotated_df) else annotated_df  # noqa: E712
    gmail_due_df = annotated_df[annotated_df["gmail_pending"] == True].reset_index(drop=True) if len(annotated_df) else annotated_df  # noqa: E712
    print(f"[잡코리아/알림 대상 판별] 신규(최초 발견) {new_count}건 / 전체 {len(annotated_df)}건 — "
          f"Slack 발송 대상 {len(slack_due_df)}건, Gmail 발송 대상 {len(gmail_due_df)}건"
          + ("" if live else " (dry-run: 운영 이력 파일 미변경)"))

    return annotated_df, slack_due_df, gmail_due_df, fetch_result, history_df


def run(live: bool) -> int:
    load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, ".env"))
    started_at = datetime.datetime.now().astimezone().isoformat()
    mode = "LIVE" if live else "DRY-RUN"
    print(f"[{started_at}] ai-job-agent main.py 시작 (mode={mode})")

    checked_df, analysis_df = run_linkedin_track(live)
    jobkorea_annotated_df, slack_due_df, gmail_due_df, jobkorea_fetch_result, jobkorea_history_df = run_jobkorea_track(live)

    # LinkedIn 트랙의 Gemini 호출(기존 로직 그대로 — 분석 대상 중 캐시 없는 건만 live에서 호출).
    # 잡코리아 트랙은 Gemini를 전혀 쓰지 않는다(목록만 다루므로).
    gemini_calls = 0
    if live:
        for idx, row in analysis_df.iterrows():
            has_cached = isinstance(row.get("gemini_response_raw"), str)
            if has_cached:
                continue
            job_text = row.get("gemini_test_input")
            if not isinstance(job_text, str) or not job_text.strip():
                continue
            prompt = summarize.build_prompt(job_text)
            response_text = summarize.call_gemini(prompt)  # noqa: F841 (LinkedIn 레코드 자동 저장 로직은 별도)
            gemini_calls += 1
    print(f"[Gemini/LinkedIn] 실제 호출 {gemini_calls}건" + ("" if live else " (dry-run)"))

    # 기록용 보고서(전체 스크리닝 결과, 채널 상관없이 전부)는 파일로 저장한다.
    generated_at = datetime.datetime.now().astimezone().isoformat()
    archival_report_md = report.build_report_markdown(
        checked_df, analysis_df, dry_run=not live, generated_at=generated_at,
        jobkorea_new_df=jobkorea_annotated_df, jobkorea_fetch_result=jobkorea_fetch_result,
    )
    report_path = report.save_report(archival_report_md, out_dir=os.path.join(PROJECT_ROOT, "reports"))
    print(f"[보고서] 저장 완료: {report_path} (전체 스크리닝 결과 기준, 채널별 발송 내용과는 다를 수 있음)")

    # 채널별로 "아직 그 채널에 성공적으로 보낸 적 없는" 공고만 담은 내용을 따로 만든다 —
    # 한 채널이 이미 성공했다면 같은 공고를 그 채널에 또 보내지 않기 위함이다.
    slack_report_md = report.build_report_markdown(
        checked_df, analysis_df, dry_run=not live, generated_at=generated_at,
        jobkorea_new_df=slack_due_df, jobkorea_fetch_result=jobkorea_fetch_result,
    )
    gmail_report_md = report.build_report_markdown(
        checked_df, analysis_df, dry_run=not live, generated_at=generated_at,
        jobkorea_new_df=gmail_due_df, jobkorea_fetch_result=jobkorea_fetch_result,
    )

    # 채널별로 "보낼 신규 대상이 아예 없으면" 실제 호출 자체를 건너뛴다 — 매주 "새 공고 없음"
    # 메시지를 반복 발송하지 않기 위함이다(스케줄 운영 시 불필요한 알림 방지).
    if len(slack_due_df) == 0:
        slack_result = {"status": "skipped", "reason": "신규 알림 대상 없음"}
        slack_ok = True  # 보낼 것이 없었으므로 이력 관점에서는 '문제 없음'과 동일
        print("[Slack] 건너뜀 — 신규 알림 대상 없음(발송 호출 자체를 하지 않음)")
    else:
        slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
        slack_result = notify.send_slack(slack_webhook, slack_report_md, dry_run=not live)
        slack_ok = notify.is_success(slack_result)
        print(f"[Slack] 성공 여부: {slack_ok} | {slack_result}")

    if len(gmail_due_df) == 0:
        gmail_result = {"status": "skipped", "reason": "신규 알림 대상 없음"}
        gmail_ok = True
        print("[Gmail] 건너뜀 — 신규 알림 대상 없음(발송 호출 자체를 하지 않음)")
    else:
        gmail_result = notify.send_gmail(
            os.environ.get("GMAIL_ADDRESS"),
            os.environ.get("GMAIL_APP_PASSWORD"),
            os.environ.get("GMAIL_TO_ADDRESS"),
            subject="[ai-job-agent] 주간 채용공고 리포트",
            body=gmail_report_md,
            dry_run=not live,
        )
        gmail_ok = notify.is_success(gmail_result)
        print(f"[Gmail] 성공 여부: {gmail_ok} | {gmail_result}")

    if live and not slack_ok:
        print("[알림] Slack 발송이 성공하지 못했습니다 — 자동으로 재시도하지 않습니다. "
              "이 공고들은 다음 실행에서도 Slack 발송 대상으로 남습니다.")
    if live and not gmail_ok:
        print("[알림] Gmail 발송이 성공하지 못했습니다 — 자동으로 재시도하지 않습니다. "
              "이 공고들은 다음 실행에서도 Gmail 발송 대상으로 남습니다.")

    if live:
        updated_history_df = analyze.update_jobkorea_notification_history(
            jobkorea_annotated_df, jobkorea_history_df, slack_ok, gmail_ok, generated_at,
        )
        updated_history_df.to_csv(JOBKOREA_HISTORY_PATH, index=False, encoding="utf-8-sig")
        print(f"[잡코리아/이력] {JOBKOREA_HISTORY_PATH} 저장 완료 "
              f"(Slack 성공 반영: {slack_ok}, Gmail 성공 반영: {gmail_ok})")
    else:
        print("[잡코리아/이력] dry-run: 운영 이력 파일(history_jobkorea_ai_ax.csv) 미변경")

    finished_at = datetime.datetime.now().astimezone().isoformat()
    print(f"[{finished_at}] ai-job-agent main.py 종료 (mode={mode})")
    return 0


def main():
    parser = argparse.ArgumentParser(description="ai-job-agent 파이프라인 (기본: dry-run)")
    parser.add_argument(
        "--live", action="store_true",
        help="실제로 Slack/Gmail을 전송하며 운영 이력을 갱신합니다(.env 필요). "
             "지정하지 않으면 dry-run(잡코리아 목록 수집 자체는 실제로 수행).",
    )
    args = parser.parse_args()
    return run(live=args.live)


if __name__ == "__main__":
    raise SystemExit(main())
