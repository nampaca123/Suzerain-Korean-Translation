# 교정 에이전트의 edits.jsonl을 검증해 data/current와 배치 input에 반영하고 reviewed.jsonl을 만든다.
import json, re, sys
from pathlib import Path
from scripts import paths
from scripts.build_corpus import read_jsonl, write_jsonl

_PH = re.compile(r"\{[^}]+\}")
_TAG = re.compile(r"\[[^\]]*\]")


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
    if len(ko_new) > 2 * max(len(ko), 20) or (en.strip() and len(ko_new) < 0.42 * len(en)):
        errs.append("length out of range")
    return errs


def apply_edits(batch_dir: Path) -> dict:
    status = json.loads((batch_dir / "status.json").read_text(encoding="utf-8"))
    rows = read_jsonl(batch_dir / "input.jsonl"); by_key = {r["key"]: r for r in rows}
    edits = read_jsonl(batch_dir / "edits.jsonl") if (batch_dir / "edits.jsonl").exists() else []
    accepted, rejected = {}, []
    for e in edits:
        row = by_key.get(e.get("key"))
        errs = ["unknown key"] if row is None else validate_edit(row, e.get("ko_new", ""))
        (rejected.append({"key": e.get("key"), "errors": errs}) if errs else accepted.__setitem__(e["key"], e))
    current_path = paths.CURRENT / f"{status['kind']}.jsonl"
    current = read_jsonl(current_path)
    for r in current:
        if r["key"] in accepted:
            r["ko"] = accepted[r["key"]]["ko_new"]
    write_jsonl(current_path, current)
    reviewed = []
    for r in rows:
        e = accepted.get(r["key"])
        reviewed.append({**r, "ko_old": r["ko"], "ko": e["ko_new"] if e else r["ko"], "edited": bool(e), "reason": e["reason"] if e else ""})
        if e:
            r["ko"] = e["ko_new"]
    write_jsonl(batch_dir / "input.jsonl", rows); write_jsonl(batch_dir / "reviewed.jsonl", reviewed)
    if rejected:
        write_jsonl(batch_dir / "apply_errors.jsonl", rejected)
    status.update(stage="edited", round=status.get("round", 0) + 1, applied=len(accepted), rejected=len(rejected))
    (batch_dir / "status.json").write_text(json.dumps(status, ensure_ascii=False), encoding="utf-8")
    return {"applied": len(accepted), "rejected": rejected}


if __name__ == "__main__":
    r = apply_edits(Path(sys.argv[1]))
    print(f"applied={r['applied']} rejected={len(r['rejected'])}", file=sys.stderr)
    sys.exit(1 if r["rejected"] else 0)
