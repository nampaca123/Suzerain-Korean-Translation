# 용어 표준 표기 결정 규칙(소르들란드 우선 → Rizia 다수 → needs_human)과 후보 출현 집계를 확인
from scripts.build_glossary import decide, count_terms, is_sordland_item

C = {"concept": "Pales", "en": "Pales", "candidates": ["팔레", "페일스"]}
PM = {"concept": "Prime Minister", "en": "Prime Minister", "candidates": ["총리", "수상"]}
AN = {"concept": "Alliance of Nations", "en": "Alliance of Nations", "candidates": ["국제연합", "AN"]}


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


def test_count_terms_gives_each_hit_to_the_longest_candidate():
    assert count_terms(["카란자스 가문과 카란자 가문."], ["카란자", "카란자스"]) == {"카란자": 1, "카란자스": 1}
    assert count_terms(["다스트누리교와 누리교"], ["누리교", "다스트누리교"]) == {"누리교": 1, "다스트누리교": 1}


def test_rizia_majority_needs_a_clear_margin():
    H = {"concept": "Halaita", "en": "Halaita", "candidates": ["할라이타", "Halaita"]}
    assert decide(H, {"할라이타": 0, "Halaita": 0}, {"할라이타": 40, "Halaita": 43})["source"] == "needs_human"
    I = {"concept": "Rizia Imperii", "en": "Rizia Imperii", "candidates": ["리치아 임페리이", "리치아 임페리"]}
    d = decide(I, {"리치아 임페리이": 0, "리치아 임페리": 0}, {"리치아 임페리이": 95, "리치아 임페리": 7})
    assert d["source"] == "rizia_majority" and d["standard"] == "리치아 임페리이"


def test_count_terms_mask_absorbs_other_concepts_hits():
    assert count_terms(["다스트누리티교와 누리티교."], ["누리티교", "누르교"],
                       mask=["다스트누리티교"]) == {"누리티교": 1, "누르교": 0}


def test_auto_replace_only_for_unambiguous_sordland_banned_forms():
    assert decide(C, {"팔레": 12, "페일스": 0}, {"팔레": 3, "페일스": 40})["auto_replace"] is True
    assert decide(AN, {"국제연합": 158, "AN": 28}, {"국제연합": 231, "AN": 353})["auto_replace"] is True
    assert decide(PM, {"총리": 175, "수상": 141}, {"총리": 662, "수상": 112})["auto_replace"] is False


def test_auto_replace_is_false_without_sordland_evidence():
    d = decide(C, {"팔레": 0, "페일스": 0}, {"팔레": 3, "페일스": 40})
    assert d["source"] == "rizia_majority" and d["auto_replace"] is False
    assert decide(C, {"팔레": 0, "페일스": 0}, {"팔레": 5, "페일스": 5})["auto_replace"] is False


def test_is_sordland_item_uses_path_only():
    assert is_sordland_item({"Path": "Sordland/News/Turn01", "AppBundleProperties": {"StoryPacks": ["StoryPack_Main"]}})
    assert not is_sordland_item({"Path": "Shared/Shared Codex Entries",
                                 "AppBundleProperties": {"StoryPacks": ["StoryPack_Main"]}})
    assert not is_sordland_item({"Path": "Rizia/News/Decision News",
                                 "AppBundleProperties": {"StoryPacks": ["StoryPack_Main", "StoryPack_Rizia"]}})
