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
    '\n\tParse the given HTML files\n\n\tParses Pandora HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
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
                if html_soup.find('div', id='content'):
                    content = html_soup.find('div', id='content')
                    if html_soup.find('table', class_='width70'):
                        product_name = ''
                        image_id = ''
                        vendor = ''
                        price = ''
                        ship_from = ''
                        ship_to = ''
                        table = html_soup.find('table', class_='width100')
                        for row in table.find_all('tr'):
                            if row.find('th', colspan='2'):
                                product_name = row.find('th', colspan='2').text
                            elif row.find('td', rowspan='6'):
                                image_id = row.find('td', rowspan='6').find('img')['src']
                                if (row.td.find_next('td').text == 'Seller:'):
                                    vendor = row.td.find_next('td').find_next('td')
                                    vendor = vendor.find('a').text
                            elif row.td:
                                if (row.td.text == 'Price:'):
                                    if row.td.find_next('td').text.find('฿'):
                                        price = row.td.find_next('td').text.split('฿')[1].split(' ')[0]
                                elif (row.td.text == 'Shipping from:'):
                                    shipping_from = row.td.find_next('td').text
                                elif (row.td.text == 'Shipping to:'):
                                    shipping_to = row.td.find_next('td').text
                        desc = ''
                        if html_soup.find('pre'):
                            desc = html_soup.find('pre').text
                        if (product_name and price):
                            items.append(('pandora', product_name, float(price), '', vendor, desc, datetime.strptime(date, '%Y-%m-%d'), ship_to, ship_from, image_id))
    return items
