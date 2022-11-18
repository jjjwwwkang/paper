import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains
import html5lib


options = webdriver.ChromeOptions()

#크롤링 막는 것을 피하기 위해서 사람처럼 보이기 위해 에이전트 입력
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

#드라이브 설정
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

#아실 홈페이지 열기
driver.get(url = 'http://asil.kr/asil/index.jsp')
time.sleep(5)

#아파트 목록

apartment = [  '이촌동삼성리버스위트', '씨티극동',
 '동아한가람', '한강타운', '가양성지2단지', '산호', 'LG한강자이', '강변힐스테이트', '장미2차', '한강현대',
 ' 파크리오', '이촌한강맨션', '힐스테이트서울숲리버', '한강쌍용', '강변그대가리버뷰', '동신대아', '가양6단지',
 '유원강변', '장미1차', '옥수하이츠', '한강밤섬자이']

#["명수대현대",'목동한신청구','한강현대']'명수대현대', '염창동동아3차','마포한강아이파크', '현대3단지', '현대프라임', '한강극동', '현대강변',
 #'금호삼성래미안', '시범','신반포2차', '이촌시범', '장미', '신동아', '서울숲푸르지오1차', '화랑', '서울숲푸르지오2차',
 #'삼부', '래미안당산1차', '리센츠', '강변래미안', '잠실엘스','선사현대',

DF = pd.DataFrame()

#아파트명 검색창으로 이동
for a in apartment :
    driver.switch_to.frame('sub1')
    time.sleep(0.3)
    element = driver.find_element(By.XPATH,'//*[@id="keyword"]')
    #검색 실시
    element.send_keys(a)
    time.sleep(0.3)
    element.send_keys('\n')
    time.sleep(3)

    #모든거래현황보기
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').click()
    time.sleep(0.3)
    #전월세 삭제
    driver.switch_to.default_content()
   #dd = driver.find_elements(By.CSS_SELECTOR, 'iframe')

    # 해당 영역으로 이동
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sub2"]'))
    # 평형정보 수집
    py = driver.find_element(By.ID, 'mCSB_1_container')
    pylists = py.find_elements(By.TAG_NAME, 'li')
    # 전세 체크해제
    driver.find_element(By.XPATH, '//*[@id="deal2"]').send_keys(Keys.ENTER)
    time.sleep(0.3)
    # 월세 체크해제
    driver.find_element(By.XPATH, '//*[@id="deal3"]').send_keys(Keys.ENTER)
    time.sleep(0.3)

    #평형 갯수에따라
    #만약 평형 종류가 6개 이상이라면 중간을 클릭하고 맨 왼쪽으로 이동
    if len(pylists) >= 6:
        ActionChains(driver).click(pylists[len(pylists) // 2]).perform()
        for i in range(30):
            ActionChains(driver).send_keys(Keys.ARROW_LEFT).send_keys(Keys.ARROW_LEFT).send_keys(
                Keys.ARROW_LEFT).send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(0.2)

    for p in range(len(pylists)):
        pylists[p].click()
        time.sleep(0.5)

        #평형 전체 중 중간에 도달했다면, 오른쪽으로 스크롤 이동
        if p == len(pylists)//2 :
            for t in range(30):
                ActionChains(driver).send_keys(Keys.ARROW_RIGHT).send_keys(Keys.ARROW_RIGHT).send_keys(
                    Keys.ARROW_RIGHT).send_keys(Keys.ARROW_RIGHT).perform()
                time.sleep(0.3)

        dd = driver.find_elements(By.CSS_SELECTOR, 'iframe')
        for i in dd:
            print(i.get_attribute('id'))
        time.sleep(2)
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrm"]'))
        time.sleep(2)

        while True:
            try:
                # driver.find_element(By.XPATH,'//*[@id="morePriceBtn"]/span').send_keys(Keys.ENTER)
                driver.find_element(By.XPATH, '//*[@id="morePriceBtn"]/span').click()
                time.sleep(4)
                driver.switch_to.default_content()
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sub2"]'))
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrm"]'))

            except:
                time.sleep(2)
                table = driver.find_element(By.XPATH, '//*[@id="tableList"]')
                # thead
                time.sleep(0.5)
                thead = table.find_element(By.TAG_NAME, "thead")
                time.sleep(0.5)
                # thead > tr > th
                thead_th = thead.find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th")
                time.sleep(0.5)
                dataindex = []
                for th in thead_th:
                    dataindex.append(th.text)  # text 속성을 인덱스로 저장
                print(dataindex)
                time.sleep(2)

                # tbody
                tbody = table.find_element(By.TAG_NAME, "tbody")

                # tbody > tr > td
                data = []
                for tr in tbody.find_elements(By.TAG_NAME, "tr"):
                    innerdata = []
                    # 실거래내역이 있는 경우에만 진행
                    #if tr.find_elements(By.TAG_NAME, "td")[0].text != '실거래 내역이 없습니다.':
                    try :

                        for td in tr.find_elements(By.TAG_NAME, "td"):
                            innerdata.append(td.get_attribute("innerText"))
                        data.append(innerdata)
                    except:
                        break
                df = pd.DataFrame(data)
                #df = pd.DataFrame(data, columns=dataindex)
                df['단지명'] = a
                df.to_csv("D:\\데이터사이언스대학원\\논문\\데이터\\논문용\\{}_{}.csv".format(a,p))
                DF = pd.concat([DF, df])

                driver.switch_to.default_content()
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sub2"]'))

                break

            # 홈으로 돌아가는 코드. 맨 마지막에 삽입
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="header"]/h1/a').click()

#컬럼명  : ['계약', '일', '경과', '체결가격', '타입', '거래 동층']
