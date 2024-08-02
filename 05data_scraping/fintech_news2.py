import requests
import pandas as pd
from datetime import date
from dbio import news_to_db
from napi_info import client_id, client_secret

client_id = client_id # 네이버 api에 접속 가능한 id 
client_secret = client_secret # 네이버 api에 접속 가능한 pw 
url = "https://openapi.naver.com/v1/search/news.json"
payload = {'query': '핀테크', 'display' : 100, 'start' : 1, 'sort': 'date'}
headers = {"X-Naver-Client-Id" : client_id, "X-Naver-Client-Secret" : client_secret}
r = requests.get(url, params=payload, headers=headers)
print(r.url)
if(r.status_code == 200):
    data = r.json()
    print(type(data))
else:
    print("Error Code:", r.status_code)

def text_clean(x):
    return x.replace("<","").replace("b", "").replace("/b", "").replace(">", "").replace("‘", "").replace("’", "")


today = date.today()
# 원하는 형식으로 변환
formatted_date = today.strftime("%d %b %Y")
print(formatted_date)  # 출력 예: 02 Aug 2024
result = {}
for item in data['items']:
    for key, info in item.items():
        if formatted_date in item['pubDate']:
            result.setdefault(key, []).append(text_clean(item[key]))
        else:
            break

df = pd.DataFrame(result)
news_to_db("fintech_news_test", today, df)



