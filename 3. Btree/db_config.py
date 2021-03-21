import psycopg2.extras
connection = psycopg2.connect(dbname='razil', user='postgres', password='postgres', host='localhost')
cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)