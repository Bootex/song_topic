import requests as rq
from .db_manager import MONGO_MANAGER

if __name__ == "__main__":
    year,week_set = "2017", [i for i in range(15,25)]
    manager = MONGO_MANAGER(db_type="mongo",db_name="song")

    for week in week_set:
        if len(str(week)) == 1: week = "0"+ str(week)

        req = rq.get("http://127.0.0.1:8000/seolab/%s/%s" % (year,str(week)))

        print(req.text)
        gaon_chart = req.json()

        b = ['name','singer','album','company','circulation','rank','play','song_id']

        for i in gaon_chart:
            row = dict(zip(b,i))
            row["year"],row["week"] = year,week
            manager.find()
            manager.insert("gaon_list",row)
            print(year,week,"  ",row)
