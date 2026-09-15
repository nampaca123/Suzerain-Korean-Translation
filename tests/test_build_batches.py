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
