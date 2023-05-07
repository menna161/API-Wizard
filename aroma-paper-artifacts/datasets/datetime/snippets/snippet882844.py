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
    '\n\tParse the given HTML files\n\n\tParses Evolution HTML pages, extracts item details and stores it in items list\n\n\tParameters:\n\tfile_names (list): list of file names to be parsed\n\n\tReturns:\n\tlist: list of items that has been parsed\n\n\t'
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
                if html_soup.find('ol', class_='breadcrumb'):
                    breadcrumb = html_soup.find('ol', class_='breadcrumb')
                    cats = breadcrumb.find_all('li')
                    for category in cats:
                        categories.append(category.text)
                image_id = ''
                if (html_soup.find('div', class_='col-md-5') and html_soup.find('div', class_='col-md-5').find('a', class_='thumbnail')):
                    image_id2 = html_soup.find('div', class_='col-md-5').find('a', class_='thumbnail').get('href')
                    image_id = '/'.join(image_id2.split('/')[3:])
                if html_soup.find('div', class_='col-md-7'):
                    info_column = html_soup.find('div', class_='col-md-7')
                    product_name = ''
                    if info_column.h3:
                        product_name = info_column.h3.text
                    elif info_column.h1:
                        product_name = info_column.h1.text
                    elif info_column.h2:
                        product_name = info_column.h2.text
                    elif info_column.h4:
                        product_name = info_column.h4.text
                    if product_name:
                        vendor = ''
                        if (info_column.find('div', class_='seller-info text-muted') and info_column.find('div', class_='seller-info text-muted').find('a')):
                            vendor2 = info_column.find('div', class_='seller-info text-muted')
                            vendor = vendor2.find('a').text
                        price = ''
                        if info_column.find('h4', class_='text-info'):
                            price2 = info_column.find('h4', class_='text-info').text
                            price = price2.split(' ')[1]
                        elif info_column.find('h3', class_='text-info'):
                            price2 = info_column.find('h3', class_='text-info').text
                            price = price2.split(' ')[1]
                        if price:
                            desc = ''
                            if html_soup.find('div', class_='product-summary'):
                                desc = html_soup.find('div', class_='product-summary').p.text
                            ship_to = ''
                            if (html_soup.find_all('div', class_='col-md-9') and (len(html_soup.find_all('div', class_='col-md-9')) > 1)):
                                ship_to2 = html_soup.find_all('div', class_='col-md-9')[1]
                                if (ship_to2.find_all('p') and (len(ship_to2.find_all('p')) > 1)):
                                    ship_to = str(ship_to2.find_all('p')[1].text)
                            ship_from = ''
                            if html_soup.find('div', class_='widget'):
                                widgets = html_soup.find_all('div', class_='widget')
                                for widget in widgets:
                                    if (widget.h3 and (widget.h3.text == 'Ships From')):
                                        ship_from = widget.p.text
                            categories_str = str('/'.join(categories))
                            items.append(('evolution', product_name, float(price), categories_str, vendor, desc, datetime.strptime(date, '%Y-%m-%d'), ship_to, ship_from, image_id))
    return items
