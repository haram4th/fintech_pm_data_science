import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

def naver_search2():
    """
    네이버 검색 서비스를 Requests 를 사용해서 구현한 모듈입니다.
    """
    service = input('''검색 서비스 번호를 입력하세요:
    1 블로그
    2 책
    3 뉴스
    4 전문자료
    ''')
    query = input("검색어를 입력하세요: ")
    
    if service == '1':
        service = 'blog'
        sort='sim'
    elif service =='2':
        service = 'book'
        sort='sim'
    elif service =='3':
        service = 'news'
        sort='date'
    elif service =='4':
        service = 'doc'
        
    
    
    book_lists = []
    page = 1
    start = 1
    
    while True:
        client_id = os.getenv('client_id') # 네이버 api에 접속 가능한 id 
        client_secret = os.getenv('client_secret') # 네이버 api에 접속 가능한 pw 
        url = f"https://openapi.naver.com/v1/search/{service}.json"
        payload = dict(query=query, display=10, start=start, sort=sort)
        headers = {"X-Naver-Client-Id" : client_id, "X-Naver-Client-Secret" : client_secret}

        try:
            r = requests.get(url, params=payload, headers=headers)
            if(r.status_code==200):
                data = r.json()
                book_lists.append(data)
                total_page = data['total'] // 10 + 1
                if total_page > 100:
                    total_page = 100
            else:
                print("Error Code:" + rescode)
                break

            if page < total_page:
                page += 1
                if start != 991:
                    start += 10
                elif start == 991:
                    start += 9
                print(f"{page:03d}/{total_page:03d}, start: {start} 추출중", end="\r")
            else:
                break
            time.sleep(0.5)
        except Exception as e:
            print(e)
            break


    print(len(book_lists))
    result = pd.DataFrame()
    for book_list in book_lists:
        temp = pd.json_normalize(book_list['items'])
        result = pd.concat([result, temp])
    result
    result.to_csv(f"naver_{service}_api_fintech_{query}_result.csv", encoding="utf-8")