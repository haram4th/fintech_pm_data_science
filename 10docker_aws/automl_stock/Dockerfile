# Python 3.10 slim 이미지를 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["python", "stock_analysis_autogluon.py"]