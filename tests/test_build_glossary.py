# 용어 표준 표기 결정 규칙(소르들란드 우선 → Rizia 다수 → needs_human)과 후보 출현 집계를 확인
from scripts.build_glossary import decide, count_terms

C = {"concept": "Pales", "en": "Pales", "candidates": ["팔레", "페일스"]}


def test_sordland_wins_even_if_rizia_prefers_other():
    d = decide(C, {"팔레": 12, "페일스": 0}, {"팔레": 3, "페일스": 40})
    assert d["standard"] == "팔레" and d["banned"] == ["페일스"] and d["source"] == "sordland"


def test_rizia_majority_when_absent_in_sordland():
    d = decide(C, {"팔레": 0, "페일스": 0}, {"팔레": 3, "페일스": 40})
    assert d["standard"] == "페일스" and d["source"] == "rizia_majority"


def test_needs_human_on_tie_or_zero():
    assert decide(C, {"팔레": 0, "페일스": 0}, {"팔레": 5, "페일스": 5})["source"] == "needs_human"
    assert decide(C, {"팔레": 0, "페일스": 0}, {"팔레": 0, "페일스": 0})["source"] == "needs_human"


def test_count_terms_counts_overlapping_forms_independently():
    assert count_terms(["팔레와 페일스, 팔레."], ["팔레", "페일스"]) == {"팔레": 2, "페일스": 1}
