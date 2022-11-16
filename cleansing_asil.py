import pandas as pd
import os
#경로확인
os.chdir('D:\데이터사이언스대학원\논문\데이터\논문용')
한강현대_0 = pd.read_csv('한강현대_0.csv', encoding='utf-8')
한강현대_1 =pd.read_csv('한강현대_1.csv', encoding='utf-8')
한강현대_2 =pd.read_csv('한강현대_2.csv', encoding='utf-8')
한강현대_3 =pd.read_csv('한강현대_3.csv', encoding='utf-8')

#읽어오기
apartment = pd.concat([한강현대_0,한강현대_1,한강현대_2,한강현대_3], axis = 0)

#쓸모없는 컬럼 삭제
apartment = apartment.drop(columns=['Unnamed: 0','경과','일'])
#빈 계약월 채우기
apartment["계약"] =apartment['계약'].fillna(method = 'ffill')
apartment= apartment.astype({'계약':'string','체결가격':'string','거래 동층':'string','타입':'string'})

#계약일을 2022.09형식으로 정리
#먼저 .을 기준으로 둘로 나눔
apartment['계약연도_p'] = apartment['계약'].str.split('.').str[0]
apartment['계약월_p'] = apartment['계약'].str.split('.').str[1]
#연도 : 두자리면 20을 더하고 한자리면 200을 더함
apartment['계약연도_작업'] = apartment['계약연도_p'].apply(lambda x : '20'+ x if len(x) == 2 else '200'+x)
#월 : 1자리면 10
apartment['계약월_작업'] = apartment['계약월_p'].apply(lambda x : '10' if x == '1' else x )
#계약일자 합치기
apartment["계약일_F"] = apartment["계약연도_작업"]+"."+apartment['계약월_작업']

#쓸모없는 컬럼 삭제
apartment = apartment.drop(columns=['계약','계약연도_p','계약월_p','계약연도_작업','계약월_작업'])

#타입에서 영문자 지우기
apartment['타입'] = apartment['타입'].str.replace('A','')
apartment['타입'] = apartment['타입'].str.replace('B','')
apartment['타입'] = apartment['타입'].str.replace('83.0','83')

#체결가격 형식맞추기
apartment['체결가격'] = apartment['체결가격'].str.replace('최고가\n','')
apartment['체결가격'] = apartment['체결가격'].str.replace('매매','')
apartment['체결가격(억,원)'] = apartment['체결가격'].str.split(' ')
apartment['체결가격(억)'] = apartment['체결가격(억,원)'].str[0]
apartment['체결가격(천만)'] = apartment['체결가격(억,원)'].str[1]

#계약취소 데이터, 동정보 없는 행 삭제
apartment = apartment[~apartment['체결가격'].str.contains("계약취소",na=False)]


#'억'제거
apartment['체결가격(억)'] = apartment['체결가격(억)'].str.replace('억','')
#천만단위가 없는 경우 0원으로 채우고, 천만단위의 ,를 없애기
apartment['체결가격(천만)'] = apartment['체결가격(천만)'].fillna('0')
apartment['체결가격(천만)'] = apartment['체결가격(천만)'].str.replace(',','')

#거래동층 데이터 정리
apartment['거래동'] = apartment['거래 동층'].str.split('\n').str[0]
apartment['거래동'] = apartment['거래동'].str.replace('동','')
apartment['거래층'] = apartment['거래 동층'].str.split('\n').str[1]
apartment['거래층'] = apartment['거래층'].str.replace('층','')
#거래동에서 동정보 업는 값 삭제
apartment = apartment[~apartment['거래동'].str.contains("\xa0",na=False)]

#광고데이터(배너상단)삭제
apartment = apartment.dropna()

#데이터 타입변경 및 마지막 정리(체결가격)
apartment= apartment.astype({'타입':'int', '체결가격(억)':'int',
                             '체결가격(천만)':'int', '거래동':'int','거래층':'int'})
apartment['거래가격'] = apartment['체결가격(억)']*10000+apartment['체결가격(천만)']
apartment['평당거래가'] = round(apartment['거래가격'] / (apartment['타입']/3.3))

#쓸모없어진 컬럼 삭제
apartment = apartment.drop(columns=['체결가격','거래 동층','체결가격(억,원)'
                                   ,'체결가격(억)','체결가격(천만)'])


print(apartment)