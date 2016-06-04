import csv

from konlpy.tag import Twitter


reader = csv.reader(open("../sample/top_song.csv",'r'))
writer = csv.writer(open("../sample/top_song_lemma.csv",'w'))
twitter = Twitter()

lema = str()

for i in reader:
    s = twitter.pos(i[4],norm=True)
    x = [i[0] for i in s if i[1] in ['Noun','Verb']]
    print(i[4],"\n",x,"\n"," ".join(x),"\n")

    result = [seg for seg in i]
    result.append(" ".join(x))
    writer.writerow(result)