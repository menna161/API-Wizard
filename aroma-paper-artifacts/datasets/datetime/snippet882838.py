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
    '\n\tParse the given HTML files\n\n\tParses Cryptomarket HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
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
                if html_soup.find_all('div', id='img'):
                    contents = html_soup.find_all('div', id='img')
                    i = 0
                    for content in contents:
                        i += 1
                        if (content.find('img', style='width:80px; height:80px') and content.find('div', id='img')):
                            images = content.find_all('img', style='width:80px; height:80px')
                            image_id = images[0]['src']
                        if content.find('div', style='min-width:200px'):
                            product_name = content.find('div', style='min-width:200px').find('a').text
                            price_raw = content.find('b', style='color:#fff665')
                            price = price_raw.text.split('/')[1].split()[0]
                            if (product_name and price):
                                vendor = price_raw.find_next('a').text
                                category = price_raw.find_next('a').find_next('a').text
                                ship_from = price_raw.find_next('b', id='img').text
                                ship_to = price_raw.find_next('b', id='img').find_next('b', id='img').text
                                items.append(('cryptomarket', product_name, float(price), category, vendor, '', datetime.strptime(date, '%Y-%m-%d'), ship_to, ship_from, image_id))
    return items
