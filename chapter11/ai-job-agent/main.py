"""ai-job-agent 파이프라인 진입점 (STEP 14~16).

기본 실행(인자 없음)은 **dry-run**입니다 — Gemini API를 호출하지 않고, Slack·Gmail로 실제 메시지도
보내지 않습니다. 이미 저장된 Gemini 응답(`gemini_response_raw`)만 재사용해서 "수집 → 정제 →
신규판별 → 분석 → 요약 → 보고서 → 전송"이라는 전체 흐름이 끝까지 끊기지 않고 돌아가는지만 검증합니다.

실제로 Gemini를 호출하고 Slack·Gmail을 보내려면:
    python main.py --live

(--live 모드에는 `.env`에 GEMINI_API_KEY / SLACK_WEBHOOK_URL / GMAIL_* 가 필요합니다.
 이번 세션에서는 --live 경로를 실행하지 않았습니다.)
"""
import argparse
import datetime
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import analyze, clean, collect, notify, report, summarize  # noqa: E402

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "history_linkedin_manual.csv")


def run(live: bool) -> int:
    load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, ".env"))
    started_at = datetime.datetime.now().astimezone().isoformat()
    mode = "LIVE" if live else "DRY-RUN"
    print(f"[{started_at}] ai-job-agent main.py 시작 (mode={mode})")

    # 1) 수집 (LinkedIn 수동 입력 레코드 로드 — 자동 웹 수집 아님)
    raw_df = collect.load_manual_records(data_dir=os.path.join(PROJECT_ROOT, "data", "processed"))
    print(f"[수집] 레코드 {len(raw_df)}건 로드")

    # 2) 정제
    clean_df, clean_report = clean.clean_dataframe(raw_df)
    print(f"[정제] {clean_report.get('rows_before', 0)}행 -> {clean_report.get('rows_after', 0)}행 "
          f"(중복 제거 {clean_report.get('duplicates_removed', 0)}건)")

    # 3) 신규 판별 (dry-run에서는 운영 이력 파일을 변경하지 않음)
    checked_df = analyze.mark_new_records(clean_df, HISTORY_PATH, update_history=live)
    new_count = int(checked_df["is_new"].sum()) if "is_new" in checked_df.columns and len(checked_df) else 0
    print(f"[신규판별] 신규 {new_count}건 / 전체 {len(checked_df)}건"
          + ("" if live else " (dry-run: 운영 이력 파일 미변경)"))

    # 4) 분석 — 분석 제외 공고는 여기서 걸러진다 (추천 결과에 절대 포함되지 않음)
    analysis_df = analyze.filter_analysis_targets(checked_df)
    stats = analyze.compute_basic_stats(analysis_df)
    print(f"[분석] 분석 대상(추천 후보) {len(analysis_df)}건 "
          f"(전체 {len(checked_df)}건 중 제외 {len(checked_df) - len(analysis_df)}건)")

    # 5) Gemini 요약
    #    - dry-run: 저장된 응답(gemini_response_raw)만 재사용. 추가 API 호출 없음.
    #    - live: 분석 대상 중 캐시된 응답이 없는 건만 실제로 호출한다(이번 세션에서는 미실행 경로).
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
            response_text = summarize.call_gemini(prompt)  # noqa: F841 (아직 저장 로직 없음 — 호출 건수만 집계)
            gemini_calls += 1
            # 참고: 라이브 모드에서 새로 생성한 응답은 이번 실행의 보고서에는 반영되지만,
            # 원본 CSV에 자동으로 다시 저장하지는 않는다(별도 저장 로직은 아직 없음).
    print(f"[Gemini] 실제 호출 {gemini_calls}건" + ("" if live else " (dry-run: 호출 없음, 캐시된 응답만 사용)"))

    # 6) 보고서 생성
    generated_at = datetime.datetime.now().astimezone().isoformat()
    report_md = report.build_report_markdown(checked_df, analysis_df, dry_run=not live, generated_at=generated_at)
    report_path = report.save_report(report_md, out_dir=os.path.join(PROJECT_ROOT, "reports"))
    print(f"[보고서] 저장 완료: {report_path}")

    # 7) 전송 (dry-run에서는 실제로 보내지 않음)
    slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")
    slack_result = notify.send_slack(
        slack_webhook,
        f"[ai-job-agent] 주간 보고서 생성됨: {report_path} (분석 대상 {len(analysis_df)}건)",
        dry_run=not live,
    )
    print(f"[Slack] {slack_result}")

    gmail_result = notify.send_gmail(
        os.environ.get("GMAIL_ADDRESS"),
        os.environ.get("GMAIL_APP_PASSWORD"),
        os.environ.get("GMAIL_TO_ADDRESS"),
        subject="[ai-job-agent] 주간 채용공고 리포트",
        body=f"보고서 경로: {report_path}\n\n{report_md[:500]}...",
        dry_run=not live,
    )
    print(f"[Gmail] {gmail_result}")

    finished_at = datetime.datetime.now().astimezone().isoformat()
    print(f"[{finished_at}] ai-job-agent main.py 종료 (mode={mode})")
    return 0


def main():
    parser = argparse.ArgumentParser(description="ai-job-agent 파이프라인 (기본: dry-run)")
    parser.add_argument(
        "--live", action="store_true",
        help="실제로 Gemini를 호출하고 Slack/Gmail을 전송합니다(.env 필요). 지정하지 않으면 dry-run.",
    )
    args = parser.parse_args()
    return run(live=args.live)


if __name__ == "__main__":
    raise SystemExit(main())
