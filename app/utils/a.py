import sqlite3

# Connect to the database (this will create a new one if it doesn't exist)
conn = sqlite3.connect('/root/AiSK-backend/demo.db')
cur = conn.cursor()

# Create restaurants table
cur.execute('''
CREATE TABLE IF NOT EXISTS restaurants
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    ADDRESS TEXT,
    LAT REAL,
    LNG REAL,
    PHONE TEXT,
    TYPE TEXT,
    URL TEXT,
    INFO TEXT,
    MENU_ID INTEGER,
    OPEN_HR_INFO TEXT,
    IMAGE_URL TEXT
    )
''')

# Create MenuItems table
cur.execute('''
CREATE TABLE IF NOT EXISTS MenuItems
    (ITEM_ID INTEGER ,
    MENU_ID INTEGER,
    ITEM_NM TEXT,
    ITEM_PRICE INTEGER,
    ITEM_INFO TEXT,
    IMAGE_URL TEXT,
    P_KEY INTEGER PRIMARY KEY AUTOINCREMENT
    )
''')

# Insert Tom N Toms KAIST branch
cur.execute('''
INSERT INTO restaurants 
(NAME, ADDRESS, PHONE, TYPE, URL, INFO, OPEN_HR_INFO, MENU_ID,LAT,LNG)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
'탐앤탐즈 카이스트점',
'KAIST 김병호IT융합빌딩(N1) 2층',
'042-350-0871',
'커피, 음료, 티, 스무디, 프레즐, 피자, 베이커리 등',
'https://www.tomntoms.com/',
'탐앤탐즈(Tom N Toms)는 대한민국을 대표하는 카페 브랜드 중 하나로, 2001년 서울에서 첫 매장을 오픈했습니다. 탐앤탐즈는 "우리나라 사람들이 사랑하는 커피 한 잔의 여유와 행복"을 제공하기 위해 설립되었습니다. 현재 탐앤탐즈는 한국을 넘어 전 세계적으로 매장을 확장하며 많은 사람들에게 사랑받고 있습니다.\n탐앤탐즈는 다양한 커피와 음료, 베이커리 메뉴를 통해 고객들에게 다채로운 선택을 제공하고 있습니다. 프리미엄 원두를 사용한 고품질 커피와 함께 독창적인 스무디, 에이드, 티, 프레첼, 베이커리 제품들이 큰 인기를 끌고 있습니다. 특히 탐앤탐즈의 프레첼은 고유의 맛과 식감으로 많은 고객들에게 사랑받고 있는 대표 메뉴 중 하나입니다.\n탐앤탐즈는 지속 가능한 경영을 실천하고 있으며, 친환경적인 매장 운영과 함께 사회 공헌 활동에도 적극적으로 참여하고 있습니다. 지역 사회와의 협력을 통해 다양한 봉사 활동을 펼치고 있으며, 친환경 제품을 사용한 지속 가능한 매장 운영을 추구하고 있습니다.',
'평일 7:00~22:00 / 주말,방학 10:00~21:00 / 공휴일 10:00~17:00',
1,
36.37411354630935,
127.3657233813467
))

# show all table
cur.execute('SELECT * FROM restaurants')
cur.fetchall()
# Insert 온천 칼국수
cur.execute('''
INSERT INTO restaurants 
(NAME, ADDRESS, PHONE, TYPE, URL, INFO, OPEN_HR_INFO, MENU_ID,LAT,LNG)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
'온천 칼국수',
'대전 유성구 온천북로 61',
'042-824-6668',
'칼국수, 쭈꾸미볶음, 한식',
'',
'온천 칼국수는 따뜻한 국물과 신선한 재료로 만든 다양한 메뉴를 통해 고객들에게 풍부한 맛과 만족을 제공하는 식당입니다.',
'영업시간: 11:00 - 21:30\n브레이크타임: 15:40 - 16:10\n라스트오더: 20:30',
2,
36.3564398,
127.3498409
))

# Insert menu items for Tom N Toms
tom_n_toms_menu = [
    ("블루 레몬 에이드", 6500, "상큼한 레몬과 달콤한 블루 큐라소 시럽이 어우러져 눈과 입을 동시에 즐겁게 하는 에이드입니다. 탄산수와 얼음이 더해져 시원하고 청량한 맛을 자랑합니다. 특별한 날 기분을 업 시켜줄 음료입니다.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_t9RjHMbg_20200728115655.png"),
    ("오리지널 흑당 버블티", 5500, "쫀득한 타피오카 펄과 달콤한 흑당 시럽이 만나 깊고 진한 맛을 내는 버블티입니다. 홍차와 우유가 더해져 부드러운 맛을 더하며, 얼음이 함께해 시원하고 상쾌한 음료입니다. 버블티 애호가들에게 추천하는 메뉴입니다.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_jBiJ7ueW_20200728024238.png"),
    ("허니 버터 브레드", 6500, "겉은 바삭하고 속은 쫄깃한 토스트에 풍부한 버터와 꿀이 어우러진 허니 버터 브레드입니다. 깊고 진한 카라멜 소스와 시나몬 파우더로 풍미를 더하고, 부드러운 생크림이 올려져 한층 더 달콤한 맛을 자랑합니다. 탐앤탐스의 베스트 메뉴로, 디저트로 즐기기에 완벽한 선택입니다.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_jzJciZXS_20200807024251.png"),
    ("아이스 아메리카노", 4900, "진한 에스프레소 샷에 시원한 물과 얼음이 더해져 깔끔하고 상쾌한 맛을 느낄 수 있는 아이스 아메리카노입니다. 에스프레소의 깊고 진한 맛을 그대로 즐길 수 있으며, 무더운 여름철에 마시기 좋은 커피 음료입니다.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_SvFITgHd_20200728122052.png"),
    ("아이스 카페 라떼", 5500, "진한 에스프레소 샷과 시원한 우유가 어우러진 아이스 라떼입니다. 부드럽고 고소한 우유 맛과 에스프레소의 진한 맛이 조화를 이루며, 얼음이 더해져 시원하게 즐길 수 있는 음료입니다. 여름철에 마시기 좋은 커피 음료로 추천합니다.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_cdsFXetN_20200728122111.png"),
    ("피자 또띠아", 6000, "얇고 바삭한 또띠아에 토마토 소스를 바르고, 신선한 모짜렐라 치즈와 다양한 재료들이 어우러져 풍부한 맛을 자랑하는 피자 또띠아입니다. 짭짤한 페퍼로니, 아삭한 양파와 파프리카, 올리브가 더해져 색다르고 맛있는 조화를 이룹니다. 간편하면서도 든든한 한 끼 식사로 추천하는 메뉴입니다.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_jpwPEyHK_20200828111543.png"),
    ("콜드브루 라떼", 5500, "탐앤탐스 스테디 샐러. 세련된 맛을 자랑하는 예가체프를 차갑게 브루잉한 메뉴를 우유와 함께 즐기세요.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/uploads/menu/24%C3%AD%C2%81%C2%B4%C3%AB%C2%9E%C2%98%C3%AC%C2%8B%C2%9D_%C3%AC%C2%BD%C2%9C%C3%AB%C2%93%C2%9C%C3%AB%C2%B8%C2%8C%C3%AB%C2%A3%C2%A8%C3%AB%C2%9D%C2%BC%C3%AB%C2%96%C2%BC_2000.png_1717981167292.png"),
    ("딸기주스", 6000, "딸기를 갈아 만든 영양만점 딸기주스.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_FE57VHyS_20200821052053.png"),
    ("곡성 멜론 스무디", 6500, "국산 곡성 멜론을 이용하여 만든 멜론 아이스크림 맛의 시원한 음료.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/menu/2038868156_ki5lpORn_20210607083543.png"),
    ("애플크림치즈 프레즐베이글", 6000, "상큼한 애플잼에 리치한 크림치즈가 특별함을 더하다! 더욱 맛있게 즐기고 싶으시다면 아메리카노와 함께 드셔보세요.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/uploads/menu/1698191798602.png"),
    ("스위트포테이토 프레즐베이글", 6000, "달달하고 고소하니 맛있구마! 부드러운 고구마 무스를 잔뜩 머금고 있어 입에 닿자마자 사르르 녹아내릴거에요.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/uploads/menu/1698191648334.png"),
    ("다크초코크림 프레즐베이글", 6000, "다크초콜릿과 크림치즈가 의외로 잘 어울린다는 사실! 달콤쌉싸름한 다크초콜릿과 크림치즈의 은은한 단맛을 한번에 느낄 수 있어요.", "https://kr.object.ncloudstorage.com/tomntoms-bucket/uploads/menu/1698191500163.png")
]


# Insert menu items for 온천 칼국수
oncheon_menu = [
    ("물총칼국수", 8500, "부드러운 칼국수 면과 신선한 물총이 어우러져 시원하고 깔끔한 맛을 자랑하는 칼국수입니다. 채소와 함께 끓여낸 육수는 깊고 풍부한 맛을 더해줍니다. 양도 넉넉하여 한 끼 식사로 충분합니다.", "https://ldb-phinf.pstatic.net/20201202_103/16068910066041OxaJ_JPEG/8mOrf82CYo3A8rWuNVUteeT4.jpg"),
    ("쭈꾸미볶음", 19000, "매콤하고 감칠맛 나는 쭈꾸미볶음은 신선한 쭈꾸미와 다양한 채소들이 어우러져 고소하고 매콤한 맛을 선사합니다. 양념은 깊고 진한 맛을 내며, 매운맛은 중간 정도로 즐길 수 있습니다.", "https://ldb-phinf.pstatic.net/20201202_189/1606891016097OXcYx_JPEG/7ZMcT8DPCRUuL3U0AzMn03yN.jpg"),
    ("물총탕", 14000, "신선한 물총을 사용한 물총탕은 깔끔하고 담백한 국물이 일품입니다. 무와 대파, 마늘이 더해져 깊고 진한 맛을 느낄 수 있으며, 청양고추로 약간의 매콤함을 더해줍니다. 시원하고 개운한 맛이 특징입니다.", "https://ldb-phinf.pstatic.net/20201202_216/1606891023289UHS0d_JPEG/uGoBL_HvTnDyIERBb8xMzVFa.jpg"),
    ("수육", 14000, "부드럽고 고소한 돼지고기 수육은 마늘과 생강, 대파를 넣고 끓여 깊고 풍부한 맛을 자랑합니다. 된장이 더해져 고기의 잡내를 잡아주며, 고기의 육즙이 살아있어 씹을 때마다 고소함을 느낄 수 있습니다.", "https://ldb-phinf.pstatic.net/20201202_9/1606891031165shJSs_JPEG/yJtohH5utPBC1ibr-BpU7lck.jpg"),
    ("공기밥", 1000, "신선한 쌀로 지은 공기밥입니다. 모든 음식과 함께 곁들이기 좋으며, 고슬고슬하고 부드러운 식감이 특징입니다.", "https://i.namu.wiki/i/sOJ69mpLeWtOEzM_SPm7Oh9pO5SZ9SJONKOikJFT0_IMaxtfJeIi-wvCO64fFPNeY64kfC6ZO2C4idJw1xIuupK8oiUO4USwSCgXqeZh9YK_6lAhPxxZByYlG65899CVYAtrdlYquvbL-aS_JO2vLA.webp")
]


alcohol_menu = [
    ("참이슬", 5000, "대한민국을 대표하는 소주로, 부드럽고 깔끔한 맛을 자랑합니다. 한국 요리와 함께 즐기기 좋은 소주입니다. 서울, 경기 지역에서 인기가 많습니다.", "https://i.namu.wiki/i/TjZubjCdGqzW1NpfMTIzQoP5zERsuXXneDLBk5ER0BARF6B0EnESl5Ip7b6Wrcl_4hgRbA4tsIkyontCkQOP-Ag8xI8CO_3Q1v71owISmBCmQKzDGJeRcmmcRNz74OF3Bq6qvTZJ72_CdnrPHw4_LA.webp"),
    ("처음처럼", 5000, "순하고 부드러운 맛이 특징인 소주로, 가벼운 목넘김을 자랑합니다. 다양한 안주와 잘 어울리는 소주입니다. 강원도 지역에서 많이 애용됩니다.", "https://i.namu.wiki/i/GrPoLgSoKmfp94HjCJWO-8bbT7eSzA1RIGtn43cW7TGIJMQWca1ti4Lvh5NU5iSShxm-zp1S7TX-20wlad4SJQH8ASABNKk-aYVEsT7MUsVFF2sc0QlhfdtibmIAPKwxGabTK-um9palTac-lohjOA.webp"),
    ("좋은데이", 5000, "순한 맛과 깔끔한 마무리가 특징인 소주로, 부담 없이 즐길 수 있는 음료입니다. 친목 도모에 좋은 선택입니다. 경상남도 지역에서 유명합니다.", "https://i.namu.wiki/i/MyfjE77W2VXoD66JQMCJC5aUD4lQ4hwGJFrPiyDYDqhBTeuFEEvXrduTcm00ZqFn1DEDuZvqJjFnh6FC60gWNApNPmEmsBHeMskVudA5Gj4SA_q4p7YpEef42tnlPMvEshOKBwiCSxeM-oZJCLFCCQ.webp"),
    ("이제우린", 5000, "부드럽고 깔끔한 맛의 소주로, 알코올의 쓴 맛을 줄여 부담 없이 즐길 수 있습니다. 다양한 음식과 잘 어울립니다. 충청남도와 대전에서 사랑받는 소주입니다.", "https://i.namu.wiki/i/prTu3R6fiA4sCdcHR8E9t9Q3nDR_Yc4WIICi5WSWOkVc80SF2DQnIwvvCaREULlSgd8dnPxP0C4mOH3sCB3hX-jw9BvFeLmSzcWauvEdJGL-Ta2WHW0oVpBEssUNNjZlr3RIptUpCZvkivraSWWHcQ.webp"),
    ("카스", 5000, "시원하고 청량한 맛이 특징인 대한민국 대표 라거 맥주입니다. 친구들과 함께 즐기기 좋은 맥주입니다.", "https://i.namu.wiki/i/OvOGXFauxd9hvf8XpW3gfsL1wI7cqWq_VSb169bCbfyQN86lsF9uoN1owUsuzIURw6-l_VgkXGCodHYxP1NcvaKDj428qRCLwAz-UomAt_dofMrA4pA-0993OqQrapf2SYLF3lj7mu_wYy8GYLPrbg.webp"),
    ("테라", 5000, "청정 라거 맥주로, 산뜻하고 시원한 맛을 자랑합니다. 갈증 해소에 좋은 맥주입니다.", "https://i.namu.wiki/i/NXgATUERr3DzNR-PhHnEXhpgKDK5gT0jsRIJ5QZfissrFRxKGmvSwuwDMfrPeIOnoWi8GIuOkwao0l9NXP7uCeXC9NuAi8UtNtNhSh_fjlRJp1qYdXDIAnTch4OmR52rzOSUHRcQu81-jnjmXVp_Tg.webp"),
    ("크러쉬", 5000, "강렬한 맛과 풍부한 향을 자랑하는 라거 맥주로, 다양한 안주와 함께 즐기기에 좋습니다.", "https://i.namu.wiki/i/_Ji6tIHZaMi0SJHp-GwKiJJ29b4sDU_qo6N4AnQocaEnNMqZRlgSiBaP32AqEmN2kXj8Gl0ci_nv0q6yRZRZhUujJpTLO-I9NFmOjfpAlEd1_jjDhrPkBctWrAVE9h_AVvKD6eHQgNWpze8HN9v5Sw.webp")
]

oncheon_menu += alcohol_menu

# Insert menu items for Tom N Toms
for k,item in enumerate(tom_n_toms_menu):
    cur.execute('''
    INSERT INTO MenuItems (MENU_ID,ITEM_ID, ITEM_NM, ITEM_PRICE, ITEM_INFO, IMAGE_URL)
    VALUES (?,?, ?, ?, ?, ?)
    ''', (1,k, item[0], item[1], item[2], item[3]))

# Insert menu items for 온천 칼국수
for k,item in enumerate(oncheon_menu):
    cur.execute('''
    INSERT INTO MenuItems (MENU_ID,ITEM_ID, ITEM_NM, ITEM_PRICE, ITEM_INFO, IMAGE_URL)
    VALUES (?,?, ?, ?, ?, ?)
    ''', (2,k, item[0], item[1], item[2], item[3]))

# Commit changes and close connection


# Insert 리코타코
cur.execute('''
INSERT INTO restaurants 
(NAME, ADDRESS, PHONE, TYPE, INFO, OPEN_HR_INFO, MENU_ID,LAT,LNG)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
'리코타코',
'대전 유성구 대학로155번길 29 101호',
'042-823-7234',
'멕시칸 음식점',
'''안녕하세요
대전 멕시칸 음식점 리코타코입니다
대전 궁동에서 9년째 영업중

1. 전문 쉐프들이 만드는 믿고 먹는 음식
-최소 5년~최대 15년차 요리사들의 고집을 보여드립니다.
신선한 재료만 쓰고 건강하게 만듭니다
2. 깔끔한 인테리어 이전한지 2년되어 깔끔한 매장을 이용하실 수 있어요
3. 2인부터 최대 12명까지 예약가능
4. 다양한 데킬라를 즐기실수 있음
요즘 핫한 멕시코 데킬라를 합리적인 가격으로 마실 수 있어요
5. 연인과 데이트하기 좋은 음식점
6. 가족들과 함께 주말을 보내기 좋은 음식점
7. 친구들과 모임하기 좋은 음식점
앞으로도 한결같은 맛유지를 위해 노력하겠습니다

예약은 전화로 문의해 주세요''',
'''매일 11:00 - 22:30
쉬는시간 15:00 - 17:00
마지막주문 14:40 / 21:30''',
3,
36.3621354,
127.3505065
))

# Insert menu items for 리코타코
rico_taco_menu = [
    ("화이트 대표", 24000, "비프, 치킨, 새우 중 원하는 고기를 선택해 싸 먹는 화이타입니다. 신선한 야채와 다양한 소스가 어우러져 풍부한 맛을 느낄 수 있습니다.", "https://ldb-phinf.pstatic.net/20230303_106/16778515606995MrKT_JPEG/Screenshot_20230303_225233_Gallery.jpg"),
    ("퀘사디아", 13000, "또띠아에 가득 넣은 100% 모짜렐라 치즈의 맛을 깔끔하게 느낄 수 있는 음식입니다.", "https://ldb-phinf.pstatic.net/20230303_26/16778515125120IK85_JPEG/Screenshot_20230303_225128_Gallery.jpg"),
    ("뽀뇨피칸테", 16000, "매콤한 소스로 촉촉하게 볶은 닭가슴살을 넣고 부드러운 베샤멜소스를 얹어 그라탕한 엔칠라다입니다.", "https://ldb-phinf.pstatic.net/20240419_116/1713490543447abq2Q_JPEG/DSC_2924.jpg"),
    ("소프트타코", 9000, "부드러운 밀또띠아로 만든 타코입니다.", "https://ldb-phinf.pstatic.net/20240503_289/1714710647197phSOR_JPEG/DSC_2934.jpg"),
    ("하드타코", 9500, "고소하고 바삭한 콘또띠아로 만든 타코입니다.", "https://ldb-phinf.pstatic.net/20240419_75/1713490409620tlCNR_JPEG/DSC_2913.jpg"),
    ("브리또", 9500, "밥과 야채가 가득한 간단하게 드시기 좋은 밸런스 좋은 한 끼 식사입니다.", "https://ldb-phinf.pstatic.net/20230303_169/1677851387886FWzgF_JPEG/%BA%EA%B8%AE%B6%C7.jpg"),
    ("치미창가", 13000, "밥 대신 100% 모짜렐라와 고기를 가득 넣어 튀긴 치미창가와 신선한 샐러드입니다.", "https://ldb-phinf.pstatic.net/20240419_281/1713490302794ezxRp_JPEG/DSC_2852.jpg"),
    ("쿠엘보 하이볼", 8500, "상큼한 라임과 깊은 맛의 데킬라를 넣어 만든 데킬라 하이볼입니다.", "https://ldb-phinf.pstatic.net/20240419_102/1713490665102pvybp_JPEG/DSC_2999.jpg"),
    ("모히또 (논알콜)", 8000, "신선한 라임과 애플민트로 만드는 모히또입니다.", "https://ldb-phinf.pstatic.net/20240419_59/1713490458349zgrHa_JPEG/DSC_2994.jpg")
]

rico_taco_menu += alcohol_menu
# Insert menu items for 리코타코
for k,item in enumerate(rico_taco_menu):
    cur.execute('''
    INSERT INTO MenuItems (MENU_ID,ITEM_ID, ITEM_NM, ITEM_PRICE, ITEM_INFO, IMAGE_URL)
    VALUES (?,?, ?, ?, ?, ?)
    ''', (3,k, item[0], item[1], item[2], item[3]))

# Commit changes and close connection
conn.commit()
conn.close()