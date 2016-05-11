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
        atist = str()
        for c0 in creaters:
            #print(c0.text,"\n...")
            label = c0.find("dt").text
            try:
                atist = c0.find("dd", class_="atist").text
            except:
                atist = None
            #print(label, "\t",atist)

        result = {'artist':atist,'lyrics':lyr}
        return result


if __name__ == "__main__":
    manager = mongo_man.MONGO_MANAGER(db_type="mongo",db_name="song")
    target = manager.db_connect["top_song"]

    Lyric_man = LYRICS("melon")

    count = 0
    try:
        for i in target.find({"lyrics":{"$exists":False},"artist":{"$exists":False}}):
            id = i["_id"]
            gaon_id = i["song_id"]
            title = i["name"]
            print(i)
            mel_id = Lyric_man.ga_mel(gaon_id)
            print("mel album is ",mel_id)
            mel_s_id = Lyric_man.get_melon_song_id(int(mel_id), title)
            print("mel id is ", mel_s_id)

            if not mel_s_id: continue

            data = Lyric_man.get_lyric(mel_s_id)

            artist,lyrics = data['artist'],data['lyrics']

            if not lyrics or lyrics is "None":
                print("----------------------\n\n\n\n")
                print("NOT FOUND!!!!!!!")
                print("----------------------\n\n\n\n")
            else:
                print("!!!", lyrics)
                target.update({"_id": id}, {"$set": {"artist":artist,"lyrics": lyrics,'melon_id':mel_s_id}})
                print("insert Success")
                print("----------------------\n\n\n\n")
                count += 1
                time.sleep(20)

            if count > 1000:
                break


    except Exception as e:
        print(e)
        print("The site block url.")
