import os
import re
import json
import codecs
import fnmatch
import logging
import itertools
from multiprocessing import Pool
import bs4
from tqdm import tqdm
import argparse


def convert_nytimes(input_file, content):
    doc = bs4.BeautifulSoup(content, 'html.parser')
    file_name_components = input_file.split('/')
    date = '/'.join(file_name_components[1:4])
    categories = file_name_components[4:(- 1)]
    file_name = '.'.join(file_name_components[(- 1)].split('.')[:(- 1)])
    url = ('http://' + input_file)
    for script in doc(['script', 'style', 'link', 'button']):
        script.decompose()
    try:
        author = doc.find('meta', attrs={'name': 'author'})['content']
    except TypeError:
        if (not doc.find('meta', attrs={'name': 'byl'})):
            logging.warning('ny:No author in {}'.format(input_file))
            return None
        author = doc.find('meta', attrs={'name': 'byl'})['content']
        author = author.replace('By ', '')
    title = doc.find('meta', property='og:title')
    if (not title):
        logging.error('no title for {}'.format(input_file))
        return
    title = re.sub('\\s+', ' ', title['content']).strip()
    if (not len(title)):
        logging.error('no title for {}'.format(input_file))
        return
    headline = doc.find('meta', property='og:description')
    if (not headline):
        logging.error('no headline for {}'.format(input_file))
        return
    headline = re.sub('\\s+', ' ', headline['content']).strip()
    if (not len(headline)):
        logging.error('no headline for {}'.format(input_file))
        return
    body = doc.find('section', attrs={'name': 'articleBody'})
    if (not body):
        body = doc.find_all('p', attrs={'class': 'story-body-text story-content'})
        if (not body):
            logging.error('no body for {}'.format(input_file))
            return
        else:
            body = ' '.join([re.sub('\\s+', ' ', p.get_text(separator=' ')).strip() for p in body])
    else:
        body = re.sub('\\s+', ' ', body.get_text(separator=' ')).strip()
    if (not len(body)):
        logging.error('no body for {}'.format(input_file))
        return
    keywords = doc.find('meta', attrs={'name': 'news_keywords'})
    if (keywords is None):
        keywords = doc.find('meta', attrs={'name': 'keywords'})
        if (not keywords):
            logging.error('no keywords for {}'.format(input_file))
            return
    keywords = re.sub('\\s+', ' ', keywords['content']).strip()
    keywords = keywords.split(',')
    keywords = [k.split(';') for k in keywords if k]
    if (not keywords):
        logging.error('no keywords for {}'.format(input_file))
        return
    return {'title': title, 'headline': headline, 'abstract': body, 'keyword': keywords, 'file_name': file_name, 'date': date, 'categories': categories, 'url': url, 'author': author}
