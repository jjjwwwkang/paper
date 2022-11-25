import pandas as pd
import os

### 각기 정제된 데이터셋을 이용해서 통합하는 코드
#### 쓰는 파일들
#- ASIL_final : crawling.py 후 cleansing_asil_whole.py사용
#- floor_seoul : floor.py사용
#- sight_final : cleansing_sight.py 사용
#- bull_bear_market_index : cleansing_marketindex_etc.py 사용 -> 2022.11.24 미팅이후 안쓰기로
#- new_market_index : new_cleansing_marketindex.py 사용

os.chdir('D:\데이터사이언스대학원\논문\데이터\논문용\\')

#아실,층정보, 조망정보 다 불러오기
ASIL_final = pd.read_csv("ASIL_final.csv")
floor_seoul = pd.read_csv('floor_seoul.csv')
sight_final = pd.read_csv('sight_final.csv')
#bull_bear_market = pd.read_csv('bull_bear_market_index.csv', encoding = 'cp949')
new_market_index = pd.read_csv('new_market_index.csv', encoding = 'cp949')


### 데이터명세
#ASIL_final : 36030x8 , 단지명 object, 나머지는 숫자
#floor_seoul : 24786x8, 단지명 object, 동명 object, 층,세대, 사용승인일숫자
#sight_final : 217 x 7, 단지명 object, 조망가능동 object, 향, 강남북 object
#bull_bear_market: 226 x 26, 시점 및 구 전원 float
#new_market_index : 226 x 52, 시점 및 구 전원 float -> 날짜가 뒤에 0이빠진것들도 조인하는덴 문제없는듯

datalist = [ASIL_final,floor_seoul, sight_final, new_market_index ]
#bull_bear_market

#데이터셋들의 쓸모없는 컬럼 삭제
for data in datalist :
    if 'Unnamed: 0' in data.columns :
        data.drop(columns=['Unnamed: 0'], inplace = True )

### 아실 과 층정보 Join
#- 아실 전체 + 층정보의 세대수, 지상층수, 사용승인일.
#- join 기준 : left 에서는 단지명 및 거래동, right 에서는 단지명_공시가, 동명_공시가

#join하기전에, 신도림 동아3차와 염창동 동아3차가 섞여버렸다.신도림동아3차를 없애자.
floor_seoul = floor_seoul[floor_seoul['주소'] != '서울특별시 구로구 신도림동 645']

# join을 위해 단지명 동명을 string으로 전환하고, 공백을 없애주기
ASIL_final= ASIL_final.astype({'거래동':'string', '단지명': 'string'})
floor_seoul= floor_seoul.astype({'동명_공시가':'string', '단지명_공시가': 'string'})

#바꿨으면 string의 앞뒤 공백을 없애주자
ASIL_final['거래동'] = ASIL_final['거래동'].str.strip()
ASIL_final['단지명'] = ASIL_final['단지명'].str.strip()

floor_seoul['동명_공시가'] = floor_seoul['동명_공시가'].str.strip()
floor_seoul['단지명_공시가'] = floor_seoul['단지명_공시가'].str.strip()

#단지명 '서울숲푸르지오1차 를 서울숲푸르지오로 변경. 아실에서 1차 붙여서 가져옴
ASIL_final['단지명'] = ASIL_final['단지명'].replace('서울숲푸르지오1차','서울숲푸르지오')
asil_floor = pd.merge(ASIL_final, floor_seoul, how = 'left',
                     left_on=['단지명','거래동'],
                     right_on = ['단지명_공시가','동명_공시가'])

#이를 실행하면 강변힐스테이트, 산호, 삼부, 시범, 신동아, 현대강변, 화랑에 데이터가 없다.
#없는 것들은 강변 힐스테이트는 값을 넣어주고, 나머지는 drop(지방아파트들임)
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '세대수']=510
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '동수']=10
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '사용승인일']=20040216
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '지상층수']=20
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '주소']='서울특별시 마포구 현석동222'
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '단지명_공시가']='강변힐스테이트'
#동명은 의미없음. 나중에 컬럼지울거라
asil_floor.loc[asil_floor['단지명']=='강변힐스테이트', '동명_공시가']='101'

#층비율 컬럼 추가
asil_floor = asil_floor.astype({'거래층': 'float'})
asil_floor['층비율'] = asil_floor['거래층'] / asil_floor['지상층수']
#산호 화랑 등 지방아파트 삭제
asil_floor = asil_floor.dropna()

#병합버전 칼럼 정리
asil_floor = asil_floor[['계약일_F','단지명','거래가격','평당거래가','타입',
                         '거래동','거래층','층비율',
                     '주소','세대수','지상층수','사용승인일']]

## 아실+층 정보와 조망정보 join : multi column key
afs = pd.merge(asil_floor, sight_final, how = 'left',
                      left_on=['단지명','거래동'],
                      right_on= ['단지명','조망가능동'])

#조망 가능여부 값을 넣어주자 : 조망이 가능하면1, 아니면 0으로
def possible(x) :
    if pd.isnull(x) :
        return 0
    else :
        return 1
afs['조망'] = afs['조망가능동'].apply(possible)

#조망향과 강남북도 nan값은 0으로 채우자
# 나중에 강남/강북으로 dataset나눈 이후에 0이 아닌 컬럼에 1이나 2 대입
afs['조망향']= afs['조망향'].fillna(0)
afs['강남북'] = afs['강남북'].fillna(0)

### 추후 작업을 위해서 컬럼형식을 바꿔주자
#- 주소 : 구별 상황 시장지표 join할때 쓸것임 (잘라서)
#- 조망동 : 둘다 string으로 바꿔서 일치여부 비교
afs=afs.astype({'주소_x':'string', '주소_y': 'string',
                '조망가능동':'string','조망향':'string','강남북' : 'string'
               })

#필요한 컬럼만 남기기
afs = afs[['계약일_F','단지명','거래가격','평당거래가','타입',
                         '거래동','거래층','층비율',
                     '주소_x','세대수','지상층수','사용승인일','조망향','강남북']]

#MARKETDATA 병합작업
#afs데이터에서 주소를 구별로 잘라서 시장지표와 병합 key로 사용
#먼저 marketdata를 횡으로 늘어서있는 것을 종으로 쌓아야

#구 이름을 모으기 위한 코드
#mlist = bull_bear_market.columns.to_list()
mlist = new_market_index.columns.to_list()

#trade_list = new_market_index에서 '변화율'이 들어가지 않은 컬럼만 모은 것
trade_list = [x for x in mlist if '변화율' not in x]
#change_list = new_market_index에서 '변화율'이 들어있는 컬럼만 모은 것
change_list = [x for x in mlist if '변화율' in x]


#왼쪽에는 날짜를 그대로 놓고 지금은 구별 시황이 가로이나 이것을 세로로 붙이는 코드
trade_list = [x for x in mlist if '변화율' not in x and '주택' not in x ]
#변화율 이름만 모으기 위한 코드
change_list = [x for x in mlist if '변화율' in x]
#mlist = bull_bear_market.columns.to_list()
#왼쪽에는 날짜를 그대로 놓고 지금은 구별 시황이 가로이나 이것을 세로로 붙이는 코드
TF = pd.DataFrame()
tf = pd.DataFrame()
for t in range(1,len(trade_list)):
    tf['시점구'] = new_market_index[trade_list[0]]
    tf['매매지수'] = new_market_index[trade_list[t]]
    tf['구'] = trade_list[t]
    tf
    TF = pd.concat([TF,tf], axis = 0 )
#시계열 226개 x 25개구 = 5,650

#변화율만 모으는 코드
CF = pd.DataFrame()
cf = pd.DataFrame()
for c in range(0,len(change_list)):
    cf['시점구'] = new_market_index[trade_list[0]]
    cf['변화율'] = new_market_index[change_list[c]]
    cf['구'] = change_list[c]
    cf
    CF = pd.concat([CF,cf], axis = 0 )

#TF와 CF['변화율']컬럼을 가로로 이어붙이고 주택가격CSI까지 이어붙이는 코드
MF = pd.concat([TF,CF['변화율']], axis = 1)
MF = pd.concat([MF,new_market_index['주택가격전망CSI']], axis = 1)

#MF = pd.DataFrame()
#mf = pd.DataFrame()

#for m in range(1,len(mlist)):
#    mf['시점'] = bull_bear_market[mlist[0]]
#    mf['시황'] = bull_bear_market[mlist[m]]
#    mf['구'] = mlist[m]
#    mf
#    MF = pd.concat([MF,mf], axis = 0 )
#시계열 226개 x 25개구 = 5,650

#afs에 '구'컬럼 생성
afs['구'] = afs['주소_x'].str.split(' ').str[1]

#asil+floor+sight+market
afsm= pd.merge(afs, MF, how = 'left', left_on=['계약일_F','구'],
               right_on = ['시점구','구'])

##  2022.10월과 11월 계약건의 시황데이터가 없어 결측치가 생겼다.
## 이것을 어떻게 채울까? 이건 그냥-2로 넣어버릴까? 지금시장이 워낙 안좋으니까
## 마침 확인해보니, 2022.09의 시황이 성동구 제외하고 전부 -2.0이었다.
## 그런데 새로운 방식에서는 안된다. 21개의 결측치는 그냥 날려야할듯


#'시점구'컬럼 삭제 및 결측치 삭제
afsm = afsm.drop(['시점구'], axis = 1)
afsm = afsm.dropna()

#'구'컬럼에서 '구로구'인 행을 drop
#afsm = afsm[afsm['구'] != '구로구']
print(afsm.isna().sum())
print(afsm)
#다 작업한 파일을 출력
afsm.to_csv('afsm.csv', index = False)

#afsm의 correaltion matrix를 그린다
#correlation matrix 표 밑에 데이터프레임명을 이름으로 넣는다
#sns.set(font_scale=1.2)
#sns.set(rc={'figure.figsize':(11.7,8.27)})
#sns.heatmap(afsm.corr(), annot=True, cmap='RdYlGn', linewidths=0.2)
#fig=plt.gcf()
#fig.savefig('afsm.png')





