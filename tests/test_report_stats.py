# report_stats의 전/후 비교 표를 작은 임시 코퍼스로 검증한다.
import json

from scripts import paths, report_stats

BEFORE_KO = '"어서 오게, 폐하."'
AFTER_KO = '"어서 오십시오, 폐하."'
TA = [{"key": "t:ReportData:1:/R/Description", "file": "ReportData", "item_name": "R1",
       "field_path": "/R/Description", "en": "One.", "ko": "보고서 내용입니다."}]


def _dialogue(ko):
    return [{"key": "d:1:1", "conv_id": 1, "conv_title": "Rizia/Turn 1/X", "seq": 0, "actor": "Hugo Toras",
             "ko": ko, "en": '"Welcome."', "menu_ko": "", "menu_en": ""}]


def _write(d, name, rows):
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def _setup(tmp_path, monkeypatch):
    for name, ko in (("corpus", BEFORE_KO), ("current", AFTER_KO)):
        _write(tmp_path / name, "dialogue.jsonl", _dialogue(ko))
        _write(tmp_path / name, "textassets.jsonl", TA)
    monkeypatch.setattr(paths, "CORPUS", tmp_path / "corpus")
    monkeypatch.setattr(paths, "CURRENT", tmp_path / "current")
    monkeypatch.setattr(report_stats, "load_glossary", lambda: [])


def test_flag_table_shows_drop(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    md = report_stats.report()
    assert "| royal_title_low_register | 1 | 0 |" in md
    assert "| hugo_low_register | 1 | 0 |" in md


def test_speaker_table_counts_hard_flags_only(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    md = report_stats.report()
    # hugo_low_register는 hard flag가 아니므로 화자 표에는 royal_title_low_register 1건만 남는다.
    assert "| Hugo Toras | 1 | 0 |" in md


def test_out_writes_file(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    out = tmp_path / "stats.md"
    report_stats.main(["--out", str(out)])
    assert "| royal_title_low_register | 1 | 0 |" in out.read_text(encoding="utf-8")
