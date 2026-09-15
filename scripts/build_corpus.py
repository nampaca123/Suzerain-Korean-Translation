# 한글(패치)·영어(스팀) 추출본을 줄 단위로 정렬해 말뭉치 jsonl을 만든다. Rizia 항목과 지정 공용 코덱스만 포함.
import json
import re
import sys
from pathlib import Path

from scripts import paths

KO = re.compile(r"[가-힣]")
SKIP_FIELD = re.compile(r"(Tags|IsEnabledVariable|Newspaper|Image|Variable|^Id|^Path|NameInDatabase|StoryPacks|Notes)$")
INDEX = re.compile(r"\[\d+\]$")
SHARED_CODEX = {"Locations_Countries_Soradis", "Locations_Countries_Vendonesam", "Locations_Countries_Markanissa",
                "History_Misc_FortifyingPerlasFutureSpeech", "Organisations_MiscOrganisations_DEZA"}


def fields(o: dict) -> dict:
    return {f["title"]: f["value"] for f in o["fields"]}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def build_dialogue(ko_tree: dict, en_tree: dict) -> list[dict]:
    actors = {int(a["id"]): fields(a).get("Name", "?") for a in ko_tree["actors"]}
    en_map = {(c["id"], e["id"]): fields(e) for c in en_tree["conversations"] for e in c["dialogueEntries"]}
    rows = []
    for c in ko_tree["conversations"]:
        title = fields(c).get("Title", "")
        if not title.startswith("Rizia"):
            continue
        seq = 0
        for e in c["dialogueEntries"]:
            kf = fields(e)
            ef = en_map.get((c["id"], e["id"]), {})
            ko, en = kf.get("en", "") or "", ef.get("en", "") or ""
            if not ko.strip() and not en.strip():
                continue
            aid = int(kf.get("Actor") or 0)
            rows.append({"key": f"d:{c['id']}:{e['id']}", "conv_id": c["id"], "conv_title": title, "entry_id": e["id"],
                         "seq": seq, "actor_id": aid, "actor": actors.get(aid, "?"), "en": en, "ko": ko,
                         "menu_en": ef.get("Menu Text en", "") or "", "menu_ko": kf.get("Menu Text en", "") or ""})
            seq += 1
    return rows


def _is_rizia(item: dict) -> bool:
    packs = item.get("AppBundleProperties", {}).get("StoryPacks", [])
    return item.get("Path", "").startswith("Rizia") or "StoryPack_Rizia" in packs


def _walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _walk(v, f"{path}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def build_textassets(ko_dir: Path, en_dir: Path, shared_names: set[str]) -> list[dict]:
    rows = []
    for p in sorted(ko_dir.glob("*.json")):
        try:
            ko_items = json.loads(p.read_text(encoding="utf-8")).get("items", [])
        except (json.JSONDecodeError, AttributeError):
            continue
        en_path = en_dir / p.name
        en_items = json.loads(en_path.read_text(encoding="utf-8")).get("items", []) if en_path.exists() else []
        en_by_id = {it["Id"]: dict(_walk(it)) for it in en_items if "Id" in it}
        for it in ko_items:
            if "Id" not in it or not (_is_rizia(it) or it.get("NameInDatabase") in shared_names):
                continue
            en_fields = en_by_id.get(it["Id"], {})
            for fp, s in _walk(it):
                # 리프 이름의 배열 첨자를 떼고 메타 필드를 거른 뒤, 한글이 있거나 미번역 영문 산문(영어 원문과 동일 + 공백 포함)만 남긴다.
                leaf = INDEX.sub("", fp.split("/")[-1])
                if len(s) < 2 or SKIP_FIELD.search(leaf):
                    continue
                en = en_fields.get(fp, "")
                if not KO.search(s) and not (s == en and " " in s):
                    continue
                rows.append({"key": f"t:{p.stem}:{it['Id']}:{fp}", "file": p.stem, "item_id": it["Id"],
                             "item_name": it.get("NameInDatabase", ""), "path": it.get("Path", ""),
                             "field_path": fp, "en": en, "ko": s})
    return rows


if __name__ == "__main__":
    ko = json.loads((paths.RAW_KO / "db.json").read_text(encoding="utf-8"))
    en = json.loads((paths.RAW_EN / "db.json").read_text(encoding="utf-8"))
    d = build_dialogue(ko, en)
    t = build_textassets(paths.RAW_KO / "textassets", paths.RAW_EN / "textassets", SHARED_CODEX)
    for name, rows in (("dialogue", d), ("textassets", t)):
        write_jsonl(paths.CORPUS / f"{name}.jsonl", rows)
        write_jsonl(paths.CURRENT / f"{name}.jsonl", rows)
    print(f"dialogue rows={len(d)} textassets rows={len(t)}", file=sys.stderr)
