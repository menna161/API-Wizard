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
    '\n\tParse the given HTML files\n\n\tParses Cloudnine HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
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
                if html_soup.find('span', class_='label label-primary'):
                    cat = html_soup.find('span', class_='label label-primary').text
                    categories = cat.strip().split('(')[0].split(' / ')
                if html_soup.find('table', class_='padded'):
                    table = html_soup.find('table', class_='padded')
                    table.extract()
                else:
                    print('no tbody found')
                if html_soup.find_all('tr'):
                    rows = html_soup.find_all('tr')
                    for row in rows:
                        image_id = ''
                        if row.td.find('a'):
                            image_id = str(row.find('img')['src'])
                        if row.find_next('td').find_next('td'):
                            href = row.find_next('td').find_next('td').a.get('href')
                            product_name = row.find_next('td').find_next('td').a.text
                            if row.find_all('td', class_='nowrap right'):
                                last_two = row.find_all('td', class_='nowrap right')
                                if (len(row.find_all('div', class_='price')) > 1):
                                    price = row.find_all('div', class_='price')[1].text.split()[0]
                                    vendor = row.find('div', class_='vendor').find('a').text
                                    if (product_name and price):
                                        categories_str = str('/'.join(categories))
                                        items.append(('cloudnine', product_name, float(price), categories_str, vendor, '', datetime.strptime(date, '%Y-%m-%d'), '', '', image_id))
    return items
