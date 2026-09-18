# 리터럴 백슬래시+n 복원이 영문 줄바꿈이 있는 줄에만 적용되는지 확인
from scripts.fix_literal_newlines import fix_row

BS = chr(92) + "n"


def test_fix_row_replaces_only_when_en_has_newline():
    r = {"ko": "가" + BS + BS + "나", "en": "a\n\nb"}
    assert fix_row(r) and r["ko"] == "가\n\n나"
    r2 = {"ko": "경로 C:" + BS + "x", "en": "path"}
    assert not fix_row(r2) and BS in r2["ko"]
