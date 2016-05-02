from pymongo import MongoClient

class MONGO_MANAGER:  # DB manage class
    def __init__(self, db_type, db_name):
        if db_type == "mongo":
            client = MongoClient('mongodb://data.bootex.xyz:27017/')
            try:
                self.db_connect = client[db_name]
                self.db_type = "mongo"

            except ConnectionRefusedError:
                self.db_connect = None
                self.db_state = False
                print(db_type, "[" + db_name + "] connect Fail")
            else:
                print(db_type, "[" + db_name + "] connect success")

        else:
            print("DB type error occur!")

    def insert(self,target,row):
        if self.db_connect is not None:
            melon_list = self.db_connect[target]
            melon_list.insert(row)
        else:
            print("DB connect error occur!")


import requests as rq
import json

if __name__ == "__main__":
    year,week_set = "2016", [i for i in range(1,15)]
    manager = MONGO_MANAGER(db_type="mongo",db_name="song")

    for week in week_set:
        if len(str(week)) == 1: week = "0"+ str(week)

        req = rq.get("http://data.bootex.xyz:8000/seolab/%s/%s" % (year,str(week)))

        print(req.text)
        gaon_chart = req.json()

        b = ['name','singer','album','company','circulation','rank','play','song_id']

        for i in gaon_chart:
            row = dict(zip(b,i))
            row["year"],row["week"] = year,week
            manager.insert("gaon_list",row)
            print(year,week,"  ",row)
