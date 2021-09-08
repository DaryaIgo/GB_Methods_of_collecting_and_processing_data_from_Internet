# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy0209

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary_hh(item['salary'])
        elif spider.name == 'sj':
            item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary_sj(item['salary'])
        del item['salary']
        item['site'] = spider.allowed_domains[0]

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, item):
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

        return salary_min, salary_max, currency_salary

    def process_salary_sj(self, salary):
        salary_min = None
        salary_max = None
        currency_salary = None
        index = 0
        try:
            for el in salary:
                salary[index] = el.replace('\xa0', '')
                index += 1
            if salary:
                if len(salary) > 4:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                    currency_salary = salary[-2]
                elif salary[0] == 'от':
                    salary_und = re.split(r'(\d+)', salary[2])
                    salary_min = int(salary_und[1])
                    currency_salary = salary_und[-1]
                    salary_max = None
                elif salary[0] == 'до':
                    salary_height = re.split(r'(\d+)', salary[2])
                    currency_salary = salary_height[-1]
                    salary_max = int(salary_height[1])
                    salary_min = None
                elif len(salary) < 5 and salary[0].isdigit():
                    salary_min = int(salary[0])
                    salary_max = int(salary[0])
                    currency_salary = salary[-2]
        except:
            pass

        return salary_min, salary_max, currency_salary
