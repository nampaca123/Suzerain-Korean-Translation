import json, zipfile, pytest
from pathlib import Path
import UnityPy
from scripts import paths
from scripts.repack_bundles import patch_db_tree, patch_textasset_json, repack
from scripts.make_patch_zip import make_zip
from scripts.extract_bundles import load_db_tree, iter_textassets

def test_patch_db_tree_writes_en_and_menu():
    tree = {"conversations": [{"id": 288, "dialogueEntries": [{"id": 27, "fields": [{"title": "en", "value": "old"}, {"title": "Menu Text en", "value": "m"}]}]}]}
    n = patch_db_tree(tree, [{"key": "d:288:27", "conv_id": 288, "entry_id": 27, "ko": "new", "menu_ko": "m2"}])
    f = {x["title"]: x["value"] for x in tree["conversations"][0]["dialogueEntries"][0]["fields"]}
    assert n == 2 and f["en"] == "new" and f["Menu Text en"] == "m2"

def test_patch_textasset_json_follows_field_path():
    text = json.dumps({"items": [{"Id": "0x01", "R": {"Options": [{"Text": "a"}, {"Text": "b"}]}}]}, ensure_ascii=False, indent=4)
    out, n = patch_textasset_json(text, [{"key": "t:X:0x01:/R/Options[1]/Text", "item_id": "0x01", "field_path": "/R/Options[1]/Text", "ko": "나"}])
    assert n == 1 and json.loads(out)["items"][0]["R"]["Options"][1]["Text"] == "나"

need = pytest.mark.skipif(not (paths.PATCH_BUNDLE_DIR / paths.DB_BUNDLE_NAME).exists(), reason="bundles missing")

@need
def test_repack_roundtrip_one_line(tmp_path):
    src = paths.PATCH_BUNDLE_DIR / paths.DB_BUNDLE_NAME; out = tmp_path / src.name
    def mutate(env):
        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                tree = obj.read_typetree()
                patch_db_tree(tree, [{"key": "d:288:27", "conv_id": 288, "entry_id": 27, "ko": "【TEST】", "menu_ko": ""}])
                obj.save_typetree(tree)
    repack(src, out, mutate)
    tree = load_db_tree(out)
    conv = next(c for c in tree["conversations"] if c["id"] == 288)
    e = next(e for e in conv["dialogueEntries"] if e["id"] == 27)
    assert {f["title"]: f["value"] for f in e["fields"]}["en"] == "【TEST】"
    assert abs(out.stat().st_size - src.stat().st_size) < 5000

def test_make_zip_layout(tmp_path):
    root = tmp_path / "patch" / "Suzerain_Data"; dist = tmp_path / "dist"
    for rel in ("StreamingAssets/aa/StandaloneWindows64/a.bundle", "StreamingAssets/aa/StandaloneWindows64/" + paths.DB_BUNDLE_NAME,
                "StreamingAssets/aa/catalog.bin", "il2cpp_data/Metadata/global-metadata.dat"):
        p = root / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b"orig")
    dist.mkdir(); (dist / paths.DB_BUNDLE_NAME).write_bytes(b"new")
    names = make_zip(tmp_path / "patch", dist, tmp_path / "out.zip")
    with zipfile.ZipFile(tmp_path / "out.zip") as z:
        assert sorted(z.namelist()) == sorted(names) and len(names) == 4
        assert z.read("Suzerain_Data/StreamingAssets/aa/StandaloneWindows64/" + paths.DB_BUNDLE_NAME) == b"new"
        assert z.read("Suzerain_Data/StreamingAssets/aa/catalog.bin") == b"orig"
