# 배치 진행 현황(stage별 개수)을 요약하고 다음에 실행할 ready 배치를 우선순위 순으로 고른다.
# 실행: .venv\Scripts\python -m scripts.run_status [--json] [--next N]
import json
import sys
from collections import Counter

from scripts import paths

NEXT_N = 5
IN_PROGRESS_STAGES = ("edited", "failed")
KINDS = ("dialogue", "textassets")


def summarize(next_n: int = NEXT_N) -> dict:
    index = {b["batch"]: b for b in json.loads((paths.BATCHES / "index.json").read_text(encoding="utf-8"))}
    st = {p.parent.name: json.loads(p.read_text(encoding="utf-8")) for p in paths.BATCHES.glob("*/status.json")}
    ordered = sorted(st, key=lambda b: (-index.get(b, {}).get("priority", 0.0), b))
    passed = Counter(s.get("kind", "") for s in st.values() if s["stage"] == "passed")
    return {
        "counts": dict(Counter(s["stage"] for s in st.values())),
        "next": [b for b in ordered if st[b]["stage"] == "ready"][:next_n],
        "needs_human": [b for b in ordered if st[b]["stage"] == "needs_human"],
        "in_progress": [b for b in ordered if st[b]["stage"] in IN_PROGRESS_STAGES],
        "passed_by_kind": {k: passed[k] for k in KINDS},
    }


def main(argv: list[str]) -> None:
    next_n = int(argv[argv.index("--next") + 1]) if "--next" in argv else NEXT_N
    s = summarize(next_n)
    if "--json" in argv:
        print(json.dumps(s, ensure_ascii=False))
        return
    kinds = " ".join(f"{k}={s['passed_by_kind'][k]}" for k in KINDS)
    print(f"stages={s['counts']}")
    print(f"next={s['next']}")
    print(f"in_progress={s['in_progress']}")
    print(f"needs_human={s['needs_human']}")
    print(f"passed {kinds}")


if __name__ == "__main__":
    main(sys.argv[1:])
