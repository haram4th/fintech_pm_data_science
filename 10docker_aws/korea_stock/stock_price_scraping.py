import pymysql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# .env 파일에서 환경 변수 로드
load_dotenv()

# MySQL 연결 정보
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# 테이블 존재 여부 확인 함수
def check_table_exists(table_name):
    with engine.connect() as conn:
        query = text(f"SHOW TABLES LIKE '{table_name}'")
        result = conn.execute(query).fetchall()
        return len(result) > 0

# DB에서 상장 기업 목록을 가져오는 함수
def get_stock_list_from_db():
    query = "SELECT 종목코드, 회사명, Market FROM korea_stock_company"
    stock_list = pd.read_sql(query, con=engine)
    return stock_list

# 주가 데이터를 수집하는 함수
def fetch_and_store_stock_data(stock_code, company_name, market):
    try:
        # 종목코드 뒤에 붙일 접미사 결정 (KOSPI -> .KS, KOSDAQ -> .KQ)
        suffix = '.KS' if market == 'KOSPI' else '.KQ'
        stock_code_yahoo = f"{stock_code}{suffix}"
        
        # 오늘 날짜 전날까지 데이터 수집
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"{company_name}({stock_code_yahoo})의 주가 데이터를 수집 중...")
        for year in range(2004, datetime.today().year + 1):  # 2004년부터 현재까지 연도별로 처리
            table_name = f'stock_prices_{year}'
            
            # 테이블이 존재하지 않으면 데이터를 바로 수집하여 테이블 생성
            if not check_table_exists(table_name):
                print(f"Table {table_name} does not exist. It will be created automatically when inserting data.")
                stock_data = yf.download(stock_code_yahoo, start=f'{year}-01-01', end=f'{year}-12-31')
                
                if not stock_data.empty:
                    stock_data['종목코드'] = stock_code
                    stock_data['회사명'] = company_name
                    stock_data.to_sql(table_name, con=engine, if_exists='append', index=True)
                    print(f"New data for {stock_code} ({company_name}) saved to table {table_name}.")
                else:
                    print(f"No data for {stock_code} ({company_name}) in {year}.")
                continue
            
            # 최신 날짜가 있는 경우 이후 데이터 수집
            latest_date_query = f"""
                SELECT MAX(Date) AS latest_date 
                FROM {table_name} 
                WHERE 종목코드='{stock_code}'
            """
            with engine.connect() as conn:
                result = pd.read_sql(latest_date_query, con=conn)
            
            latest_date = result['latest_date'].values[0] if not result.empty else None
            
            # 최신 데이터가 없으면 해당 연도의 처음부터 가져오기
            if pd.isna(latest_date):
                start_date = f'{year}-01-01'
            else:
                start_date = (pd.to_datetime(latest_date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
            
            # 연도 말일 기준으로 데이터 수집
            end_date = f'{year}-12-31' if year < datetime.today().year else today
            
            # 주가 데이터 수집
            stock_data = yf.download(stock_code_yahoo, start=start_date, end=end_date)
            time.sleep(1)

            if not stock_data.empty:
                stock_data['종목코드'] = stock_code
                stock_data['회사명'] = company_name
                stock_data.to_sql(table_name, con=engine, if_exists='append', index=True)
                print(f"New data for {stock_code} ({company_name}) saved to table {table_name}.")
            else:
                print(f"No new data for {stock_code} ({company_name}) in {year}.")
    except Exception as e:
        print(f"Error retrieving data for {stock_code} ({company_name}): {e}")

# 전체 주가 데이터를 수집하고 저장하는 함수
def collect_all_stock_data():
    stock_list = get_stock_list_from_db()
    
    for idx, row in stock_list.iterrows():
        stock_code = row['종목코드']
        company_name = row['회사명']
        market = row['Market']  # KOSPI 또는 KOSDAQ 정보
        
        fetch_and_store_stock_data(stock_code, company_name, market)

# 함수 실행 부분
if __name__ == "__main__":
    collect_all_stock_data()
