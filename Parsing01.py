#coding=utf-8
import random

import requests
from bs4 import BeautifulSoup
import json
import csv
from time import sleep

#################################################  1  ################################################################

# первым делом мы с помощью requests.get достанем html всех 23 страниц, затем скормим переменную с этим содержимым супу
# products_urls_list = []
# for i in range(24):
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.928 Yowser/2.5 Safari/537.36'
#     }
#     url = f'https://rusgroupp.ru/store/promyishlennyie-sistemyi-ohlazhdeniya/?page={i}&limit=10&ms%7Cprice=0%2C0&holodoproizvoditelnost=2%2C1764&moshchnost-kompressora=0%2C371'
#     req = requests.get(url=url, headers=headers)
#     src = req.content
#     soup = BeautifulSoup(src, 'lxml')
#     products = soup.find(class_='col-sm-9 col-12 row view view-page-products').find_all(class_='title')
#
#     for product in products:
#         product_url = 'https://rusgroupp.ru/' + product.get('href')
#         products_urls_list.append(product_url)
#
# with open('products_urls_list.txt', 'a', encoding='utf-8') as file:
#     for line in products_urls_list:
#         file.write(f'{line}\n')

# Теперь у нас есть свой файл с ссылками, а значит весь предыдущий код уже не нужен, закомментируем его

##################################################  2  #########################################################

with open('products_urls_list.txt', encoding='utf-8') as file:
    lines = [line.strip() for line in file.readlines()]
    data_list = []
    count = 0
    for line in lines:
        if count == 0:
            req = requests.get(line)
            result = req.content
            soup = BeautifulSoup(result, 'lxml')
            title = soup.find(id='___content', class_='node-products').find(id="page_title").text
            description = soup.find(class_='fullContent col-12').text.replace('\n', '').strip()

            # характеристики представляют из себя таблицу, поэтому парсить будем в два этапа
            features_1 = soup.find(id='content-1', class_='msProductOptions').find_all(class_='_title')
            features_keys = []
            for item in features_1:
                features_keys.append(item.text.replace(':', ''))
            features_2 = soup.find(id='content-1', class_='msProductOptions').find_all(class_='col-6 col-sm-5')
            features_values = []
            for value in features_2:
                features_values.append(value.text.replace(' ', '').strip())
            all_features = dict(zip(features_keys, features_values))
            data = {
                'title': title,
                'description': description,
                'features': all_features
            }
            count += 1
            print(f'#{count}: {line} is done!')
            data_list.append(data)
            with open('data.json' ,'w', encoding='utf-8') as json_file:
                json.dump(data_list, json_file, indent=4, ensure_ascii=False)

            with open('content.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        description,
                        all_features
                    )
                )

            sleep(random.randrange(2, 4))