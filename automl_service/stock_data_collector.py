import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Date, Float, String, BigInteger
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 불러오기
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SQLAlchemy 엔진 생성
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# 한국과 미국 주식 목록 가져오기
def get_all_stock_tickers():
    us_tickers = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'AMD']
    kr_tickers = ['005930.KS', '000660.KS', '035420.KS']
    return us_tickers + kr_tickers

# stock_data 테이블이 있는지 확인하고, 없으면 생성하는 함수
def create_stock_data_table_if_not_exists():
    inspector = inspect(engine)
    if not inspector.has_table("stock_data"):
        metadata = MetaData()
        stock_data_table = Table('stock_data', metadata,
            Column('Date', Date, primary_key=True),
            Column('Open', Float),
            Column('High', Float),
            Column('Low', Float),
            Column('Close', Float),
            Column('Adj_Close', Float),
            Column('Volume', BigInteger),
            Column('Dividends', Float),
            Column('Stock_Splits', Float),
            Column('ticker', String(10), primary_key=True)
        )
        metadata.create_all(engine)
        print("stock_data 테이블이 생성되었습니다.")
    else:
        print("stock_data 테이블이 이미 존재합니다.")

# 주식 데이터를 수집하는 함수
def collect_stock_data():
    create_stock_data_table_if_not_exists()
    
    tickers = get_all_stock_tickers()

    for ticker in tickers:
        print(f'{ticker} 데이터 수집 중...')
        df = yf.download(ticker)
        df.reset_index(inplace=True)
        df['ticker'] = ticker

        # 열 이름 출력
        print(f'{ticker}의 열 이름들:', df.columns)

        # 열 이름 매핑: yfinance에서 반환하는 열 이름을 DB와 일치시키기 위해 변경
        column_mapping = {
            "Adj Close": "Adj_Close",  # 공백이 있는 경우
            "Date": "Date",
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume",
            "Dividends": "Dividends",  # yfinance 데이터에 따라 다름
            "Stock Splits": "Stock_Splits"  # yfinance 데이터에 따라 다름
        }

        # 열 이름을 데이터베이스 스키마와 일치시키기 위해 매핑
        df.rename(columns=column_mapping, inplace=True)

        # 'Dividends'와 'Stock Splits' 컬럼이 없을 때 기본값으로 추가
        if 'Dividends' not in df.columns:
            df['Dividends'] = 0
        if 'Stock_Splits' not in df.columns:
            df['Stock_Splits'] = 0

        # 데이터베이스에서 이미 존재하는 데이터 확인
        date_list = df['Date'].dt.strftime('%Y-%m-%d').tolist()
        date_list_str = "', '".join(date_list)
        existing_data_query = f'SELECT * FROM stock_data WHERE ticker = \'{ticker}\' AND "Date" IN (\'{date_list_str}\')'
        
        # SQL 쿼리 실행하여 기존 데이터 확인
        existing_data = pd.read_sql(existing_data_query, engine)

        # 이미 존재하는 데이터를 업데이트, 새로운 데이터는 추가
        if not existing_data.empty:
            df = df[~df['Date'].isin(existing_data['Date'])]

        # 새 데이터 추가
        if not df.empty:
            df.to_sql('stock_data', engine, if_exists='append', index=False)
            print(f'{ticker} 데이터가 PostgreSQL에 저장되었습니다.')
        else:
            print(f'{ticker}의 새로운 데이터가 없습니다.')

if __name__ == "__main__":
    collect_stock_data()
