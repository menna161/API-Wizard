from __future__ import unicode_literals
import argparse
import re
import six
from datetime import datetime
from django.core.management.base import BaseCommand
from analytics import utils
from articles.models import ArticlePage, SeriesPage


def valid_date(self, date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        message = "Not a valid date: '{0}'.".format(date_string)
        raise argparse.ArgumentTypeError(message)
    else:
        return date_string
