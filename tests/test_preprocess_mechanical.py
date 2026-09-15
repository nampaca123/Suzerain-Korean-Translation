# preprocess_mechanical의 결정적 규칙(따옴표·곡선따옴표·대시·효과 표기·용어 치환) 검증.
from scripts.preprocess_mechanical import fix_quotes, normalize_curly, fix_dashes, fix_effect_tags, apply_glossary, preprocess_row


def test_fix_quotes_adds_outer_quotes_and_keeps_effect_tag():
    assert fix_quotes('"Hello."', '안녕하오.') == '"안녕하오."'
    assert fix_quotes('"Hello."', '안녕하오. [-1 예산]') == '"안녕하오." [-1 예산]'
    assert fix_quotes('"Hello."', '"안녕하오."') == '"안녕하오."'
    assert fix_quotes('He smiled.', '그는 웃었다.') == '그는 웃었다.'


def test_normalize_curly():
    assert normalize_curly('“안녕,” 그녀가 ‘말했다’.') == '"안녕," 그녀가 \'말했다\'.'


def test_fix_dashes():
    assert fix_dashes('"폐하--"') == ('"폐하..."', False)
    assert fix_dashes('"그건 -- 아니오."') == ('"그건, 아니오."', False)
    assert fix_dashes('"이--것"') == ('"이--것"', True)


def test_fix_effect_tags():
    assert fix_effect_tags('"좋소." [+2 Budget]') == '"좋소." [+2 예산]'
    assert fix_effect_tags('x [-1 Energy Per Turn, +1 Authority]') == 'x [턴당 -1 에너지, +1 권위]'
    assert fix_effect_tags('x [-2 예산]') == 'x [-2 예산]'


def test_apply_glossary_only_auto_replace_entries():
    g = [{"concept": "Pales", "standard": "팔레", "banned": ["페일스"], "source": "sordland", "auto_replace": True},
         {"concept": "X", "standard": "가", "banned": ["나"], "source": "sordland", "auto_replace": False}]
    assert apply_glossary("페일스와 나", g) == ("팔레와 나", ["Pales"])


def test_apply_glossary_ascii_banned_needs_word_boundary():
    g = [{"concept": "Alliance of Nations", "standard": "국제연합", "banned": ["AN"],
          "source": "sordland", "auto_replace": True}]
    assert apply_glossary("AN 총회", g) == ("국제연합 총회", ["Alliance of Nations"])
    assert apply_glossary("CANADA ANALYSIS 보고서", g) == ("CANADA ANALYSIS 보고서", [])


def test_preprocess_row_logs_each_rule():
    row = {"key": "d:1:1", "en": '"Go -- now." ', "ko": '“가라 -- 지금.” [+1 Authority]'}
    ko, log = preprocess_row(row, [])
    assert ko == '"가라, 지금." [+1 권위]'
    assert [l["rule"] for l in log] == ["curly", "dash", "effect_tag"]


def test_apply_glossary_skips_protected_proper_noun():
    g = [{"concept": "Pales", "standard": "팔레", "banned": ["페일스"], "source": "sordland", "auto_replace": True}]
    assert apply_glossary("페일스트림 송유관은 페일스로 이어진다", g) == ("페일스트림 송유관은 팔레로 이어진다", ["Pales"])
    assert apply_glossary("페일스트림 송유관", g) == ("페일스트림 송유관", [])
