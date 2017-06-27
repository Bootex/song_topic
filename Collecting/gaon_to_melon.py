import requests
import re, json
import sys, os
sys.path.append(os.getcwd())
from db_manager import MONGO_MANAGER
from bs4 import BeautifulSoup
import time, random

url="http://www.melon.com/song/detail.htm?songId="+str(8047229)
result=requests.get(url)
soup=BeautifulSoup(result.text)
print(result.text)


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

        print(res_url)


        if self.target == "melon":
            url_pattern = re.compile("((http|https).+=|%.{0,2})")
            result = url_pattern.sub("",res_url)
            return (result)
            #return result

        else:
            return "Bad type"


    def get_melon_song_id(self,m_a_id, title):
        url = "http://www.melon.com/album/detail.htm?albumId=%s"%(str(m_a_id))
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        song_list = list(soup.find_all("a", class_="btn btn_icon_detail"))

        title_pat = re.compile('\W+')
        title = title_pat.sub("",title).lower()

        print(song_list)
        for a in song_list:
            t0 = a.find("span", class_="odd_span").text
            t = t0.split(" 상세정보 페이지 이동")[0]

            t = title_pat.sub("",t).lower()
            print(t,"==",title,t in title, title in t)

            if(t in title or title in t):
                s_id = str(a).split("'")[1]
                return s_id


    def get_lyric(self,m_s_id):
        url = "http://www.melon.com/song/detail.htm?songId=%s"  %(str(m_s_id))
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        txt = soup.find("div", class_="lyric",id="d_video_summary")
        line = list(str(txt).split("<br>"))
        """
        print("첫줄 :", line[0])
        print(line[-2])
        print("마지막줄 :", line[-1])

        print("----------")
        """

        rep = re.compile("(<div.+-->|</div.?>|</?br/?>)") # 속성값 제거
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
    manager = MONGO_MANAGER(db_type="mongo",db_name="song")
    target = manager.db_connect["top_song"]

    Lyric_man = LYRICS("melon")

    count = 0
    try:
        for i in target.find({"lyrics":{"$exists":False},"artist":{"$exists":False},"count":{"$gte":10}}):
        #for i in target.find({"melon_id":"3006873"}):
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
                print("!!!", lyrics,len(lyrics))
                if len(lyrics) <80:
                    print("lyrics is cutted")
                    continue

                target.update({"_id": id}, {"$set": {"artist":artist,"lyrics": lyrics,'melon_id':mel_s_id}})
                print("insert Success")
                print("----------------------\n\n\n\n")
                count += 1

            if count > 1000:
                break

    except Exception as e:
        print(e)
        print("The site block url.")
