# prompts/ 아래 에이전트 규칙·프롬프트 파일이 존재하고 필수 참조·항목을 담았는지 검사한다.
from pathlib import Path
P = Path(__file__).resolve().parent.parent / "prompts"

def test_prompt_files_exist_and_reference_rules():
    for n in ("register_table.md", "checklist.md", "editor.md", "reviewer.md"):
        assert (P / n).exists(), n
    ed, rv = (P / "editor.md").read_text(encoding="utf-8"), (P / "reviewer.md").read_text(encoding="utf-8")
    for t in (ed, rv):
        assert "{BATCH_DIR}" in t and "humanizer" in t and "register_table.md" in t and "glossary.md" in t and "checklist.md" in t
    assert "edits.jsonl" in ed and "flags_resolved" in ed and "needs_human.jsonl" in ed
    assert "findings.jsonl" in rv and '"block"' in rv

def test_register_table_has_spec_sections():
    t = (P / "register_table.md").read_text(encoding="utf-8")
    for s in ("5.1", "5.2", "5.3", "5.4", "6.1", "6.2", "6.3", "6.4", "연설 판정 순서"):
        assert s in t, s

FLAGS = ("narration_not_declarative", "dialogue_declarative_ending", "royal_title_low_register",
         "romus_mixed_register", "romus_hapsyo_not_speech", "speech_not_hapsyo", "romus_haeyo",
         "subject_not_hapsyo", "vina_not_haeyo", "foreign_not_hapsyo", "hugo_low_register",
         "menu_mismatch", "same_en_diff_register", "glossary_violation", "josa_mismatch",
         "dash_remaining", "curly_quote", "quote_missing", "english_effect_tag", "pronoun_dangsin",
         "glossary_hint",
         "ta_register_mismatch", "missing_paragraph", "placeholder_mismatch", "codex_variant_mismatch")

def test_checklist_covers_every_flag():
    t = (P / "checklist.md").read_text(encoding="utf-8")
    for f in FLAGS:
        assert f in t, f
