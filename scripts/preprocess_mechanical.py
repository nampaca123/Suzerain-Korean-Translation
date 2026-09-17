# 결정적 규칙만 적용하는 전처리(따옴표·곡선따옴표·대시·효과 표기·용어). 화계·어미는 건드리지 않는다.
# data/current/*.jsonl을 제자리에서 고치므로, 재실행 전에는 build_corpus로 data/current를 다시 만들어야 한다.
import json, re, sys
from functools import lru_cache
from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl
from scripts.build_glossary import load_glossary

EFFECT_LABELS = {"Authority": "권위", "Budget": "예산", "Energy": "에너지", "Military Equipment": "군수 장비",
                 "Military Personnel": "군사 인력", "Tanks": "전차", "Support Vehicles": "지원 차량",
                 "Bombers": "폭격기", "Fighters": "전투기", "Warships": "군함", "Submarines": "잠수함",
                 "Equipment": "군수 장비", "Manpower": "군사 인력", "Military Manpower": "군사 인력",
                 "Trucks": "지원 차량", "Military Ships": "군함",
                 "군사 장비": "군수 장비", "장비": "군수 장비", "인력": "군사 인력", "병력": "군사 인력", "함선": "군함"}
_LABEL_RX = "|".join(sorted(map(re.escape, EFFECT_LABELS), key=len, reverse=True))
_EFFECT_ITEM = re.compile(rf"([+-]?\d+)\s+({_LABEL_RX})(?![가-힣A-Za-z])(\s+Per Turn)?")
_TAIL_TAG = re.compile(r"(\s*\[[^\]]*\])+\s*$")


def fix_quotes(en: str, ko: str) -> str:
    e, k = en.strip(), ko.strip()
    if not (e.startswith('"') and e.endswith('"')) or k.startswith(('"', '“')):
        return ko
    m = _TAIL_TAG.search(k)
    body, tag = (k[:m.start()].rstrip(), k[m.start():]) if m else (k, "")
    return f'"{body}"{tag}'


def normalize_curly(ko: str) -> str:
    return ko.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")


def fix_dashes(ko: str) -> tuple[str, bool]:
    k = re.sub(r'--(?=\s*["\']?\s*$)', "...", ko)
    k = re.sub(r'--(?=")', "...", k)
    k = re.sub(r"\s+--\s+", ", ", k)
    return k, bool(re.search(r"--|—|–", k))


_KO_LABEL_FIRST = re.compile(rf"(?<![가-힣])(?<!군수 )(?<!군사 )({_LABEL_RX})(?=\s*[+-]?\d)")  # '[병력 -250]'처럼 라벨이 앞에 오는 꼴


def _translate_tag(m: re.Match) -> str:
    def item(im: re.Match) -> str:
        num, label, per = im.group(1), EFFECT_LABELS[im.group(2)], im.group(3)
        return f"턴당 {num} {label}" if per else f"{num} {label}"
    body = _EFFECT_ITEM.sub(item, m.group(1))
    return "[" + _KO_LABEL_FIRST.sub(lambda lm: EFFECT_LABELS[lm.group(1)], body) + "]"


def fix_effect_tags(ko: str) -> str:
    return re.sub(r"\[([^\]]*)\]", _translate_tag, ko)


_PROTECTED = ("페일스트림",)  # PaleStream: Pales와 무관한 고유명사라 금지 표기 '페일스'를 품고 있다.


@lru_cache(maxsize=None)
def _banned_rx(form: str) -> re.Pattern:
    # 라틴 금지 표기는 앞뒤 라틴 문자·숫자만 경계로 삼는다(ANALYSIS 속 AN은 제외, 'AN에'는 치환).
    esc = re.escape(form)
    return re.compile(rf"(?<![A-Za-z0-9]){esc}(?![A-Za-z0-9])" if form.isascii() else esc)


def apply_glossary(ko: str, glossary: list[dict]) -> tuple[str, list[str]]:
    applied, kept = [], [p for p in _PROTECTED if p in ko]
    for i, p in enumerate(kept):
        ko = ko.replace(p, f"\x00{i}\x00")
    for g in glossary:
        if not g.get("auto_replace") or not g.get("standard"):
            continue
        for b in g.get("banned", []):
            if not b:
                continue
            new = _banned_rx(b).sub(lambda _m, s=g["standard"]: s, ko)
            if new != ko:
                ko = new
                applied.append(g["concept"])
    for i, p in enumerate(kept):
        ko = ko.replace(f"\x00{i}\x00", p)
    return ko, sorted(set(applied))


def _apply_rules(en: str, ko: str, glossary: list[dict]) -> tuple[str, list[dict]]:
    log = []
    for rule, fn in (("curly", normalize_curly), ("quote", lambda k: fix_quotes(en, k)),
                     ("dash", lambda k: fix_dashes(k)[0]), ("effect_tag", fix_effect_tags),
                     ("glossary", lambda k: apply_glossary(k, glossary)[0])):
        new = fn(ko)
        if new != ko:
            log.append({"rule": rule, "before": ko, "after": new}); ko = new
    return ko, log


def preprocess_row(row: dict, glossary: list[dict]) -> tuple[str, list[dict]]:
    return _apply_rules(row.get("en", ""), row["ko"], glossary)


def preprocess_menu(row: dict, glossary: list[dict]) -> tuple[str, list[dict]]:
    return _apply_rules(row.get("menu_en", ""), row.get("menu_ko", ""), glossary)


if __name__ == "__main__":
    glossary = load_glossary()
    paths.LOGS.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(paths.LOGS / "preprocess.jsonl", "w", encoding="utf-8") as logf:
        for name in ("dialogue", "textassets"):
            rows = read_jsonl(paths.CURRENT / f"{name}.jsonl")
            for r in rows:
                new, log = preprocess_row(r, glossary)
                menu_new, menu_log = preprocess_menu(r, glossary) if r.get("menu_ko") else ("", [])
                for key, entries in ((r["key"], log), (r["key"] + "#menu", menu_log)):
                    for l in entries:
                        logf.write(json.dumps({"key": key, **l}, ensure_ascii=False) + "\n")
                if log:
                    r["ko"] = new
                if menu_log:
                    r["menu_ko"] = menu_new
                total += bool(log or menu_log)
            write_jsonl(paths.CURRENT / f"{name}.jsonl", rows)
    print(f"preprocessed rows changed={total}", file=sys.stderr)
