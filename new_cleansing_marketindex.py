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
#price= price.set_index('시점구')
price =price.astype('float')
#price = price.reset_index()

#컬럼명 모음
price_list = price.columns.to_list()
#price = 매매지수 변화율 계산 및 담음
for i in price_list[1:] :
    price[i+'변화율'] = round(price[i].pct_change()*100,2)

#소비자심리지수
consumer = consumer.drop(columns=['CSI분류코드별'])
print(consumer)

#두 시장지표 join
#join key 형식맞춰주기
#market_index = 매매지수 변화율과 소비자심리지수 병합
#merge price_change and consumer on '시점'
market_index = pd.merge(price, consumer, how = 'left', left_on='시점구', right_on='시점')
market_index = market_index.astype({'주택가격전망CSI' :'float'})
market_index = market_index.drop(columns=['시점'])

#소비자심리결측치 채우기
market_index['주택가격전망CSI'] = market_index['주택가격전망CSI'].fillna(100)
#데이터 없는 2003년 10월 제거
market_index = market_index.dropna()
print(market_index)
#시장상황을 담은 DF를 csv로 저장
market_index.to_csv('new_market_index.csv', encoding='cp949', index=False)