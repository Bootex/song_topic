import requests
from bs4 import BeautifulSoup


def gaon_top_rank(year, week) :
    """
    y_li = range(2010, 2016+1)       # y_li[5] = 2015
    w_li = range(1,52+1)             # w_li[45] = 46
    year = str(y_li[5])
    week = str(w_li[43])
    """
    print(year, week)
    url = "http://www.gaonchart.co.kr/main/section/chart/online.gaon?nationGbn=T&serviceGbn=ALL&targetTime=%s&hitYear=%s&termGbn=week"  %(week, year)
    res = requests.get(url)
    #print (res.text)

    soup = BeautifulSoup(res.text, 'html.parser')
    subject = list(soup.find_all("td", class_="subject"))
    production = list(soup.find_all("td", class_="production"))
    ranking = list(soup.find_all("td", class_="ranking"))
    param_album = list(soup.find_all("div", class_="chart_play"))

    #print(param_album[0])
    #idx = 0

    top_rank = []
    for idx in list(range(100)) :
        ## 가온차트 정보 수집
        soup0 = BeautifulSoup(str(subject[idx]), 'html.parser')
        title = soup0.p["title"]    # 음원제목

        song_info = soup0.find("p", class_="singer")["title"]
        artist = list(song_info.split(" | "))[0]    # 아티스트명
        album = list(song_info.split(" | "))[1]     # 앨범명

        soup1 = BeautifulSoup(str(production[idx]), 'html.parser')
        pro = soup1.find("p", class_="pro")["title"]    # 제작사
        dist = soup1.find("p", class_="dist")["title"]  # 유통사

        soup2 = BeautifulSoup(str(ranking[idx]), 'html.parser')
        if idx < 5 :
            rank = soup2.span.contents[0]   # 5위이내 순위정보
        else :
            rank = soup2.td.contents[0]     # 6~100위 순위정보

        soup3 = BeautifulSoup(str(param_album[idx]), 'html.parser')
        href = str(soup3.select('a')[0]).strip()
        gaon_company_id = list(href.split('"'))[1]      # 가온차트 내 회사코드
        gaon_album_id = list(href.split('"'))[3]        # 가온차트 내 앨범코드
        """
        ### 멜론 앨범id 수집
        url2 = 'http://www.gaonchart.co.kr/main/section/chart/ReturnUrl.gaon?serviceGbn=ALL&seq_company=3715&seq_mom=%s' %(str(gaon_album_id))
        res2 = requests.get(url2)
        melon_album_id = list(res2.url.split("="))[1]
        if melon_album_id.count('%') > 0 :
            melon_album_id = melon_album_id.split('%')[0]

        url3 = 'http://www.melon.com/album/detail.htm?albumId=%s' %(str(melon_album_id))
        print(title,"\t", artist,"\t", album,"\t", pro,"\t", dist,"\t", rank,"\t", gaon_company_id,"\t", gaon_album_id,"\t",melon_album_id)
        gaon_li = [title, artist, album, pro, dist, rank, gaon_company_id, gaon_album_id, melon_album_id]
        """
        print(title,"\t", artist,"\t", album,"\t", pro,"\t", dist,"\t", rank,"\t", gaon_company_id,"\t", gaon_album_id)
        gaon_li = [title, artist, album, pro, dist, rank, gaon_company_id, gaon_album_id]
        top_rank.append(gaon_li)
    return top_rank