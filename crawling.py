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

#아파트명 검색창으로 이동
for a in apartment :
    driver.switch_to.frame('sub1')
    time.sleep(0.3)
    element = driver.find_element(By.XPATH,'//*[@id="keyword"]')
    element.send_keys(a)
    time.sleep(0.3)
    element.send_keys('\n')
    time.sleep(3)

    driver.switch_to.default_content()
    driver.find_element(By.XPATH,'//*[@id="header"]/h1/a').click()


