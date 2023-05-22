import urllib
import cgi
from django.utils.text import truncate_html_words


def date(date, format):
    'Format datetime\n    '
    return date.strftime(format)
