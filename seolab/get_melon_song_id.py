import requests
from bs4 import BeautifulSoup

# 샘플데이터
"""
m_a_id = 2330981    # 여자친구 3집
title = "오늘부터 우리는 (Me Gustas Tu)"
"""

def get_melon_song_id(m_a_id, title):
    url = "http://www.muse.com/album/detail.htm?albumId=%s"    %(str(m_a_id))
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    song_list = list(soup.find_all("a", class_="btn btn_icon_detail"))
    for a in song_list:
        #print(a)
        t0 = a.find("span", class_="odd_span").text
        t = t0.split(" 상세정보 페이지 이동")[0]
        if(t==title):
            s_id = str(a).split("'")[1]
            print("title:",t , "\tsong_id:", s_id)
            return s_id

"""
z = get_melon_song_id(2663668, "시간을 달려서 (Rough)")
print(z)
"""