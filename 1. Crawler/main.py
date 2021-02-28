import requests, os
search_query = 'кошка'
folder_name = 'sites'
max_requests = 5 # 30 lines per request
index = open("index.txt", "a", encoding="utf-8")
os.mkdir(folder_name)
iterator = 0
for i in range(max_requests):
    request = requests.get('https://www.liveinternet.ru/rating/today.tsv?;search='+ search_query +';page=' + str(i))
    data = request.text.split("\n")
    for row in data[1:30]:
        iterator += 1
        url = row.split("\t")[1].replace("/", "")
        print(str(iterator) + '. ' + url + " ... ", end='')
        try:
            page = requests.get("http://" + url)
            filename = folder_name + '/' + str(iterator) + '. ' + url + ".html"
            html = open(filename, "a", encoding="utf-8")
            html.write(page.text)
            html.close()
            index.write(str(iterator) + '. ' + url + "\n")
        except requests.exceptions.ConnectionError:
            print("not ok")
        else:
            print("ok")
index.close()


