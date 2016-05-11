import requests
from bs4 import BeautifulSoup
import re

# 샘플데이터
m_s_id = 8174712

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
    lyr = data.strip()


    # 작사가 정보 추출
    creaters = list(soup.find_all("div", class_="box_lyric"))
    for c0 in creaters:
        #print(c0.text,"\n...")
        label = c0.find("dt").text
        atist = c0.find("dd", class_="atist").text
        #print(label, "\t",atist)

    result = {'artist':atist,'lyrics':lyr}
    return result

if __name__ == "__main__":
    y = get_lyric(m_s_id)
    print(y)