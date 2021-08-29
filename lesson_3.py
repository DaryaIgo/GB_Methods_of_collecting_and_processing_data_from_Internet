# Урок 3. Системы управления базами данных MongoDB и SQLite в Python
# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.
import pandas as pd

from pprint import pprint
from pymongo import MongoClient

from lesson_2 import parser_vacancy

client = MongoClient('localhost', 27017)
db = client['Vacancies']

df = parser_vacancy('python')
vacancy = 'python'

df.rename(columns={'Название': 'name',
                   'Ссылка': 'url',
                   'Мин. з/п': 'salary_min',
                   'Макс. з/п': 'salary_max',
                   'Валюта': 'cur_sal'
                   },
          inplace=True)

df_dict = df.to_dict('Records')
db.vacancies.delete_many({})
db.vacancies.insert_many(df_dict)

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).

salary = 1000

objects = db.vacancies.find({'salary_max': {'$gt': salary}})
for obj in objects:
    pprint(obj)
