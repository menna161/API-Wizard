from bs4 import BeautifulSoup
import boto3
import itertools
from datetime import datetime
import config
import cassandra
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import explode, concat_ws, udf, concat, col, lit, when


def parse_files(file_names):
    '\n\tParse the given HTML files\n\n\tParses Silkroad2 HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
    s3 = boto3.resource('s3')
    items = []
    for file_name in file_names:
        if ((file_name is not None) and (file_name is not '')):
            obj = s3.Object(config.s3['S3BUCKET2'], file_name)
            if (obj is not None):
                body = obj.get()['Body'].read()
                x = file_name.split('/')
                date = x[1]
                category = x[3]
                html_soup = BeautifulSoup(body, 'html.parser')
                item_container = html_soup.find_all('div', class_='item')
                for item in item_container:
                    if item.find('div', class_='item_title'):
                        title = item.find('div', class_='item_title')
                        if title.a:
                            link = title.a
                            product_name = title.a.text.strip()
                            href = link.get('href')
                            if item.find('div', class_='item_details'):
                                details = item.find('div', class_='item_details')
                                if details.a:
                                    vendor = details.a.text.strip()
                                    if details.br:
                                        ship_from = details.br.next_sibling.strip()[12:]
                                        ship_to = details.find_all('br')[(- 1)].next_sibling.strip()[10:]
                                    else:
                                        ship_from = ' '
                                        ship_to = ' '
                                    if item.find('div', class_='price_big'):
                                        price = item.find('div', class_='price_big').text.strip()[1:]
                                        items.append(('silkroad2', product_name, float(price), category, vendor, '', datetime.strptime(date, '%Y-%m-%d'), ship_to, ship_from, href))
    return items
