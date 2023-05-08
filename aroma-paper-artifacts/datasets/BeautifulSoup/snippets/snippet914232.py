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


def convert_jptimes(input_file, content):
    content = fix_unclosed('meta', content)
    content = fix_unclosed('link', content)
    doc = bs4.BeautifulSoup(content, 'html.parser')
    file_name_components = input_file.split('/')
    date = '/'.join(file_name_components[2:5])
    categories = file_name_components[5:(- 1)]
    file_name = file_name_components[(- 1)]
    url = ('https://' + input_file)
    try:
        author = doc.find('meta', attrs={'name': 'author'})['content']
    except TypeError:
        try:
            author = doc.find('a', attrs={'class': 'author'}).text
        except AttributeError:
            logging.warning('jp:No author in {}'.format(input_file))
    title = doc.find('meta', property='og:title')
    if (not title):
        logging.error('no title for {}'.format(input_file))
        return
    title = re.sub('\\s+', ' ', title['content']).strip()
    title = re.sub('\\| The Japan Times', '', title)
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
    body = doc.find('div', attrs={'id': 'jtarticle'})
    if (not body):
        logging.error('no body for {}'.format(input_file))
        return
    body = re.sub('\\s+', ' ', body.get_text(separator=' ')).strip()
    if (not len(body)):
        logging.error('no body for {}'.format(input_file))
        return
    keywords = doc.find('meta', attrs={'name': 'keywords'})
    if (keywords is None):
        logging.error('no keywords for {}'.format(input_file))
        return
    keywords = re.sub('\\s+', ' ', keywords['content']).strip()
    keywords = keywords.split(', ')
    keywords = [k.split(';') for k in keywords if k]
    if (not keywords):
        logging.error('no keywords for {}'.format(input_file))
        return
    return {'title': title, 'headline': '', 'abstract': body, 'keyword': keywords, 'file_name': file_name, 'date': date, 'categories': categories, 'url': url, 'author': author}
