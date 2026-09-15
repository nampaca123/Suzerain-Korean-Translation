# Suzerain Rizia 캠페인 한글 패치 어투 교정

Rizia 캠페인 한글 패치(GPT 번역)의 화계·호칭·문체를 메인 캠페인 기준에 맞게 교정하는 파이프라인.
설계: document-base/superpower-docs/suzerain-ko-patch/2026-09-15-rizia-register-fix-design.md

## 실행 순서
1. `.venv\Scripts\python scripts/extract_bundles.py`
2. `.venv\Scripts\python scripts/build_corpus.py`
3. `.venv\Scripts\python scripts/build_glossary.py`
4. `.venv\Scripts\python scripts/preprocess_mechanical.py`
5. `.venv\Scripts\python scripts/flag_lines.py`
6. `.venv\Scripts\python scripts/build_batches.py`
7. 배치별로 교정·검수 에이전트 실행 → `apply_edits.py` → `check_batch.py`
8. `.venv\Scripts\python scripts/repack_bundles.py` → `make_patch_zip.py`

`data/`, `dist/`는 게임 원문을 포함하므로 저장소에 올리지 않는다.
