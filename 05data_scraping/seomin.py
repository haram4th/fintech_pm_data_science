import requests
import certifi
from bs4 import BeautifulSoup as bs

# url = "https://apis.data.go.kr/1160100/service/GetSmallLoanFinanceInstituteInfoService/getOrdinaryFinanceInfo"
url2 = "https://apis.data.go.kr/1160100/service/GetSmallLoanFinanceInstituteInfoService/getOrdinaryFinanceInfo?serviceKey=8Ym5dhmVJdr12XzGnyYrQjSBS1QuRBYK8yHfx65JCl4vACM9uLKo8fxCVOFJkPB71llD7F2rOEROZnHgNGoj3A%3D%3D"
# service_key = "8Ym5dhmVJdr12XzGnyYrQjSBS1QuRBYK8yHfx65JCl4vACM9uLKo8fxCVOFJkPB71llD7F2rOEROZnHgNGoj3A=="
# payload = dict(serviceKey=service_key, numOfRows=1, pageNo=1, resultType="json")
r = requests.get(url2)
print(r.url)
print(r.status_code)
print(r.text)
