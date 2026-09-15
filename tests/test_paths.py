# scripts.paths 상수가 존재하고 원본 폴더가 읽기 전용 용도로만 참조되는지 확인
from pathlib import Path
from scripts import paths

def test_constants_exist():
    for name in ("ROOT","PATCH_BUNDLE_DIR","STEAM_BUNDLE_DIR","DB_BUNDLE_NAME","TEXT_BUNDLE_NAME",
                 "DATA","RAW_KO","RAW_EN","CORPUS","CURRENT","FLAGS","LOGS","BATCHES","PROMPTS","DIST"):
        assert isinstance(getattr(paths, name), (Path, str)), name

def test_data_dirs_under_root():
    for p in (paths.DATA, paths.RAW_KO, paths.RAW_EN, paths.CORPUS, paths.CURRENT, paths.FLAGS, paths.LOGS, paths.DIST):
        assert paths.ROOT in p.parents, p

def test_bundle_names():
    assert paths.DB_BUNDLE_NAME.startswith("database_assets_all_")
    assert paths.TEXT_BUNDLE_NAME.startswith("defaultlocalgroup_assets_assets_database_entitytextassets")
