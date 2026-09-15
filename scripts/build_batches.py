# 말뭉치를 에이전트 작업 단위(배치)로 나눠 batches/<id>/ 에 input.jsonl·context.md·status.json을 만든다.
# 배치 목록과 우선순위(flag 비율)는 batches/index.json에 기록한다.
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl

_TURN = re.compile(r"Rizia/Turn (\d+)/")
_KO = re.compile(r"[가-힣]")


def _letters():
    for i in itertools.count():
        yield chr(ord("a") + i)


def group_dialogue(rows: list[dict], max_rows: int = 2500) -> list[tuple[str, list[dict]]]:
    groups: dict[str, list[list[dict]]] = defaultdict(list)
    for _, conv in itertools.groupby(sorted(rows, key=lambda r: (r["conv_id"], r["seq"])), key=lambda r: r["conv_id"]):
        conv = list(conv)
        m = _TURN.search(conv[0]["conv_title"])
        groups[f"turn{int(m.group(1)):02d}" if m else "misc"].append(conv)
    out = []
    # 턴 번호 순으로 먼저, 턴이 없는 misc는 맨 뒤로.
    for gname in sorted(groups, key=lambda g: (g == "misc", g)):
        cur, letters = [], _letters()
        for conv in groups[gname]:
            if cur and len(cur) + len(conv) > max_rows:
                out.append((f"d-{gname}-{next(letters)}", cur))
                cur = []
            cur.extend(conv)
        if cur:
            out.append((f"d-{gname}-{next(letters)}", cur))
    return out


def _chunk(rows: list[dict], prefix: str, max_chars: int) -> list[tuple[str, list[dict]]]:
    out, n, cur, size = [], 1, [], 0
    for _, item in itertools.groupby(rows, key=lambda r: (r["file"], r["item_id"])):
        item = list(item)
        isz = sum(len(r["ko"]) for r in item)
        if cur and size + isz > max_chars:
            out.append((f"{prefix}-{n:02d}", cur))
            n += 1
            cur, size = [], 0
        cur.extend(item)
        size += isz
    if cur:
        out.append((f"{prefix}-{n:02d}", cur))
    return out


def group_textassets(rows: list[dict], max_chars: int = 60000,
                     min_file_chars: int = 5000) -> list[tuple[str, list[dict]]]:
    ordered = sorted(rows, key=lambda r: (r["file"], r["item_id"], r["key"]))
    totals = Counter()
    for r in ordered:
        totals[r["file"]] += len(r["ko"])
    # 문턱이 배치 용량보다 작을 때만, 자잘한 파일을 t-misc 풀로 합친다.
    tiny = {f for f, t in totals.items() if t < min_file_chars} if min_file_chars < max_chars else set()
    out, pool = [], []
    for file, frows in itertools.groupby(ordered, key=lambda r: r["file"]):
        if file in tiny:
            pool.extend(frows)
        else:
            out.extend(_chunk(list(frows), f"t-{file}", max_chars))
    return out + _chunk(pool, "t-misc", max_chars)


def sordland_samples(file: str, n: int = 3) -> list[str]:
    p = paths.RAW_KO / "textassets" / f"{file}.json"
    if not p.exists():
        return []
    items = json.loads(p.read_text(encoding="utf-8")).get("items", [])
    texts = []
    for it in items:
        packs = it.get("AppBundleProperties", {}).get("StoryPacks", [])
        if not (it.get("Path", "").startswith("Sordland") or "StoryPack_Main" in packs):
            continue
        texts += [s for s in json.dumps(it, ensure_ascii=False).split('"') if len(s) >= 40 and _KO.search(s)]
    texts.sort(key=len, reverse=True)
    return [s.replace("\\n", "\n") for s in texts[:n]]


def write_batch(batch_dir: Path, rows: list[dict], flags: dict[str, dict], context: str) -> None:
    batch_dir.mkdir(parents=True, exist_ok=True)
    merged = [{**r, **flags.get(r["key"], {"flags": [], "register": "other"})} for r in rows]
    write_jsonl(batch_dir / "input.jsonl", merged)
    (batch_dir / "context.md").write_text(context, encoding="utf-8")
    kind = "dialogue" if batch_dir.name.startswith("d-") else "textassets"
    (batch_dir / "status.json").write_text(
        json.dumps({"batch": batch_dir.name, "stage": "ready", "round": 0, "kind": kind}), encoding="utf-8")


def _context(bid: str, rows: list[dict], flags: dict[str, dict]) -> str:
    c = Counter(f for r in rows for f in flags.get(r["key"], {}).get("flags", []))
    lines = [f"# 배치 {bid}", "",
             "규칙 파일(반드시 먼저 읽을 것): prompts/register_table.md, prompts/glossary.md, prompts/checklist.md", "",
             f"줄 수: {len(rows)}, flag 분포: {dict(c.most_common())}", ""]
    if bid.startswith("d-"):
        lines.append("대화 목록: " + ", ".join(sorted({r["conv_title"] for r in rows})))
    else:
        files = Counter(r["file"] for r in rows)
        for file, _ in files.most_common():
            lines.append(f"파일: {file}. 목표 문체는 register_table.md 6장의 {file} 행을 따른다.")
        # 표본은 줄 수가 많은 파일부터 훑어 표본이 있는 첫 파일에서 뽑는다.
        samples = next((s for s in (sordland_samples(f) for f, _ in files.most_common()) if s), [])
        for i, s in enumerate(samples, 1):
            lines += ["", f"## 소르들란드 문체 표본 {i}", "", s]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    index = []
    for kind, grouper in (("dialogue", group_dialogue), ("textassets", group_textassets)):
        rows = read_jsonl(paths.CURRENT / f"{kind}.jsonl")
        flags = {f["key"]: f for f in read_jsonl(paths.FLAGS / f"{kind}.jsonl")}
        for bid, brows in grouper(rows):
            write_batch(paths.BATCHES / bid, brows, flags, _context(bid, brows, flags))
            flagged = sum(1 for r in brows if flags.get(r["key"], {}).get("flags"))
            index.append({"batch": bid, "kind": kind, "rows": len(brows), "flagged": flagged,
                          "priority": flagged / max(len(brows), 1)})
    index.sort(key=lambda x: -x["priority"])
    (paths.BATCHES / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"batches={len(index)}", file=sys.stderr)
