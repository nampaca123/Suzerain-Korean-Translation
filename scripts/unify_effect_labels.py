# 효과 표기 [N 라벨]의 라벨을 HUDStatData 명칭(권위·예산·에너지·군수 장비·군사 인력 등)으로 통일한다(R72).
# data/current 전체와 아직 시작하지 않은(ready) 배치의 input.jsonl에만 적용. 실행: .venv\Scripts\python -m scripts.unify_effect_labels [--dry]
import json
import sys

from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl
from scripts.preprocess_mechanical import fix_effect_tags


def unify_file(path, dry: bool) -> int:
    rows, changed = list(read_jsonl(path)), 0
    for r in rows:
        for f in ("ko", "menu_ko"):
            if r.get(f) and (new := fix_effect_tags(r[f])) != r[f]:
                r[f], changed = new, changed + 1
    if changed and not dry:
        write_jsonl(path, rows)
    return changed


def main(argv: list[str]) -> None:
    dry = "--dry" in argv
    targets = [paths.CURRENT / "dialogue.jsonl", paths.CURRENT / "textassets.jsonl"]
    for st in paths.BATCHES.glob("*/status.json"):
        if json.loads(st.read_text(encoding="utf-8"))["stage"] == "ready":
            targets.append(st.parent / "input.jsonl")
    total = 0
    for t in targets:
        n = unify_file(t, dry)
        total += n
        if n:
            print(f"{t}: {n} fields changed")
    print(f"total={total} dry={dry}")


if __name__ == "__main__":
    main(sys.argv[1:])
