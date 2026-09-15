# 로무스 대사 중 '연설 부분'과 '연설 중 주변 대화'를 구분한다(spec 5.1 판정 순서).
# 연설 시작 표지는 1인칭 주어(나는/내가)가 무대에 서는 서술만 인정한다(취재진 카메라·타인의 연단 오탐 방지).
import re

_CROWD = re.compile(r"(여러분|들이여|신민이여)")
_START = re.compile(
    r"(?<![가-힣])(나는|내가)[^.!?]{0,30}"
    r"(마이크|연단 뒤|연단으로|연단에 서|연단에 올|카메라 렌즈|붉은 표시등|말을 시작했다|대국민 연설)"
)
_END = re.compile(r"(연설을 마치|원고를 내려놓|촬영이 멈|환호가 터져|박수가|연단에서 내려|무대에서 내려)")
_SINGULAR = re.compile(r"(폐하|비나|어머니|사존 씨|숙부|공작|총리|대통령|여왕)")


def tag_speech(rows: list[dict]) -> dict[str, str]:
    out: dict[str, str] = {}
    in_window = False
    prev_conv = None
    for r in sorted(rows, key=lambda x: (x["conv_id"], x["seq"])):
        ko, actor = r["ko"], r["actor"]
        if r["conv_id"] != prev_conv:
            in_window = False
            prev_conv = r["conv_id"]
        if "HODShutdown" in r["conv_title"]:
            out[r["key"]] = "none"
            continue
        if actor == "Narrator":
            if _END.search(ko):
                in_window = False
            elif _START.search(ko):
                in_window = True
            out[r["key"]] = "none"
            continue
        if actor != "Player_Romus":
            out[r["key"]] = "none"
        elif _CROWD.search(ko):
            out[r["key"]] = "speech"
        elif in_window:
            out[r["key"]] = "aside" if _SINGULAR.search(ko) else "speech"
        else:
            out[r["key"]] = "none"
    return out
