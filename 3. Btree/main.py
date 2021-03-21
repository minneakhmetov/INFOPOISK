from normalizer import preprocess_text
from db_config import cursor, connection

print('Введите запрос:')
query_tokens = preprocess_text(input())
cursor.execute('SELECT url FROM word join site s on s.id = word.site_id where word.word in %s group by s.url', (tuple(query_tokens),))
result = cursor.fetchall()
print('Результаты:')
for row in result:
    print('\t' + row['url'])
cursor.close()
connection.close()

