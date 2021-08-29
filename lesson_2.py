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
# Общий результат можно вывести с помощью dataFrame через pandas.
# Сохраните в json либо csv.

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


def parser_hh(vacancy):
    result = []
    link = 'https://hh.ru/search/vacancy'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }
    params = {
        'text': vacancy,
        'search_field': 'name',
        'items_on_page': '100',
        'page': ''
    }
    response = requests.get(link, params=params, headers=headers)

    if response.ok:
        parsed_html = bs(response.text, 'html.parser')

        page_stop = parsed_html.find('div', {'data-qa': 'pager-block'})

        if not page_stop:
            last_page = '1'
        else:
            last_page = int(page_stop.find_all('a', {'data-qa': 'pager-page'})[-1].getText())

    for page in range(0, last_page):
        params['page'] = page
        html = requests.get(link, params=params, headers=headers)

        if html.ok:
            parsed_html = bs(html.text, 'html.parser')

            vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}).find_all('div', {
                'class': 'vacancy-serp-item'})

            for item in vacancy_items:
                result.append(pars_items_hh(item))

    return result


def pars_items_hh(item):
    vacancy_param = {}

    vacancy_param['site'] = 'www.hh.ru'

    vacancy_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
    vacancy_param['vacancy_name'] = vacancy_name

    try:
        company_name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
        vacancy_param['company_name'] = company_name
    except:
        vacancy_param['company_name'] = None

    vacancy_url = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
    vacancy_param['url'] = vacancy_url

    salary_min = None
    salary_max = None
    currency_salary = None
    try:
        salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        vacancy_salary = salary.getText().split()

        if vacancy_salary[0] == 'от':
            salary_min = int(f'{vacancy_salary[1]}{vacancy_salary[2]}')
        elif vacancy_salary[0] == 'до':
            salary_max = int(f'{vacancy_salary[1]}{vacancy_salary[2]}')
        else:
            salary_min = int(f'{vacancy_salary[0]}{vacancy_salary[1]}')
            salary_max = int(f'{vacancy_salary[3]}{vacancy_salary[4]}')
        currency_salary = vacancy_salary[-1]
    except:
        pass

    vacancy_param['salary_min'] = salary_min
    vacancy_param['salary_max'] = salary_max
    vacancy_param['cur_sal'] = currency_salary

    return vacancy_param


def parser_vacancy(vacancy):
    vacancy_date = []
    vacancy_date.extend(parser_hh(vacancy))
    df = pd.DataFrame(vacancy_date)
    return df


def save_csv(vacancy):
    with open('file.csv', 'a') as f:
        parser_vacancy(vacancy).to_csv(f, header=False, index=False)


if "__main__" == __name__:
    # parser_hh('python')
    # parser_vacancy('python')
    save_csv('python')
