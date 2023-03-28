import re, json
from dateutil.parser import parse
import urllib.request as urllib
from bs4 import BeautifulSoup
import urllib2 as urllib
from BeautifulSoup import BeautifulSoup


def _extractFromHTMLTag(parsedHTML):
    for time in parsedHTML.findAll('time'):
        datetime = time.get('datetime', '')
        if (len(datetime) > 0):
            return parseStrDate(datetime)
        datetime = time.get('class', '')
        if ((len(datetime) > 0) and (datetime[0].lower() == 'timestamp')):
            return parseStrDate(time.string)
    tag = parsedHTML.find('span', {'itemprop': 'datePublished'})
    if (tag is not None):
        dateText = tag.get('content')
        if (dateText is None):
            dateText = tag.text
        if (dateText is not None):
            return parseStrDate(dateText)
    for tag in parsedHTML.find_all(['span', 'p', 'div'], class_=re.compile('pubdate|timestamp|article_date|articledate|date', re.IGNORECASE)):
        dateText = tag.string
        if (dateText is None):
            dateText = tag.text
        possibleDate = parseStrDate(dateText)
        if (possibleDate is not None):
            return possibleDate
    return None
