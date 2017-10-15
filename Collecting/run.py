import collector
import db_manager

if __name__ == '__main__':
    mongo_manager = db_manager.MongoManager('song')
    query = {"melon_id": {'$exists': False}}
    mongo_manager.find('counted_song', query)
    lyric_manager = collector.lyrics('bugs')

    for idx, data in enumerate(mongo_manager):
        try:
            lyric_url = lyric_manager.match_id(data['song_id'], data['name'])
            lyric = lyric_manager.get_lyrics(lyric_url)
            print("lyric:", lyric)
            print(idx, data)
            mongo_manager.db_connect['counted_song'].update({"_id": data["_id"]}, {"$set":
                {"lyrics": lyric.strip(), "melon_id":0}})
        except Exception as e:
            print(e)
            continue
        if idx > 600:
            break
