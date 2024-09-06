from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from datetime import date
import time
import pandas as pd
import dbio
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

cols13 = ('통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', 
       '송금_보낼때', '송금_받을때', 'T/C_살때', '외화_수표_팔때', '매매기준율', '환가_료율',
       '미화 환산율', 'date')
sorted_cols13 = ('date', '통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', 
       '송금_보낼때', '송금_받을때', 'T/C_살때', '외화_수표_팔때', '매매기준율', '환가_료율',
       '미화 환산율')

cols12 = ('통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', 
       '송금_보낼때', '송금_받을때', '외화_수표_팔때', '매매기준율', '환가_료율', '미화 환산율', 'date')
sorted_cols12 = ('date', '통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', 
       '송금_보낼때', '송금_받을때', '외화_수표_팔때', '매매기준율', '환가_료율', '미화 환산율')

cols11 = ('통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', 
       '송금_보낼때', '송금_받을때', '매매기준율', '환가_료율', '미화 환산율', 'date')
sorted_cols11 = ('date', '통화', '현찰_살때_환율', '현찰_살때_Spread', '현찰_팔때_환율', '현찰_팔때_Spread', 
       '송금_보낼때', '송금_받을때', '매매기준율', '환가_료율', '미화 환산율')

today = str(date.today())

# Headless로 실행하기
options = webdriver.ChromeOptions()
options.add_argument("--headless") # Headless모드
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 크롬 웹브라우저 드라이버 자동 다운로드
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.set_window_size(1920, 1080) #웹브라우저 해상도 조절
driver.get("https://www.kebhana.com/cms/rate/index.do?contentUrl=/cms/rate/wpfxd651_01i.do#//HanaBank")

wait = WebDriverWait(driver, 10)  # 웹 요소가 나타날 때까지 최대 10초 기다림.
time.sleep(5)

# 날짜 입력창
serch_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tmpInqStrDt")))
serch_box.clear()
serch_box.send_keys(today+Keys.ENTER)
time.sleep(2)

# 조회 버튼
search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#HANA_CONTENTS_DIV > div.btnBoxCenter > a")))
search_button.click()
time.sleep(5)

# 환율 정보 테이블이 뜰 때까지 기다림
exchage_rate_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchContentDiv > div.printdiv > table")))

# HTML 소스를 읽어서 데이터프레임으로 만들고 DB저장                                
page_html = driver.page_source
df = pd.read_html(page_html)
df = df[1]
df['date'] = today # 날짜 컬럼 추가

# cols에 정의한 컬럼명으로 변경하기 컬럼 길이가 가변적으로 변하기 때문에 조건을 줌
if len(df.columns) == 13:
       df.columns = cols13
       df = df[[*sorted_cols13]] # date 컬럼을 가장 앞으로 보내기
elif len(df.columns) == 12:
       df.columns = cols12
       df = df[[*sorted_cols12]] # date 컬럼을 가장 앞으로 보내기
elif len(df.columns) == 11:
       df.columns = cols11
       df = df[[*sorted_cols11]] # date 컬럼을 가장 앞으로 보내기

# DB에 저장
dbio.exi_to_db("exchange_rate", today, df)
driver.close()  

