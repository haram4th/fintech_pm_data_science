import pymysql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import gradio as gr
import logging
import numpy as np
import koreanize_matplotlib
from autogluon.tabular import TabularPredictor

# .env 파일에서 환경 변수 로드
load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.info("Starting stock_estimation.py...")

# MySQL 연결 정보
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4")

# 회사명을 입력받아 부분 일치하는 회사 리스트를 반환하는 함수
def search_company_by_name(partial_name):
    query = text("SELECT 종목코드, 회사명 FROM korea_stock_company WHERE 회사명 LIKE :company_name")
    result = pd.read_sql(query, con=engine, params={"company_name": f"%{partial_name}%"} )
    
    if result.empty:
        return [], f"'{partial_name}'와(과) 일치하는 회사를 찾을 수 없습니다."
    
    # Dropdown에 표시할 회사 목록 생성
    company_list = [f"{row['회사명']} ({row['종목코드']})" for idx, row in result.iterrows()]
    
    return company_list, None

# 모든 연도별 테이블에서 데이터를 불러와서 합치는 함수
def load_all_stock_data(company_code, start_date, end_date):
    years = range(2004, datetime.today().year + 1)
    combined_df = pd.DataFrame()

    for year in years:
        table_name = f"stock_prices_{year}"
        try:
            # 파라미터 바인딩 대신 직접 값 삽입
            query = f"""
            SELECT Date, Open, High, Low, Close, Volume, 종목코드, 회사명
            FROM {table_name}
            WHERE 종목코드 = '{company_code}'
            AND Date BETWEEN '{start_date}' AND '{end_date}'
            """
            
            # 쿼리 실행 로그 출력
            logging.info(f"Executing query on table {table_name}: {query}")
            
            df = pd.read_sql(query, con=engine)
            
            if not df.empty:
                combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            logging.warning(f"Error loading data from table {table_name}: {e}")
    
    if combined_df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "해당 기간에 데이터가 없습니다."  # 에러 메시지 반환

    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    return combined_df.head(), combined_df.tail(), combined_df, None  # 에러가 없을 때 None 반환


# 선택된 종목코드를 저장할 변수
selected_company_code = None

# 분석 및 시각화하는 함수
def analyze_stock_from_db(company_code, start_date, end_date):
    # 종목코드와 기간을 이용하여 load_all_stock_data 함수로 데이터를 불러옴
    combined_df_head, combined_df_tail, combined_df, error_message = load_all_stock_data(company_code, start_date, end_date)

    if error_message:
        return None, None, None, error_message

    # 분석할 데이터 (combined_df 전체를 사용)
    df = combined_df

    if df.empty:
        return None, None, None, f"종목 코드 '{company_code}'에 대한 데이터가 없습니다."
    
    # 열 이름 정리 (예: Adj Close -> Adj_Close)
    if 'Adj Close' in df.columns:
        df.rename(columns={'Adj Close': 'Adj_Close'}, inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = (df['Date'] - df['Date'].min()).dt.days

    # 50일, 200일 이동평균선 계산
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    df['Signal'] = 0
    df.loc[50:, 'Signal'] = np.where(df['MA50'][50:] > df['MA200'][50:], 1, 0)
    df['Position'] = df['Signal'].diff()

    # AutoGluon을 이용한 종가 예측
    train_data = df[['Day', 'Close']].copy()
    train_data = train_data.rename(columns={'Close': 'label'})
    
    # AutoGluon 학습 모델 적용
    predictor = TabularPredictor(label='label').fit(train_data)

    # 향후 30일 예측값 계산
    future_dates = [df['Date'].max() + timedelta(days=i) for i in range(1, 31)]
    future_days = [(date - df['Date'].min()).days for date in future_dates]
    future_df = pd.DataFrame({'Day': future_days})

    # AutoGluon으로 미래 30일 예측
    future_predictions = predictor.predict(future_df)

    # 시각화 함수
    def plot_graph(data_df, future_dates, future_predictions, title):
        plt.figure(figsize=(14, 8))
        plt.plot(data_df['Date'], data_df['Close'], label=f'{company_code} Actual Close Prices', color='#A1C6EA')
        plt.plot(data_df['Date'], data_df['MA50'], label='50-Day Moving Average', color='#F4B3C2', linestyle='--')
        plt.plot(data_df['Date'], data_df['MA200'], label='200-Day Moving Average', color='#B3D4A7', linestyle='--')
        plt.plot(data_df[data_df['Position'] == 1]['Date'], data_df[data_df['Position'] == 1]['Close'], '^', markersize=10, color='red', label='Buy Signal')
        plt.plot(data_df[data_df['Position'] == -1]['Date'], data_df[data_df['Position'] == -1]['Close'], 'v', markersize=10, color='blue', label='Sell Signal')
        # 예측된 미래 가격 추가
        plt.plot(future_dates, future_predictions, label='Future Predicted Prices', color='#B3D4A7', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        
        return plt.gcf()

    # 전체 기간 시각화
    total_graph = plot_graph(df, future_dates, future_predictions, "전체 기간 및 예측")
    
    # 최근 3개월 시각화
    last_3_months = df[df['Date'] >= (df['Date'].max() - timedelta(days=90))]
    three_month_graph = plot_graph(last_3_months, future_dates, future_predictions, "최근 3개월 및 예측")
    
    # 최근 1개월 시각화
    last_1_month = df[df['Date'] >= (df['Date'].max() - timedelta(days=30))]
    one_month_graph = plot_graph(last_1_month, future_dates, future_predictions, "최근 1개월 및 예측")

    return total_graph, three_month_graph, one_month_graph, f"종목 코드 '{company_code}' 분석 완료"
    
    
# Gradio UI 수정
app = gr.Blocks()

with app:
    gr.Markdown("## 주식 데이터 조회 및 분석")
    
    stock_name_input = gr.Textbox(label="회사명을 입력하세요 (부분 입력 가능)", interactive=True)
    start_date_input = gr.Textbox(label="시작 날짜 (YYYY-MM-DD)", value="2014-01-01")
    end_date_input = gr.Textbox(label="종료 날짜 (YYYY-MM-DD)", value=datetime.now().strftime('%Y-%m-%d'))
    
    company_dropdown = gr.Dropdown(label="검색된 회사 목록", choices=[], interactive=True)
    df_head_output = gr.Dataframe(label="Head 데이터")
    df_tail_output = gr.Dataframe(label="Tail 데이터")
    error_output = gr.Textbox(label="에러 메시지", visible=False)
    
    stock_view_button = gr.Button("주가 보기")
    stock_analysis_button = gr.Button("주식 분석하기")

    # 회사명 입력 시 엔터를 누르면 자동으로 검색 실행
    def update_dropdown(company_name):
        company_list, error_message = search_company_by_name(company_name)
        return gr.update(choices=company_list), error_message

    stock_name_input.submit(fn=update_dropdown, 
                            inputs=[stock_name_input], 
                            outputs=[company_dropdown, error_output])

    # 드롭다운에서 선택 시 선택한 회사명을 Textbox에 업데이트하고 종목코드를 저장
    def update_textbox(selected_company):
        global selected_company_code
        company_name = selected_company.split(" (")[0]  # 회사명만 반환
        selected_company_code = selected_company.split(" (")[-1].strip(")")  # 종목코드 추출
        return company_name  # 화면에는 회사명만 반환

    company_dropdown.change(fn=update_textbox, 
                            inputs=[company_dropdown], 
                            outputs=[stock_name_input])

    # 주가 보기 버튼 클릭 시 실행
    def on_stock_view_button_click(company_name, start_date, end_date):
        global selected_company_code
        if selected_company_code is None:
            return pd.DataFrame(), pd.DataFrame(), "종목 코드가 선택되지 않았습니다."
        
        # 종목코드를 이용해 DB 검색
        print("company_code", company_name, selected_company_code)
        
        # load_all_stock_data 호출하여 데이터 가져옴
        df_head, df_tail, combined_df, error_message = load_all_stock_data(selected_company_code, start_date, end_date)
        
        # 세 번째 출력으로 error_message 추가
        if error_message:
            return df_head, df_tail, error_message  # 에러 메시지를 반환
        
        return df_head, df_tail, ""  # 에러가 없을 경우 빈 메시지를 반환

    stock_view_button.click(fn=on_stock_view_button_click, 
                            inputs=[stock_name_input, start_date_input, end_date_input], 
                            outputs=[df_head_output, df_tail_output, error_output])
    
    total_graph_output = gr.Plot(label="전체 기간 그래프")
    three_month_graph_output = gr.Plot(label="최근 3개월 그래프")
    one_month_graph_output = gr.Plot(label="최근 1개월 그래프")
    analysis_text_output = gr.Textbox(label="분석 결과")
    
    stock_analysis_button.click(
        fn=lambda start_date, end_date: analyze_stock_from_db(selected_company_code, start_date, end_date), 
        inputs=[start_date_input, end_date_input], 
        outputs=[total_graph_output, three_month_graph_output, one_month_graph_output, analysis_text_output]
    )

app.launch(inline=False, inbrowser=True, server_name="0.0.0.0")
