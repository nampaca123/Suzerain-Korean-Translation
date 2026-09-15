# data/current의 한글을 원본 패치 번들에 되써 넣어 dist/ 에 재패킹한다. 원본은 읽기만 한다.
import json, re, sys
from pathlib import Path
from typing import Callable
import UnityPy
from scripts import paths
from scripts.build_corpus import read_jsonl

_SEG = re.compile(r"/([^/\[]+)((?:\[\d+\])*)")


def patch_db_tree(tree: dict, rows: list[dict]) -> int:
    want = {(r["conv_id"], r["entry_id"]): r for r in rows}
    n = 0
    for c in tree["conversations"]:
        for e in c["dialogueEntries"]:
            r = want.get((c["id"], e["id"]))
            if not r:
                continue
            for f in e["fields"]:
                if f["title"] == "en" and f["value"] != r["ko"]:
                    f["value"] = r["ko"]; n += 1
                elif f["title"] == "Menu Text en" and r.get("menu_ko") and f["value"] != r["menu_ko"]:
                    f["value"] = r["menu_ko"]; n += 1
    return n


def _set_path(obj, field_path: str, value: str) -> bool:
    cur = obj
    segs = [(m.group(1), [int(i) for i in re.findall(r"\[(\d+)\]", m.group(2))]) for m in _SEG.finditer(field_path)]
    for i, (key, idxs) in enumerate(segs):
        last = i == len(segs) - 1
        if last and not idxs:
            if key not in cur: return False
            cur[key] = value; return True
        cur = cur[key]
        for j, ix in enumerate(idxs):
            if last and j == len(idxs) - 1:
                cur[ix] = value; return True
            cur = cur[ix]
    return False


def patch_textasset_json(text: str, rows: list[dict]) -> tuple[str, int]:
    # 일부 _GameFlow 항목은 대문자 Id가 없으므로(소문자 id) 건너뛴다.
    obj = json.loads(text); by_id = {it["Id"]: it for it in obj.get("items", []) if "Id" in it}
    n = sum(1 for r in rows if r["item_id"] in by_id and _set_path(by_id[r["item_id"]], r["field_path"], r["ko"]))
    return json.dumps(obj, ensure_ascii=False, indent=4), n


def repack(src_bundle: Path, out_bundle: Path, mutate: Callable) -> None:
    env = UnityPy.load(str(src_bundle)); mutate(env)
    out_bundle.parent.mkdir(parents=True, exist_ok=True)
    with open(out_bundle, "wb") as f:
        f.write(env.file.save(packer="lz4"))


def _mutate_db(rows):
    def m(env):
        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                tree = obj.read_typetree()
                if tree.get("m_Name") == "Suzerain":
                    print(f"db fields patched={patch_db_tree(tree, rows)}", file=sys.stderr); obj.save_typetree(tree)
    return m


def _mutate_text(rows):
    by_file = {}
    for r in rows: by_file.setdefault(r["file"], []).append(r)
    def m(env):
        total = 0
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                d = obj.read(); name = d.m_Name.replace(" ", "_")
                if name in by_file:
                    s = d.m_Script if isinstance(d.m_Script, str) else d.m_Script.decode("utf-8")
                    new, n = patch_textasset_json(s, by_file[name]); d.m_Script = new; d.save(); total += n
        print(f"textasset fields patched={total}", file=sys.stderr)
    return m


if __name__ == "__main__":
    repack(paths.PATCH_BUNDLE_DIR / paths.DB_BUNDLE_NAME, paths.DIST / paths.DB_BUNDLE_NAME, _mutate_db(read_jsonl(paths.CURRENT / "dialogue.jsonl")))
    repack(paths.PATCH_BUNDLE_DIR / paths.TEXT_BUNDLE_NAME, paths.DIST / paths.TEXT_BUNDLE_NAME, _mutate_text(read_jsonl(paths.CURRENT / "textassets.jsonl")))
