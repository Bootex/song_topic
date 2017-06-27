The project is recreated by Shephexd.


My goal is to generate the lyrics based on the current music lyrics in Korea. Before this project, i made the word2vec model with my friend, Seolab. It is a preprocessing before generating lyrics.
But our code is quite messy and difficult to understand, That's why i am repackaging our project. Also, i will try to generate quite natural lyrics with deep learning.



## Database

- gaon_list
- counted_song
- top_song



gaon_list

This collection contains the data with the key value, {year, week,  song_id}. It shows the songs that is displayed in each weeks and each months.



### dp_song

This collection is abstracted one based on gaon_list collection. it contains counted data with the key value, song_id. It is to check how many times the song is displayed on the top rank board.


### top_song

top_song is the data with lyrics. The cut off is used with the count of dp_song. If the count value is bigger than cutoff, the song will be saved with lyrics into top_song collection. It is the main database to




