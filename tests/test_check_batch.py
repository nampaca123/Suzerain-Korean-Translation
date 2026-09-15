import json
from scripts.check_batch import check_batch, HARD_FLAGS
from scripts.build_corpus import write_jsonl

def _batch(tmp_path, ko, findings):
    b = tmp_path / "d-turn01-a"; b.mkdir()
    row = {"key": "d:1:1", "en": '"Welcome."', "ko": ko, "actor": "Hugo Toras", "conv_id": 1, "seq": 0, "conv_title": "Rizia/Turn 1/A", "menu_en": "", "menu_ko": ""}
    write_jsonl(b / "input.jsonl", [row]); write_jsonl(b / "findings.jsonl", findings)
    (b / "status.json").write_text(json.dumps({"batch": "d-turn01-a", "stage": "edited", "round": 1, "kind": "dialogue"}))
    return b

def test_fails_on_hard_flag(tmp_path):
    r = check_batch(_batch(tmp_path, '"어서 오게, 폐하."', []))
    assert r["stage"] == "failed" and "royal_title_low_register" in r["remaining_flags"]

def test_fails_on_block_finding(tmp_path):
    r = check_batch(_batch(tmp_path, '"어서 오십시오, 폐하."', [{"key": "d:1:1", "type": "meaning", "severity": "block", "evidence": "", "suggestion": ""}]))
    assert r["stage"] == "failed" and r["blocks"] == 1

def test_passes_clean(tmp_path):
    b = _batch(tmp_path, '"어서 오십시오, 폐하."', [])
    r = check_batch(b)
    assert r["stage"] == "passed" and json.loads((b / "status.json").read_text())["stage"] == "passed"
    assert "royal_title_low_register" in HARD_FLAGS

def _rows_batch(tmp_path, rows, kind="dialogue", findings=(), **status_extra):
    b = tmp_path / "b"; b.mkdir()
    write_jsonl(b / "input.jsonl", rows)
    if findings is not None:
        write_jsonl(b / "findings.jsonl", list(findings))
    (b / "status.json").write_text(json.dumps({"batch": "b", "stage": "edited", "round": 1, "kind": kind, **status_extra}))
    return b

def _line(i, ko, en, actor="Narrator"):
    return {"key": f"d:1:{i}", "en": en, "ko": ko, "actor": actor, "conv_id": 1, "seq": i, "conv_title": "Rizia/Turn 1/A", "menu_en": "", "menu_ko": ""}

def test_fails_when_findings_missing(tmp_path):
    r = check_batch(_rows_batch(tmp_path, [_line(0, '"어서 오십시오, 폐하."', '"Welcome."', "Hugo Toras")], findings=None))
    assert r["stage"] == "failed" and r["reason"] == "findings.jsonl missing" and r["blocks"] == 0

def test_narration_limit_is_stricter_than_dialogue(tmp_path):
    rows = [_line(i, "비가 내렸다.", "Rain fell.") for i in range(99)] + [_line(99, "그는 갔습니다.", "He left.")]
    rows += [_line(100 + i, '"어서 오십시오, 폐하."', '"Welcome."', "Hugo Toras") for i in range(99)]
    rows += [_line(199, '"어서 오게, 폐하."', '"Greetings."', "Hugo Toras")]
    r = check_batch(_rows_batch(tmp_path, rows))
    assert r["stage"] == "failed"
    assert r["hard_flag_rate"] == {"narration": 0.01}

def test_textassets_group_by_file_over_limit(tmp_path):
    rows = [{"key": f"t:ReportData:{i}", "file": "ReportData", "field_path": "/ReportProperties/Description",
             "item_name": "R_A", "en": "The mine closed.",
             "ko": "금광이 문을 닫았다." if i == 0 else "금광이 문을 닫았습니다."} for i in range(50)]
    r = check_batch(_rows_batch(tmp_path, rows, kind="textassets"))
    assert r["stage"] == "failed" and r["hard_flag_rate"] == {"ReportData": 0.02}
    assert r["remaining_flags"] == {"ta_register_mismatch": 1}

def test_status_keeps_unrelated_keys(tmp_path):
    b = _rows_batch(tmp_path, [_line(0, '"어서 오십시오, 폐하."', '"Welcome."', "Hugo Toras")], note="keep me")
    assert check_batch(b)["stage"] == "passed"
    s = json.loads((b / "status.json").read_text(encoding="utf-8"))
    assert s["note"] == "keep me" and s["round"] == 1 and s["stage"] == "passed"
