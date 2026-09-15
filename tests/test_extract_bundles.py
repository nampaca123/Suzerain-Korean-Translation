# 실제 번들이 있을 때만 도는 통합 테스트. 없으면 skip.
import json, pytest
from scripts import paths
from scripts.extract_bundles import load_db_tree, iter_textassets, extract_all

need = pytest.mark.skipif(not (paths.PATCH_BUNDLE_DIR / paths.DB_BUNDLE_NAME).exists(), reason="patch bundles missing")

@need
def test_load_db_tree_has_conversations():
    tree = load_db_tree(paths.PATCH_BUNDLE_DIR / paths.DB_BUNDLE_NAME)
    assert tree["m_Name"] == "Suzerain"
    assert len(tree["conversations"]) == 521

@need
def test_iter_textassets_yields_73():
    names = [n for n, _ in iter_textassets(paths.PATCH_BUNDLE_DIR / paths.TEXT_BUNDLE_NAME)]
    assert len(names) == 73 and "StoryPackData" in names

@need
def test_extract_all_writes_files(tmp_path):
    r = extract_all(paths.PATCH_BUNDLE_DIR, paths.STEAM_BUNDLE_DIR, tmp_path / "ko", tmp_path / "en")
    assert (tmp_path / "ko" / "db.json").exists() and (tmp_path / "en" / "db.json").exists()
    assert r["ko"]["textassets"] == 73 and r["en"]["textassets"] == 73
    sp = json.loads((tmp_path / "ko" / "textassets" / "StoryPackData.json").read_text(encoding="utf-8"))
    assert sp["items"][1]["NameInDatabase"] == "StoryPack_Rizia"
