# 용어집의 자동 치환 항목을 data/current 전체와 아직 시작하지 않은(ready) 배치의 input.jsonl에 다시 적용한다(멱등).
# 용어집에 항목을 추가·변경했을 때 한 번 실행. 실행: .venv\Scripts\python -m scripts.reapply_glossary [--dry]
import json
import sys

from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl
from scripts.build_glossary import load_glossary
from scripts.preprocess_mechanical import apply_glossary


def reapply_file(path, glossary: list[dict], dry: bool) -> int:
    rows, changed = list(read_jsonl(path)), 0
    for r in rows:
        for f in ("ko", "menu_ko"):
            if r.get(f):
                new, applied = apply_glossary(r[f], glossary)
                if applied:
                    r[f], changed = new, changed + 1
    if changed and not dry:
        write_jsonl(path, rows)
    return changed


def main(argv: list[str]) -> None:
    dry, glossary = "--dry" in argv, load_glossary()
    targets = [paths.CURRENT / "dialogue.jsonl", paths.CURRENT / "textassets.jsonl"]
    for st in paths.BATCHES.glob("*/status.json"):
        if json.loads(st.read_text(encoding="utf-8"))["stage"] == "ready":
            targets.append(st.parent / "input.jsonl")
    total = 0
    for t in targets:
        n = reapply_file(t, glossary, dry)
        total += n
        if n:
            print(f"{t}: {n} fields changed")
    print(f"total={total} dry={dry}")


if __name__ == "__main__":
    main(sys.argv[1:])
