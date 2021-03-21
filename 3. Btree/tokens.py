from db_config import cursor, connection
from normalizer import preprocess_text
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

cursor.execute('SELECT * FROM site')
sites = cursor.fetchall()

for row in sites:
    print('Processing ' + row['url'])
    html_file = open(row['filename'], "r", encoding="utf-8")
    html = html_file.read().replace("<br>", "\n")
    html_file.close()
    parsed_html = BeautifulSoup(html, features="html.parser")
    tokens = preprocess_text(parsed_html.text)
    for word in tokens:
        cursor.execute('INSERT INTO word (site_id, word) VALUES (%s, %s)', (row['id'], word))
        connection.commit()
cursor.close()
connection.close()