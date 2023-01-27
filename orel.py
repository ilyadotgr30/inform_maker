
import requests
from bs4 import BeautifulSoup as bs
from docxtpl import DocxTemplate
import datetime
import time

d = datetime.date.weekday(datetime.date.today() + datetime.timedelta(days=1))
url = 'https://newsorel.ru/'
response = requests.get(url)
soup = bs(response.text, 'lxml')
quotes = soup.find_all('a', class_='post-title')
hrefs = []
news_headers = []
texts = []
# сбор ссылок и заговловков
for i in range(0,6):
    hrefs.append(quotes[i].get('href'))
    news_headers.append(quotes[i].text)
# переход по каждой ссылке и извлечение текста

for i in range(0,6):
    url_to_parse = url + hrefs[i]
    response = requests.get(url_to_parse)
    soup = bs(response.text, 'lxml')
    quotes = soup.find('div', class_='post-content')
    quotes = quotes.find_all('p')
    texts.append(i)
    url_to_parse = ''
    # добавление абзацев в texts
    for quote in quotes:
        texts.append(quote.text)

print(texts)

'''
test_url = 'https://newsorel.ru/fn_1283367.html'
response = requests.get(test_url)
soup = bs(response.text, 'lxml')
quotes = soup.find('div', class_='post-content')
quotes = quotes.find_all('p')
texts = [text.text for text in quotes]
print(texts)
'''
