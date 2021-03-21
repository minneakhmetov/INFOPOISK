from db_config import cursor, connection

file = 'index.txt'
sql = """
with per_word_count as (select word, count(word) as word_count from word group by word),
     all_words_count as (select count(*) as all_words from word),
     all_sites_count as (select count(*) as count from (select site_id from word group by site_id) as foo),
     tf as (select word, (word_count::double precision / all_words::double precision) as tf
            from per_word_count,
                 all_words_count),
     idf as (select site_id, word, log(all_sites_count.count::double precision / count(word.word)::double precision) as idf
             from word,
                  all_sites_count
             group by site_id, word, all_sites_count.count),
    tf_idf as (select tf.word, tf, idf, (tf * idf) as "tf-idf" from idf join tf on idf.word = tf.word)
select * from tf_idf;
"""
cursor.execute(sql)
result = cursor.fetchall()
index = open(file, 'a', encoding='utf-8')
index.write('word tf idf tf-idf\n')
for row in result:
    index.write(row['word'] + ' ' + str(row['tf']) + ' ' + str(row['idf']) + ' ' + str(row['tf-idf']) + '\n')
cursor.close()
connection.close()

