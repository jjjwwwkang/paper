#path : 내 하드에 매매가격지수 파일이 있는 곳
path = r'/content/drive/MyDrive/논문/유형별_매매가격지수_20221012.csv'
data = pd.read_csv(path, encoding = 'cp949').transpose()

#쓸모없는 행1 2 3 삭제
data2 = data.drop(['주택유형별(1)','지역별(1)','지역별(2)','지역별(3)'])
cols = list(data2.iloc[0])
#컬럼으로 사용할 행정구역명에 '구'붙여주기
new_cols = []
for i in cols :
  new_cols.append(i+'구')

data2.iloc[0] = new_cols
#1행을 인덱스로 하고 행 삭제
data3 = data2.rename(columns = data2.iloc[0])
data3.drop(data3.index[0])
price_index_data = data3.drop('소계구', axis = 1 ).drop(['지역별(4)'])


price_index_data
