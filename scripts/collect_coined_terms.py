# 선례 없는 새 표기(뜻풀이형 번역 등)를 배치별 coined_terms.jsonl과 prompts/coined_terms.jsonl에서 모아 보고서로 만든다(R74).
# 실행: .venv\Scripts\python -m scripts.collect_coined_terms [출력.md]
import json
import sys

from scripts import paths


def collect() -> list[dict]:
    files = [paths.PROMPTS / "coined_terms.jsonl", *sorted(paths.BATCHES.glob("*/coined_terms.jsonl"))]
    out = []
    for f in files:
        if not f.exists():
            continue
        src = "controller" if f.parent == paths.PROMPTS else f.parent.name
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append({"source": src, **json.loads(line)})
    return out


def to_md(rows: list[dict]) -> str:
    lines = ["# 신규 표기 대장 (선례 없는 번역, 사후 확인용)", "",
             "| 영문 | 채택 표기 | 종류 | 근거 | 출처 | key |", "|---|---|---|---|---|---|"]
    for r in rows:
        keys = ", ".join(r.get("keys", [])[:3]) + (" …" if len(r.get("keys", [])) > 3 else "")
        lines.append(f"| {r.get('en','')} | {r.get('ko','')} | {r.get('kind','')} | {r.get('reason','')} | {r['source']} | {keys} |")
    return "
".join(lines) + "
"


if __name__ == "__main__":
    rows = collect()
    md = to_md(rows)
    if len(sys.argv) > 1:
        open(sys.argv[1], "w", encoding="utf-8").write(md)
    print(f"coined_terms={len(rows)}")
