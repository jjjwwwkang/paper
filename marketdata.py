import pandas as pd
import os

#매매가격지수 정리

df = pd.read_csv('D:\데이터사이언스대학원\논문\데이터\논문용\유형별_매매가격지수_20221107.csv', encoding = 'cp949')
df2 = df.drop(index = [0,1,], axis = 0)
df3 = df2.drop(columns=['주택유형별(1)'], axis = 1 )
df4 = df3.rename(columns=df3.iloc[0])
df4 = df4.drop(df4.index[0])

#구이름 정리
df4.rename(columns= lambda x : x + '구',inplace = True)
df4.rename(columns={'시점구' : '시점'}, inplace = True)

price_index = df4
price_index.set_index('시점', drop = True, append = True, inplace = True )
price_index= price_index.astype('float')

#소비자 CSI정리
df_csi = pd.read_csv('D:\데이터사이언스대학원\논문\데이터\논문용\소비자동향조사_20221107.csv', encoding = 'cp949')
df_csi = df_csi.drop(columns=['CSI분류코드별'], axis =1 )
df_csi.set_index('시점',drop = True, append = True, inplace = True )

df_csi = df_csi.astype('float')


#시장지표 병합
#합치기 위해서 인덱스를 조절
merge1 = price_index.reset_index()
merge2 = df_csi.reset_index()
merge1 = merge1.astype({'시점':'float'})
market = pd.merge(merge1, merge2, how = 'outer', on = '시점' )

#합친것에서 쓸모없는 행렬정리
marketdata = market.drop(['level_0_y'], axis =1)
marketdata = marketdata.drop(marketdata.index[227])
marketdata
