import pandas as pd
import os
os.chdir('D:\데이터사이언스대학원\논문\데이터\논문용')

#파일 불러오기
sight = pd.read_excel('조망단지.xlsx')
#쓸모없는 컬럼 삭제
sight=sight.drop(columns=['조망가능동.1','거래동','층'])

#한강타운과 동신대아 이름변경
sight2 = sight
sight2['단지명'] = sight2['단지명'].str.replace('한강타운아파트','한강타운')
sight2['단지명'] = sight2['단지명'].str.replace('동신대아아파트','동신대아')

#아실 기준으로 단지명 변경
sight2.replace({'단지명' : {'마포강변힐스테이트' : '강변힐스테이트',
                         '이촌삼성리버스위트':'이촌동삼성리버스위트',
                        '이촌시범중산':'이촌시범',
                        '잠실 리센츠':'리센츠',
                        '잠실 엘스':'잠실엘스',
                        '잠실파크리오':'파크리오'}}, inplace= True)

print(sight2)
sight2.to_csv("sight_final.csv",encoding='utf-8')

