# 종결 화계 분류기가 하오/해요/합쇼/해라/해/하게체와 서술문을 구분하는지 확인
import pytest
from scripts.register_classify import (classify, clause_registers, is_quoted, is_narrative, strip_markup,
                                       HAO, HAEYO, HAPSYO, HAERA, HAE, HAGE, OTHER)

@pytest.mark.parametrize("text,expected", [
    ('"평의회에 온 것을 환영하오, 공작부인."', HAO), ('"좀 더 존중을 보이는 게 좋겠소."', HAO),
    ('"그런 일은 없을 거요."', HAO), ('"내가 휴고에게 한 말을 들었잖소."', HAO), ('"셔츠를 바로 채우시오, 휴고."', HAO),
    ('"무슨 일로 오셨소?"', HAO), ('"아니오."', HAO), ('"그게 뭐요?"', HAO), ('"앉는 게 어떻겠소?"', HAO), ('"계속하시오."', HAO),
    ('"이런 일은 시간이 좀 걸리잖아요."', HAEYO), ('"괜찮으세요?"', HAEYO), ('"저는 신경 쓰지 마세요."', HAEYO),
    ('"관찰자로 참석했을 뿐이에요."', HAEYO), ('"그렇지 않나요?"', HAEYO), ('"제가 설득했어요."', HAEYO),
    ('"물론이죠."', HAEYO), ('"들려주셨으면 좋겠어요."', HAEYO), ('"자랑스럽군요."', HAEYO), ('"어떻게 하실 겁니까?"', HAPSYO),
    ('"두 분께 사과드립니다."', HAPSYO), ('"용서해주십시오."', HAPSYO), ('"여쭤봐도 되겠습니까?"', HAPSYO),
    ('"명백한 침략 행위였습니다."', HAPSYO), ('"그렇게 말할 줄 알았습니다."', HAPSYO), ('"즉시 처리하겠습니다, 폐하."', HAPSYO),
    ('"의인의 길을 보여주겠습니다!"', HAPSYO), ('"받아주십시오."', HAPSYO), ('"저희가 도움이 되기를 바랍니다."', HAPSYO), ('"아름다운 배입니다."', HAPSYO),
    ('"둘 다 제정신이냐?"', HAERA), ('"국왕이 말하라고 명한다."', HAERA), ('"둘 다 어서 말해 보거라."', HAERA),
    ('"왜 말하지 않았니?"', HAERA), ('"기억해라."', HAERA), ('"충고하마."', HAERA), ('"짚었구나."', HAERA), ('"네 마음대로 하렴."', HAERA),
    ('"함께 오라고 했다."', HAERA), ('"나는 내 권력을 넘겼다."', HAERA), ('"가자."', HAERA),
    ('"펜만 쥐여 줘."', HAE), ('"그게 아니야."', HAE), ('"세월의 흔적이 보이기 시작했지."', HAE), ('"괜찮아?"', HAE),
    ('"그만해."', HAE), ('"몸매를 망칠 가치가 있겠지."', HAE), ('"내가 갈게."', HAE), ('"모르겠어."', HAE), ('"그래."', HAE), ('"안 될 거야."', HAE),
    ('"모두 참석해줘서 고맙네."', HAGE), ('"어서 오게."', HAGE), ('"알겠네, 폐하."', HAGE), ('"자네가 맡게."', HAGE),
    ('"그런가."', HAGE), ('"어찌 생각하나?"', HAGE), ('"수고했네."', HAGE), ('"기쁘군."', HAGE), ('"그렇게 하세."', HAGE), ('"오게나."', HAGE),
    ('그는 웃었다.', HAERA), ('휴고는 황급히 셔츠 단추를 다시 채웠다.', HAERA), ('나는 손을 들어 경례했다.', HAERA),
    ('"흠..."', OTHER), ('1905|몬키즈|리치아 왕국', OTHER), ('"..."', OTHER), ('"폐하--"', OTHER), ('"저희 둘이 살라베스에서..."', OTHER),
    ('"어서 오게, 폐하."', HAGE), ('"어서 오십시오, 폐하."', HAPSYO), ('"그렇게 하고 있습니다."', HAPSYO),
    ('"고맙소, 베르너 씨, 에스퀴벨 씨."', HAO),
    ('"왕명일세."', HAGE), ('"발그슬란드가 가만있지 않을 걸세."', HAGE), ('"덧붙이고 싶은 말이라도 있나?"', HAGE),
    ('"다음에 봅시다."', HAO), ('"당장 시추를 시작합시다!"', HAO),
    ('"평의회는 공주가 있을 곳이 아니다."', HAERA), ('"누구보다 잘 아니까."', HAE), ('"신경 쓰지 말게."', HAGE),
])
def test_classify(text, expected):
    assert classify(text) == expected

def test_multiline_uses_last_line():
    assert classify('첫 줄이다.\n\n"마지막은 해요체예요."') == HAEYO

def test_clause_registers_mixed():
    assert clause_registers('"팔레를 최우선으로 삼았소. 하지만 우리는 많은 것을 잃었지."') == [HAO, HAE]
    assert clause_registers('"팔레를 삼았소. 많은 것을 잃었지."') == [HAO, HAE]

def test_is_quoted_and_narrative():
    assert is_quoted('"안녕."') and is_quoted('“안녕.”') and not is_quoted('그는 웃었다.')
    assert is_narrative('그는 웃었다.') and not is_narrative('"제정신이냐?"')
    assert is_narrative('그것은 우연이 아니다.') is True

def test_strip_markup():
    assert strip_markup('"*그거야말로* 좋소." [-1 예산]') == '그거야말로 좋소.'


def test_vocative_title_is_not_ending():
    assert classify("고맙소, 최고 대현자.") == HAO
    assert classify("최고 대현자") == OTHER
    assert classify("어서 가자.") == HAERA


def test_guryeo_is_hao():
    assert classify("아아, 오늘은 주께서 우리를 축복하지 않으셨구려.") == HAO
