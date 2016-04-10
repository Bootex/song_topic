import requests
from bs4 import BeautifulSoup

def test(a):
    return a

years = 2015    #range(2010, 2017)
weeks = range(1,52)
#url = "http://www.gaonchart.co.kr/main/section/chart/online.gaon?nationGbn=T&serviceGbn=ALL&targetTime="+str(weeks[45])+"&hitYear="+str(years)+"&termGbn=week"
url = "http://www.gaonchart.co.kr/main/section/chart/online.gaon?nationGbn=T&serviceGbn=ALL&targetTime=%s&hitYear=%s&termGbn=week"  %(str(weeks[45]), str(years))
res = requests.get(url)
#print (res.text)

soup = BeautifulSoup(res.text, 'html.parser')
subject = list(soup.find_all("td", class_="subject"))
production = list(soup.find_all("td", class_="production"))
ranking = list(soup.find_all("td", class_="ranking"))
param_album = list(soup.find_all("div", class_="chart_play"))

#print(param_album[0])

soup0 = BeautifulSoup(str(subject[0]), 'html.parser')   # index 값 주의(rank 순)
title = soup0.p["title"]
song_info = soup0.find("p", class_="singer")["title"]
artist = list(song_info.split(" | "))[0]
album = list(song_info.split(" | "))[1]
soup1 = BeautifulSoup(str(production[0]), 'html.parser')
pro = soup1.find("p", class_="pro")["title"]
dist = soup1.find("p", class_="dist")["title"]
soup2 = BeautifulSoup(str(ranking[0]), 'html.parser')
rank = soup2.span.contents[0]
soup3 = BeautifulSoup(str(param_album[0]), 'html.parser')
href = str(soup3.select('a')[0]).strip()
gaon_company_id = list(href.split('"'))[1]
gaon_album_id = list(href.split('"'))[3]
print(title,"|", artist,"|", album,"|", pro,"|", dist,"|", rank,"|", gaon_company_id,"|", gaon_album_id)

url2 = 'http://www.gaonchart.co.kr/main/section/chart/ReturnUrl.gaon?serviceGbn=ALL&seq_company=3715&seq_mom=%s' %(str(gaon_album_id))
print(url2)
res2 = requests.get(url2)
melon_album_id = list(res2.url.split("="))[1]
print(melon_album_id)