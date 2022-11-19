import pandas as pd
import os

#아실 크롤링 코드에서 받아와야할 변수.
## 조망데이터 & 층 join한 것에서 단지데이터를 뽑고, 그게 아실크롤링과 이곳으로 온다.

apartment_list = ['명수대현대', '염창동동아3차','마포한강아이파크', '현대3단지', '현대프라임', '한강극동', '현대강변', '금호삼성래미안', '시범',
'신반포2차', '이촌시범', '장미', '신동아', '서울숲푸르지오1차', '화랑', '서울숲푸르지오2차', '삼부', '래미안당산1차', '리센츠', '강변래미안', '잠실엘스','선사현대',  '이촌동삼성리버스위트', '씨티극동',
'동아한가람', '한강타운', '가양성지2단지', '산호', 'LG한강자이', '강변힐스테이트', '장미2차', '한강현대',
' 파크리오', '이촌한강맨션', '힐스테이트서울숲리버', '한강쌍용', '강변그대가리버뷰', '동신대아', '가양6단지',
 '유원강변', '장미1차', '옥수하이츠', '한강밤섬자이']


#전체 CSV 다읽어오기
os.chdir("D:\데이터사이언스대학원\논문\데이터\논문용")
toread = os.listdir()

#폴더에 아파트명 외 다른 파일들이 있으므로, 아파트명만 골라내자
toreadlist = []
for i in toread :
    if 'csv' in i :
        toreadlist.append(i)
#아파트 이름이 아닌 것들을 지워야한다
deldict = {}
for j in toreadlist:
    # 만약 확장자를 뺀 파일명이 아파트 리스트에 있는지 여부로 deldict에저장
    if j[:-6] not in apartment_list:
        deldict[j] = False
    else:
        deldict[j] = True
#deldict에서 False인 것들을 지운다.
D = []
for d in deldict :
    if deldict[d] == True :
        D.append(d)

#쓸모없는것들이 성공적으로 제거되었으니 D에 있는 것들을 읽어오면된다
# 전부 다 읽어오자
ASIL = pd.DataFrame()
for a in D:
    df = pd.read_csv('{}'.format(a))
    ASIL = pd.concat([ASIL, df], axis=0)

#컬럼이없으니 맞춰주고
ASIL.columns=['삭제요망','계약','일','경과','체결가격','타입','거래 동층','단지명']

#이제 미리 짜놓았던 코드가 빛을 발할 차례다
#쓸데없는 컬럼 삭제
ASIL = ASIL.drop(columns=['삭제요망','경과','일'])

#빈 계약월 채우기
ASIL["계약"] =ASIL['계약'].fillna(method = 'ffill')
ASIL= ASIL.astype({'계약':'string','체결가격':'string','거래 동층':'string','타입':'string'})
#계약일을 2022.09형식으로 정리
#먼저 .을 기준으로 둘로 나눔ㅜ
ASIL['계약연도_p'] = ASIL['계약'].str.split('.').str[0]
ASIL['계약월_p'] = ASIL['계약'].str.split('.').str[1]
#연도 : 두자리면 20을 더하고 한자리면 200을 더함
ASIL['계약연도_작업'] = ASIL['계약연도_p'].apply(lambda x : '20'+ x if len(x) == 2 else '200'+x)
#월 : 1자리면 10
ASIL['계약월_작업'] = ASIL['계약월_p'].apply(lambda x : '10' if x == '1' else x )
#계약일자 합치기
ASIL["계약일_F"] = ASIL["계약연도_작업"]+"."+ASIL['계약월_작업']
#쓸모없는 컬럼 삭제
ASIL = ASIL.drop(columns=['계약','계약연도_p','계약월_p','계약연도_작업','계약월_작업'])

#타입에서 영문자 지우기
ASIL['타입'] = ASIL['타입'].str.replace('A','')
ASIL['타입'] = ASIL['타입'].str.replace('B','')
ASIL['타입'] = ASIL['타입'].str.replace('C','') #금번 추가
#ASIL['타입'] = ASIL['타입'].str.replace('83.0','83')

#체결가격 형식맞추기
ASIL['체결가격'] = ASIL['체결가격'].str.replace('최고가\n','')
ASIL['체결가격'] = ASIL['체결가격'].str.replace('매매','')
ASIL['체결가격(억,원)'] = ASIL['체결가격'].str.split(' ')
ASIL['체결가격(억)'] = ASIL['체결가격(억,원)'].str[0]
ASIL['체결가격(천만)'] = ASIL['체결가격(억,원)'].str[1]

#계약취소 데이터, 동정보 없는 행 삭제
ASIL = ASIL[~ASIL['체결가격'].str.contains("계약취소",na=False)]


#'억'제거, ,제거, 직거래제거
ASIL['체결가격(억)'] = ASIL['체결가격(억)'].str.replace('억','')
ASIL['체결가격(억)'] = ASIL['체결가격(억)'].str.replace(',','')
ASIL['체결가격(억)'] = ASIL['체결가격(억)'].str.replace('직거래\n','')
ASIL['체결가격(억)'] = ASIL['체결가격(억)'].str.replace('최고가직거래\n','')
ASIL['체결가격(억)'] = ASIL['체결가격(억)'].str.replace('최고가','')
#그냥 replace로하면 직거래를 없앨 수 없다 이부분이 대거 추가됨

#천만단위가 없는 경우 0원으로 채우고, 천만단위의 ,를 없애기
ASIL['체결가격(천만)'] = ASIL['체결가격(천만)'].fillna('0')
ASIL['체결가격(천만)'] = ASIL['체결가격(천만)'].str.replace(',','')

#거래동층 데이터 정리
ASIL['거래동'] = ASIL['거래 동층'].str.split('\n').str[0]
ASIL['거래동'] = ASIL['거래동'].str.replace('동','')
ASIL['거래층'] = ASIL['거래 동층'].str.split('\n').str[1]
ASIL['거래층'] = ASIL['거래층'].str.replace('층','')
#거래동에서 동정보 업는 값 삭제
ASIL = ASIL[~ASIL['거래동'].str.contains("\xa0",na=False)]
notdong = ASIL[ASIL['거래동'] =='-']
#notdong이라는 것으로 따로 정리하고, 해당 변수는 없애줌.
ASIL = ASIL[~ASIL['거래동'].str.contains("-",na=False)]


#광고데이터(배너상단)삭제
ASIL = ASIL.dropna()
#타입에 59,라는 이상한 값이 있어서 이것을 59로 변경
ASIL['타입'] = ASIL['타입'].replace('59,','59')

#데이터 타입변경 및 마지막 정리(체결가격)
ASIL= ASIL.astype({'타입':'float', '체결가격(억)':'int',
                             '체결가격(천만)':'int', '거래동':'int','거래층':'int'})
ASIL['거래가격'] = ASIL['체결가격(억)']*10000+ASIL['체결가격(천만)']
ASIL['평당거래가'] = round(ASIL['거래가격'] / (ASIL['타입']/3.3))
#쓸모없어진 컬럼 삭제
ASIL = ASIL.drop(columns=['체결가격','거래 동층','체결가격(억,원)'
                                   ,'체결가격(억)','체결가격(천만)'])

print(ASIL.shape)
print(ASIL)