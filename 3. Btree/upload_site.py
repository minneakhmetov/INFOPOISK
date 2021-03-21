from os import listdir
from os.path import isfile, join
from db_config import cursor, connection


sites_path = 'sites'
sites = [f for f in listdir(sites_path) if isfile(join(sites_path, f))]
insert_query = 'INSERT INTO site (url, filename) VALUES (%s, %s)'


for site in sites:
    print('Processing ' + site)
    url = site.split('.html', 1)[0]
    cursor.execute(insert_query, (url, sites_path + "/" + site))
    connection.commit()
cursor.close()
connection.close()
