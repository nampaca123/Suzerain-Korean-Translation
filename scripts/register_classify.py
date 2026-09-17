# 한국어 문장 종결 화계 분류기. 탐지 전용이며 치환은 하지 않는다.
import re

HAO, HAEYO, HAPSYO, HAERA, HAE, HAGE, OTHER = "hao", "haeyo", "hapsyo", "haera", "hae", "hage", "other"
_TAIL = r'[.?!]*[\s"”’\'\)\]…]*$'
# 검사 순서가 결과를 결정한다: 합쇼 → 함정 → 하오 → 하게 → 해요 → 해라 → 해체
# 함정: `-ㄹ게`·`거야`는 해체, `-ㄹ 거요`·`뭐요`는 하오체, `가자`는 해라체 청유
_RULES = [
    (HAPSYO, r'([가-힣](?<!아)니다|[가-힣](?<!아)니까|십시오|십시다)'),
    (HAO,    r'(거요|뭐요|이오|하오|시오|아니오|겠소|았소|었소|잖소|구려)'),
    (HAE,    r'(할게|갈게|볼게|올게|줄게|일게|살게|있을게|없을게|그래|거야)'),
    (HAERA,  r'(가자|하자|보자)'),
    (HAO,    r'([가-힣]소|[가-힣]오|[가-힣]시다)'),
    (HAGE,   r'([가-힣]네|[가-힣]게|게나|겠나|는가|인가|런가|은가|하나|하세|일세|걸세|을세|[가-힣](?<!구)나\?|군)'),
    (HAEYO,  r'(요|죠)'),
    (HAERA,  r'(다|라|냐|니|자|마|렴|구나|거라)'),
    (HAE,    r'(어|아|지|야|해|줘|워|래|데|거든|니까)'),
]
_COMPILED = [(name, re.compile(pat + _TAIL)) for name, pat in _RULES]
_BROKEN = re.compile(r'(--|—|…|\.\.\.|\|)[\s"”]*$')
_HANGUL = re.compile(r'[가-힣]')
_NARR = re.compile(r'(다|였다|았다|었다|ㄴ다|는다|이다)\.?' + _TAIL)


def strip_markup(text: str) -> str:
    t = re.sub(r'\s*\[[^\]]*\]\s*$', '', text.strip())
    t = t.replace('*', '')
    return t.strip().strip('"“”\'‘’').strip()


def last_clause(text: str) -> str:
    lines = [l for l in text.split("\n") if l.strip()]
    if not lines:
        return ""
    parts = [p for p in re.split(r'(?<=[.?!…])\s+', strip_markup(lines[-1])) if p.strip()]
    return parts[-1] if parts else strip_markup(lines[-1])


_VOCATIVE_TITLE = re.compile(r'(리치아|팔레|사조니|만세|대현자|대현사|현자|공작|공작부인|백작|백작부인|총리|대통령|의장|장관|사령관|장군|재상|대재상|폐하|전하|각하|여왕|국왕|왕자|공주|어머니|숙부|삼촌|여러분)(님)?' + _TAIL)


def _match_ending(c: str) -> str:
    if not c or _BROKEN.search(c) or not _HANGUL.search(c) or "|" in c:
        return OTHER
    if _VOCATIVE_TITLE.search(c):  # "…, 최고 대현자." 같은 호격은 종결어미가 아니다('자' 오탐 방지)
        return OTHER
    for name, rx in _COMPILED:
        if rx.search(c):
            return name
    return OTHER


def _classify_clause(c: str) -> str:
    c = c.strip()
    found = _match_ending(c)
    if found != OTHER:
        return found
    # 끝에 호격("…, 폐하.")이 붙으면 쉼표로 잘라 뒤에서부터 실제 종결어미를 찾는다
    for seg in reversed(c.split(",")):
        found = _match_ending(seg.strip())
        if found != OTHER:
            return found
    return OTHER


def classify(text: str) -> str:
    return _classify_clause(last_clause(text))


def clause_registers(text: str) -> list[str]:
    body = strip_markup(" ".join(l for l in text.split("\n") if l.strip()))
    parts = [p for p in re.split(r'(?<=[.?!])\s+', body) if p.strip()]
    return [_classify_clause(p) for p in parts]


def is_quoted(text: str) -> bool:
    return text.lstrip().startswith(('"', '“'))


def is_narrative(text: str) -> bool:
    return not is_quoted(text) and classify(text) == HAERA and _NARR.search(last_clause(text)) is not None
