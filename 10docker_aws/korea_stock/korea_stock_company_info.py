import pymysql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

# MySQL 연결 정보
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# 데이터베이스 생성 함수
def create_database_if_not_exists():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"Database '{db_name}' checked/created successfully.")
    finally:
        connection.close()

# KRX 상장 기업 목록 가져오기 (FinanceDataReader)
def get_fdr_stock_list():
    return fdr.StockListing('KRX')

# 한국 주식 목록 가져오기 (KRX 홈페이지)
def get_kr_stock_list():
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    kr_stock_list = pd.read_html(url, header=0, encoding='euc-kr')[0]
    kr_stock_list['종목코드'] = kr_stock_list['종목코드'].apply(lambda x: f'{x:06d}')
    return kr_stock_list

# 두 개의 데이터프레임을 합쳐서 반환하는 함수
def merge_stock_lists():
    stock_list_fdr = get_fdr_stock_list()
    stock_list_kr = get_kr_stock_list()

    # FinanceDataReader 데이터프레임의 열 이름 변경
    stock_list_fdr.rename(columns={'Code': '종목코드', 'Name': '회사명'}, inplace=True)

    # 두 데이터프레임을 '종목코드' 기준으로 inner join
    merged_stock_list = pd.merge(stock_list_fdr, stock_list_kr, on='종목코드', how='inner')
    merged_stock_list
    return merged_stock_list

# 테이블이 없으면 생성하는 함수 (데이터프레임 컬럼에 맞게 테이블 생성)
def create_table_based_on_dataframe(df):
    # 데이터프레임의 컬럼을 추출하여 SQL 테이블 생성 쿼리를 동적으로 생성
    columns = ", ".join([f"`{col}` VARCHAR(255)" for col in df.columns])

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS korea_stock_company (
        {columns}
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_table_query))
        print("Table 'korea_stock_company' created successfully based on dataframe columns.")
        
# 상장 기업 목록을 DB에 저장하는 함수
def insert_stock_company_data():
    # 데이터 수집 후 병합
    merged_stock_list = merge_stock_lists()

    # 필요 없는 컬럼을 삭제
    columns_to_drop = ['ISU_CD', 'Dept', 'Close', 'ChangeCode', 'Changes', 'ChagesRatio', 
                       'Open', 'High', 'Low', 'Volume', 'Amount', 'MarketId', '회사명_y']
    merged_stock_list = merged_stock_list.drop(columns=columns_to_drop)

    # '회사명_x' 컬럼 이름을 '회사명'으로 변경
    merged_stock_list = merged_stock_list.rename(columns={'회사명_x': '회사명'})
    display(merged_stock_list)
    # 테이블이 없으면 데이터프레임을 참고하여 테이블 생성
    create_table_based_on_dataframe(merged_stock_list)

    # 기존 종목코드 목록 가져오기
    existing_codes = get_existing_stock_codes()

    # 기존 데이터에 없는 종목만 필터링
    new_data = merged_stock_list[~merged_stock_list['종목코드'].isin(existing_codes)]

    if not new_data.empty:
        # 새 데이터만 MySQL에 추가
        new_data.to_sql('korea_stock_company', con=engine, if_exists='append', index=False)
        print(f"New stock company data inserted successfully.")
    else:
        print("No new data to insert.")


# 테이블에서 이미 존재하는 종목코드 목록을 가져오는 함수
def get_existing_stock_codes():
    query = "SELECT 종목코드 FROM korea_stock_company"
    try:
        existing_codes = pd.read_sql(query, con=engine)['종목코드'].tolist()
    except Exception:
        # 테이블이 없을 경우 빈 리스트 반환
        existing_codes = []
    return existing_codes

# 함수 실행 부분
if __name__ == "__main__":
    # 데이터베이스 생성 확인
    create_database_if_not_exists()

    # 상장 기업 데이터 삽입 또는 업데이트
    insert_stock_company_data()
