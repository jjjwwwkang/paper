import pandas as pd
import os
import numpy as np

os.chdir('D:\데이터사이언스대학원\논문\데이터\논문용')

price = pd.read_csv('유형별_매매가격지수_20221107.csv', encoding = 'cp949')
consumer = pd.read_csv('소비자동향조사_20221107.csv',encoding = 'cp949')

##매매가지수
#컬럼명 정리
price.iloc[2] = price.iloc[2]+'구'
price = price.rename(columns=price.iloc[2])
price = price.drop([0,1,2])
price = price.drop(columns=['주택유형별(1)구'])

#인덱스 및 데이터타입 정리
price= price.set_index('시점구')
price =price.astype('float')
price = price.reset_index()

#컬럼명 모음
price_list = price.columns.to_list()
#변화율을 담을 DF
price_change = pd.DataFrame()
#price_change = 매매지수 변화율 계산 및 담음
price_change['시점'] = price['시점구']
for i in price_list[1:] :
    price_change[i] = round(price[i].pct_change()*100,2)
print(price_change)

#소비자심리지수
consumer = consumer.drop(columns=['CSI분류코드별'])
print(consumer)

#두 시장지표 join
#join key 형식맞춰주기
price_change = price_change.astype({'시점' :'float'})
#market_index = 매매지수 변화율과 소비자심리지수 병합
#merge price_change and consumer on '시점'
market_index = pd.merge(price_change, consumer, how = 'left', left_on='시점', right_on='시점')
market_index = market_index.astype({'주택가격전망CSI' :'float'})

#상승하락장 판단을 담을 DF
bullbear = pd.DataFrame()
#인덱스 리스트
mk = market_index.columns.to_list()
print(market_index.dtypes)
#소비자심리결측치 채우기
market_index['주택가격전망CSI'] = market_index['주택가격전망CSI'].fillna(999)
#데이터 없는 2003년 10월 제거
market_index = market_index.dropna()

#소비자심리지수 시황 수치화 -> 상승 :1 하락 :-1 없음 : 0
market_index['CSI_시황'] = market_index['주택가격전망CSI'].apply(lambda x: 1 if 999>x>100
                                         else (-1 if x <100 else 0))

#구별 매매가격변동률 시황 수치화 -> 상승 : 1 하락 : -1 보합 : 0
for i in mk[1:-1] :
    market_index[i+'-시장'] = market_index[i].apply(lambda x : 1 if x > 0.25
                                  else (-1 if x < -0.25 else 0))

#중복으로 생긴 컬럼 삭제
market_index=market_index.drop(columns=mk[1:])

mk2 = market_index.columns.to_list()

#최종 시장상황
#판단함수
def bullbear(a,b) :
    return a+b

#매매지수와 소비자심리지수를 합친 시장상황
for i in mk2[2:]:
    market_index[i[:-3]] = market_index.apply(lambda x: bullbear(x[i], x['CSI_시황']), axis=1)

#중복으로 생긴 컬럼 삭제
market_index=market_index.drop(columns=mk2[1:])

print(market_index)