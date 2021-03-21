from normalizer import preprocess_text
from db_config import cursor, connection

print('Введите запрос:')
query_tokens = preprocess_text(input())
cursor.execute('SELECT url, "tf-idf" FROM tf_idf join site s on s.id = tf_idf.site_id where tf_idf.word in %s group by s.url, "tf-idf" order by "tf-idf"', (tuple(query_tokens),))
result = cursor.fetchall()
print('Результаты:')
all_results = {}
for row in result:
    if row['url'] in all_results.items():
        all_results[row['url']] = all_results.get(row['url']) * row['id']
    else:
        all_results[row['url']] = row['tf-idf']

all_results = dict(sorted(all_results.items(), key=lambda item: item[1]))

for key, value in all_results.items():
    print('\t' + key + ' ' + str(value))
cursor.close()
connection.close()

