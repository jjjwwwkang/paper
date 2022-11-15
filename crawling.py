import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
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
apartment = ["명수대현대",'목동한신청구','한강현대']

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
    driver.find_element(By.XPATH, '//*[@id="deal2"]').click()
    time.sleep(0.3)
    # 월세 체크해제
    driver.find_element(By.XPATH, '//*[@id="deal3"]').click()
    time.sleep(0.3)

    #평형 갯수에따라
    if len(pylists) >= 6:
        k = 2
    else:
        k = 0
    for p in range(k, len(pylists)):
        pylists[p].click()
        time.sleep(0.5)
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
                    for td in tr.find_elements(By.TAG_NAME, "td"):
                        innerdata.append(td.get_attribute("innerText"))
                    data.append(innerdata)
                df = pd.DataFrame(data, columns=dataindex)
                df['단지명'] = a
                df.to_csv("D:\\데이터사이언스대학원\\논문\\데이터\\논문용\\{}_{}.csv".format(a,p))
                DF = pd.concat([DF, df])

                driver.switch_to.default_content()
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="sub2"]'))

                break
                #파일저장을 저기다 놓으니, 매 단지마다 저장이 되네요. 즉, 평형하나 다모으면 저장
                #다음평형 모으면 덮어쓰기저장, 이런식이다.
                #첫단지의 경우에는 다끝나고 DF를 저장하면되지만 그 다음단지작업이 끝나면 DF를 저장하면 누적저장이되어버린다. 이걸어쩌지

            # 홈으로 돌아가는 코드. 맨 마지막에 삽입
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="header"]/h1/a').click()