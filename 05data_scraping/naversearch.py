import os
import sys
import urllib.request
import json
import pandas as pd
import time
from dotenv import load_dotenv
load_dotenv()

def naver_search():
    """
    이 함수는 naver 검색 api를 이용해서 블로그, 책, 뉴스, 전문자료를 검색하는 함수입니다.
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
        encText = urllib.parse.quote(query)
    #     print(encText)
        url = f"https://openapi.naver.com/v1/search/{service}.json?query={encText}&display=10&start={start}&sort={sort}"
    #     print("url:", url, end="\r")
        try:
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                data = json.loads(response_body.decode('utf-8'))
                book_lists.append(json.loads(response_body.decode('utf-8')))
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
    
