# prompts/ 아래 에이전트 규칙·프롬프트 파일이 존재하고 필수 참조·항목을 담았는지 검사한다.
from pathlib import Path
P = Path(__file__).resolve().parent.parent / "prompts"

def test_prompt_files_exist_and_reference_rules():
    for n in ("register_table.md", "checklist.md", "editor.md", "reviewer.md"):
        assert (P / n).exists(), n
    ed, rv = (P / "editor.md").read_text(encoding="utf-8"), (P / "reviewer.md").read_text(encoding="utf-8")
    for t in (ed, rv):
        assert "{BATCH_DIR}" in t and "humanizer" in t and "register_table.md" in t and "glossary.md" in t and "checklist.md" in t
    assert "edits.jsonl" in ed and "flags_resolved" in ed
    assert "findings.jsonl" in rv and '"block"' in rv

def test_register_table_has_spec_sections():
    t = (P / "register_table.md").read_text(encoding="utf-8")
    for s in ("5.1", "5.2", "5.3", "5.4", "6.1", "6.2", "6.3", "6.4", "연설 판정 순서"):
        assert s in t, s
