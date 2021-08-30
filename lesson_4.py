# Урок 4. Парсинг HTML. XPath
# Написать приложение, которое собирает основные новости с сайта
# на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath.

# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

# Сложить собранные данные в БД

import requests
from lxml import html
from pymongo import MongoClient
import pandas as pd
from pprint import pprint

news_lenta = []

client = MongoClient('localhost', 27017)
db = client['Lenta_news']

lenta_link = 'https://lenta.ru/'

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
}
response = requests.get(lenta_link, headers=header)
root = html.fromstring(response.text)

elements = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item'] | //section["
                      "@class='row b-top7-for-main js-top-seven']//div[@class='first-item']")

for elem in elements:
    new = {}
    name_new = elem.xpath(".//a[not(@class)]/text() | .//a[@class='b-link-external']/text()")[0]
    name = name_new.replace(u'\xa0', u' ')

    link = elem.xpath(".//a[not(@class)]/@href | .//a[@class='b-link-external']/@href")[0]
    url = lenta_link + link

    source_name = 'lenta.ru'

    source_date = root.xpath(".//a[1]/time[1]/text()")[0]

    new['name'] = name
    new['source_name'] = source_name
    new['source_date'] = source_date
    new['link'] = url

    news_lenta.append(new)

df = pd.DataFrame(news_lenta)

df_dict = df.to_dict('Records')
db.news.delete_many({})
db.news.insert_many(df_dict)

objects = db.news.find()
for obj in objects:
    pprint(obj)
