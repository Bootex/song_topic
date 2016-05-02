import requests
import re, json
from muse import mongo_man

def ga_mel(site,gaon_id):#
    sites = {"bugs":"1594","muse":"3715"} # I will add more after

    target_url = 'http://www.gaonchart.co.kr/main/section/chart/ReturnUrl.gaon?' \
           'serviceGbn=ALL&seq_company=%s&seq_mom=%s' % (sites[site],str(gaon_id))

    res = requests.get(url=target_url)
    res_url = res.url
    if site == "muse":
        url_pattern = re.compile("(http|https)://.+=(?P<id>\d+)%?.+")
        result = url_pattern.sub("\g<id>",res_url)
        print(res_url)
        return result

    elif site == "bugs":
        url_pattern = re.compile("(http|https)://.+/(?P<id>\d+)%?.+")
        result = url_pattern.sub("\g<id>",res_url)
        print(res_url)
        return result

    else:
        return "Bad type"

if __name__ == "__main__":
    for i in range(500):
        try:
            print(ga_mel("muse",604800))
        except:
            print ("muse Die")

        try:
            print(ga_mel("bugs", 604800))
        except:
            print("bugs Die")

        print("count = ",i)
    '''
    manager = mongo_man.MONGO_MANAGER(db_type="mongo",db_name="song")
    target = manager.db_connect["co_dp_song"]

    for i in target.find():
        id = i["_id"]
        gaon_song = i["song_id"]
        m_albumId = ga_mel(gaon_id=gaon_song)
        target.update({"_id":id},{"$set": {"m_albumId":m_albumId} })
    '''
