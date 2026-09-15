# 파이프라인 전체가 쓰는 경로 상수. 원본 폴더(패치·스팀)는 읽기 전용이다.
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATCH_BUNDLE_DIR = Path(r"C:/Users/a/Downloads/Suzerain_Data/StreamingAssets/aa/StandaloneWindows64")
STEAM_BUNDLE_DIR = Path(r"C:/Program Files/Steam/steamapps/common/Suzerain/Suzerain_Data/StreamingAssets/aa/StandaloneWindows64")
DB_BUNDLE_NAME = "database_assets_all_2c5c6df453acd4d096b216389ddafa9b.bundle"
TEXT_BUNDLE_NAME = "defaultlocalgroup_assets_assets_database_entitytextassets.asset_ec95223fa5819b4eb4d612c0ee4914b6.bundle"

DATA = ROOT / "data"
RAW_KO = DATA / "raw" / "ko"
RAW_EN = DATA / "raw" / "en"
CORPUS = DATA / "corpus"
CURRENT = DATA / "current"
FLAGS = DATA / "flags"
LOGS = DATA / "logs"
DIST = ROOT / "dist"
BATCHES = ROOT / "batches"
PROMPTS = ROOT / "prompts"
