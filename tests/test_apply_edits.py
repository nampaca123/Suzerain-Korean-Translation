import json
from pathlib import Path
from scripts import paths
from scripts.apply_edits import validate_edit, apply_edits
from scripts.build_corpus import write_jsonl, read_jsonl

ROW = {"key": "d:1:1", "en": '"Go {X} now.\n\nSecond."', "ko": '"가라 {X} 지금.\n\n둘째."', "actor": "Player_Romus", "conv_id": 1, "seq": 0, "conv_title": "Rizia/Turn 1/A", "menu_en": "", "menu_ko": ""}
KO_NEW = '"가시오 {X} 지금.\n\n둘째요."'

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

def test_apply_menu_edit(tmp_path, monkeypatch):
    from scripts import paths
    monkeypatch.setattr(paths, "CURRENT", tmp_path / "current")
    row = {**ROW, "menu_en": ROW["en"], "menu_ko": '"가라 {X} 지금.\n\n둘째."'}
    write_jsonl(paths.CURRENT / "dialogue.jsonl", [row])
    b = tmp_path / "d-turn01-a"; b.mkdir()
    write_jsonl(b / "input.jsonl", [{**row, "flags": [], "speech": "none", "register": "haera"}])
    (b / "status.json").write_text(json.dumps({"batch": "d-turn01-a", "stage": "ready", "round": 0, "kind": "dialogue"}))
    write_jsonl(b / "edits.jsonl", [{"key": "d:1:1#menu", "ko_new": '"가시오 {X} 지금.\n\n둘째요."', "reason": "", "flags_resolved": []}])
    assert apply_edits(b)["applied"] == 1
    assert read_jsonl(paths.CURRENT / "dialogue.jsonl")[0]["menu_ko"] == '"가시오 {X} 지금.\n\n둘째요."'

def _mk(tmp_path, monkeypatch, current, edits, row=ROW, **status_extra):
    monkeypatch.setattr(paths, "CURRENT", tmp_path / "current")
    write_jsonl(paths.CURRENT / "dialogue.jsonl", current)
    b = tmp_path / "d-turn01-a"; b.mkdir()
    write_jsonl(b / "input.jsonl", [{**row, "flags": [], "speech": "none", "register": "haera"}])
    (b / "status.json").write_text(json.dumps({"batch": "d-turn01-a", "stage": "ready", "round": 0, "kind": "dialogue", **status_extra}))
    write_jsonl(b / "edits.jsonl", edits)
    return b

def test_rejects_edit_whose_key_is_absent_from_current(tmp_path, monkeypatch):
    b = _mk(tmp_path, monkeypatch, [{**ROW, "key": "d:2:2"}], [{"key": "d:1:1", "ko_new": KO_NEW, "reason": "하오체", "flags_resolved": []}])
    r = apply_edits(b)
    assert r["applied"] == 0 and r["rejected"][0] == {"key": "d:1:1", "errors": ["key not in current corpus"]}
    assert read_jsonl(paths.CURRENT / "dialogue.jsonl")[0]["ko"] == ROW["ko"]
    rv = read_jsonl(b / "reviewed.jsonl")[0]
    assert rv["edited"] is False and rv["ko"] == ROW["ko"]
    assert read_jsonl(b / "input.jsonl")[0]["ko"] == ROW["ko"]

def test_rejects_menu_edit_whose_base_key_is_absent_from_current(tmp_path, monkeypatch):
    menu_row = {**ROW, "menu_en": ROW["en"], "menu_ko": ROW["ko"]}
    b = _mk(tmp_path, monkeypatch, [{**menu_row, "key": "d:2:2"}],
            [{"key": "d:1:1#menu", "ko_new": KO_NEW, "reason": "", "flags_resolved": []}], row=menu_row)
    r = apply_edits(b)
    assert r["applied"] == 0 and r["rejected"][0] == {"key": "d:1:1#menu", "errors": ["key not in current corpus"]}
    assert read_jsonl(b / "input.jsonl")[0]["menu_ko"] == ROW["ko"]

def test_input_jsonl_carries_post_edit_ko(tmp_path, monkeypatch):
    b = _mk(tmp_path, monkeypatch, [ROW], [{"key": "d:1:1", "ko_new": KO_NEW, "reason": "하오체", "flags_resolved": []}])
    apply_edits(b)
    assert read_jsonl(b / "input.jsonl")[0]["ko"] == KO_NEW

def test_apply_errors_names_key_and_error(tmp_path, monkeypatch):
    b = _mk(tmp_path, monkeypatch, [ROW], [{"key": "d:1:1", "ko_new": "", "reason": "", "flags_resolved": []}])
    apply_edits(b)
    assert read_jsonl(b / "apply_errors.jsonl") == [{"key": "d:1:1", "errors": ["empty ko_new"]}]

def test_archives_findings_and_drops_stale_apply_errors(tmp_path, monkeypatch):
    b = _mk(tmp_path, monkeypatch, [ROW], [])
    write_jsonl(b / "findings.jsonl", [{"key": "d:1:1", "severity": "warn"}])
    write_jsonl(b / "apply_errors.jsonl", [{"key": "d:0:0", "errors": ["stale"]}])
    apply_edits(b)
    assert not (b / "findings.jsonl").exists() and not (b / "apply_errors.jsonl").exists()
    assert read_jsonl(b / "findings.round0.jsonl")[0]["key"] == "d:1:1"

def test_status_keeps_unrelated_keys(tmp_path, monkeypatch):
    b = _mk(tmp_path, monkeypatch, [ROW], [], note="keep me")
    apply_edits(b)
    s = json.loads((b / "status.json").read_text(encoding="utf-8"))
    assert s["note"] == "keep me" and s["batch"] == "d-turn01-a" and s["applied"] == 0 and s["rejected"] == 0
