from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date
import os
import utils
import json
from collections import defaultdict
import re
import urllib.request
import atexit
import copy
import pprint


def load_date_from_commit(url, driver):
    'Given the URL of a commit identifier, returns the date of the commit'
    if ('googlesource.com' in url):
        try:
            with urllib.request.urlopen((url + '?format=JSON')) as source:
                src = source.read()[5:]
                data = json.loads(src.decode())
                time_string = data['author']['time']
                time = datetime.strptime(time_string, '%a %b %d %H:%M:%S %Y %z')
                return time.date()
        except urllib.error.HTTPError:
            utils.fetchPage(driver, url)
            rows = driver.find_elements_by_xpath('//div[contains(@class, "Metadata")]/table/tbody/tr')
            for row in rows:
                if (row.find_element_by_tag_name('th').get_attribute('innerHTML') != 'author'):
                    continue
                time_string = row.find_elements_by_xpath('./td')[1].get_attribute('innerHTML')
                time = datetime.strptime(time_string, '%a %b %d %H:%M:%S %Y %z')
                return time.date()
    elif (('codeaurora.org' in url) or ('git.kernel.org' in url)):
        utils.fetchPage(driver, url)
        rows = driver.find_elements_by_xpath('//table[@class="commit-info"]/tbody/tr')
        for row in rows:
            if (row.find_element_by_tag_name('th').get_attribute('innerHTML') != 'author'):
                continue
            time_string = row.find_element_by_xpath('./td[@class="right"]').get_attribute('innerHTML')
            time = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S %z')
            return time.date()
    elif ('github.com' in url):
        utils.fetchPage(driver, url)
        time_string = driver.find_element_by_xpath('//div[contains(@class, "commit-meta")]//relative-time').get_attribute('datetime')
        time = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
        return time.date()
    raise Exception(("Don't know how to deal with " + url))
