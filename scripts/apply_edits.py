# 교정 에이전트의 edits.jsonl을 검증해 data/current와 배치 input에 반영하고 reviewed.jsonl을 만든다.
import json, re, sys
from pathlib import Path
from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl

_PH = re.compile(r"\{[^}]+\}")
_TAG = re.compile(r"\[[^\]]*\]")
MENU = "#menu"


def validate_edit(row: dict, ko_new: str) -> list[str]:
    errs, ko, en = [], row["ko"], row.get("en", "")
    if not ko_new or not ko_new.strip():
        return ["empty ko_new"]
    ref = en if en.strip() else ko
    if sorted(_PH.findall(ko_new)) != sorted(_PH.findall(ref)):
        errs.append("placeholder set changed")
    if ko_new.count("\n") < ko.count("\n"):
        errs.append("newline count decreased")
    if len(_TAG.findall(ko_new)) != len(_TAG.findall(ko)):
        errs.append("effect tag count changed")
    # R44: 원문 ko가 이미 영문보다 많이 짧으면 0.42*len(en) 하한을 못 넘는다. 원문 대비 0.9면 통과시킨다.
    too_short = len(ko_new) < 0.42 * len(en) and len(ko_new) < 0.9 * len(ko)
    if len(ko_new) > 2 * max(len(ko), 20) or (en.strip() and too_short):
        errs.append("length out of range")
    return errs


def _reset_round(batch_dir: Path, rnd: int) -> None:
    # 라운드마다 새 검수 결과를 강요한다: 지난 findings는 보관하고 낡은 apply_errors는 지운다.
    f = batch_dir / "findings.jsonl"
    if f.exists():
        f.replace(batch_dir / f"findings.round{rnd}.jsonl")
    (batch_dir / "apply_errors.jsonl").unlink(missing_ok=True)


def apply_edits(batch_dir: Path) -> dict:
    status = json.loads((batch_dir / "status.json").read_text(encoding="utf-8"))
    rows = read_jsonl(batch_dir / "input.jsonl"); by_key = {r["key"]: r for r in rows}
    _reset_round(batch_dir, status.get("round", 0))
    edits = read_jsonl(batch_dir / "edits.jsonl") if (batch_dir / "edits.jsonl").exists() else []
    current_path = paths.CURRENT / f"{status['kind']}.jsonl"
    current = read_jsonl(current_path); in_current = {r["key"] for r in current}
    acc_ko, acc_menu, rejected = {}, {}, []
    for e in edits:
        key = e.get("key") or ""; is_menu = key.endswith(MENU); base = key[:-len(MENU)] if is_menu else key
        row = by_key.get(base)
        if row is None:
            errs = ["unknown key"]
        else:
            ref = {**row, "ko": row.get("menu_ko", ""), "en": row.get("menu_en", "")} if is_menu else row
            errs = validate_edit(ref, e.get("ko_new", "")) + ([] if base in in_current else ["key not in current corpus"])
        rejected.append({"key": key, "errors": errs}) if errs else (acc_menu if is_menu else acc_ko).__setitem__(base, e)
    for r in current:
        if r["key"] in acc_ko: r["ko"] = acc_ko[r["key"]]["ko_new"]
        if r["key"] in acc_menu: r["menu_ko"] = acc_menu[r["key"]]["ko_new"]
    write_jsonl(current_path, current)
    reviewed = []
    for r in rows:
        e, m = acc_ko.get(r["key"]), acc_menu.get(r["key"])
        rv = {**r, "ko_old": r["ko"], "ko": e["ko_new"] if e else r["ko"], "edited": bool(e), "reason": e["reason"] if e else ""}
        if m:
            rv["menu_ko"] = r["menu_ko"] = m["ko_new"]
        reviewed.append(rv)
        if e:
            r["ko"] = e["ko_new"]
    write_jsonl(batch_dir / "input.jsonl", rows); write_jsonl(batch_dir / "reviewed.jsonl", reviewed)
    if rejected:
        write_jsonl(batch_dir / "apply_errors.jsonl", rejected)
    applied = len(acc_ko) + len(acc_menu)
    status.update(stage="edited", round=status.get("round", 0) + 1, applied=applied, rejected=len(rejected))
    (batch_dir / "status.json").write_text(json.dumps(status, ensure_ascii=False), encoding="utf-8")
    return {"applied": applied, "rejected": rejected}


if __name__ == "__main__":
    r = apply_edits(Path(sys.argv[1]))
    print(f"applied={r['applied']} rejected={len(r['rejected'])}", file=sys.stderr)
    sys.exit(1 if r["rejected"] else 0)
