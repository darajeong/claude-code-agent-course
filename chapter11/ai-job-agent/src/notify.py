"""전송 단계 — Slack(STEP 12)·Gmail(STEP 13).

`dry_run=True`(기본값)이면 실제 네트워크 요청을 전혀 보내지 않고, 무엇을 보낼 예정이었는지만
돌려준다. `dry_run=False`일 때만 실제로 전송한다 — 이번 작업에서는 `dry_run=False` 경로를
실행하지 않았다.
"""
from typing import Optional


def send_slack(webhook_url: Optional[str], text: str, dry_run: bool = True) -> dict:
    if dry_run:
        return {"dry_run": True, "would_send_to": "slack", "text_preview": text[:80]}
    if not webhook_url:
        return {"dry_run": False, "status": "skipped", "reason": "SLACK_WEBHOOK_URL 없음"}

    import requests

    resp = requests.post(webhook_url, json={"text": text}, timeout=10)
    return {"dry_run": False, "status_code": resp.status_code, "body": resp.text}


def send_gmail(
    address: Optional[str],
    app_password: Optional[str],
    to_address: Optional[str],
    subject: str,
    body: str,
    dry_run: bool = True,
) -> dict:
    if dry_run:
        return {
            "dry_run": True,
            "would_send_to": "gmail",
            "to_preview": "(설정됨)" if to_address else "(없음)",
            "subject": subject,
        }
    if not (address and app_password and to_address):
        return {"dry_run": False, "status": "skipped", "reason": "Gmail 환경변수 누락"}

    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = address
    msg["To"] = to_address

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
        server.starttls()
        server.login(address, app_password)
        server.sendmail(address, [to_address], msg.as_string())
    return {"dry_run": False, "status": "sent"}
