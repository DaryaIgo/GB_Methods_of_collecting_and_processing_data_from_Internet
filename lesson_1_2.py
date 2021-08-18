# Урок 1. Парсинг данных: Основы клиент-серверного взаимодействия.
# Парсинг API

# 2 Изучить список открытых API.
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import requests

# для авторизации в API Trello
auth_params = {
    'key': '4a476b77ed0a26e096aacb6ba2dffb34',
    #в целях безопасности не публикую токен
    'token': "toker"
}

url_main = "https://api.trello.com/1/{}"
board_id = "queWGUef"


column_data = requests.get(url_main.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

# не знаю почему, но только так получилось хоть что-то записать в файл
data_1 = str(column_data[0])
data = data_1
f = open("datatrello.json", "w")
f.write(data)
f.close()
