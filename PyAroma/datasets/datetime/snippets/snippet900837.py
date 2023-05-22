import urllib
import cgi
from django.utils.text import truncate_html_words


def date_to_xmlschema(date):
    'Format a date for use in XML.\n\n    date - The Time to format.\n\n    Examples\n\n        date_to_xmlschema(datetime.datetime.now())\n        => "2011-04-24T20:34:46+05:30"\n\n    Returns the formatted String.\n    '
    return date.strftime('%Y-%m-%dT00:00:00+5:30')
