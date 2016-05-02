import requests
import re, json
from muse import mongo_man
from bs4 import BeautifulSoup
import time,random

class LYRICS:

    def __init__(self,target):
        self.target = target

        sites = {"bugs": "1594", "melon": "3715"}  # I will add more after
        self.site = sites[target]

    def ga_mel(self,gaon_id):#

        target_url = 'http://www.gaonchart.co.kr/main/section/chart/ReturnUrl.gaon?' \
               'serviceGbn=ALL&seq_company=%s&seq_mom=%s' % (self.site,str(gaon_id))

        res = requests.get(url=target_url)
        res_url = res.url

        if self.target == "melon":
            url_pattern = re.compile("(http|https)://.+=(?P<id>\d+)%?.+")
            result = url_pattern.sub("\g<id>",res_url)
            return result

        elif self.target == "bugs":
            url_pattern = re.compile("(http|https)://.+/(?P<id>\d+)%?.+")
            result = url_pattern.sub("\g<id>",res_url)
            return result

        else:
            return "Bad type"

    def get_melon_song_id(self,m_a_id, title):
        url = "http://www.melon.com/album/detail.htm?albumId=%s"%(str(m_a_id))
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        song_list = list(soup.find_all("a", class_="btn btn_icon_detail"))

        for a in song_list:
            t0 = a.find("span", class_="odd_span").text
            t = t0.split(" 상세정보 페이지 이동")[0]
            if(t==title):
                s_id = str(a).split("'")[1]
                print("title:",t , "\tsong_id:", s_id)
                return s_id

    def get_lyric(self,m_s_id):
        url = "http://www.melon.com/song/detail.htm?songId=%s"  %(str(m_s_id))
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        txt = soup.find("div", class_="lyric")
        line = list(str(txt).split("<br>"))

        rep = re.compile("(<div.+>|</div>|</?br>|\n)")  # 속성값 제거
        data = rep.sub(" ",str(txt))
        x = data.strip()
        return x

if __name__ == "__main__":
    manager = mongo_man.MONGO_MANAGER(db_type="mongo",db_name="song")
    target = manager.db_connect["co_dp_song"]

    Lyric_man = LYRICS("melon")

    count = 0
    for i in target.find({"lyrics":{"$exists":False}}):
        id = i["_id"]
        gaon_id = i["song_id"]
        title = i["name"]
        print(i)

        mel_id = Lyric_man.ga_mel(gaon_id)
        print("mel album is ",mel_id)
        mel_s_id = Lyric_man.get_melon_song_id(int(mel_id), title)
        print("mel id is ", mel_s_id)
        data = Lyric_man.get_lyric(mel_s_id)

        if not data or data is "None":
            print("----------------------\n\n\n\n")
            print("NOT FOUND!!!!!!!")
            print("----------------------\n\n\n\n")
        else:
            print("!!!", data)
            target.update({"_id": id}, {"$set": {"lyrics": data}})
            print("insert Success")
            print("----------------------\n\n\n\n")
            count += 1

        if count > 3:
            break
