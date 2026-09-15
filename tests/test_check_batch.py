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
