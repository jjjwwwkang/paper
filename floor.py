# #### URL과 서비스키 확인완료

#encoding
service_key1 = 'sb%2BD3hM4VtI54rA0YCSWdk%2FkqTeiKsccu%2BJ6tyzYvQGF7R7fZj7AnNjMjH9fsOEh4zZip5OmbGmJKGBVk0cAgA%3D%3D'
#decoding
service_key2 = 'sb+D3hM4VtI54rA0YCSWdk/kqTeiKsccu+J6tyzYvQGF7R7fZj7AnNjMjH9fsOEh4zZip5OmbGmJKGBVk0cAgA=='
#요청형식 : url1 + 상세서비스명 + url2 + 서비스키
url1 = 'https://api.odcloud.kr/api/AptIdInfoSvc/v1/'
url2 = '?page='
url3 = '&perPage=100&serviceKey=' #페이지당 100개씩


import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime
import os
import xml.etree.ElementTree as ET
import dataframe_image as dfi
import time
import json
import math


def get_data(name,page):
    service_key = service_key1
    res = requests.get(url1 + name + url2 + page +url3 +service_key1)
    return res


#### 아파트 기본정보


#데이터 형식 확인
res = get_data('getAptInfo','1')

#잘 불러와짐
print(res)


##### API로 불러온 전체 데이터 갯수 확인 및 저장

r_dict = json.loads(res.text)
#전체 데이터갯수
totcnt = r_dict['totalCount']
#페이지당 출력
numofrows =r_dict['perPage']

#### 총 API호출횟수

loop = math.ceil(totcnt/numofrows)

#### 전체 데이터를 저장할 객체
aptdata = pd.DataFrame()

#페이지 전부 읽어오는 식
for i in range(1,loop+1) :
    res = get_data('getAptInfo',str(i)) #원래는 str(i)가 없었음
    r_dict = json.loads(res.text)
    r_data = pd.json_normalize(r_dict['data'])
    aptdata = pd.concat([aptdata, r_data], axis = 0, ignore_index=True)


aptdata.shape

#컬럼명 변경
aptdata = aptdata.rename(columns={'ADRES' : '주소', 'COMPLEX_GB_CD' : '단지종류',
                          'COMPLEX_NM1' : '단지명_공시가',
                          'COMPLEX_NM2' : '단지명_건축물대장',
                          'COMPLEX_NM3' : '단지명_도로명주소',
                          'COMPLEX_PK' : '고유번호',
                          'DONG_CNT' : '동수',
                          'PNU' : '필지번호',
                          'UNIT_CNT' : '세대수',
                          'USEAPR_DT' : '사용승인일'})


aptdata1 = aptdata


#### 데이터 형식변환, 쓸모없는 열 삭제

aptdata1['고유번호'] = pd.to_numeric(aptdata1['고유번호'])
aptdata1= aptdata1.astype({'동수':'int','세대수':'int'})
aptdata1= aptdata1.drop('필지번호', axis=1)


### 세부 동정보(층)

floor = get_data('getDongInfo','1')

#### 전체 불러온 갯수 확인 및 저장, 루프 횟수 지정

f_dict = json.loads(floor.text)
#전체 데이터갯수
floor_totcnt = f_dict['totalCount']
#페이지당 출력
floor_numofrows =f_dict['perPage']
#API호출을 반복할 횟수
f_loop = math.ceil(floor_totcnt/floor_numofrows)

#### 층정보 전체를 저장할 객체

floordata = pd.DataFrame()

#페이지 전부 읽어오는 식
for i in range(1,f_loop+1) :
    floor = get_data('getDongInfo',str(i))
    f_dict = json.loads(floor.text)
    f_data = pd.json_normalize(f_dict['data'])
    floordata = pd.concat([floordata, f_data], axis = 0, ignore_index=True)


#컬럼명 변경
floordata = floordata.rename(columns={'GRND_FLR_CNT' : '지상층수',
                          'DONG_NM1' : '동명_공시가',
                          'DONG_NM2' : '동명_건축물대장',
                          'DONG_NM3' : '동명_도로명주소',
                          'COMPLEX_PK' : '고유번호'})
#### 마찬가지로 데이터 형식변환
floordata1 = floordata
floordata1['고유번호'] = pd.to_numeric(floordata1['고유번호'])
floordata1= floordata1.astype({'지상층수':'int'})


#### 두 데이터프레임 merge
aptfloor = pd.merge(floordata1, aptdata1, how = 'left',left_on = '고유번호', right_on='고유번호' )

final_aptfloor = aptfloor[['주소','단지명_공시가', '단지명_건축물대장', '단지명_도로명주소', '동수', '세대수',
                           '동명_공시가', '동명_건축물대장', '동명_도로명주소', '지상층수',
                           '고유번호','사용승인일']]
final_aptfloor.to_csv('D:\데이터사이언스대학원\논문\데이터\논문용\\final_aptfloor.csv')

