import json
from pathlib import Path
from scripts.apply_edits import validate_edit, apply_edits
from scripts.build_corpus import write_jsonl, read_jsonl

ROW = {"key": "d:1:1", "en": '"Go {X} now.\n\nSecond."', "ko": '"가라 {X} 지금.\n\n둘째."', "actor": "Player_Romus", "conv_id": 1, "seq": 0, "conv_title": "Rizia/Turn 1/A", "menu_en": "", "menu_ko": ""}

def test_validate_edit_rules():
    assert validate_edit(ROW, '"가시오 {X} 지금.\n\n둘째요."') == []
    assert "empty" in validate_edit(ROW, "")[0]
    assert any("placeholder" in e for e in validate_edit(ROW, '"가시오 지금.\n\n둘째요."'))
    assert any("newline" in e for e in validate_edit(ROW, '"가시오 {X} 지금. 둘째요."'))
    assert any("length" in e for e in validate_edit(ROW, '"가시오 {X} 지금.\n\n둘째요." ' + "가" * 200))

def test_apply_edits_updates_current_and_writes_reviewed(tmp_path, monkeypatch):
    from scripts import paths
    monkeypatch.setattr(paths, "CURRENT", tmp_path / "current")
    write_jsonl(paths.CURRENT / "dialogue.jsonl", [ROW])
    b = tmp_path / "d-turn01-a"; b.mkdir()
    write_jsonl(b / "input.jsonl", [{**ROW, "flags": ["romus_mixed_register"], "speech": "none", "register": "haera"}])
    (b / "status.json").write_text(json.dumps({"batch": "d-turn01-a", "stage": "ready", "round": 0, "kind": "dialogue"}))
    write_jsonl(b / "edits.jsonl", [{"key": "d:1:1", "ko_new": '"가시오 {X} 지금.\n\n둘째요."', "reason": "하오체", "flags_resolved": ["romus_mixed_register"]},
                                    {"key": "d:9:9", "ko_new": "x", "reason": "", "flags_resolved": []}])
    r = apply_edits(b)
    assert r["applied"] == 1 and r["rejected"][0]["key"] == "d:9:9"
    assert read_jsonl(paths.CURRENT / "dialogue.jsonl")[0]["ko"] == '"가시오 {X} 지금.\n\n둘째요."'
    rv = read_jsonl(b / "reviewed.jsonl")[0]
    assert rv["edited"] is True and rv["ko_old"] == ROW["ko"] and rv["reason"] == "하오체"
    assert json.loads((b / "status.json").read_text())["round"] == 1
