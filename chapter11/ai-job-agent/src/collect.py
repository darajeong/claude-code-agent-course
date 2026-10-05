"""수집 단계 — LinkedIn 수동 입력 레코드 + 잡코리아 목록 수집 + (중단됨) Greenhouse Job Board API.

LinkedIn은 robots.txt가 일반 크롤러를 전면 차단(Disallow: /)하고 있어 자동 수집이 불가능함을
STEP 03-LI-A/B에서 확인했다. 그래서 `load_manual_records()`는 "자동으로 웹에서 가져오는" 수집이
아니라, 사용자가 LinkedIn 화면에서 직접 복사해 `data/processed/`에 저장해 둔 레코드(csv)를 불러온다.

잡코리아 목록 수집(`fetch_jobkorea_search_list`, 2026-10-05)은 검색 결과 **목록 페이지 1회만** 조회한다
(상세 페이지는 전혀 방문하지 않음 — 본문·자격요건은 수집하지 않는다는 사용자 지시에 따름). robots.txt
(`User-agent: *`)가 `/Search/`를 막지 않음을 같은 날 재확인했다(docs/STATUS.md "잡코리아 자동 수집
가능성 검증" 참고). 회사명·공고 제목·URL만 추출한다.

**Greenhouse Job Board API(`fetch_greenhouse_jobs` 등)는 2026-10-05 중 사용자 지시로 중단되었다** —
main.py에서는 더 이상 호출하지 않는다. 함수 자체는 나중에 다시 쓸 수도 있어 삭제하지 않고 남겨뒀다.
"""
import glob
import os

import pandas as pd

# Greenhouse Job Board API를 쓰는 것으로 2026-10-05 조사에서 실제 확인한 한국 기업 4곳.
# (이 4곳이 전부는 아니다 — Greenhouse를 쓰는 다른 한국 기업은 전수 조사하지 않았음, docs/STATUS.md 참고)
# ⚠️ 2026-10-05 중 사용자 지시로 Greenhouse 트랙 자체는 중단됨(main.py에서 호출 안 함) — 아래 참고.
GREENHOUSE_COMPANIES = ["krafton", "daangn", "sendbird", "moloco"]

_DEFAULT_HEADERS = {
    "User-Agent": "ai-job-agent/1.0 (educational project; contact via GitHub repo)",
}


def load_manual_records(data_dir: str = "data/processed", pattern: str = "linkedin_manual_*.csv") -> pd.DataFrame:
    """`data_dir` 아래에서 `pattern`과 일치하는 CSV를 전부 읽어 하나의 DataFrame으로 합친다.

    지금은 파일이 1개(linkedin_manual_4469459251.csv)뿐이지만, 사용자가 공고를 더 수동
    입력하면 파일이 늘어날 수 있으므로 와일드카드로 찾는다. 파일이 하나도 없으면 빈 DataFrame을
    반환한다(예외를 던지지 않음 — "수집 실패"와 "정상적으로 0건"을 구분하기 위해 호출하는 쪽에서
    len(df)로 직접 판단하게 한다).
    """
    paths = sorted(glob.glob(os.path.join(data_dir, pattern)))
    if not paths:
        return pd.DataFrame()
    frames = [pd.read_csv(p, encoding="utf-8-sig") for p in paths]
    return pd.concat(frames, ignore_index=True)


def fetch_greenhouse_company(company: str, timeout: int = 20) -> dict:
    """한 기업의 Greenhouse Job Board 공개 API를 실제로 호출한다(인증 불필요).

    **"수집 실패"를 "0건"으로 흡수하지 않는다** — 네트워크 오류·비정상 상태코드·JSON 파싱 실패는
    전부 `status="error"`로 돌려주고 예외를 던지지 않는다. 호출하는 쪽(analyze/main)은 반드시
    `status`를 먼저 확인해야 하며, `status="error"`인 회사는 "공고 0건"이 아니라 "이번 실행에서는
    확인 못함"으로 다뤄야 한다(해당 회사의 기존 이력도 이번 실행에서는 변경하지 않는다).
    """
    import requests

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    try:
        resp = requests.get(url, headers=_DEFAULT_HEADERS, timeout=timeout)
    except requests.RequestException as exc:
        return {"company": company, "status": "error", "jobs": None, "error": f"요청 실패: {exc}"}

    if resp.status_code != 200:
        return {"company": company, "status": "error", "jobs": None, "error": f"HTTP {resp.status_code}"}

    try:
        data = resp.json()
    except ValueError as exc:
        return {"company": company, "status": "error", "jobs": None, "error": f"JSON 파싱 실패: {exc}"}

    jobs = data.get("jobs")
    if jobs is None:
        return {"company": company, "status": "error", "jobs": None, "error": "응답에 'jobs' 필드가 없음"}

    return {"company": company, "status": "ok", "jobs": jobs, "error": None}


def fetch_greenhouse_jobs(companies=None) -> list:
    """여러 기업을 순회하며 `fetch_greenhouse_company()`를 호출한다.

    한 기업이 실패해도 나머지 기업은 계속 조회한다(한 곳의 장애가 전체 수집을 막지 않도록).
    반환값은 기업별 결과 리스트([{"company", "status", "jobs", "error"}, ...])이며,
    `parse_greenhouse_job()`으로 각 공고를 펼치는 것은 호출하는 쪽(analyze.py)의 몫이다.
    """
    companies = companies or GREENHOUSE_COMPANIES
    return [fetch_greenhouse_company(c) for c in companies]


def parse_greenhouse_job(company: str, job: dict) -> dict:
    """Greenhouse API의 공고 1건(raw dict)을 본문 텍스트까지 펼친 평평한 dict로 변환한다.

    일부 공고(회사 담당자가 Greenhouse 에디터에 붙여넣은 방식에 따라 다름)는 `content`가
    HTML 엔티티로 한 번 더 이스케이프되어 온다(예: `&lt;div&gt;` 형태) — 2026-10-05 실제 수집에서
    krafton 일부 공고에서 이 현상을 확인했다. `html.unescape()`를 먼저 적용하면 정상 HTML에는
    영향이 없으면서도(멱등적) 이런 이중 이스케이프 공고도 올바르게 본문을 추출할 수 있다.
    """
    import html as html_module

    from bs4 import BeautifulSoup

    content_html = html_module.unescape(job.get("content") or "")
    body_text = BeautifulSoup(content_html, "html.parser").get_text("\n", strip=True)
    location = (job.get("location") or {}).get("name") or ""
    return {
        "company": company,
        "job_id": job.get("id"),
        "title": (job.get("title") or "").strip(),
        "location": location,
        "job_url": job.get("absolute_url"),
        "greenhouse_updated_at": job.get("updated_at"),
        "body_text": body_text,
        "body_len": len(body_text),
    }


JOBKOREA_DEFAULT_KEYWORD = "AI 엔지니어"


def fetch_jobkorea_search_list(keyword: str = JOBKOREA_DEFAULT_KEYWORD, timeout: int = 15) -> dict:
    """잡코리아 검색 결과 **목록 페이지만** 1회 GET으로 조회한다 — 공고 상세 페이지는 전혀 방문하지
    않는다(본문·자격요건 수집 없음, 2026-10-05 사용자 지시). robots.txt(`User-agent: *`)가 `/Search/`를
    막지 않음을 같은 날 재확인했다(docs/STATUS.md 참고).

    회사명은 목록 카드의 로고 이미지 `alt` 속성(`"{회사명} 로고"`)에서 추출한다 — 못 찾으면 `None`으로
    남기고 추측해서 채우지 않는다.

    **"수집 실패"를 "0건"으로 흡수하지 않는다** — Greenhouse 수집 함수와 동일한 원칙으로, 네트워크
    오류·비정상 상태코드는 전부 `status="error"`로 반환한다.
    """
    import urllib.parse

    import requests
    from bs4 import BeautifulSoup

    search_url = f"https://www.jobkorea.co.kr/Search/?stext={urllib.parse.quote(keyword)}"
    try:
        resp = requests.get(search_url, headers=_DEFAULT_HEADERS, timeout=timeout)
    except requests.RequestException as exc:
        return {"status": "error", "jobs": None, "error": f"요청 실패: {exc}",
                "keyword": keyword, "search_url": search_url}

    if resp.status_code != 200:
        return {"status": "error", "jobs": None, "error": f"HTTP {resp.status_code}",
                "keyword": keyword, "search_url": search_url}

    resp.encoding = resp.apparent_encoding or "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []
    for card in soup.find_all(attrs={"data-sentry-component": "CardJob"}):
        title_a = card.find("a", attrs={"data-sentry-component": "Title"})
        if not title_a:
            continue
        href = (title_a.get("href") or "").split("?")[0]
        if not href:
            continue
        title_text = title_a.get_text(strip=True)
        company = None
        logo_img = card.find("img", alt=True)
        if logo_img:
            alt = (logo_img.get("alt") or "").strip()
            company = alt[:-len(" 로고")] if alt.endswith(" 로고") else (alt or None)
        jobs.append({"company_name": company, "job_title": title_text, "job_url": href})

    return {"status": "ok", "jobs": jobs, "error": None, "keyword": keyword, "search_url": search_url}
