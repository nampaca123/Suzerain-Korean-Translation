# 한글에 문자 그대로 남은 백슬래시+n(두 글자)을 실제 줄바꿈으로 되돌린다(영문에 실제 줄바꿈이 있는 줄만). 멱등.
# 실행: .venv\Scripts\python -m scripts.fix_literal_newlines [--dry]
import json
import sys

from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl

LITERAL = chr(92) + "n"


def fix_row(r: dict) -> bool:
    changed = False
    for f, ef in (("ko", "en"), ("menu_ko", "menu_en")):
        if r.get(f) and LITERAL in r[f] and "\n" in (r.get(ef) or ""):
            r[f], changed = r[f].replace(LITERAL, "\n"), True
    return changed


def main(argv: list[str]) -> None:
    dry = "--dry" in argv
    targets = [paths.CURRENT / "dialogue.jsonl", paths.CURRENT / "textassets.jsonl"]
    for st in paths.BATCHES.glob("*/status.json"):  # 배치 입력과 검수본도 함께 갱신(검수자가 옛 표기를 보지 않게)
        targets += [st.parent / n for n in ("input.jsonl", "reviewed.jsonl") if (st.parent / n).exists()]
    total = 0
    for t in targets:
        rows = list(read_jsonl(t))
        n = sum(fix_row(r) for r in rows)
        if n and not dry:
            write_jsonl(t, rows)
        if n:
            print(f"{t.name if t.name != 'input.jsonl' else t.parent.name}: {n}")
        total += n
    print(f"total={total} dry={dry}")


if __name__ == "__main__":
    main(sys.argv[1:])
