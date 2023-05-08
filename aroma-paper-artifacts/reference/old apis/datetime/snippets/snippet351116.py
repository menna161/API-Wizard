import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
import dateutil.parser
import dateutil.relativedelta
from arxivtimes_indicator.data_api import DataApi
from peewee import *
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict


def issue_to_dict(self, issue):
    issue_dict = model_to_dict(issue, backrefs=True)
    headline = Issue.extract_headline(issue_dict['body'])
    issue_dict['headline'] = headline
    labels = [lb['name'] for lb in issue_dict['labels']]
    issue_dict['labels'] = labels
    issue_dict['genres'] = self.labels_to_genres(labels)
    if isinstance(issue_dict['created_at'], datetime):
        issue_dict['created_at'] = issue_dict['created_at'].strftime('%Y-%m-%dT%H:%M:%SZ')
    return issue_dict
