import requests
import html.parser



url = "http://www.gaonchart.co.kr/main/section/chart/online.gaon?nationGbn=T&serviceGbn=ALL&targetTime=11&hitYear=2016&termGbn=week"
res = requests.get(url)
print (res.text)


## 파싱 처리해서 list 뽑아보려 했는데...fail
h = html.parser.HTMLParser()
ti = h.handle_startendtag("td", [("class", "ranking")])
#print(ti)

