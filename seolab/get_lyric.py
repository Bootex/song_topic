import requests
from bs4 import BeautifulSoup
import re

# 샘플데이터
#m_s_id = 8028724

def get_lyric(m_s_id):
    url = "http://www.melon.com/song/detail.htm?songId=%s"  %(str(m_s_id))
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    txt = soup.find("div", class_="lyric")
    line = list(str(txt).split("<br>"))
    """
    print("첫줄 :", line[0])
    print(line[-2])
    print("마지막줄 :", line[-1])

    print("----------")
    """
    rep = re.compile("(<div.+>|</div>|</?br>|\n)")  # 속성값 제거
    data = rep.sub(" ",str(txt))
    x = data.strip()
    #print(x)
    return x
