# Python 3.10-slim 버전 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 필요한 Python 패키지 설치를 위한 requirements.txt 복사
COPY requirements.txt /app/requirements.txt

# Python 패키지 설치
RUN pip install --no-cache-dir -r /app/requirements.txt

# stock_analysis_autogluon.py 및 stock_data_collector.py 복사
COPY stock_analysis_autogluon.py /app/stock_analysis_autogluon.py
COPY stock_data_collector.py /app/stock_data_collector.py

# .env 파일 복사 (Docker 환경에서 사용할 경우)
COPY .env /app/.env

# 기본 실행 명령 (이 명령은 docker-compose.yml에서 재정의 가능)
CMD ["python", "/app/stock_analysis_autogluon.py"]
