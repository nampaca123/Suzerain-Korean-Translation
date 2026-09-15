# 말뭉치 생성기가 Rizia 대사·공용 코덱스만 골라 한/영을 짝지어 정렬하는지 확인
import json
from pathlib import Path
from scripts.build_corpus import build_dialogue, build_textassets, write_jsonl, read_jsonl
FX = Path(__file__).parent / "fixtures"

def _db(name): return json.loads((FX / name).read_text(encoding="utf-8"))

def test_build_dialogue_rizia_only_with_text():
    rows = build_dialogue(_db("mini_db_ko.json"), _db("mini_db_en.json"))
    assert [r["key"] for r in rows] == ["d:288:27", "d:288:28"]
    r = rows[0]
    assert r["actor"] == "Player_Romus" and r["ko"] == '"환영하오."' and r["menu_ko"] == '"환영합니다."'
    assert r["en"] and r["conv_title"] == "Rizia/Turn 1/Start_Coronation" and r["seq"] == 0
    assert rows[1]["seq"] == 1 and rows[1]["menu_ko"] == ""

def test_build_textassets_filters_and_paths():
    rows = build_textassets(FX / "ta_ko", FX / "ta_en", shared_names={"Soradis"})
    keys = sorted(r["key"] for r in rows)
    assert keys == ["t:ReportData:0x01:/ReportProperties/Description", "t:ReportData:0x01:/ReportProperties/Title",
                    "t:ReportData:0x03:/ReportProperties/Description", "t:ReportData:0x03:/ReportProperties/Title"]
    d = next(r for r in rows if r["key"].endswith("0x01:/ReportProperties/Description"))
    assert d["ko"].count("\n") == 2 and d["en"] and d["file"] == "ReportData" and d["item_name"] == "R_A"

def test_jsonl_roundtrip(tmp_path):
    rows = [{"key": "a", "ko": "가"}, {"key": "b", "ko": "나\n다"}]
    write_jsonl(tmp_path / "x.jsonl", rows)
    assert read_jsonl(tmp_path / "x.jsonl") == rows

def test_build_textassets_skips_items_without_id(tmp_path):
    doc = {"items": [{"id": "0xD6", "StoryPack": "StoryPack_Rizia", "Path": "", "Description": ""},
                     {"Id": "0x01", "Path": "Rizia/Reports", "NameInDatabase": "R_A",
                      "ReportProperties": {"Title": "보고서"}}]}
    for side in ("ko", "en"):
        (tmp_path / side).mkdir()
        (tmp_path / side / "F.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    rows = build_textassets(tmp_path / "ko", tmp_path / "en", shared_names=set())
    assert [r["key"] for r in rows] == ["t:F:0x01:/ReportProperties/Title"]

def test_build_textassets_excludes_identifier_and_script_strings(tmp_path):
    ko = {"items": [{"Id": "0x11", "Path": "Rizia/X", "NameInDatabase": "E_A", "ReportProperties": {
        "Title": "Story DLC", "Description": "본문이다.", "Parameters": "Rizia_A, Rizia_B",
        "Instruction": "Set(X) = 1", "Subtitle": "Rizia_A, Rizia_B", "HeaderText": "Set(X) = 1"}}]}
    en = json.loads(json.dumps(ko))
    en["items"][0]["ReportProperties"]["Description"] = "This is the body."
    for side, doc in (("ko", ko), ("en", en)):
        (tmp_path / side).mkdir()
        (tmp_path / side / "F.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    rows = build_textassets(tmp_path / "ko", tmp_path / "en", shared_names=set())
    assert sorted(r["key"] for r in rows) == ["t:F:0x11:/ReportProperties/Description",
                                              "t:F:0x11:/ReportProperties/Title"]

def test_build_textassets_warns_and_skips_unreadable_file(tmp_path, capsys):
    good = {"items": [{"Id": "0x21", "Path": "Rizia/X", "NameInDatabase": "G", "P": {"Title": "제목이다."}}]}
    for side in ("ko", "en"):
        (tmp_path / side).mkdir()
        (tmp_path / side / "Good.json").write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
        (tmp_path / side / "BadKo.json").write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
        (tmp_path / side / "BadEn.json").write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "ko" / "BadKo.json").write_text("{oops", encoding="utf-8")
    (tmp_path / "en" / "BadEn.json").write_text("{oops", encoding="utf-8")
    rows = build_textassets(tmp_path / "ko", tmp_path / "en", shared_names=set())
    assert [r["key"] for r in rows] == ["t:Good:0x21:/P/Title"]
    err = capsys.readouterr().err
    assert "warning: skipping unreadable textasset file BadKo.json" in err
    assert "warning: skipping unreadable textasset file BadEn.json" in err
