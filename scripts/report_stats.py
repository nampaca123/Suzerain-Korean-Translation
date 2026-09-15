# 교정 전(corpus)과 후(current)의 flag 분포·화자별 hard flag 건수를 비교하는 markdown 표를 만든다.
# 실행: .venv\Scripts\python -m scripts.report_stats [--out <path>]
import sys
from collections import Counter
from pathlib import Path

from scripts import paths
from scripts.build_corpus import read_jsonl
from scripts.build_glossary import load_glossary
from scripts.check_batch import HARD_FLAGS
from scripts.flag_lines import flag_dialogue, flag_textassets

TOP_SPEAKERS = 15


def collect(src: Path, glossary: list[dict]) -> tuple[Counter, Counter]:
    dialogue_rows = read_jsonl(src / "dialogue.jsonl")
    d = flag_dialogue(dialogue_rows, glossary)
    t = flag_textassets(read_jsonl(src / "textassets.jsonl"), glossary)
    flags = Counter(f for v in list(d.values()) + list(t.values()) for f in v["flags"])
    hard = Counter()
    for r in dialogue_rows:
        n = sum(1 for f in d[r["key"]]["flags"] if f in HARD_FLAGS)
        if n:
            hard[r["actor"]] += n
    return flags, hard


def _table(head: str, before: Counter, after: Counter, keys: list[str]) -> list[str]:
    rows = [f"| {head} | 교정 전 | 교정 후 |", "|---|---|---|"]
    rows += [f"| {k} | {before[k]} | {after[k]} |" for k in keys]
    return rows


def report() -> str:
    g = load_glossary()
    before, hard_before = collect(paths.CORPUS, g)
    after, hard_after = collect(paths.CURRENT, g)
    flag_keys = sorted(set(before) | set(after), key=lambda k: (-before[k], k))
    speaker_keys = sorted(set(hard_before) | set(hard_after),
                          key=lambda k: (-max(hard_before[k], hard_after[k]), k))[:TOP_SPEAKERS]
    out = ["### flag별 건수"] + _table("flag", before, after, flag_keys)
    out += [f"| **합계** | {sum(before.values())} | {sum(after.values())} |"]
    out += ["", f"### 화자별 hard flag 건수 (상위 {TOP_SPEAKERS})"] + _table("화자", hard_before, hard_after, speaker_keys)
    return "\n".join(out)


def main(argv: list[str]) -> None:
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    md = report()
    if out:
        Path(out).write_text(md + "\n", encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
    else:
        print(md)


if __name__ == "__main__":
    main(sys.argv[1:])
