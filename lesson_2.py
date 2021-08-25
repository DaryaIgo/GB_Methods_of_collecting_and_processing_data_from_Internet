# Урок 2. Парсинг HTML. BeautifulSoup, MongoDB
# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с HH
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#   Наименование вакансии.
#   Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта, цифры преобразуем к цифрам).
#   Ссылку на саму вакансию.
#   Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии
# (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.
# Сохраните в json либо csv.

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re


def parser_hh(vacancy):
    result = []
    url = 'https://spb.hh.ru'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/92.0.4515.159 Safari/537.36'
    }
    params = {
        'text': vacancy,
        'search_field': 'name',
        'items_on_page': '100',
        'page': ''
    }
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)

    if response.ok:
        parsed_html = bs(response.text, 'html.parser')
        pages = parsed_html.find_all('a', {'data-qa': 'pager-page'})
        last_page = []
        for page in pages:
            last_page.append(int(page.find('span').text))

        for elem in range(0,  last_page[-1] - 1):
            if len(last_page) > 1:
                params['page'] = elem
                response = requests.get(url + '/search/vacancy', params=params, headers=headers)
                parsed_html = bs(response.text, 'html.parser')
                vacancies = parsed_html.find_all('div', {'class': 'vacancy-serp-item'})
                for vacancy in vacancies:
                    result.append(pars_items_hh(vacancy))

    return result


def pars_items_hh(item):
    vacancy_param = {}

    vacancy_param['site'] = 'www.hh.ru'

    vacancy_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
    vacancy_param['vacancy_name'] = vacancy_name

    company_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
    vacancy_param['company_name'] = company_name

    vacancy_url = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
    vacancy_param['url'] = vacancy_url

    salary = item.find('span', {'data-qa': 'vacancy-serp-item__compensation'})

    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace(u'\xa0', u'')
        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[1])

        salary_currency = salary[2]

    vacancy_param['salary_min'] = salary_min
    vacancy_param['salary_max'] = salary_max
    vacancy_param['salary_currency'] = salary_currency

    return vacancy_param


def scrap_hh(vacancy):
    result = []
    result.extend(parser_hh(vacancy))
    df = pd.DataFrame(result)
    return df


if __name__ == '__main__':
    parser_hh('python')