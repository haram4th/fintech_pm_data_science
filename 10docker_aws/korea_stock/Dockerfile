# Python 3.10 slim 이미지를 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# curl 설치를 위한 추가
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y cron

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# cron 설정 복사 및 실행 권한 부여
COPY korea_stock_cron.sh /app/korea_stock_cron.sh
RUN chmod +x /app/korea_stock_cron.sh

# wait-for-it.sh 스크립트 복사 및 실행 권한 설정
COPY wait-for-it.sh /usr/bin/wait-for-it.sh
RUN chmod +x /usr/bin/wait-for-it.sh
RUN curl -o /usr/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/bin/wait-for-it.sh

CMD [ "sh", "-c", "/usr/bin/wait-for-it.sh db:3306 --timeout=180 --strict -- && python korea_stock_company_info.py && python stock_estimation.py && cron -f" ]
