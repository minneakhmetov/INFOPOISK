from os import listdir
from os.path import isfile, join
import re
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from collections import Counter
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

#nltk.download("stopwords") # used only for first time

words_path = 'words.txt'
tokens_path = 'tokens.txt'
sites_path = 'sites'

sites = [f for f in listdir(sites_path) if isfile(join(sites_path, f))]
mystem = Mystem()
russian_stopwords = stopwords.words("russian")
words = []

print('Parsing sites......................')
files_len = len(sites)
for i in range(files_len):
    file = sites[i]
    print('Processing site ' + str(i) + '/' + str(files_len) + '. ' + file)
    html_file = open(sites_path + '/' + file, "r", encoding="utf-8")
    html = html_file.read().replace("<br>", " ")
    html_file.close()
    parsed_html = BeautifulSoup(html, features="html.parser")
    sentence = re.sub(r"[\n\s.,:–\\?—\-!()/»+©\"]+", " ", parsed_html.text, flags=re.UNICODE).lower() # makes normalization faster
    tokens = [token for token in sentence.split(" ") if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation and len(token) > 1]
    words.extend(tokens)
    
words_file = open(words_path, "a", encoding="utf-8")
words_dict = Counter(words)

print('Dumping words to file......................')
for key, value in words_dict.items():
    words_file.write(key + " " + str(value) + "\n")
words_file.close()

tokens = {}

print('Lemmatizing words to file......................')
words_len = len(words)
for i in range(words_len):
    word = words[i]
    print('Processing word ' + str(i) + '/' + str(words_len) + '. ' + word)
    token = mystem.lemmatize(word)[0]
    if token in tokens:
        tokens.get(token).add(word)
    else:
        tokens[token] = set(word)

print("Dumping tokens to file......................")
tokens_file = open(tokens_path, "a", encoding="utf-8")
for key, words_tokens in tokens.items():
    tokens_file.write(key + " ")
    for word in words_tokens:
        if word != key and len(word) > 1:
            tokens_file.write(word + " ")
    tokens_file.write("\n")


