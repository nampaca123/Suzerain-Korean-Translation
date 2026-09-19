from scripts.flag_lines import flag_dialogue, flag_textassets, josa_ok

def D(key, actor, ko, en='"x."', seq=0, title="Rizia/Turn 1/EnT_CouncilBriefing", menu_ko="", menu_en=""):
    return {"key": key, "actor": actor, "ko": ko, "en": en, "seq": seq, "conv_id": 1, "conv_title": title,
            "menu_ko": menu_ko, "menu_en": menu_en}

def test_josa_ok():
    assert josa_ok("스몰라크", "는") and not josa_ok("스몰라크", "은")
    assert josa_ok("금광", "이") and not josa_ok("금광", "가") and josa_ok("살타나", "와")

def test_dialogue_flags():
    rows = [D("a", "Hugo Toras", '"어서 오게, 폐하."'),
            D("b", "Narrator", '그렇게 하고 있습니다.'),
            D("b2", "Narrator", '"아닙니다, 대장님. 몇 분만 더 필요합니다."'),
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
    assert "narration_not_declarative" not in f["b2"]["flags"]
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


def T(key, file, item_name, field_path, ko, en="x"):
    return {"key": key, "file": file, "item_name": item_name, "field_path": field_path, "en": en, "ko": ko}

def test_romus_mixed_register_ignores_short_clause():
    rows = [D("a", "Player_Romus", '"흥미롭군. 그들에 관해 더 듣고 싶소."'),
            D("b", "Player_Romus", '"팔레를 삼았소. 많은 것을 잃었지."', seq=1)]
    f = flag_dialogue(rows, [])
    assert "romus_mixed_register" not in f["a"]["flags"]
    assert "romus_mixed_register" in f["b"]["flags"]

def test_codex_variant_mismatch_groups_only_real_variants():
    rows = [T("c1", "CodexEntryData", "Locations_Cities_Iza", "/CodexEntryProperties/Description", "이자는 항구 도시입니다."),
            T("c2", "CodexEntryData", "Locations_Cities_Iza_PartOfBrenas", "/CodexEntryProperties/Description", "이자는 브레나스의 항구 도시였다."),
            T("c3", "CodexEntryData", "Locations_Cities_Iza", "/CodexEntryProperties/Keywords", "이자 도시 정보")]
    f = flag_textassets(rows, [])
    assert "codex_variant_mismatch" in f["c1"]["flags"] and "codex_variant_mismatch" in f["c2"]["flags"]
    assert "codex_variant_mismatch" not in f["c3"]["flags"]

def test_codex_variant_mismatch_ignores_sibling_entries():
    rows = [T("c1", "CodexEntryData", "Locations_Cities_Argno", "/CodexEntryProperties/Description", "아르그노는 도시입니다."),
            T("c2", "CodexEntryData", "Locations_Cities_Iza", "/CodexEntryProperties/Description", "이자는 항구 도시였다.")]
    f = flag_textassets(rows, [])
    assert not any("codex_variant_mismatch" in f[k]["flags"] for k in ("c1", "c2"))

def test_ta_register_mismatch_skips_titles_and_fragments():
    rows = [T("n1", "NewsData", "N1", "/NewsProperties/Title", "안톤 라이네, 방문"),
            T("n2", "NewsData", "N2", "/NewsProperties/Description", "안톤 라이네가 리치아를 방문했습니다.")]
    f = flag_textassets(rows, [])
    assert "ta_register_mismatch" not in f["n1"]["flags"]
    assert "ta_register_mismatch" in f["n2"]["flags"]

def test_pronoun_dangsin_includes_romus():
    f = flag_dialogue([D("a", "Player_Romus", '"당신이 결정하시오."')], [])
    assert "pronoun_dangsin" in f["a"]["flags"]

def test_english_effect_tag_any_latin_word():
    rows = [T("e1", "PolicyData", "P1", "/P/Description", "x [-500 Equipment, -500 Manpower]"),
            T("e2", "PolicyData", "P2", "/P/Description", "x [Immediate]"),
            T("e3", "PolicyData", "P3", "/P/Description", "x [-2 예산]")]
    f = flag_textassets(rows, [])
    assert "english_effect_tag" in f["e1"]["flags"] and "english_effect_tag" in f["e2"]["flags"]
    assert "english_effect_tag" not in f["e3"]["flags"]

def test_english_effect_tag_skips_hangul_bracket():
    rows = [T("h1", "PolicyData", "P1", "/P/Description", "x [RNC 제안]"),
            T("h2", "PolicyData", "P2", "/P/Description", "x [Immediate]")]
    f = flag_textassets(rows, [])
    assert "english_effect_tag" not in f["h1"]["flags"]
    assert "english_effect_tag" in f["h2"]["flags"]

def test_royal_title_low_register_only_on_vocative():
    rows = [D("a", "Hugo Toras", '"그래도 고맙네, 베르너 씨. 보고서는 내가 폐하께 확실히 전달하겠네."'),
            D("b", "Hugo Toras", '"어서 오게, 폐하."', seq=1)]
    f = flag_dialogue(rows, [])
    assert "royal_title_low_register" not in f["a"]["flags"]
    assert "royal_title_low_register" in f["b"]["flags"]

def test_glossary_violation_ignores_longer_standard_and_prefixed_word():
    g = [{"concept": "PM", "standard": "총리", "banned": ["수상", "재상"], "source": "sordland"},
         {"concept": "Empire", "standard": "리치아 임페리이", "banned": ["리치아 임페리"], "source": "sordland"}]
    rows = [D("a", "Hugo Toras", '대재상은 말했다.'),
            D("b", "Hugo Toras", '재상은 말했다.', seq=1),
            D("c", "Hugo Toras", '리치아 임페리이가 왔다.', seq=2),
            D("d", "Hugo Toras", '리치아 임페리가 왔다.', seq=3)]
    f = flag_dialogue(rows, g)
    assert "glossary_violation" not in f["a"]["flags"]
    assert "glossary_violation" in f["b"]["flags"]
    assert "glossary_violation" not in f["c"]["flags"]
    assert "glossary_violation" in f["d"]["flags"]

def test_narration_ignores_trailing_quote():
    rows = [D("a", "Narrator", '한 혁명가가 소리쳤다. "그만하십시오. 이제 충분합니다!"'),
            D("b", "Narrator", '한 혁명가가 소리쳤습니다. "그만하십시오."', seq=1),
            D("c", "Narrator", '그는 웃었다.', seq=2),
            D("d", "Narrator", '그렇게 하고 있습니다.', seq=3),
            D("e", "Narrator", '그러다 앞서 봤던 구호가 떠올랐다, "국민 외에는 왕이 없다."', seq=4)]
    f = flag_dialogue(rows, [])
    assert "narration_not_declarative" not in f["a"]["flags"]
    assert "narration_not_declarative" not in f["e"]["flags"]
    assert "narration_not_declarative" in f["b"]["flags"]
    assert "narration_not_declarative" not in f["c"]["flags"]
    assert "narration_not_declarative" in f["d"]["flags"]

def test_glossary_hint_for_non_auto_replace_entries():
    g = [{"concept": "PM", "standard": "총리", "banned": ["수상", "재상"], "auto_replace": False, "source": "sordland"},
         {"concept": "Pales", "standard": "팔레", "banned": ["페일스"], "auto_replace": True, "source": "sordland"}]
    rows = [D("a", "Hugo Toras", '수상한 움직임이 있었네.'),
            D("b", "Hugo Toras", '페일스는 위험하네.', seq=1)]
    f = flag_dialogue(rows, g)
    assert "glossary_hint" in f["a"]["flags"] and "glossary_violation" not in f["a"]["flags"]
    assert "glossary_violation" in f["b"]["flags"] and "glossary_hint" not in f["b"]["flags"]


def test_subject_mixed_register_flags_mid_sentence_haeyo():
    rows = [D("m1", "Elena Werner", '"그렇군요. 바로 보고드리겠습니다."'), D("m2", "Elena Werner", '"알겠습니다. 바로 보고드리겠습니다."')]
    f = flag_dialogue(rows, [])
    assert "subject_mixed_register" in f["m1"]["flags"]
    assert "subject_mixed_register" not in f["m2"]["flags"]


def test_mixed_register_tolerates_hortative_and_echo():
    rows = [D("t1", "Patricio Alvarez (R)", '"좋습니다. 이야기해 보시죠."'), D("t2", "Patricio Alvarez (R)", '"글쎄요, 폐하. 병력을 많이 잃으셨잖습니까."'),
            D("t3", "Player_Romus", '"반리치아적이라니? 그게 무슨 협박이오?"'), D("t4", "Axel Reinhart", '"모욕은 이쯤 하시지요, 폐하. 어떻게 하실 건지 말씀하십시오."')]
    f = flag_dialogue(rows, [])
    assert "subject_mixed_register" not in f["t1"]["flags"] and "subject_mixed_register" not in f["t2"]["flags"]
    assert "romus_mixed_register" not in f["t3"]["flags"]
    assert "subject_mixed_register" not in f["t4"]["flags"]


def test_menu_mismatch_ignores_effect_tags():
    rows = [D("mm", "Player_Romus", '"거래하겠소."', en='"Deal."', menu_ko='"거래하지." [+1 권위]', menu_en='"Deal." [+1 Authority]'),
            D("mm2", "Player_Romus", '"거래하겠소."', en='"Deal."', menu_ko='"거래하겠소." [+1 권위]', menu_en='"Deal." [+1 Authority]')]
    f = flag_dialogue(rows, [])
    assert "menu_mismatch" in f["mm"]["flags"] and "menu_mismatch" not in f["mm2"]["flags"]


def test_mixed_register_ignores_single_quoted_scripture():
    rows = [D("q1", "Jorga Azmal", "\"성 브루헤지께서 쓰셨듯, '신께서 내려 주신 미덕은 흔들리지 않는다.' 그렇습니다.\"")]
    assert "subject_mixed_register" not in flag_dialogue(rows, [])["q1"]["flags"]
