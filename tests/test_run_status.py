# run_status의 배치 현황 요약(단계별 개수·다음 실행 대상·진행 중 목록)을 임시 batches 폴더로 검증한다.
import json

from scripts import paths, run_status

# (배치, 우선순위, stage, kind)
BATCHES = [
    ("d-low", 0.2, "ready", "dialogue"),
    ("d-high", 0.9, "ready", "dialogue"),
    ("d-mid", 0.5, "edited", "dialogue"),
    ("t-fail", 0.7, "failed", "textassets"),
    ("t-pass", 0.4, "passed", "textassets"),
    ("d-pass", 0.3, "passed", "dialogue"),
    ("d-human", 0.1, "needs_human", "dialogue"),
]


def _setup(tmp_path, monkeypatch):
    root = tmp_path / "batches"
    root.mkdir()
    index = [{"batch": b, "kind": k, "rows": 10, "flagged": 5, "priority": p} for b, p, _, k in BATCHES]
    (root / "index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    for b, _, stage, k in BATCHES:
        (root / b).mkdir()
        (root / b / "status.json").write_text(
            json.dumps({"batch": b, "stage": stage, "round": 0, "kind": k}), encoding="utf-8")
    monkeypatch.setattr(paths, "BATCHES", root)
    return root


def test_counts_every_stage(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert run_status.summarize()["counts"] == {
        "ready": 2, "edited": 1, "failed": 1, "passed": 2, "needs_human": 1}


def test_next_is_ready_only_ordered_by_priority(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert run_status.summarize()["next"] == ["d-high", "d-low"]


def test_next_respects_limit(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert run_status.summarize(next_n=1)["next"] == ["d-high"]


def test_in_progress_holds_edited_and_failed(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert sorted(run_status.summarize()["in_progress"]) == ["d-mid", "t-fail"]


def test_needs_human_listed(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert run_status.summarize()["needs_human"] == ["d-human"]


def test_passed_counted_per_kind(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert run_status.summarize()["passed_by_kind"] == {"dialogue": 1, "textassets": 1}


def test_batch_missing_from_index_sorts_last(tmp_path, monkeypatch):
    root = _setup(tmp_path, monkeypatch)
    (root / "d-orphan").mkdir()
    (root / "d-orphan" / "status.json").write_text(
        json.dumps({"batch": "d-orphan", "stage": "ready", "round": 0, "kind": "dialogue"}), encoding="utf-8")
    assert run_status.summarize()["next"] == ["d-high", "d-low", "d-orphan"]


def test_json_output_is_machine_readable(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    run_status.main(["--json", "--next", "1"])
    out = json.loads(capsys.readouterr().out)
    assert out["next"] == ["d-high"]
    assert out["counts"]["passed"] == 2


def test_text_output_shows_stages_and_passed_kinds(tmp_path, monkeypatch, capsys):
    _setup(tmp_path, monkeypatch)
    run_status.main([])
    out = capsys.readouterr().out
    assert "next=['d-high', 'd-low']" in out
    assert "passed dialogue=1 textassets=1" in out
