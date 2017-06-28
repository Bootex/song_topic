from db_manager import MONGO_MANAGER
from gaon_to_melon import LYRICS

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
