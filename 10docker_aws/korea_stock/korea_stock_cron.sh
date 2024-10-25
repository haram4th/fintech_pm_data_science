#!/bin/sh
# Crontab for stock update tasks

# Every day at 6:30 PM: Update the stock company info
echo "30 18 * * * python /app/korea_stock_company_info.py >> /var/log/cron.log 2>&1" > /etc/cron.d/korea_stock_cron

# Every day at 6:40 PM: Start stock price scraping
echo "40 18 * * * python /app/stock_price_scraping.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/korea_stock_cron

# Set proper permissions and apply cron job
chmod 0644 /etc/cron.d/korea_stock_cron
crontab /etc/cron.d/korea_stock_cron

# Start cron
touch /var/log/cron.log
crond -f
