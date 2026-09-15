# 용어 후보마다 소르들란드(메인) 출현 횟수를 세어 표준 표기를 정한다. 창작은 하지 않는다.
import json, re, sys
from collections import Counter
from typing import Iterable
from scripts import paths
from scripts.build_corpus import fields, read_jsonl

CANDIDATES = paths.PROMPTS / "glossary_candidates.json"
GLOSSARY_JSON = paths.PROMPTS / "glossary.json"
GLOSSARY_MD = paths.PROMPTS / "glossary.md"


def count_terms(texts: Iterable[str], candidates: list[str], mask: Iterable[str] = ()) -> dict[str, int]:
    # 겹치는 표기(카란자 ⊂ 카란자스)는 긴 쪽에만 한 번 센다. mask는 다른 개념의 표기라 세지 않고 흡수만 한다.
    forms = sorted(set(candidates) | set(mask), key=len, reverse=True)
    pat = re.compile("|".join(re.escape(k) for k in forms))
    c = Counter({k: 0 for k in candidates})
    for t in texts:
        for m in pat.finditer(t):
            if m.group() in c:
                c[m.group()] += 1
    return dict(c)


def _replaceable(form: str) -> bool:
    return form.isascii() or sum(1 for ch in form if "가" <= ch <= "힣") >= 3


def decide(concept: dict, sord_counts: dict[str, int], rizia_counts: dict[str, int]) -> dict:
    base = {"concept": concept["concept"], "en": concept.get("en", ""), "standard": None, "banned": [],
            "source": "needs_human", "auto_replace": False,
            "evidence": {"sordland": sord_counts, "rizia": rizia_counts}}
    for name, counts, margin in (("sordland", sord_counts, 1.0), ("rizia_majority", rizia_counts, 1.2)):
        ranked = sorted(counts.items(), key=lambda kv: -kv[1])
        if not ranked or ranked[0][1] == 0:
            continue
        top, second = ranked[0][1], ranked[1][1] if len(ranked) > 1 else 0
        if top > second and top >= second * margin:
            banned = [k for k, _ in ranked[1:]]
            base.update(standard=ranked[0][0], banned=banned, source=name,
                        auto_replace=name == "sordland" and all(_replaceable(b) for b in banned))
        return base  # 동률·근소 차 → needs_human
    return base


def is_sordland_item(item: dict) -> bool:
    return item.get("Path", "").startswith("Sordland")


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
            if is_sordland_item(it):
                out.extend(_walk_strings(it))
    return out


def rizia_texts() -> list[str]:
    rows = read_jsonl(paths.CORPUS / "dialogue.jsonl") + read_jsonl(paths.CORPUS / "textassets.jsonl")
    return [r["ko"] for r in rows]


def load_glossary() -> list[dict]:
    return json.loads(GLOSSARY_JSON.read_text(encoding="utf-8"))


def _to_md(entries: list[dict]) -> str:
    lines = ["# 용어집 (자동 생성: build_glossary.py)", "",
             "원칙: 메인 캠페인 출현 표기만 표준. `needs_human`은 에이전트가 원문 그대로 두고 보고한다.",
             "`자동 치환 = 아니오`인 항목은 일괄 치환 금지(금지 표기가 일반 낱말과 겹칠 수 있다). 문맥을 보고 고치거나 보고만 한다.", "",
             "| 개념 | 영문 | 표준 | 금지 | 근거 | 자동 치환 | 소르들란드 출현 | Rizia 출현 |",
             "|---|---|---|---|---|---|---|---|"]
    for e in entries:
        lines.append(f"| {e['concept']} | {e['en']} | {e['standard'] or '(needs_human)'} | {', '.join(e['banned'])} | {e['source']} | "
                     f"{'예' if e['auto_replace'] else '아니오(보고만)'} | {e['evidence']['sordland']} | {e['evidence']['rizia']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    concepts = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    st, rt = sordland_texts(), rizia_texts()
    entries = [decide(c, count_terms(st, c["candidates"], c.get("mask", ())),
                      count_terms(rt, c["candidates"], c.get("mask", ()))) for c in concepts]
    GLOSSARY_JSON.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    GLOSSARY_MD.write_text(_to_md(entries), encoding="utf-8")
    n = sum(1 for e in entries if e["source"] == "needs_human")
    print(f"glossary entries={len(entries)} needs_human={n}", file=sys.stderr)
