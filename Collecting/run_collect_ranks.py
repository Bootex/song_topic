import requests as rq
import os,sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from Collecting.db_manager import MONGO_MANAGER

if __name__ == "__main__":

    assert len(sys.argv) == 4

    year, start_week, end_week = sys.argv[1], sys.argv[2],sys.argv[3]

    week_set =  [i for i in range(int(start_week),int(end_week)+1)]
    manager = MONGO_MANAGER(db_type="mongo",db_name="song")
    target_db = 'gaon_list'
    cursor = manager.db_connect[target_db]

    for week in week_set:
        if len(str(week)) == 1: week = "0"+ str(week)

        req = rq.get("http://127.0.0.1:8000/gaon/%s/%s" % (year,str(week)))

        print(req.text)
        gaon_chart = req.json()

        b = ['name','singer','album','company','circulation','rank','play','song_id']


        for i in gaon_chart:
            row = dict(zip(b,i))
            row["year"],row["week"] = year,week
            print(year,week,"  ",row)
            if cursor.find_one({'year':year,'week':week,'song_id':row['song_id']}):
                print('already exist')
            else:
                manager.insert("gaon_list",row)
