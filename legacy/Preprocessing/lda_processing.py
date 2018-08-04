#!/usr/bin/python
# -*- coding: utf-8 -*-

## to see logging events
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

## data import from database
from pymongo import MongoClient
class MONGO_MANAGER:  # DB manage class
    def __init__(self, db_type, db_name):
        if db_type == "mongo":
            client = MongoClient('mongodb://data.bootex.xyz:27017/')
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
            melon_list = self.db_connect[target]
            melon_list.insert(row)
        else:
            print("DB connect error occur!")
"""
import sys
sys.path.append("/home/data/song_topic")    # server directory setting
from muse import mongo_man
"""
manager = MONGO_MANAGER(db_type="mongo", db_name="song")
target = manager.db_connect["top_song"]
#target = manager.db_connect["song_detail"]

query = {"$and": [
    {"lyrics": {"$exists": True}},
    {"count": {"$gte": 20}}
]}
proj = {"lyrics": True, "_id": False}
cursor = target.find(query, proj)
lyrics_set = []
for doc in cursor:
    # print(doc["lyrics"])
    lyrics_set.append(str(doc["lyrics"]))
print("===== complete data import =====")

## tokenization and tagging using konlpy
from konlpy.tag import Twitter
tw = Twitter()

## stopword elimination(보류)
""" 패키지 수정해야될지, 진짜 필요한 부분인지, 대체할 수 있는 방법 없는지 논의
from many_stop_words import get_stop_words
stopwords = list(get_stop_words('kr'))
for sw in stopwords:
    print(sw)
"""

## create English stop words list
from stop_words import get_stop_words
en_stop = get_stop_words('en')

## Create p_stemmer of class PorterStemmer
from nltk.stem.porter import PorterStemmer

p_stemmer = PorterStemmer()  # 접미사 제거

# pprint(en_stop)

## list for tokenized documents in loop
texts = []
## loop through document list
for i in lyrics_set:
    # clean and tokenize document string
    i0 = i.lower()
    tokens_pos = tw.pos(i0)
    stopped_tokens = []
    for pos in tokens_pos:
        # print(pos[0], pos[1])
        if pos[1] == "Alpha" and pos[0] in en_stop:
            #print(pos[0], pos[1])
            continue
        #elif pos[1] in ["Josa", "Suffix", "Punctuation", "Number", "Eomi"]:
            # 조사, 접미사, 구두점, 숫자, 어미
        elif pos[1] not in ["Noun", "Verb", "Adjective", "Adverb"]:
            # 명사, 동사, 형용사, 부사
            #print(pos[0], pos[1])
            continue
        ## lemmatization 대신 stemming
        ## porter 방식이 가장 효과적인 방법인지에 대해서는 논의 필요
        #print("insert value:", pos[0], pos[1])
        stopped_tokens.append(p_stemmer.stem(pos[0]))
    texts.append(stopped_tokens)

## remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1] for text in texts]


## gensim 패키지를 이용한 방법 =>> fail
## turn our tokenized documents into a id <-> term dictionary
from gensim import corpora
dictionary = corpora.Dictionary(texts)
print("\n","=========== dictionary ============")
print(dictionary)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate TF-IDF, LDA model
from gensim import models
tfidf_model = models.TfidfModel(corpus)
tfidf = tfidf_model[corpus]
print("\n","=========== TF-IDF ============")
# print first 10 elements of first document's tf-idf vector
print("\n",tfidf.corpus[0][:10])
# print top 10 elements of first document's tf-idf vector
print("\n",sorted(tfidf.corpus[0], key=lambda x: x[1], reverse=True)[:10])
# print token of most frequent element
#print("\n",dictionary.get(13))

n_topics = 5
lda = models.ldamodel.LdaModel(tfidf, num_topics=n_topics, id2word=dictionary, passes=1)
print("\n","=========== lda.show_topics() ============")
#print(lda.show_topics())
print(lda.print_topics(num_topics=n_topics, num_words=10))

import matplotlib
matplotlib.use('qt5agg')

import pyLDAvis.gensim as gensimvis
import pyLDAvis

vis_data = gensimvis.prepare(lda, corpus, dictionary)
x = pyLDAvis.prepared_data_to_html(vis_data)
print (x)


