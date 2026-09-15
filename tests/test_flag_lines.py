from scripts.flag_lines import flag_dialogue, flag_textassets, josa_ok

def D(key, actor, ko, en='"x."', seq=0, title="Rizia/Turn 1/EnT_CouncilBriefing", menu_ko="", menu_en=""):
    return {"key": key, "actor": actor, "ko": ko, "en": en, "seq": seq, "conv_id": 1, "conv_title": title,
            "menu_ko": menu_ko, "menu_en": menu_en}

def test_josa_ok():
    assert josa_ok("스몰라크", "는") and not josa_ok("스몰라크", "은")
    assert josa_ok("금광", "이") and not josa_ok("금광", "가") and josa_ok("살타나", "와")

def test_dialogue_flags():
    rows = [D("a", "Hugo Toras", '"어서 오게, 폐하."'),
            D("b", "Narrator", '"그렇게 하고 있습니다."'),
            D("c", "Player_Romus", '"팔레를 삼았소. 많은 것을 잃었지."'),
            D("d", "Player_Romus", '"그렇게 말할 줄 알았습니다."'),
            D("e", "Vina Toras", '"아버지, 그렇게 하겠습니다."'),
            D("f", "Emmerich Hegel (R)", '"당신이 결정하시오."'),
            D("g", "Player_Romus", '"환영하오."', en='"Welcome."', menu_ko='"환영합니다."', menu_en='"Welcome."'),
            D("h", "Lucita Azaro", '"페일스는 위험합니다."'),
            D("i", "Player_Romus", '"스몰라크은 틀렸소."'),
            D("j", "Player_Romus", '안녕하오.', en='"Hi."')]
    g = [{"concept": "Pales", "standard": "팔레", "banned": ["페일스"], "source": "sordland"}]
    f = flag_dialogue(rows, g)
    assert "royal_title_low_register" in f["a"]["flags"] and "hugo_low_register" in f["a"]["flags"]
    assert "narration_not_declarative" in f["b"]["flags"]
    assert "romus_mixed_register" in f["c"]["flags"]
    assert "romus_hapsyo_not_speech" in f["d"]["flags"]
    assert "vina_not_haeyo" in f["e"]["flags"]
    assert {"foreign_not_hapsyo", "pronoun_dangsin"} <= set(f["f"]["flags"])
    assert "menu_mismatch" in f["g"]["flags"]
    assert "glossary_violation" in f["h"]["flags"] and "subject_not_hapsyo" not in f["h"]["flags"]
    assert "josa_mismatch" in f["i"]["flags"]
    assert "quote_missing" in f["j"]["flags"]

def test_same_en_diff_register():
    rows = [D("a", "Player_Romus", '"알겠소."', en='"Fine."'), D("b", "Player_Romus", '"알겠어요."', en='"Fine."', seq=1)]
    f = flag_dialogue(rows, [])
    assert "same_en_diff_register" in f["a"]["flags"] and "same_en_diff_register" in f["b"]["flags"]

def test_textassets_flags():
    rows = [{"key": "t:ReportData:1:/R/Description", "file": "ReportData", "item_name": "R1", "field_path": "/R/Description",
             "en": "Para one.\n\nPara two.", "ko": "문단 하나다."},
            {"key": "t:NewsData:2:/N/Description", "file": "NewsData", "item_name": "N1", "field_path": "/N/Description",
             "en": "Long english text here that is fairly long.", "ko": "짧은 기사 문장이 실렸습니다."},
            {"key": "t:CodexEntryData:3:/C/Description", "file": "CodexEntryData", "item_name": "City_Iza", "field_path": "/C/Description",
             "en": "Iza {X} text.", "ko": "이자 {Y} 설명입니다."}]
    f = flag_textassets(rows, [])
    assert {"ta_register_mismatch", "missing_paragraph"} <= set(f[rows[0]["key"]]["flags"])
    assert "ta_register_mismatch" in f[rows[1]["key"]]["flags"]
    assert "placeholder_mismatch" in f[rows[2]["key"]]["flags"]

def test_missing_paragraph_only_on_lost_line_breaks():
    rows = [{"key": "k1", "file": "ReportData", "item_name": "R", "field_path": "/R/Description",
             "en": "A fairly long english sentence that a dense korean line renders compactly.", "ko": "짧지만 온전한 번역입니다."},
            {"key": "k2", "file": "ReportData", "item_name": "R", "field_path": "/R/Description",
             "en": "One.\n\nTwo.\n\nThree.", "ko": "하나입니다.\n\n둘입니다."}]
    f = flag_textassets(rows, [])
    assert "missing_paragraph" not in f["k1"]["flags"]
    assert "missing_paragraph" in f["k2"]["flags"]
