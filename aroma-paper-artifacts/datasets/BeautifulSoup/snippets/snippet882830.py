from bs4 import BeautifulSoup
import sys
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
    '\n\tParse the given HTML files\n\n\tParses Agora HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
    sys.setrecursionlimit(10000)
    s3 = boto3.resource('s3')
    items = []
    for file_name in file_names:
        if ((file_name is not None) and (file_name is not '')):
            obj = s3.Object(config.s3['S3BUCKET2'], file_name)
            if (obj is not None):
                body = obj.get()['Body'].read()
                x = file_name.split('/')
                date = x[1]
                html_soup = BeautifulSoup(body, 'html.parser')
                categories = []
                if html_soup.find_all('div', class_='topnav-element'):
                    cats = html_soup.find_all('div', class_='topnav-element')
                    for category in cats:
                        if category.find('a'):
                            categories.append(category.find('a').text)
                    if html_soup.find_all('tr', class_='products-list-item'):
                        products = html_soup.find_all('tr', class_='products-list-item')
                        for row in products:
                            image_id = ''
                            if row.find('td', style='text-align: center;'):
                                if row.find('td', style='text-align: center;').find('img'):
                                    image_id = str(row.find('td', style='text-align: center;').find('img')['src'])
                            if row.find('td', class_='column-name'):
                                if row.find('td', class_='column-name').a:
                                    product_name = str(row.find('td', class_='column-name').a.text).strip()
                                    desc = ''
                                    if row.find('td', class_='column-name').span:
                                        desc = row.find('td', class_='column-name').span.text.strip()
                                    if row.find_next('td').find_next('td').find_next('td'):
                                        price_text = row.find_next('td').find_next('td').find_next('td').text
                                        if (' BTC' in price_text):
                                            price = price_text.split(' ')[0]
                                            (ship_to, ship_from) = ('', '')
                                            if row.find('td', style='white-space: nowrap;'):
                                                shipping = row.find('td', style='white-space: nowrap;')
                                                if (shipping.find('img', class_='flag-img') and shipping.find('i', class_='fa fa-truck') and shipping.find('i', class_='fa fa-truck').next_sibling):
                                                    ship_from = shipping.find('i', class_='fa fa-truck').next_sibling.next_sibling
                                                if shipping.find('i', class_='fa fa-home'):
                                                    ship_to = str(shipping.find('i', class_='fa fa-home').next_sibling).strip().split(' ')[(- 1)]
                                            vendor = ''
                                            if row.find('a', class_='gen-user-link'):
                                                vendor = str(row.find('a', class_='gen-user-link').next_sibling)
                                            categories_str = str('/'.join(categories))
                                            items.append(('agora', product_name, float(price), categories_str, vendor, desc, datetime.strptime(date, '%Y-%m-%d'), ship_to, ship_from, image_id))
    return items
