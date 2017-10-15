import sys
from db_manager import MONGO_MANAGER
from pymongo import MongoClient

sys.path.append('.')
sys.path.append('../')

client = MongoClient("mongodb://127.0.0.1:20177")

db = client.song
chart = db['gaon_list']


res = {}
total = 0
for song in chart.find():
    if song['song_id'] in list(res.keys()):
        res[song['song_id']]['count'] += 1
    else :
        info = {'song_id':song['song_id'], 'count':1, 'name':song['name'], 'singer':song['singer'], 'album':song['album']}
        res.update({song['song_id'] : info})
    print(song)
    total += 1

manager = MONGO_MANAGER(db_type="mongo",db_name="song")
t = 0


target_db = 'counted_song'
cursor = manager.db_connect[target_db]

for item in list(res.keys()):
    print(item, "\t", res[item])
    if cursor.find_one({'song_id':item}):
        print('update',res[item]['song_id'])
        cursor.update_one({'song_id': item}, {'$set':{'count': res[item]["count"]}})
    else:
        print('insert',res[item])
        manager.insert(target_db, res[item])
    t += 1
print(total, t)
