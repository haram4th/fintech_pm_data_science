import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from autogluon.tabular import TabularPredictor
from datetime import datetime, timedelta
import numpy as np
import gradio as gr
import koreanize_matplotlib

# 1. 분석할 주식 리스트 (Apple, Microsoft, Amazon, Tesla, Nvidia, AMD)
tickers = {'AAPL': 'Apple', 'MSFT': 'Microsoft', 'AMZN': 'Amazon', 'TSLA': 'Tesla', 'NVDA': 'Nvidia', 'AMD': 'AMD'}

# 2. 날짜 설정 (2014년 1월 1일부터 전날까지)
end_date = datetime.now() - timedelta(days=1)  # 전날까지의 데이터
start_date = datetime.strptime("2014-01-01", "%Y-%m-%d")  # 2014년 1월 1일부터

# 3. 주식 데이터를 불러오는 함수
def load_stock_data(selected_ticker):
    if selected_ticker not in tickers:
        return f"잘못된 티커를 입력하셨습니다."

    # yfinance로 주식 데이터 불러오기
    df = yf.download(selected_ticker, start=start_date, end=end_date)

    if df.empty:
        return f"{tickers[selected_ticker]}에 대한 데이터가 없습니다."

    return df.head(), df.tail()  # 데이터를 head와 tail로 반환

# 4. 분석 및 시각화하는 함수
def analyze_stock(selected_ticker):
    df = yf.download(selected_ticker, start=start_date, end=end_date)

    # 데이터 전처리
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = (df['Date'] - df['Date'].min()).dt.days  # 날짜를 숫자로 변환

    # 50일, 200일 이동평균선 계산
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # 매수 및 매도 시점 계산
    df['Signal'] = 0
    df.loc[50:, 'Signal'] = np.where(df['MA50'][50:] > df['MA200'][50:], 1, 0)
    df['Position'] = df['Signal'].diff()

    # AutoGluon을 이용한 종가 예측
    train_data = df[['Day', 'Close']].copy()
    train_data = train_data.rename(columns={'Close': 'label'})
    predictor = TabularPredictor(label='label').fit(train_data)

    best_model = predictor.model_best
    models = predictor.get_model_names()
    all_predictions = [predictor.predict(train_data.drop(columns=['label']), model=model) for model in models]
    mean_predictions = np.mean(np.array(all_predictions), axis=0)
    std_predictions = np.std(np.array(all_predictions), axis=0)

    mape = np.mean(np.abs((train_data['label'] - mean_predictions) / train_data['label'])) * 100

    # 향후 30일 예측값 계산
    future_dates = [end_date + timedelta(days=i) for i in range(1, 31)]
    future_days = [(date - df['Date'].min()).days for date in future_dates]
    future_df = pd.DataFrame({'Day': future_days})
    future_all_predictions = [predictor.predict(future_df, model=model) for model in models]
    future_mean_predictions = np.mean(np.array(future_all_predictions), axis=0)
    future_std_predictions = np.std(np.array(future_all_predictions), axis=0)

    # 시각화 함수
    def plot_graph(data_df, future_dates, future_mean_predictions, future_std_predictions, title):
        plt.figure(figsize=(14, 8))
        plt.plot(data_df['Date'], data_df['Close'], label=f'{selected_ticker} Actual Close Prices', color='#A1C6EA')  # 파스텔 블루
        plt.plot(data_df['Date'], data_df['MA50'], label='50-Day Moving Average', color='#F4B3C2', linestyle='--')  # 파스텔 핑크
        plt.plot(data_df['Date'], data_df['MA200'], label='200-Day Moving Average', color='#B3D4A7', linestyle='--')  # 파스텔 그린
        plt.plot(data_df[data_df['Position'] == 1]['Date'], data_df[data_df['Position'] == 1]['Close'], '^', markersize=10, color='red', lw=0, label='Buy Signal')
        plt.plot(data_df[data_df['Position'] == -1]['Date'], data_df[data_df['Position'] == -1]['Close'], 'v', markersize=10, color='blue', lw=0, label='Sell Signal')
        plt.plot(future_dates, future_mean_predictions, label='Future Predicted Prices', color='#B3D4A7', linestyle='--')
        plt.fill_between(future_dates, future_mean_predictions - future_std_predictions, future_mean_predictions + future_std_predictions, color='#B3D4A7', alpha=0.2)
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title(title)
        plt.legend()
        plt.tight_layout()

        # Gradio에서 그래프를 반환할 수 있도록 설정
        return plt.gcf()

    # 전체 기간 그래프
    total_graph = plot_graph(df, future_dates, future_mean_predictions, future_std_predictions, "전체 기간 및 예측")

    # 최근 3개월 데이터
    last_3_months = df[df['Date'] >= (end_date - timedelta(days=90))]
    three_month_graph = plot_graph(last_3_months, future_dates, future_mean_predictions, future_std_predictions, "최근 3개월 및 예측")

    # 최근 1개월 데이터
    last_1_month = df[df['Date'] >= (end_date - timedelta(days=30))]
    one_month_graph = plot_graph(last_1_month, future_dates, future_mean_predictions, future_std_predictions, "최근 1개월 및 예측")

    # MAPE 계산 결과 텍스트와 함께 반환
    return total_graph, three_month_graph, one_month_graph, f"{tickers[selected_ticker]} 분석 완료, MAPE: {mape:.2f}%"

# Gradio 이벤트 정의 수정
def stock_analysis(selected_ticker):
    total_graph, three_month_graph, one_month_graph, analysis_result = analyze_stock(selected_ticker)
    # 각각의 그래프와 텍스트를 개별적으로 반환
    return total_graph, three_month_graph, one_month_graph, analysis_result

# Gradio UI 수정
app = gr.Blocks()

with app:
    gr.Markdown("## 주식 데이터 조회 및 분석")

    stock_ticker_dropdown = gr.Dropdown(choices=list(tickers.keys()), label="주식을 선택하세요", value="AAPL")

    with gr.Row():
        stock_ticker_dropdown

    df_head_output = gr.Dataframe(label="Head 데이터")
    df_tail_output = gr.Dataframe(label="Tail 데이터")

    stock_view_button = gr.Button("주가 보기")

    with gr.Row():
        stock_view_button

    with gr.Row():
        df_head_output
        df_tail_output

    total_graph_output = gr.Plot(label="전체 기간 그래프")
    three_month_graph_output = gr.Plot(label="최근 3개월 그래프")
    one_month_graph_output = gr.Plot(label="최근 1개월 그래프")
    analysis_text_output = gr.Textbox(label="분석 결과")

    stock_analysis_button = gr.Button("주식 분석하기")

    with gr.Row():
        stock_analysis_button

    with gr.Row():
        total_graph_output
        three_month_graph_output
        one_month_graph_output
        analysis_text_output

    # Gradio 이벤트 정의
    stock_view_button.click(load_stock_data, inputs=stock_ticker_dropdown, outputs=[df_head_output, df_tail_output])
    stock_analysis_button.click(stock_analysis, inputs=stock_ticker_dropdown, outputs=[total_graph_output, three_month_graph_output, one_month_graph_output, analysis_text_output])

# Gradio 앱 실행
app.launch(inline=False, inbrowser=True, server_name="0.0.0.0")