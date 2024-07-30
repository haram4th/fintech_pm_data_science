import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import date
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql
import time
pymysql.install_as_MySQLdb()
load_dotenv(dotenv_path=".dbenv")

today = str(date.today()).replace("-","_")

def str2int(x):
    x = int(x.replace(",", ""))
    return x

# DB 연결
def create_conn():
    engine = create_engine("")
    conn = engine.connect()
    return engine, conn


# DB에 접속해서 저장하는 함수
def stock_info_to_db(idx, code, df):
    engine, conn = create_conn()
    df.to_sql(f"{today}_stock_price_info_windows", con=conn, if_exists='append', index=False)
    conn.close()
    return print(f"{today}, {idx}, {code}, {'저장완료':<30s}", end="\r")



def stock_info_scraping():
    # mysql에서 테이블 불러오기
    engine, conn = create_conn()
    data = pd.read_sql('2024_07_stock_company_info', con=conn)
    conn.close()
        
    errors = {}
    for idx, (company, code) in enumerate(zip(data['회사명'], data['종목코드'])):
        stock_price_detail = {}
        url = f"https://finance.naver.com/item/main.naver?code={code}" 
        try:
            r = requests.get(url)
            print(r.status_code, f"{idx+1}/{len(data['종목코드'])} 수집중                    ", end="\r")
            soup = bs(r.text, 'lxml')
            # 가격
            price = int((soup.select_one(".today").text).strip("\n").split("\n")[1].replace(",", ""))
            # 변동금액
            price_chage = int((soup.select_one(".today").text).strip("\n").split("\n")[9].replace(",", ""))
            # 변화율
            rate_of_chage = float(((soup.select_one(".today").text).strip("\n").split("\n")[13]+(soup.select_one(".today").text).strip("\n").split("\n")[15]).replace("%",""))
            stock_price_detail.setdefault('회사명', []).append(company)
            stock_price_detail.setdefault('종목코드', []).append(code)
            stock_price_detail.setdefault('현재가', []).append(price)
            stock_price_detail.setdefault('변동금액', []).append(price_chage)
            stock_price_detail.setdefault('변화율', []).append(rate_of_chage)
            table = soup.select_one(".no_info")
            for tr in table.select("tr"):
                for td in tr.select('td'):
                    stock_price_detail.setdefault(td.select_one('span').text, []).append(str2int(td.select_one("span.blind").text))
            df = pd.DataFrame(stock_price_detail)
            stock_info_to_db(idx, code, df)
            time.sleep(5)
        except Exception as e:
            print(e)
            print(r.status_code, f"{idx+1}/{len(data['종목코드'])} 수집중 에러", end="\r")
            errors.setdefault("에러", []).append(code)
    
    return print(f"{today}_stock_prices have been saved to DB")

if __name__ == "__main__":
    stock_info_scraping()