from pymongo import MongoClient
from collections import Iterator


class MongoManager(Iterator):  # DB manage class
    def __init__(self, db_name):
        client = MongoClient('mongodb://127.0.0.1:20177/')
        self.data = list()
        db_type = "mongo"

        try:
            self.db_connect = client[db_name]

        except ConnectionRefusedError:
            self.db_connect = None
            self.db_state = False
            print(db_type, "[" + db_name + "] connect Fail")
        else:
            print(db_type, "[" + db_name + "] connect success")

    def insert(self, target, row):
        if self.db_connect is not None:
            cursor = self.db_connect[target]
            cursor.insert(row)
        else:
            print("DB connect error occur!")

    def find(self, target, query={}):
        if self.db_connect is not None:
            cursor = self.db_connect[target]
            self.data = cursor.find(query)
        else:
            print("DB connect error occur!")

    def __next__(self):
        if self.data is None:
            raise StopIteration
        return next(self.data)


if __name__ == '__main__':
    mongo_manager = MongoManager('song')
    mongo_manager.find('counted_song')
    for idx, data in enumerate(mongo_manager):
        print(idx, data)
        if idx > 10:
            break
