import mongo_man

if __name__ == "__main__":
    manager = mongo_man.MONGO_MANAGER(db_type="mongo",db_name="song")
    source = manager.db_connect["dp_song"]
    target = manager.db_connect["top_song"]

    count = 0

    for i in source.find({"count":{"$gte":15}}):
        print(i["_id"])
        FLAG = target.find_one({"_id":i["_id"]})
        
        if not FLAG:
            manager.insert("top_song",i);

