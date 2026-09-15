from scripts.speech_detect import tag_speech


def R(key, actor, ko, seq, title="Rizia/Turn 6/A_PalaceBalconySpeech"):
    return {"key": key, "actor": actor, "ko": ko, "seq": seq, "conv_id": 372, "conv_title": title}


def test_marker_window_and_vocative():
    rows = [R("a", "Player_Romus", '"오늘은 축하할 날이오."', 0),
            R("b", "Narrator", "나는 발코니로 나가 마이크 앞에 섰다.", 1),
            R("c", "Player_Romus", '"오늘 우리는 엄숙한 의무 아래 하나로 섰소."', 2),
            R("d", "Player_Romus", '"리치아 국민 여러분."', 3),
            R("e", "Hugo Toras", '"폐하, 잘하고 계십니다."', 4),
            R("f", "Player_Romus", '"고맙소, 숙부님."', 5),
            R("g", "Narrator", "연설을 마치자 광장에서 환호가 터져 나왔다.", 6),
            R("h", "Player_Romus", '"이제 들어갑시다."', 7)]
    assert tag_speech(rows) == {"a": "none", "b": "none", "c": "speech", "d": "speech", "e": "none",
                                "f": "aside", "g": "none", "h": "none"}


def test_vocative_outside_window_is_speech():
    rows = [R("a", "Player_Romus", '"충성스러운 신민 여러분, 오늘 나는 선언합니다."', 0, "Rizia/Turn 11/Ending_Speech")]
    assert tag_speech(rows) == {"a": "speech"}


def test_hod_shutdown_never_speech():
    rows = [R("a", "Player_Romus", '"여러분, 이 의회는 해산한다."', 0, "Rizia/Turn 10/HODShutdown")]
    assert tag_speech(rows) == {"a": "none"}


def test_press_scrum_camera_does_not_open_window():
    rows = [R("a", "Narrator", "페를라에 도착하자 언론진이 카메라와 마이크를 내 쪽으로 들이밀었다.", 0),
            R("b", "Player_Romus", '"페를라는 언제나 인상적이오."', 1)]
    assert tag_speech(rows) == {"a": "none", "b": "none"}


def test_sitting_at_podium_does_not_open_window():
    rows = [R("a", "Narrator", "휴고와 나는 평소 앉던 연단의 자리에 앉았다.", 0, "Rizia/Turn 8/A_HouseOfDelegates3"),
            R("b", "Player_Romus", '"그가 고통받는 모습을 기대하고 있소."', 1, "Rizia/Turn 8/A_HouseOfDelegates3")]
    assert tag_speech(rows) == {"a": "none", "b": "none"}


def test_name_ending_with_naneun_is_not_first_person():
    rows = [R("a", "Narrator", "살타나는 다시 한번 마이크를 두드렸다.", 0),
            R("b", "Player_Romus", '"계속 진행합시다."', 1)]
    assert tag_speech(rows) == {"a": "none", "b": "none"}


def test_leaving_podium_closes_window():
    rows = [R("a", "Narrator", "나는 연단으로 향했다.", 0),
            R("b", "Player_Romus", '"리치아는 합의를 지켜왔소."', 1),
            R("c", "Narrator", "내가 연단에서 내려오자 청중이 박수를 보냈다.", 2),
            R("d", "Player_Romus", '"이제 돌아갑시다."', 3)]
    assert tag_speech(rows) == {"a": "none", "b": "speech", "c": "none", "d": "none"}


def test_plain_mention_of_subjects_is_not_speech():
    rows = [R("a", "Player_Romus", '"내 신민은 모두 나를 사랑해."', 0, "Rizia/Turn 3/Public Opinion")]
    assert tag_speech(rows) == {"a": "none"}


def test_broadcast_cue_opens_window():
    rows = [R("a", "Narrator", "감독이 고개를 끄덕이자 붉은 표시등이 켜졌고, 나는 말을 시작했다.", 0, "Rizia/Turn 11/Ending_Speech"),
            R("b", "Player_Romus", '"오늘 나는 무거운 마음으로 이 자리에 섰습니다."', 1, "Rizia/Turn 11/Ending_Speech"),
            R("c", "Narrator", "나는 촬영진에게 고개를 끄덕였다. 촬영이 멈췄다.", 2, "Rizia/Turn 11/Ending_Speech"),
            R("d", "Player_Romus", '"수고했소."', 3, "Rizia/Turn 11/Ending_Speech")]
    assert tag_speech(rows) == {"a": "none", "b": "speech", "c": "none", "d": "none"}
