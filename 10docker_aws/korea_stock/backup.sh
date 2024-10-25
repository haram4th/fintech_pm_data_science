#!/bin/bash

# 현재 날짜로 백업 파일명 생성
BACKUP_FILE="/app/db_data/korea_stock_backup_$(date +\%Y-\%m-\%d).sql"

# MySQL 데이터베이스 백업
mysqldump -u${DB_USER} -p${DB_PASSWORD} -h${DB_HOST} ${DB_NAME} > ${BACKUP_FILE}

# 백업이 완료되면 로그에 기록
echo "Database backup completed at $(date)" >> /var/log/cron.log
