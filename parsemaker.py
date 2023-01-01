import requests
from bs4 import BeautifulSoup as bs
from docxtpl import DocxTemplate
import datetime
import time


# сделать парсер на Орёл 
# добавить подсчет слов для оперативного информирования
themes = ['Военно-политическая обстановка в мире','Новости мировой и отечественной культуры','Актуальные вопросы политической и социально-экономической жизни общества','Актуальные вопросы военной службы, новинки российской техники и вооружения','Новейшие информационные технологии','Актуальные события города Орла и Орловской области']
urls = ['https://ria.ru/world/','https://ria.ru/search/?query=культура','https://ria.ru/politics/','https://ria.ru/defense_safety/','https://ria.ru/search/?query=информационные+технологии','']

# формирование документа
def form_doc(theme, headers, tommorow, mounth, dmy, texts, briefing_text, name):
    doc = DocxTemplate('sample.docx')
    context = {'theme' : theme,
                'tomm_date' : tommorow,
                'm' : mounth,
                'y' : dmy[2],
                'creator_name' : name,
                'header_1' : headers[0],
                'header_2' : headers[1],
                'header_3' : headers[2],
                'header_4' : headers[3],
                'header_5' : headers[4],
                'text_1' : texts[0],
                'text_2' : texts[1],
                'text_3' : texts[2],
                'text_4' : texts[3],
                'text_5' : texts[4],
                'briefing_text' : briefing_text
                }
    doc.render(context)
    doc.save('Информирование.docx')

def get_mounth(date):
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('.')
    return month_list[int(date_list[1]) - 1]

# форматирование даты
def get_date(date):
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('.')
    return ( date_list[0]+ ' ' +
        month_list[int(date_list[1]) - 1] + ' ' +
        date_list[2] + ' года')

# получение завтрашней даты
def tommorow_date():
    today = datetime.date.today()
    tommorow = (today + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
    return tommorow
    
# парсинг РИА Новости
def parse_ria_news(news_count,urls):
    d = datetime.date.weekday(datetime.date.today() + datetime.timedelta(days=1))
    url = urls[d]
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    quotes = soup.find_all('a', class_='list-item__title color-font-hover-only')
    hrefs = []
    news_headers = []
    texts = []
    # сбор ссылок и заговловков
    for i in range(0,news_count):
        hrefs.append(quotes[i].get('href'))
        news_headers.append(quotes[i].text)
    # переход по каждой ссылке и извлечение текста
    for i in range(0,news_count):
        url = hrefs[i]
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        quotes = soup.find_all('div', class_='article__text')
        texts.append(i)
        # добавление абзацев в texts
        for quote in quotes:
            texts.append(quote.text)
    return texts,  news_headers



def parse_briefing():
    url = 'https://z.mil.ru/spec_mil_oper/brief/briefings.htm'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    quotes = soup.find_all('div', class_='newsitem')
    href = quotes[0].find('a').get('href')         # ссылка на брифинг
    briefing_header =  quotes[0].find('a').text     # заголовок
    # спарсить брифинг
    response = requests.get('https://z.mil.ru/' + href)
    soup = bs(response.text, 'lxml')
    quotes = soup.find_all('p')
    text = []
    briefing_text = ''
    for quote in quotes:
        text.append(quote.text)

    text = list(filter(None, text))
        
    for i in range(0, len(text)):
        briefing_text += '\a' + text[i]
    
    return briefing_text

# преобразует массив в формат 1 новость = 1 элемент списка
def modify_texts(texts):
    modified_texts = []

    index_1 = texts.index(1)
    text = ''
    for i in range(1, index_1):
        text += '\a' + texts[i]    
    modified_texts.append(text)

    index_2 = texts.index(2)
    text = ''
    for i in range(index_1 + 1, index_2):
        text += '\a' + texts[i]
    modified_texts.append(text)

    index_3 = texts.index(3)
    text = ''
    for i in range(index_2 + 1, index_3):
        text += '\a' + texts[i]
    modified_texts.append(text)

    index_4 = texts.index(4)
    text = ''
    for i in range(index_3 + 1, index_4):
        text += '\a' + texts[i]
    modified_texts.append(text)

    text = ''
    for i in range(index_4 + 1, len(texts)):
        text += '\a' + texts[i]
    modified_texts.append(text)

    return modified_texts

texts, headers = parse_ria_news(5,urls)
mod_texts = modify_texts(texts)
'''
print('Привет! Это прога сделает тебе информирование на завтра (временно не рекомендуется запускать ее в пятницу и в субботу). \n Для запуска необходимо ввести своё имя в формате "И.И. Иванов".')
your_name = input('Введи имя: ')

texts, headers = parse_ria_news(5,urls) 

tommorow = get_date(tommorow_date()) # получили дату 20 декабря 2022 года
mounth = get_mounth(tommorow_date()) # получили месяц в формате декабря

date_list = tommorow_date().split('.')           # [20 12 2022]
dmy = [date_list[0], date_list[1], date_list[2]] # [20 12 2022]

mod_texts = modify_texts(texts) # 1 новость = 1 элемент списка
briefing_text = parse_briefing()

form_doc(themes[datetime.date.weekday(datetime.date.today() + datetime.timedelta(days=1))],
           headers,
           tommorow,
           mounth,
           dmy,
           mod_texts,
           briefing_text,
           your_name) # cформировали документ

parse_briefing()

print('Твоё информирование готово! Пожалуйста проверь объём информирования))) \n<3')
time.sleep(7)
'''