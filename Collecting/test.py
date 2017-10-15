import db_manager


mongo_manager = db_manager.MongoManager('song')
query = {"lyrics": {"$exists": True}}
mongo_manager.find('counted_song', query)

min_len = 999999
max_len = 0

for idx, data in enumerate(mongo_manager):
    if data['lyrics']:
        lyric_len = len(data['lyrics'])
        if lyric_len > max_len: max_len = lyric_len
        if lyric_len < min_len: min_len = lyric_len
        print(lyric_len)
print('max: ',max_len)
print('min: ', min_len)
