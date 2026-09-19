# 패치(한글)·스팀(영어) 번들에서 대화 DB typetree와 TextAsset JSON을 추출한다.
import json, sys
from pathlib import Path
from typing import Iterator
import UnityPy
from scripts import paths


def _script_text(asset) -> str:
    s = asset.m_Script
    return s if isinstance(s, str) else s.decode("utf-8")


def load_db_tree(bundle_path: Path) -> dict:
    env = UnityPy.load(str(bundle_path))
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            tree = obj.read_typetree()
            if tree.get("m_Name") == "Suzerain":
                return tree
    raise RuntimeError(f"Suzerain MonoBehaviour not found in {bundle_path}")


def iter_textassets(bundle_path: Path) -> Iterator[tuple[str, str]]:
    env = UnityPy.load(str(bundle_path))
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            d = obj.read()
            yield d.m_Name, _script_text(d)


def _extract_one(bundle_dir: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    (out / "textassets").mkdir(exist_ok=True)
    tree = load_db_tree(bundle_dir / paths.DB_BUNDLE_NAME)
    (out / "db.json").write_text(json.dumps(tree, ensure_ascii=False), encoding="utf-8")
    n = 0
    for name, text in iter_textassets(bundle_dir / paths.TEXT_BUNDLE_NAME):
        (out / "textassets" / (name.replace(" ", "_") + ".json")).write_text(text, encoding="utf-8")
        n += 1
    return {"db": out / "db.json", "textassets": n}


def extract_all(patch_dir: Path, steam_dir: Path, out_ko: Path, out_en: Path) -> dict:
    result = {"ko": _extract_one(patch_dir, out_ko), "en": _extract_one(steam_dir, out_en)}
    print(f"extracted ko={result['ko']['textassets']} en={result['en']['textassets']} textassets", file=sys.stderr)
    return result


if __name__ == "__main__":
    extract_all(paths.PATCH_BUNDLE_DIR, paths.STEAM_BUNDLE_DIR, paths.RAW_KO, paths.RAW_EN)
