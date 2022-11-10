import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time 

options = webdriver.ChromeOptions()

#크롤링 막는 것을 피하기 위해서 사람처럼 보이기 위해 에이전트 입력 
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

#드라이브 설정 
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

#아실 홈페이지 열기
driver.get(url = 'http://asil.kr/asil/index.jsp')
time.sleep(3)

apartment = '명수대현대'
'''
#iframes확인
frames = []
iframes = driver.find_elements(By.CSS_SELECTOR, 'iframe')
for i in iframes :
    frames.append(i.get_attribute('id'))
print(frames)
'''
#아파트명 검색창으로 이동
driver.switch_to.frame('sub1')
time.sleep(0.3)
element = driver.find_element(By.XPATH,'//*[@id="keyword"]')

#아파트명 검색
element.send_keys(apartment)
time.sleep(0.3)
element.send_keys('\n')

#모든 거래현황 클릭
time.sleep(0.3)
driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').click()
time.sleep(0.3)
'''
#이 화면의 frame검색
driver.switch_to.default_content()
dd = driver.find_elements(By.CSS_SELECTOR, 'iframe')
for i in dd :
    print(i.get_attribute('id'))
'''
#오른쪽 iframe으로 이동
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sub2"]'))

#평형정보 수집
py = driver.find_element(By.ID,'mCSB_1_container')
pylists = py.find_elements(By.TAG_NAME, 'li')

#전월세 체크해제
#전세 체크해제
driver.find_element(By.XPATH,'//*[@id="deal2"]').click()
time.sleep(0.3)
#월세 체크해제
driver.find_element(By.XPATH,'//*[@id="deal3"]').click()
time.sleep(0.3)

#평형별 거래현황 수집
DF = pd.DataFrame()
if len(pylists) >= 6 :
    k = 2
else :
    k = 0

for i in range(k, len(pylists)) :

    #driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrm"]'))

    time.sleep(0.5)
    pylists[i].click()
    dd = driver.find_elements(By.CSS_SELECTOR, 'iframe')
    for i in dd:
        print(i.get_attribute('id'))
    time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrm"]'))
    #이 아래만은 잘 작동함
    # table element 접근. 찾는 속성은 적절하게 고려한다.
    time.sleep(2)
    table = driver.find_element(By.XPATH,'//*[@id="tableList"]')
    # thead
    time.sleep(0.5)
    thead = table.find_element(By.TAG_NAME,"thead")
    time.sleep(0.5)
    # thead > tr > th
    thead_th = thead.find_element(By.TAG_NAME,"tr").find_elements(By.TAG_NAME,"th")
    time.sleep(0.5)
    dataindex = []
    for th in thead_th:
        dataindex.append(th.text) # text 속성을 인덱스로 저장
    print(dataindex)
    time.sleep(2)

    # tbody
    tbody = table.find_element(By.TAG_NAME, "tbody")

    # tbody > tr > td
    data = []
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        innerdata = []
        for td in tr.find_elements(By.TAG_NAME, "td"):
            innerdata.append(td.get_attribute("innerText"))
        data.append(innerdata)
    df = pd.DataFrame(data, columns=dataindex)
    DF = pd.concat([DF, df])
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sub2"]'))
DF['단지명'] = apartment
    # 수정요망 : 거래 더보기 버튼을 눌러서 긁어와야하는데 에러남
    '''
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrm"]'))
    while driver.find_element(By.XPATH,'//*[@id="morePriceBtn"]/span') : 
        driver.find_element(By.XPATH,'//*[@id="morePriceBtn"]/span').click()
        time.sleep(0.2)
    '''
