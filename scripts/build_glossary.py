# 용어 후보마다 소르들란드(메인) 출현 횟수를 세어 표준 표기를 정한다. 창작은 하지 않는다.
import json, sys
from collections import Counter
from typing import Iterable
from scripts import paths
from scripts.build_corpus import fields, read_jsonl

CANDIDATES = paths.PROMPTS / "glossary_candidates.json"
GLOSSARY_JSON = paths.PROMPTS / "glossary.json"
GLOSSARY_MD = paths.PROMPTS / "glossary.md"


def count_terms(texts: Iterable[str], candidates: list[str]) -> dict[str, int]:
    c = Counter({k: 0 for k in candidates})
    for t in texts:
        for k in candidates:
            c[k] += t.count(k)
    return dict(c)


def decide(concept: dict, sord_counts: dict[str, int], rizia_counts: dict[str, int]) -> dict:
    base = {"concept": concept["concept"], "en": concept.get("en", ""), "standard": None, "banned": [],
            "source": "needs_human", "evidence": {"sordland": sord_counts, "rizia": rizia_counts}}
    for name, counts in (("sordland", sord_counts), ("rizia_majority", rizia_counts)):
        ranked = sorted(counts.items(), key=lambda kv: -kv[1])
        if ranked and ranked[0][1] > 0 and (len(ranked) == 1 or ranked[0][1] > ranked[1][1]):
            base.update(standard=ranked[0][0], banned=[k for k, _ in ranked[1:]], source=name)
            return base
        if ranked and ranked[0][1] > 0:
            return base  # 동률 → needs_human
    return base


def _walk_strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _walk_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk_strings(v)
    elif isinstance(o, str):
        yield o


def sordland_texts() -> list[str]:
    db = json.loads((paths.RAW_KO / "db.json").read_text(encoding="utf-8"))
    out = [f.get("en", "") for c in db["conversations"] if fields(c).get("Title", "").startswith("Sordland")
           for e in c["dialogueEntries"] for f in [fields(e)] if f.get("en")]
    for p in (paths.RAW_KO / "textassets").glob("*.json"):
        try:
            items = json.loads(p.read_text(encoding="utf-8")).get("items", [])
        except (json.JSONDecodeError, AttributeError):
            continue
        for it in items:
            packs = it.get("AppBundleProperties", {}).get("StoryPacks", [])
            if it.get("Path", "").startswith("Sordland") or "StoryPack_Main" in packs:
                out.extend(_walk_strings(it))
    return out


def rizia_texts() -> list[str]:
    rows = read_jsonl(paths.CORPUS / "dialogue.jsonl") + read_jsonl(paths.CORPUS / "textassets.jsonl")
    return [r["ko"] for r in rows]


def load_glossary() -> list[dict]:
    return json.loads(GLOSSARY_JSON.read_text(encoding="utf-8"))


def _to_md(entries: list[dict]) -> str:
    lines = ["# 용어집 (자동 생성: build_glossary.py)", "", "원칙: 메인 캠페인 출현 표기만 표준. `needs_human`은 에이전트가 원문 그대로 두고 보고한다.", "",
             "| 개념 | 영문 | 표준 | 금지 | 근거 | 소르들란드 출현 | Rizia 출현 |", "|---|---|---|---|---|---|---|"]
    for e in entries:
        lines.append(f"| {e['concept']} | {e['en']} | {e['standard'] or '(needs_human)'} | {', '.join(e['banned'])} | {e['source']} | "
                     f"{e['evidence']['sordland']} | {e['evidence']['rizia']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    concepts = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    st, rt = sordland_texts(), rizia_texts()
    entries = [decide(c, count_terms(st, c["candidates"]), count_terms(rt, c["candidates"])) for c in concepts]
    GLOSSARY_JSON.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    GLOSSARY_MD.write_text(_to_md(entries), encoding="utf-8")
    n = sum(1 for e in entries if e["source"] == "needs_human")
    print(f"glossary entries={len(entries)} needs_human={n}", file=sys.stderr)
