import requests
import re, json
from melon import mongo_man

def ga_mel(gaon_id):
    target_url = 'http://www.gaonchart.co.kr/main/section/chart/ReturnUrl.gaon?' \
           'serviceGbn=ALL&seq_company=3715&seq_mom=%s' % (str(gaon_id))

    res = requests.get(url=target_url)
    melon_url = res.url
    url_pattern = re.compile("^http://.+=(?P<id>\d+)%09")
    result = url_pattern.sub("\g<id>",melon_url)
    return result

if __name__ == "__main__":
    manager = mongo_man.MONGO_MANAGER(db_type="mongo",db_name="song")
    target = manager.db_connect["Copy_dp_song"]

    for i in target.find():
        id = i["_id"]
        target.update({"_id":id},{"$set": {"name":"eastluck"} })
        print(i)
