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
    '\n\tParse the given HTML files\n\n\tParses Diabolus HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
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
                if html_soup.find('div', style='min-width:275px'):
                    content = html_soup.find('div', style='min-width:275px')
                    product_name = None
                    if content.find('h1'):
                        product_name = content.find('h1').text
                    if content.find('h3'):
                        product_name = content.find('h3').text
                    if content.find('h2'):
                        product_name = content.find('h2').text
                    if content.find('h4'):
                        product_name = content.find('h4').text
                    image_id = ''
                    if content.find('a', target='_blank'):
                        image_id = content.find('a', target='_blank').get('href')
                    if content.find_all('span', class_='form-control'):
                        spans = content.find_all('span', class_='form-control')
                        if spans[0].find('img', src='btc.png'):
                            if spans[1].text.split('/'):
                                prices = spans[1].text.split('/')
                                for price_item in prices:
                                    if ('BTC' in price_item):
                                        price = price_item.strip().split()[0]
                            if (product_name and price):
                                vendor = ''
                                if ('Vendor' in spans[2].text):
                                    vendor = spans[2].find('a').text
                                ship_from = ''
                                if ('from' in spans[3].text.lower()):
                                    ship_from = ' '.join(spans[3].text.split()[2])
                                ship_to = ''
                                if ('to' in spans[4].text.lower()):
                                    ship_to = ' '.join(spans[4].text.split()[2])
                                category = ''
                                if ('category' in spans[7].text.lower()):
                                    category = spans[7].text.split()[1]
                                desc = ''
                                if content.find('div', id='cats'):
                                    desc = content.find('div', id='cats').text
                                items.append(('diabolus', product_name, float(price), category, vendor, desc, datetime.strptime(date, '%Y-%m-%d'), ship_to, ship_from, image_id))
    return items
