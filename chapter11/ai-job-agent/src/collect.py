"""수집 단계 — LinkedIn 수동 입력 레코드를 불러온다.

LinkedIn은 robots.txt가 일반 크롤러를 전면 차단(Disallow: /)하고 있어 자동 수집이 불가능함을
STEP 03-LI-A/B에서 확인했다. 그래서 이 모듈은 "자동으로 웹에서 가져오는" 수집이 아니라,
사용자가 LinkedIn 화면에서 직접 복사해 `data/processed/`에 저장해 둔 레코드(csv)를 불러온다.
"""
import glob
import os

import pandas as pd


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
