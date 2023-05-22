import os, json, re
import gzip
import tldextract
from datetime import datetime, timedelta
from StringIO import BytesIO
from io import BytesIO


def generate(self, term_list):
    d = (datetime.today() - timedelta(days=2))
    date = d.strftime('%Y-%m-%d')
    for folder in self._czds_folder_list:
        directory = './data/{folder}/{date}/'.format(folder=folder, date=date)
        self.__get_each_term(term_list, directory)
    for folder in self._whoisds_folder_list:
        directory_names = []
        whoisds_directory = './data/{folder}/'.format(folder=folder)
        for (root, d_names, f_names) in os.walk(whoisds_directory):
            for d in d_names:
                directory_names.append(os.path.join(root, d))
        for directory in directory_names:
            self.__get_each_term(term_list, directory)
    self.__save_blacklist()
