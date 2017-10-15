import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file

from pymongo import MongoClient
from collections import Iterator
class MongoManager(Iterator):  # DB manage class
    def __init__(self, db_name):
        client = MongoClient('mongodb://220.149.124.213:20177/')
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

mongo_manager = MongoManager('song')
mongo_manager.find('counted_song')

lyrics = ""
for idx, data in enumerate(mongo_manager):
    if 'lyrics' in data:
        print(idx, data['lyrics'])
        lyrics +=" " + data['lyrics'].strip() + " ."

lyrics = re.sub('(\t|\n|\r)+', ' ', lyrics)
chars = sorted(list(set(lyrics)))

char2idx = dict((c, i) for i,c in enumerate(chars)) # char to ID
idx2char = dict((i, c) for i,c in enumerate(chars)) # ID to char

maxlen = 20
step = 3
sentences = []
next_chars = []

for i in range(0, len(lyrics) - maxlen, step):
    sentences.append(lyrics[i: i+maxlen])
    next_chars.append(lyrics[i + maxlen])

print("학습할 구문의 수", len(sentences))
print("Learning Text to ID vector")

X = np.zeros((len(lyrics), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(lyrics), len(chars)), dtype=np.bool)


