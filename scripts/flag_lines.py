# spec 4장·5장·6장·10.2의 기계 검사 항목을 줄마다 flag로 붙인다. 탐지 전용이며 본문은 고치지 않는다.
import itertools, json, re, sys
from collections import Counter, defaultdict
from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl
from scripts.build_glossary import load_glossary
from scripts.register_classify import (classify, is_quoted, is_narrative,
                                       HAO, HAEYO, HAPSYO, HAERA, HAE, HAGE, OTHER)
from scripts.speech_detect import tag_speech

NARRATORS = {"Narrator", "Player_Romus_Italic"}
SUBJECTS = {"Lucita Azaro", "Elena Werner", "Laurento Esquibel", "Titus Gordion", "Sal Ignacius", "Taddeus Azaro",
            "Daria de Rava", "Pabel Adria", "Russello Montoro", "Adarfo Sotelato", "Manus Sazon", "Alma Saltana",
            "Carlos Robles Azaro", "Sevrio Castellanus", "Rico Toras", "Axel Reinhart", "Angelica Sazon", "Leona Sazon"}
FOREIGN = {"Patricio Alvarez (R)", "Wiktor Smolak (R)", "Emmerich Hegel (R)", "Anton Rayne (R)", "Dwight Walker (R)",
           "Jorga Azmal", "Leon Malenyev (R)", "Maartin Van Hoorten (R)", "Ephraim Nines (R)", "Petr Vectern (R)",
           "Deivid Wisci (R)", "Ewald Alphonso (R)", "Gus Manger (R)", "Marcel Koronti (R)"}
LOW = {HAGE, HAERA, HAE}
TA_TARGET = {"ReportData": {HAPSYO}, "JournalEntryData": {HAPSYO}, "DecreeData": {HAPSYO}, "SituationData": {HAPSYO},
             "CodexEntryData": {HAPSYO}, "StoryPackData": {HAPSYO}, "NewsData": {HAERA}}
_PLACEHOLDER = re.compile(r"\{[^}]+\}")
_NAMES = ("스몰라크", "살타나", "알바레즈", "헤겔", "라이네", "휴고", "비나", "루시타", "마누스", "티투스", "금광")
_JOSA = re.compile("(" + "|".join(_NAMES) + r")(은|는|이|가|을|를|과|와)(?![가-힣])")
_HANGUL = re.compile(r"[가-힣]")
_SENTENCE = re.compile(r"(?<=[.?!])\s+")
_EFFECT_TAG = re.compile(r"\[[^\]가-힣]*[A-Za-z]{3,}[^\]가-힣]*\]")
_TA_SKIP_FIELD = re.compile(r"(Title|Keywords|Name|Label|Header|Author)")
_SENTENCE_END = re.compile(r"[.?!]")
MIN_CLAUSE_SYLLABLES = 5


def _long_clauses(ko: str) -> list[str]:
    # R23: "그렇군." 같은 짧은 독립 감탄절은 화계 혼용 판정에서 뺀다(하오체와 섞여도 자연스럽다).
    body = " ".join(l for l in ko.split("\n") if l.strip())
    return [p for p in _SENTENCE.split(body) if len(_HANGUL.findall(p)) >= MIN_CLAUSE_SYLLABLES]


def josa_ok(word: str, josa: str) -> bool:
    code = ord(word[-1]) - 0xAC00
    has_final = 0 <= code < 11172 and code % 28 != 0
    return josa in ({"은", "이", "을", "과"} if has_final else {"는", "가", "를", "와"})


def _common_flags(ko: str, en: str, glossary: list[dict]) -> list[str]:
    f = []
    if re.search(r"--|—|–", ko): f.append("dash_remaining")
    if re.search(r"[“”‘’]", ko): f.append("curly_quote")
    if _EFFECT_TAG.search(ko): f.append("english_effect_tag")
    if any(b in ko for g in glossary for b in g.get("banned", []) if g.get("standard")): f.append("glossary_violation")
    return f


def _register_flags(r: dict, reg: str, speech: str) -> list[str]:
    a, ko, f = r["actor"], r["ko"], []
    if a in NARRATORS:
        if not is_quoted(ko) and not is_narrative(ko) and reg != OTHER: f.append("narration_not_declarative")
        return f
    if is_quoted(ko) and is_narrative(ko.strip('"')) and reg == HAERA and re.search(r"(였|았|었|ㄴ|는|이)다[.!]?\"?$", ko.strip()):
        f.append("dialogue_declarative_ending")
    if "폐하" in ko and reg in LOW: f.append("royal_title_low_register")
    if a == "Player_Romus":
        cr = [c for c in (classify(p) for p in _long_clauses(ko)) if c != OTHER]
        if HAO in cr and (set(cr) & LOW): f.append("romus_mixed_register")
        if reg == HAPSYO and speech != "speech": f.append("romus_hapsyo_not_speech")
        if speech == "speech" and reg not in (HAPSYO, OTHER): f.append("speech_not_hapsyo")
        if reg == HAEYO: f.append("romus_haeyo")
    elif a in SUBJECTS and reg not in (HAPSYO, OTHER): f.append("subject_not_hapsyo")
    elif a == "Vina Toras" and reg not in (HAEYO, OTHER): f.append("vina_not_haeyo")
    elif a in FOREIGN and reg not in (HAPSYO, OTHER): f.append("foreign_not_hapsyo")
    elif a == "Hugo Toras" and reg in LOW: f.append("hugo_low_register")
    if "당신" in ko and a not in {"Lucita Azaro", "Estela Toras", "Beatrice Livingston (R)"}:
        f.append("pronoun_dangsin")
    return f


def flag_dialogue(rows: list[dict], glossary: list[dict]) -> dict[str, dict]:
    out, by_en = {}, defaultdict(list)
    for _, grp in itertools.groupby(sorted(rows, key=lambda r: (r["conv_id"], r["seq"])), key=lambda r: r["conv_id"]):
        g = list(grp); speech = tag_speech(g)
        for r in g:
            reg = classify(r["ko"]); f = _common_flags(r["ko"], r["en"], glossary) + _register_flags(r, reg, speech[r["key"]])
            if r["en"].strip().startswith('"') and not is_quoted(r["ko"]): f.append("quote_missing")
            if r.get("menu_ko") and r.get("menu_en", "").strip() == r["en"].strip() and r["menu_ko"].strip() != r["ko"].strip():
                f.append("menu_mismatch")
            if any(not josa_ok(m.group(1), m.group(2)) for m in _JOSA.finditer(r["ko"])): f.append("josa_mismatch")
            out[r["key"]] = {"flags": f, "speech": speech[r["key"]], "register": reg}
            if r["en"].strip(): by_en[(r["actor"], r["en"].strip())].append(r["key"])
    for keys in by_en.values():
        if len({out[k]["register"] for k in keys} - {OTHER}) > 1:
            for k in keys: out[k]["flags"].append("same_en_diff_register")
    return out


def flag_textassets(rows: list[dict], glossary: list[dict]) -> dict[str, dict]:
    out, by_base = {}, defaultdict(list)
    for r in rows:
        reg = classify(r["ko"]); target = TA_TARGET.get(r["file"])
        f = _common_flags(r["ko"], r["en"], glossary)
        if r["file"] == "DecisionData":
            target = {HAERA} if "Options" in r["field_path"] else {HAPSYO}
        if sorted(_PLACEHOLDER.findall(r["ko"])) != sorted(_PLACEHOLDER.findall(r["en"])): f.append("placeholder_mismatch")
        leaf = r["field_path"].rsplit("/", 1)[-1]
        gradable = not _TA_SKIP_FIELD.search(leaf) and _SENTENCE_END.search(r["ko"])
        if target and gradable and reg not in target and reg != OTHER: f.append("ta_register_mismatch")
        # 한국어는 영문보다 글자 수가 늘 짧아(길이비 중앙값 0.44) 길이비는 신호가 못 된다. 문단 구분 손실만 센다.
        if r["en"].count("\n") > r["ko"].count("\n"): f.append("missing_paragraph")
        out[r["key"]] = {"flags": f, "register": reg, "target": sorted(target) if target else []}
        if r["file"] == "CodexEntryData":
            # R24: 이름 끝을 떼고도 밑줄이 2개 이상 남을 때만 같은 항목의 변형판이다(형제 항목끼리 묶이지 않게).
            base = r["item_name"].rsplit("_", 1)[0]
            by_base[base if base.count("_") >= 2 else r["item_name"]].append(r["key"])
    for keys in by_base.values():
        if len({out[k]["register"] for k in keys} - {OTHER}) > 1:
            for k in keys:
                if out[k]["register"] != OTHER: out[k]["flags"].append("codex_variant_mismatch")
    return out


if __name__ == "__main__":
    g = load_glossary()
    d = flag_dialogue(read_jsonl(paths.CURRENT / "dialogue.jsonl"), g)
    t = flag_textassets(read_jsonl(paths.CURRENT / "textassets.jsonl"), g)
    write_jsonl(paths.FLAGS / "dialogue.jsonl", [{"key": k, **v} for k, v in d.items()])
    write_jsonl(paths.FLAGS / "textassets.jsonl", [{"key": k, **v} for k, v in t.items()])
    for name, res in (("dialogue", d), ("textassets", t)):
        c = Counter(f for v in res.values() for f in v["flags"])
        n = sum(1 for v in res.values() if v["flags"])
        print(f"{name} rows={len(res)} flagged={n} " + json.dumps(c.most_common(), ensure_ascii=False), file=sys.stderr)
