# Урок 1. Парсинг данных: Основы клиент-серверного взаимодействия.
# Парсинг API

# 1 Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев
# для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
import json
import requests

url = 'https://api.github.com'
user = 'DaryaIgo'

response = requests.get(f'{url}/users/{user}/repos')

with open('data.json', 'w') as f:
    json.dump(response.json(), f)

for _ in response.json():
    print(_['name'])
