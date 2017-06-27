from pymongo import MongoClient

class MONGO_MANAGER:  # DB manage class
    def __init__(self, db_type, db_name):
        if db_type == "mongo":
            client = MongoClient('mongodb://127.0.0.1:27017/')
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
            cursor = self.db_connect[target]
            cursor.insert(row)
        else:
            print("DB connect error occur!")

    def find(self,target,query):
        if self.db_connect is not None:
            cursor = self.db_connect[target]
            return cursor.find(query)
        else:
            print("DB connect error occur!")

