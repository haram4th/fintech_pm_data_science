import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
import random
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
load_dotenv(dotenv_path="./.dbenv")

# 현재 날짜 추출
today = datetime.today()
today = today.date()
today = str(today)
print("today: ", today)

# DB 연결
def create_conn():
    engine = create_engine(f"{os.getenv('db')}+{os.getenv('dbtype')}://{os.getenv('user')}:{os.getenv('pw')}@{os.getenv('host')}/{os.getenv('database')}")
    conn = engine.connect()
    return engine, conn

def stock_info_to_db(date, idx, company, code, df):

    engine, conn = create_conn()
    # DataFrame을 MySQL 테이블로 저장
    engine = create_engine(f"{os.getenv('db')}+{os.getenv('dbtype')}://{os.getenv('user')}:{os.getenv('pw')}@{os.getenv('host')}/{os.getenv('database')}")
    conn = engine.connect()
    table_name = f'{date[:4].replace("-","_")}_stock_price_info_mac'
    df.to_sql(table_name, con=conn, if_exists='append', index=False)
    conn.close()

    return print(f"{date}, {idx}, {company}, {code}, {'저장 완료':<30s}", end="\r")


def stock_info_scraping():
    # MySQL 테이블을 DataFrame으로 읽기
    engine, conn = create_conn()
    company_list = pd.read_sql_table(f'{today[:7].replace("-","_")}_stock_company_info', con=engine)
    con_name_codes = company_list[['회사명', '종목코드']]
    errors = {}
    for idx, (company, code) in list(con_name_codes.iterrows()):
        stock_price_detail = {}
        url2 =f"https://finance.naver.com/item/main.naver?code={code}"
        r2 = None
        try:
            r2 = requests.get(url2)
            print(f"{r2.status_code}, {idx}/{len(con_name_codes)}, {company:<20s} 수집중", end="\r")
            soup2 = bs(r2.text, 'lxml')
            rate_info2 = soup2.select_one(".rate_info")
            current_price = int((rate_info2.select_one("p.no_today").text).strip("\n").split("\n")[1].replace(",", ""))
            price_change = (rate_info2.select_one("p.no_exday").text).strip("\n").split("\n")[4]
            rate_of_change_str = "".join((rate_info2.select_one("p.no_exday").text).strip("\n").split("\n")[8:10])
            rate_of_change = float(rate_of_change_str) if len(rate_of_change_str) <= 4 else float(rate_of_change_str[:4])
            keys = ('년월일', '회사명', '종목코드', '현재가', '변동금액', '변동률')
            values = (today, company, code, current_price, price_change, rate_of_change)
            for key, value in zip(keys, values):
                stock_price_detail.setdefault(key, []).append(value)
            for trs in rate_info2.select('tr'):
                for td in trs.select('td'):
                    claened_num = int((td.select_one("span.blind").text).replace(",", ""))
                    stock_price_detail.setdefault(td.select_one('span').text, []).append(claened_num)
            stock_price_detail_df = pd.DataFrame(stock_price_detail)
            stock_price_detail_df.to_csv(f"./stock_price_info/{today.replace('-','_')}주가정보.csv", mode= 'a', encoding="utf-8", index=False)
            stock_info_to_db(today, idx, company, code, stock_price_detail_df)
            ran_num = random.uniform(5, 8)
            time.sleep(ran_num)
        except Exception as e:
            print(e)
            print(f"{r2.status_code}, {idx}/{len(con_name_codes)}, {company} 수집중 에러", end="\r")
            for e_key, e_values in zip(('today','idx', 'company', 'code'), (today, idx, company, code)):
                errors.setdefault(e_key, []).append(e_values)
            continue

    # 수집 결과 저장
    
    errors_df = pd.DataFrame(errors)
    print(errors_df.to_string())
    return print(f"{today}_stock_prices have been saved to DB")

    
if __name__ == "__main__":
    stock_info_scraping()





