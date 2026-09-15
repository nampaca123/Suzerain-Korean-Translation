# 배치의 flag를 다시 계산하고 검수 findings의 block 여부를 합쳐 통과/실패를 status.json에 기록한다.
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
from scripts.build_corpus import read_jsonl
from scripts.build_glossary import load_glossary, GLOSSARY_JSON
from scripts.flag_lines import flag_dialogue, flag_textassets

HARD_FLAGS = {"royal_title_low_register", "romus_mixed_register", "narration_not_declarative",
              "speech_not_hapsyo", "menu_mismatch", "glossary_violation", "placeholder_mismatch", "english_effect_tag",
              "curly_quote", "ta_register_mismatch", "missing_paragraph"}
LIMIT = {"dialogue": 0.02, "narration": 0.005, "textassets": 0.01}
MIN_DENOMINATOR = 50


def check_batch(batch_dir: Path) -> dict:
    status = json.loads((batch_dir / "status.json").read_text(encoding="utf-8"))
    rows = read_jsonl(batch_dir / "input.jsonl")
    glossary = load_glossary() if GLOSSARY_JSON.exists() else []
    flags = flag_dialogue(rows, glossary) if status["kind"] == "dialogue" else flag_textassets(rows, glossary)
    remaining = Counter(f for v in flags.values() for f in v["flags"] if f in HARD_FLAGS)
    per_group, size = defaultdict(int), defaultdict(int)
    for r in rows:
        g = "narration" if r.get("actor") in ("Narrator", "Player_Romus_Italic") else (r.get("actor") or r.get("file"))
        size[g] += 1; per_group[g] += bool(set(flags[r["key"]]["flags"]) & HARD_FLAGS)
    # R53: 분모에 하한을 둔다. 6줄짜리 화자의 hard flag 1건이 16.7%로 튀어 배치를 막던 문제.
    rate = {g: per_group[g] / max(size[g], MIN_DENOMINATOR) for g in size}
    over = {g: v for g, v in rate.items() if v > LIMIT["narration" if g == "narration" else status["kind"]]}
    fp = batch_dir / "findings.jsonl"
    findings = read_jsonl(fp) if fp.exists() else []
    blocks = sum(1 for f in findings if f.get("severity") == "block")
    reason = "" if fp.exists() else "findings.jsonl missing"
    result = {"stage": "passed" if not over and blocks == 0 and not reason else "failed", "reason": reason,
              "hard_flag_rate": {g: round(v, 4) for g, v in over.items()},
              "blocks": blocks, "remaining_flags": dict(remaining)}
    status.update(result); (batch_dir / "status.json").write_text(json.dumps(status, ensure_ascii=False), encoding="utf-8")
    return result


if __name__ == "__main__":
    r = check_batch(Path(sys.argv[1]))
    print(json.dumps(r, ensure_ascii=False), file=sys.stderr)
    sys.exit(0 if r["stage"] == "passed" else 1)
