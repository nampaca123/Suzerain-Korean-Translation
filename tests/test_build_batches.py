import json
from scripts.build_batches import group_dialogue, group_textassets, write_batch

def D(conv_id, seq, title):
    return {"key": f"d:{conv_id}:{seq}", "conv_id": conv_id, "seq": seq, "conv_title": title, "actor": "Narrator", "en": "x", "ko": "y.", "menu_en": "", "menu_ko": ""}

def test_group_dialogue_keeps_conversations_whole_and_splits_by_size():
    rows = [D(1, i, "Rizia/Turn 1/A") for i in range(3)] + [D(2, i, "Rizia/Turn 1/B") for i in range(3)] + [D(3, 0, "Rizia/Prologue")]
    g = group_dialogue(rows, max_rows=4)
    assert [(bid, len(r)) for bid, r in g] == [("d-turn01-a", 3), ("d-turn01-b", 3), ("d-misc-a", 1)]
    assert {r["conv_id"] for r in g[0][1]} == {1}

def test_group_textassets_by_file_and_chars():
    rows = [{"key": f"t:ReportData:{i}:/D", "file": "ReportData", "item_id": str(i), "ko": "가" * 30, "en": "x"} for i in range(5)]
    rows += [{"key": "t:NewsData:9:/D", "file": "NewsData", "item_id": "9", "ko": "나", "en": "x"}]
    g = group_textassets(rows, max_chars=70)
    assert [(bid, len(r)) for bid, r in g] == [("t-NewsData-01", 1), ("t-ReportData-01", 2), ("t-ReportData-02", 2), ("t-ReportData-03", 1)]

def test_write_batch_merges_flags(tmp_path):
    rows = [D(1, 0, "Rizia/Turn 1/A")]
    write_batch(tmp_path / "d-turn01-a", rows, {"d:1:0": {"flags": ["quote_missing"], "speech": "none", "register": "haera"}}, "ctx")
    line = json.loads((tmp_path / "d-turn01-a" / "input.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert line["flags"] == ["quote_missing"] and line["speech"] == "none"
    assert json.loads((tmp_path / "d-turn01-a" / "status.json").read_text())["stage"] == "ready"
    assert (tmp_path / "d-turn01-a" / "context.md").read_text(encoding="utf-8") == "ctx"


def T(file, item_id, chars):
    return {"key": f"t:{file}:{item_id}:/D", "file": file, "item_id": item_id, "ko": "가" * chars, "en": "x"}

def test_group_textassets_pools_tiny_files_into_misc():
    rows = [T(f, "0", 100) for f in ("Alpha", "Beta", "Gamma")] + [T("Big", "0", 6000)]
    g = group_textassets(rows)
    assert [(bid, len(r)) for bid, r in g] == [("t-Big-01", 1), ("t-misc-01", 3)]
    assert {r["file"] for r in g[1][1]} == {"Alpha", "Beta", "Gamma"}

def test_group_textassets_misc_pool_splits_by_chars_without_breaking_items():
    rows = [T("Alpha", "0", 100), T("Alpha", "0", 100), T("Beta", "0", 100), T("Gamma", "0", 100)]
    g = group_textassets(rows, max_chars=250, min_file_chars=240)
    assert [(bid, len(r)) for bid, r in g] == [("t-misc-01", 2), ("t-misc-02", 2)]
    assert {r["file"] for r in g[0][1]} == {"Alpha"}

def test_misc_context_lists_every_file():
    from scripts.build_batches import _context
    rows = [T("Alpha", "0", 100), T("Alpha", "1", 100), T("Beta", "0", 100)]
    md = _context("t-misc-01", rows, {})
    assert "파일: Alpha. 목표 문체는 register_table.md 6장의 Alpha 행을 따른다." in md
    assert "파일: Beta. 목표 문체는 register_table.md 6장의 Beta 행을 따른다." in md


def _write_raw(tmp_path, monkeypatch, items):
    from scripts import paths
    (tmp_path / "textassets").mkdir()
    (tmp_path / "textassets" / "Fake.json").write_text(json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(paths, "RAW_KO", tmp_path)

def test_sordland_samples_returns_longest_first(tmp_path, monkeypatch):
    from scripts.build_batches import sordland_samples
    _write_raw(tmp_path, monkeypatch, [{"Path": f"Sordland/{i}", "Body": "가" * n} for i, n in enumerate((90, 300, 150, 60))])
    assert [len(s) for s in sordland_samples("Fake")] == [300, 150, 90]

def test_sordland_samples_skips_rizia_items_and_missing_file(tmp_path, monkeypatch):
    from scripts.build_batches import sordland_samples
    _write_raw(tmp_path, monkeypatch, [{"Path": "Rizia/0", "Body": "가" * 300}, {"Path": "Sordland/1", "Body": "나" * 120}])
    assert [len(s) for s in sordland_samples("Fake")] == [120]
    assert sordland_samples("Absent") == []
