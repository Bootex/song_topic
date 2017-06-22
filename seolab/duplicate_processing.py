from pymongo import MongoClient
import sys

sys.path.append('muse/')
from mongo_man import MONGO_MANAGER

client = MongoClient("mongodb://127.0.0.1:27017")

db = client.song
chart = db['gaon_list']

#writer = csv.writer(open('list.csv','w'))

res = {}
total = 0
for song in chart.find():
    #print(type(song), song)
    #print(song['name'], song['singer'], song['song_id'])
    if song['song_id'] in list(res.keys()):
        #print("count\t", res[song['song_id']]['count'])
        res[song['song_id']]['count'] += 1
    else :
        info = {'song_id':song['song_id'], 'count':1, 'name':song['name'], 'singer':song['singer'], 'album':song['album']}
        res.update({song['song_id'] : info})
        #print("append new item\t", song['name'], song['singer'], song['album'], song['song_id'])
    total += 1

manager = MONGO_MANAGER(db_type="mongo",db_name="song")
t = 0
'''
manager.insert("dp_song",{"a":1111,"b":22222})
'''
for item in list(res.keys()):
    print(item, "\t", res[item])
    manager.insert("dp_song", res[item])
    t += 1
print(total, t)
