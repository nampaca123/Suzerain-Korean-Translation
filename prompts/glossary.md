# 용어집 (자동 생성: build_glossary.py)

원칙: 메인 캠페인 출현 표기만 표준. `needs_human`은 에이전트가 원문 그대로 두고 보고한다.
`자동 치환 = 아니오`인 항목은 일괄 치환 금지(금지 표기가 일반 낱말과 겹칠 수 있다). 문맥을 보고 고치거나 보고만 한다.

| 개념 | 영문 | 표준 | 금지 | 근거 | 자동 치환 | 소르들란드 출현 | Rizia 출현 |
|---|---|---|---|---|---|---|---|
| St. Wruhec (성인 이름) | St. Wruhec | 성 브루헤지 | 성 브루헤크, 성 루헥, 성 브루헥 | sordland | 예 | {'성 브루헤지': 7, '성 브루헤크': 0, '성 루헥': 0, '성 브루헥': 0} | {'성 브루헤지': 7, '성 브루헤크': 110, '성 루헥': 11, '성 브루헥': 0} |
| Wruhec 종교 | Wruhec | 브루헤지교 | 브루헤크교 | sordland | 예 | {'브루헤크교': 0, '브루헤지교': 33} | {'브루헤크교': 18, '브루헤지교': 761} |
| Golcondism | Golcondism | 골콘다주의 | 골콘다교, 골콘디즘 | sordland | 예 | {'골콘다교': 0, '골콘디즘': 0, '골콘다주의': 50} | {'골콘다교': 61, '골콘디즘': 10, '골콘다주의': 467} |
| House of Delegates | House of Delegates | 대의회 | 대의원회 | sordland | 예 | {'대의회': 1, '대의원회': 0} | {'대의회': 493, '대의원회': 68} |
| Alliance of Nations | Alliance of Nations | 국제연합 | AN, 국가연합 | sordland | 예 | {'국제연합': 113, 'AN': 24, '국가연합': 0} | {'국제연합': 231, 'AN': 353, '국가연합': 0} |
| WHR | WHR | 인권감시단 | WHR | sordland | 예 | {'인권감시단': 19, 'WHR': 0} | {'인권감시단': 5, 'WHR': 9} |
| Gasom | Gasom | 가솜 | Gasom, GASOM | sordland | 예 | {'가솜': 726, 'Gasom': 338, 'GASOM': 1} | {'가솜': 41, 'Gasom': 14, 'GASOM': 9} |
| OMEC | OMEC | 메르코파경제개발기구 | OMEC, 메르코파 경제개발기구 | sordland | 예 | {'메르코파경제개발기구': 28, '메르코파 경제개발기구': 0, 'OMEC': 19} | {'메르코파경제개발기구': 14, '메르코파 경제개발기구': 18, 'OMEC': 30} |
| GRACE | Guild of Royal Allies for Commercial Exchange | GRACE | 상호무역 왕실연합 길드, 왕실 동맹국 상업 교류 길드 | sordland | 예 | {'GRACE': 8, '상호무역 왕실연합 길드': 0, '왕실 동맹국 상업 교류 길드': 0} | {'GRACE': 310, '상호무역 왕실연합 길드': 13, '왕실 동맹국 상업 교류 길드': 1} |
| Rizia Imperii | Rizia Imperii | 리치아 임페리이 | 리치아 임페리 | rizia_majority | 아니오(보고만) | {'리치아 임페리이': 0, '리치아 임페리': 0} | {'리치아 임페리이': 95, '리치아 임페리': 7} |
| Pales | Pales | 팔레 | 페일스 | sordland | 예 | {'팔레': 26, '페일스': 0} | {'팔레': 3014, '페일스': 19} |
| Prime Minister | Prime Minister | 총리 | 수상, 재상 | sordland | 아니오(보고만) | {'총리': 153, '수상': 126, '재상': 0} | {'총리': 662, '수상': 112, '재상': 164} |
| Duke Reinhart | Duke Reinhart | 레이나르트 대공 | 레이나르트 공작 | sordland | 예 | {'레이나르트 공작': 0, '레이나르트 대공': 1} | {'레이나르트 공작': 250, '레이나르트 대공': 43} |
| Butler | Butler | 집사 | 시종 | sordland | 아니오(보고만) | {'집사': 8, '시종': 1} | {'집사': 113, '시종': 56} |
| Grand Wiseman | Grand Wiseman | 대현사 | 이그나시우스 현자 | rizia_majority | 아니오(보고만) | {'대현사': 0, '이그나시우스 현자': 0} | {'대현사': 295, '이그나시우스 현자': 5} |
| late King Valero | late King Valero | 선왕 | 부왕 | rizia_majority | 아니오(보고만) | {'선왕': 0, '부왕': 0} | {'선왕': 69, '부왕': 3} |
| Grand Hall | Grand Hall | 대연회장 | 대회랑, 대전당 | rizia_majority | 아니오(보고만) | {'대전당': 0, '대연회장': 0, '대회랑': 0} | {'대전당': 5, '대연회장': 12, '대회랑': 8} |
| profit share | profit share | 수익 분배 | 이익 배분, 이익 지분, 수익 배분, 수익 몫, 이익 공유, 이익 분배 | user_decision | 예 | {'수익 분배': 3, '이익 배분': 0, '이익 지분': 0, '수익 배분': 0, '수익 몫': 0, '이익 공유': 0, '이익 분배': 0} | {'수익 분배': 0, '이익 배분': 1, '이익 지분': 2, '수익 배분': 2, '수익 몫': 2, '이익 공유': 0, '이익 분배': 0} |
| Armed Forces | Rizian Armed Forces | 리치아 육군 | 리치아 국군, 리치아군 | user_decision | 아니오(보고만) | {'리치아 국군': 0, '리치아군': 0, '리치아 육군': 0} | {'리치아 국군': 0, '리치아군': 97, '리치아 육군': 82} |
| Mouser | Mouser | 무세르 | 모우세르 | rizia_majority | 아니오(보고만) | {'무세르': 0, '모우세르': 0} | {'무세르': 17, '모우세르': 9} |
| Kabet | Kabet | 카베테 | 카베트 | sordland | 예 | {'카베트': 0, '카베테': 1} | {'카베트': 11, '카베테': 13} |
| Karanza | Karanza | 카란자 | 카란자스 | user_decision | 예 | {'카란자': 0, '카란자스': 0} | {'카란자': 9, '카란자스': 9} |
| Nur 종교 | Nurist religion | 누리티교 | 누리교, 누르교 | sordland | 예 | {'누리티교': 63, '누르교': 0, '누리교': 1} | {'누리티교': 148, '누르교': 23, '누리교': 6} |
| Dastnur 종교 | Dastnurist religion | 다스트누리티교 | 다스트누리교 | sordland | 예 | {'다스트누리티교': 36, '다스트누리교': 1} | {'다스트누리티교': 381, '다스트누리교': 0} |
| Halaita(의례어) | Halaita | 할라이타 | Halaita | user_decision | 예 | {'할라이타': 0, 'Halaita': 0} | {'할라이타': 40, 'Halaita': 43} |
| Van Hoorten (인명) | Van Hoorten | 판호르턴 | 판 호르턴, 판 호르텐, 판판호르턴, 반 판판호르턴 | sordland | 예 | {'판호르턴': 66, '판 호르턴': 1, '판 호르텐': 0, '판판호르턴': 0, '반 판판호르턴': 0} | {'판호르턴': 12, '판 호르턴': 0, '판 호르텐': 0, '판판호르턴': 6, '반 판판호르턴': 2} |
| Drazon | Drazon | 드라촌 | 드라존 | sordland | 예 | {'드라존': 1, '드라촌': 7} | {'드라존': 655, '드라촌': 2} |
| Wiscerer (직함) | Wiscerer | 위스세러 | 위스케러, 위스커러 | rizia_majority | 아니오(보고만) | {'위스세러': 0, '위스케러': 0, '위스커러': 0} | {'위스세러': 10, '위스케러': 4, '위스커러': 0} |
| Crown Supreme Campaign | Crown Supreme Campaign | 왕실 선양 캠페인 | 크라운 슈프림 캠페인, 왕실 최고 캠페인, 왕실 선전 | user_decision | 예 | {'왕실 선양 캠페인': 0, '크라운 슈프림 캠페인': 0, '왕실 최고 캠페인': 0, '왕실 선전': 0} | {'왕실 선양 캠페인': 0, '크라운 슈프림 캠페인': 4, '왕실 최고 캠페인': 2, '왕실 선전': 3} |
| Walker Plan | Walker Plan | 워커 플랜 | 워커플랜 | user_decision | 예 | {'워커 플랜': 1, '워커플랜': 0} | {'워커 플랜': 6, '워커플랜': 4} |
| Glovurius axa Rizia (구호) | Glovurius axa Rizia | 글로부리우스 악사 리치아 | Glovurius axa Rizia | user_decision | 예 | {'글로부리우스 악사 리치아': 0, 'Glovurius axa Rizia': 0} | {'글로부리우스 악사 리치아': 52, 'Glovurius axa Rizia': 0} |
| Lachaven (도시) | Lachaven | 라지하벤 | 라카벤, 라차벤 | sordland | 예 | {'라지하벤': 387, '라카벤': 0, '라차벤': 0} | {'라지하벤': 4, '라카벤': 5, '라차벤': 2} |
| Sourne (지명) | Sourne | 소우르네 | 소우른 | sordland | 예 | {'소우르네': 4, '소우른': 0} | {'소우르네': 2, '소우른': 2} |
| Artor Wisci (인명) | Artor Wisci | 아르토르 비스지 | 아르토르 위시 | sordland | 예 | {'아르토르 비스지': 26, '아르토르 위시': 0} | {'아르토르 비스지': 0, '아르토르 위시': 2} |
| United Sordland Party | United Sordland Party | 소르들란드통합당 | 소르들란드 통합당, 통합 소르들란드당 | sordland | 예 | {'소르들란드통합당': 199, '소르들란드 통합당': 12, '통합 소르들란드당': 0} | {'소르들란드통합당': 0, '소르들란드 통합당': 2, '통합 소르들란드당': 2} |
| Deivid Wisci (인명) | Deivid Wisci | 데이비드 비스지 | 데이비드 위시, 데이비드 위스치 | sordland | 예 | {'데이비드 비스지': 23, '데이비드 위시': 0, '데이비드 위스치': 0} | {'데이비드 비스지': 0, '데이비드 위시': 3, '데이비드 위스치': 1} |
| NSWNP (베흘렌 여당) | Nurist Socialist Wehlen Nationalist Party | 누리티교 사회주의 베흘렌 민족주의당 | 누리티교사회주의베흘렌민족주의당, 누리스트 사회주의 베흘렌 민족주의당 | user_decision | 예 | {'누리티교사회주의베흘렌민족주의당': 0, '누리티교 사회주의 베흘렌 민족주의당': 0, '누리스트 사회주의 베흘렌 민족주의당': 0} | {'누리티교사회주의베흘렌민족주의당': 3, '누리티교 사회주의 베흘렌 민족주의당': 0, '누리스트 사회주의 베흘렌 민족주의당': 2} |
| United Contana | United Contana | 콘타나 연방 | 통일 콘타나, 연합 콘타나, 콘타나 연합 | sordland | 예 | {'콘타나 연방': 357, '통일 콘타나': 0, '연합 콘타나': 0, '콘타나 연합': 0} | {'콘타나 연방': 52, '통일 콘타나': 32, '연합 콘타나': 22, '콘타나 연합': 1} |
| Haelm (지명) | Haelm | 헬름 | 하엘름 | sordland | 예 | {'헬름': 17, '하엘름': 0} | {'헬름': 9, '하엘름': 1} |
| Nines (인명) | Ephraim Nines | 니네스 | 나인스 | sordland | 예 | {'니네스': 16, '나인스': 0} | {'니네스': 20, '나인스': 17} |
| President Nines (국제연합 총회 의장) | President Nines | 니네스 의장 | 니네스 대통령 | sordland | 예 | {'니네스 의장': 11, '니네스 대통령': 0} | {'니네스 의장': 2, '니네스 대통령': 12} |
| Royal Decree (칙령/왕령) | Royal Decree | 왕령 | 칙령 | user_decision | 예 | {'왕령': 0, '칙령': 1} | {'왕령': 550, '칙령': 214} |
| Beatrice 친족어(비나→베아트리체) | Aunt Bea | 베아 이모 | 베아 고모 | user_decision | 예 | {'베아 이모': 0, '베아 고모': 0} | {'베아 이모': 11, '베아 고모': 6} |
| Beatrice 친족어 2 | Aunt Beatrice | 베아트리체 이모 | 베아트리체 고모 | user_decision | 예 | {'베아트리체 이모': 0, '베아트리체 고모': 0} | {'베아트리체 이모': 0, '베아트리체 고모': 0} |
| Captain Gordion (금위대장) | Captain Gordion | 고르디온 대장 | 고르디온 대위 | user_decision | 예 | {'고르디온 대장': 0, '고르디온 대위': 0} | {'고르디온 대장': 53, '고르디온 대위': 98} |
| noble houses (귀족 가문) | noble houses | 귀족 가문들 | 왕가들 | user_decision | 예 | {'귀족 가문들': 0, '왕가들': 0} | {'귀족 가문들': 40, '왕가들': 49} |
| Councilor of War and Internal Security | Councilor of War and Internal Security | 전쟁·안보 평의원 | 전쟁 및 국내안보 평의원, 전쟁·안보 대의원, 전쟁·안보 담당 평의원, 전쟁·내부안보 왕실 평의원, 전쟁·내부안보 왕실평의원, 전쟁·안보 왕실평의원, 전쟁·내무안보 대의원, 전쟁·내무 평의원 | user_decision | 예 | {'전쟁·안보 평의원': 0, '전쟁 및 국내안보 평의원': 0, '전쟁·안보 대의원': 0, '전쟁·안보 담당 평의원': 0, '전쟁·내부안보 왕실 평의원': 0, '전쟁·내부안보 왕실평의원': 0, '전쟁·안보 왕실평의원': 0, '전쟁·내무안보 대의원': 0, '전쟁·내무 평의원': 0} | {'전쟁·안보 평의원': 33, '전쟁 및 국내안보 평의원': 17, '전쟁·안보 대의원': 8, '전쟁·안보 담당 평의원': 7, '전쟁·내부안보 왕실 평의원': 5, '전쟁·내부안보 왕실평의원': 1, '전쟁·안보 왕실평의원': 1, '전쟁·내무안보 대의원': 5, '전쟁·내무 평의원': 1} |
| King Romus (호칭) | King Romus | 로무스 국왕 | 로무스 왕 | sordland | 예 | {'로무스 국왕': 8, '로무스 왕': 1} | {'로무스 국왕': 590, '로무스 왕': 6} |
| MITZ (메프티엠 국제무역지대) | Meftiem International Trade Zone | 메프티엠 국제무역지대 | 메프티엠 국제 무역 지대, 메프티엠 국제 무역지대 | user_decision | 예 | {'메프티엠 국제무역지대': 0, '메프티엠 국제 무역 지대': 0, '메프티엠 국제 무역지대': 0} | {'메프티엠 국제무역지대': 83, '메프티엠 국제 무역 지대': 12, '메프티엠 국제 무역지대': 4} |
| International Trade Zone (약칭) | International Trade Zone | 국제무역지대 | 국제 무역 지대, 국제 무역지대 | user_decision | 예 | {'국제무역지대': 0, '국제 무역 지대': 0, '국제 무역지대': 0} | {'국제무역지대': 5, '국제 무역 지대': 7, '국제 무역지대': 0} |
| PaleStream (가스관·사업명) | PaleStream | 페일스트림 | PaleStream, 팔레스트림 | user_decision | 예 | {'페일스트림': 0, 'PaleStream': 0, '팔레스트림': 0} | {'페일스트림': 13, 'PaleStream': 8, '팔레스트림': 2} |
| intelligence hub (정보거점) | intelligence hub | 정보거점 | 정보 거점 | user_decision | 예 | {'정보거점': 0, '정보 거점': 0} | {'정보거점': 9, '정보 거점': 9} |
| Rumburg (국명) | Rumburg | 룸부르크 | 룸버그 | sordland | 예 | {'룸부르크': 1033, '룸버그': 0} | {'룸부르크': 961, '룸버그': 9} |
| South Merkopa (지역) | South Merkopa | 남메르코파 | 남부 메르코파 | user_decision | 예 | {'남메르코파': 2, '남부 메르코파': 2} | {'남메르코파': 179, '남부 메르코파': 19} |
| Queen Lucita (왕비) | Queen Lucita | 루시타 왕비 | 루시타 여왕 | user_decision | 예 | {'루시타 왕비': 0, '루시타 여왕': 0} | {'루시타 왕비': 7, '루시타 여왕': 10} |
| Golden Gate (의회 정문) | Golden Gate | 황금문 | 골든 게이트 | user_decision | 예 | {'황금문': 0, '골든 게이트': 0} | {'황금문': 3, '골든 게이트': 0} |
| Silver Gate (의회 문) | Silver Gate | 은문 | 실버 게이트 | user_decision | 예 | {'은문': 0, '실버 게이트': 0} | {'은문': 1, '실버 게이트': 4} |
| shell corporation | shell corporation | 페이퍼 컴퍼니 | 유령회사, 유령 회사 | user_decision | 예 | {'페이퍼 컴퍼니': 0, '유령회사': 0, '유령 회사': 0} | {'페이퍼 컴퍼니': 8, '유령회사': 4, '유령 회사': 0} |
| A proso (리치아어 구호) | A proso | 아 프로소 | A proso, A Proso | user_decision | 예 | {'아 프로소': 0, 'A proso': 0, 'A Proso': 0} | {'아 프로소': 4, 'A proso': 0, 'A Proso': 0} |
| Heart of Sordland (기구명) | Heart of Sordland | 소르들란드의 심장 | 하트 오브 소르들란드 | user_decision | 예 | {'소르들란드의 심장': 0, '하트 오브 소르들란드': 0} | {'소르들란드의 심장': 0, '하트 오브 소르들란드': 2} |
| Duchess Azaro (루시타 작위) | Duchess Azaro | 아자로 여공작 | 아자로 공작부인, 아자로 공작 | user_decision | 예 | {'아자로 여공작': 0, '아자로 공작부인': 0, '아자로 공작': 0} | {'아자로 여공작': 40, '아자로 공작부인': 153, '아자로 공작': 28} |
| Camp Domus (군 기지) | Camp Domus | 캠프 도무스 | 도무스 훈련소, 도무스 캠프 | user_decision | 예 | {'캠프 도무스': 0, '도무스 훈련소': 0, '도무스 캠프': 0} | {'캠프 도무스': 27, '도무스 훈련소': 7, '도무스 캠프': 1} |
| National Defense Headquarters | National Defense Headquarters | 국가 국방본부 | 국가 방위 본부 | user_decision | 예 | {'국가 국방본부': 0, '국가 방위 본부': 0} | {'국가 국방본부': 10, '국가 방위 본부': 2} |
| Supreme Council of Nur | Supreme Council of Nur | 누르 최고평의회 | 누리티교 최고평의회 | user_decision | 예 | {'누르 최고평의회': 0, '누리티교 최고평의회': 0} | {'누르 최고평의회': 8, '누리티교 최고평의회': 0} |
| Duchess of Valenqiris (비나 작위) | Duchess of Valenqiris | 발렌키리스 여공작 | 발렌키리스 공작부인, 발렌키리스의 여공작, 발렌키리스의 공작부인 | user_decision | 예 | {'발렌키리스 여공작': 0, '발렌키리스 공작부인': 0, '발렌키리스의 여공작': 0, '발렌키리스의 공작부인': 0} | {'발렌키리스 여공작': 3, '발렌키리스 공작부인': 18, '발렌키리스의 여공작': 1, '발렌키리스의 공작부인': 0} |
| Ax populat Rizati (구호) | Ax populat Rizati | 악스 포풀라트 리차티 | Ax populat Rizati | user_decision | 예 | {'악스 포풀라트 리차티': 0, 'Ax populat Rizati': 0} | {'악스 포풀라트 리차티': 0, 'Ax populat Rizati': 0} |
| Queen Mother 극존칭 | Queen Mother | 왕대비 | 왕대비마마, 대비마마 | user_decision | 예 | {'왕대비': 1, '왕대비마마': 0, '대비마마': 0} | {'왕대비': 80, '왕대비마마': 67, '대비마마': 40} |
| Queen 극존칭 | Queen (마마) | 왕비 | 왕비마마 | user_decision | 예 | {'왕비': 0, '왕비마마': 0} | {'왕비': 103, '왕비마마': 5} |
| Princess 극존칭 | Princess (마마) | 공주 전하 | 공주마마 | user_decision | 예 | {'공주 전하': 0, '공주마마': 0} | {'공주 전하': 95, '공주마마': 5} |
| Countess Leona Sazon (본인 작위) | Countess Leona Sazon | 레오나 사존 여백작 | 레오나 사존 백작부인, 레오나 백작부인, 사존 백작부인 | user_decision | 예 | {'레오나 사존 여백작': 0, '레오나 사존 백작부인': 0, '레오나 백작부인': 0, '사존 백작부인': 0} | {'레오나 사존 여백작': 0, '레오나 사존 백작부인': 5, '레오나 백작부인': 2, '사존 백작부인': 1} |
| Museum Mile (박물관 거리) | Museum Mile | 박물관 거리 | 뮤지엄 마일 | user_decision | 예 | {'박물관 거리': 0, '뮤지엄 마일': 0} | {'박물관 거리': 2, '뮤지엄 마일': 4} |
| Capital Police (수도 경찰) | Capital Police | 수도 경찰 | 수도경찰 | user_decision | 예 | {'수도 경찰': 0, '수도경찰': 0} | {'수도 경찰': 4, '수도경찰': 3} |
| Captain Castellanus (카스텔라누스 대장) | Captain Castellanus | 카스텔라누스 대장 | 카스텔라누스 대위 | user_decision | 예 | {'카스텔라누스 대장': 0, '카스텔라누스 대위': 0} | {'카스텔라누스 대장': 6, '카스텔라누스 대위': 9} |
| Palantor Security Solutions (팔란토르 시큐리티) | Palantor Security Solutions | 팔란토르 시큐리티 | 팔란토르 보안 솔루션 | user_decision | 예 | {'팔란토르 시큐리티': 2, '팔란토르 보안 솔루션': 0} | {'팔란토르 시큐리티': 8, '팔란토르 보안 솔루션': 2} |
| Wruhec (브루헤지, 단독형) | Wruhec | 브루헤지 | 브루헤크 | user_decision | 예 | {'브루헤지': 43, '브루헤크': 0} | {'브루헤지': 779, '브루헤크': 304} |
| Duchess Angelica Sazon (본인 작위) | Duchess Angelica Sazon | 안젤리카 사존 여공작 | 안젤리카 사존 공작부인, 안젤리카 여공작, 안젤리카 공작부인 | user_decision | 예 | {'안젤리카 사존 여공작': 0, '안젤리카 사존 공작부인': 0, '안젤리카 여공작': 0, '안젤리카 공작부인': 0} | {'안젤리카 사존 여공작': 3, '안젤리카 사존 공작부인': 2, '안젤리카 여공작': 4, '안젤리카 공작부인': 9} |
| Duchess Angelica (짧은 형) | Duchess Angelica | 안젤리카 여공작 | 안젤리카 공작부인 | user_decision | 예 | {'안젤리카 여공작': 0, '안젤리카 공작부인': 0} | {'안젤리카 여공작': 4, '안젤리카 공작부인': 9} |
| Duke Axel (악셀 대공) | Duke Axel | 악셀 대공 | 악셀 공작 | user_decision | 예 | {'악셀 대공': 0, '악셀 공작': 0} | {'악셀 대공': 0, '악셀 공작': 3} |
| Divus zaitu (리치아어 의례어) | Divus zaitu | 디부스 자이투 | Divus zaitu | user_decision | 예 | {'디부스 자이투': 0, 'Divus zaitu': 0} | {'디부스 자이투': 0, 'Divus zaitu': 8} |
| Bi mare volu (리치아어 의례어) | Bi mare volu | 비 마레 볼루 | Bi mare volu | user_decision | 예 | {'비 마레 볼루': 0, 'Bi mare volu': 0} | {'비 마레 볼루': 2, 'Bi mare volu': 12} |
| Ales Bay (알레스만) | Ales Bay | 알레스만 | 알레스 만 | user_decision | 예 | {'알레스만': 0, '알레스 만': 0} | {'알레스만': 3, '알레스 만': 2} |
| Archsanctuary (대성소) | Archsanctuary | 대성소 | 대신전 | user_decision | 예 | {'대성소': 30, '대신전': 0} | {'대성소': 303, '대신전': 14} |
| East Merkopa (동메르코파) | East Merkopa | 동메르코파 | 동부 메르코파 | user_decision | 예 | {'동메르코파': 43, '동부 메르코파': 13} | {'동메르코파': 56, '동부 메르코파': 14} |
| West Merkopa (서메르코파) | West Merkopa | 서메르코파 | 서부 메르코파 | user_decision | 예 | {'서메르코파': 2, '서부 메르코파': 0} | {'서메르코파': 4, '서부 메르코파': 2} |
| North Merkopa (북메르코파) | North Merkopa | 북메르코파 | 북부 메르코파 | user_decision | 예 | {'북메르코파': 0, '북부 메르코파': 0} | {'북메르코파': 1, '북부 메르코파': 4} |
| Duchess of Iza (이자 여공작) | Duchess of Iza | 이자 여공작 | 이자 공작부인 | user_decision | 예 | {'이자 여공작': 0, '이자 공작부인': 0} | {'이자 여공작': 0, '이자 공작부인': 11} |
| Golden Shield (황금 방패) | Golden Shield | 황금 방패 | 골든 실드 | user_decision | 예 | {'황금 방패': 0, '골든 실드': 0} | {'황금 방패': 14, '골든 실드': 12} |
| Agard (아가드) | Agard | 아가드 | 아가르드 | user_decision | 예 | {'아가드': 0, '아가르드': 5} | {'아가드': 15, '아가르드': 11} |
| Baroness de Rava (본인 작위) | Baroness de Rava | 데 라바 여남작 | 데 라바 남작부인 | user_decision | 예 | {'데 라바 여남작': 0, '데 라바 남작부인': 0} | {'데 라바 여남작': 0, '데 라바 남작부인': 26} |
| Duchess Vina (비나 여공작) | Duchess Vina | 비나 여공작 | 비나 공작부인 | user_decision | 예 | {'비나 여공작': 0, '비나 공작부인': 0} | {'비나 여공작': 0, '비나 공작부인': 3} |
| Nurist (형용사형, 누리티) | Nurist | 누리티 | 누리스트 | user_decision | 예 | {'누리티': 110, '누리스트': 0} | {'누리티': 567, '누리스트': 18} |
| opposition speaker | opposition speaker | 야당 대표 | 야당 의장 | user_decision | 예 | {'야당 대표': 7, '야당 의장': 0} | {'야당 대표': 14, '야당 의장': 7} |
| Valgish (민족명 단독형) | Valgish | 발그슬란드인 | 발그인, 발그족, 발기쉬 | user_decision | 예 | {'발그슬란드인': 11, '발그인': 1, '발그족': 0, '발기쉬': 0} | {'발그슬란드인': 9, '발그인': 3, '발그족': 1, '발기쉬': 1} |
| Central Police | Central Police | 중앙 경찰 | 중앙경찰 | user_decision | 예 | {'중앙 경찰': 0, '중앙경찰': 0} | {'중앙 경찰': 24, '중앙경찰': 16} |
| Antacean Sea | Antacean Sea | 안타케아해 | 안타시아해, 안타케아 해, 안타세아해 | user_decision | 예 | {'안타케아해': 7, '안타시아해': 0, '안타케아 해': 0, '안타세아해': 0} | {'안타케아해': 17, '안타시아해': 3, '안타케아 해': 2, '안타세아해': 22} |
| Sordland (MT 오기 솔드랜드) | Sordland | 소르들란드 | 솔드랜드 | user_decision | 예 | {'소르들란드': 6716, '솔드랜드': 0} | {'소르들란드': 521, '솔드랜드': 24} |
| Sords (MT 오기 솔드인) | Sords | 소르드인 | 솔드인 | user_decision | 예 | {'소르드인': 122, '솔드인': 0} | {'소르드인': 26, '솔드인': 11} |
| Trade Zone (단독형) | Trade Zone | 무역지대 | 무역 지대 | user_decision | 예 | {'무역지대': 1, '무역 지대': 1} | {'무역지대': 116, '무역 지대': 54} |
