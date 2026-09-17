# Rizia 텍스트에셋의 이름 필드(칙령·정책·코덱스·지도 토큰·세력·작전 제목)를 영문·현재 한글·코퍼스 출현 수로 뽑아 용어 사전 승인용 표를 만든다.
# 실행: .venv\Scripts\python -m scripts.list_rizia_names <출력.md>
import re
import sys
from collections import Counter

from scripts import paths
from scripts.build_corpus import read_jsonl

NAME_FIELDS = {"DecreeData": "Title", "PolicyData": "Title", "CodexEntryData": "Title", "MapTokenData": "Name",
               "FactionData": "Title", "OperationData": "OperationName", "ConnectionData": "Name",
               "TokenStatusEffectData": "Title", "SituationData": "Title", "WarFragmentData": "HubWarFragmentTitle"}
LATIN = re.compile(r"[A-Za-z]{3,}")
# 뜻이 있는 영어 낱말을 소리로만 옮긴 흔적(R74 뜻풀이형 검토 대상)
SUSPECT = re.compile(r"(크라운|슈프림|캠페인|이니셔티브|프로젝트|프로그램|오퍼레이션|무브먼트|얼라이언스|어코드|팩트|서밋|페스티벌|유니언|프론트|리그|플랜|액트|데이|위크|퍼레이드|파티|하우스|오브|더 |리버|마운틴|밸리)")


def main(out: str) -> None:
    ta = list(read_jsonl(paths.CURRENT / "textassets.jsonl"))
    texts = [r["ko"] for r in ta] + [r["ko"] for r in read_jsonl(paths.CURRENT / "dialogue.jsonl")]
    blob = "\n".join(texts)
    seen, rows = set(), []
    for r in ta:
        if NAME_FIELDS.get(r["file"]) != r["field_path"].split("/")[-1] or not r["en"].strip():
            continue
        key = (r["file"], r["en"].strip())
        if key in seen:
            continue
        seen.add(key)
        ko = r["ko"].strip()
        rows.append((r["file"], r["en"].strip(), ko, blob.count(ko) if ko else 0, bool(LATIN.search(ko)), bool(SUSPECT.search(ko))))
    lines = ["# Rizia 이름 필드 전수 목록 (용어 사전 승인용)", "",
             f"항목 {len(rows)}개. '출현'은 현재 코퍼스(대사+텍스트에셋)에서 한글 표기가 나오는 횟수. '로마자'는 한글 안에 영문이 남은 경우.", "",
             "| 파일 | 영문 | 현재 한글 | 출현 | 로마자 | 음차 의심 |", "|---|---|---|---|---|---|"]
    for f, en, ko, n, latin, sus in sorted(rows):
        lines.append(f"| {f} | {en} | {ko} | {n} | {'예' if latin else ''} | {'예' if sus else ''} |")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"rows={len(rows)} latin={sum(1 for r in rows if r[4])} suspect={sum(1 for r in rows if r[5])}")
    for r in sorted(rows):
        if r[5]:
            print(f"  {r[0]} | {r[1]} | {r[2]} | {r[3]}")
    print(Counter(r[0] for r in rows))


if __name__ == "__main__":
    main(sys.argv[1])
