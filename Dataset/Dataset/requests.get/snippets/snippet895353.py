import re
import os
import sys
import json
import hashlib
from functools import partial
from urllib.parse import quote
from lxml import etree
from ebooklib import epub
from PyPDF2 import PdfFileReader
from PyPDF2.generic import IndirectObject, TextStringObject
import requests


def build_metas(options):
    '\n    读取所有数据的元数据\n    '
    entry = XPath('//atom:entry')
    metas = read_old_meta()
    tocs = []
    for dir_meta in metas:
        dir_name = dir_meta['dir_name']
        print(('reads: ' + dir_name))
        books = []
        if ('books' in dir_meta):
            old_books = dir_meta['books']
        else:
            old_books = []
        old_sha = {book['file']: (book['sha_256'], index) for (index, book) in enumerate(old_books)}
        for f in os.listdir(dir_name):
            file_name = os.path.join(dir_name, f)
            if os.path.isfile(file_name):
                hash_sum = file_sha256(file_name)
                if (('-f' not in options) and old_books and (f in old_sha) and (old_sha[f][0] == hash_sum)):
                    meta = old_books[old_sha[f][1]]
                    print(('|--read meta miss: ' + f))
                elif f.endswith('.pdf'):
                    opf_name = os.path.join(dir_name, (f[:f.rfind('.')] + '.opf'))
                    if (('-o' not in options) and os.path.exists(opf_name)):
                        print(('|--read opf meta: ' + f))
                        meta = read_meta_opf(opf_name)
                        if ('rating' in meta):
                            del meta['rating']
                    else:
                        print(('|--read pdf meta: ' + f))
                        meta = read_meta_pdf(file_name)
                    meta['type'] = 'pdf'
                elif f.endswith('.epub'):
                    print(('|--read epub meta: ' + f))
                    meta = read_meta_epub(file_name)
                    if ('rating' in meta):
                        del meta['rating']
                    meta['type'] = 'epub'
                else:
                    meta = None
                if meta:
                    if (('-d' in options) and ('identifier' in meta) and ('douban' in meta['identifier'])):
                        douban_id = meta['identifier']['douban']
                        douban_url = ('https://api.douban.com/v2/book/%s?apikey=0df993c66c0c636e29ecbb5344252a4a' % douban_id)
                        print('|-- read douban meta: ', douban_url)
                        r = requests.get(douban_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'})
                        data = r.json()
                        douban_meta = douban_to_meta_v2(data)
                        douban_meta['type'] = meta['type']
                        douban_meta['title'] = meta['title']
                        douban_meta['meta_type'] = 'douban'
                        meta = douban_meta
                    meta['sha_256'] = hash_sum
                    meta['file'] = f
                    books.append(meta)
        books.sort(key=(lambda x: x['file']))
        dir_meta['books'] = books
    save_old_meta(metas)
    print('------complete------')
