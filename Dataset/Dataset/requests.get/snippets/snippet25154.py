import requests
import arrow
import json
from django.conf import settings
from django.urls import reverse
from main.models import SharedNotebook
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ohapi import api
import logging
from open_humans.models import OpenHumansMember
from django.contrib import messages
from collections import defaultdict


def suggest_data_sources(notebook_content):
    potential_sources = re.findall('direct-sharing-\\d+', str(notebook_content))
    if potential_sources:
        response = requests.get('https://www.openhumans.org/api/public-data/members-by-source/')
        results = response.json()['results']
        while response.json()['next']:
            response = requests.get('https://www.openhumans.org/api/public-data/members-by-source/')
            results.append(response.json()['results'])
        source_names = {i['source']: i['name'] for i in results}
        suggested_sources = [source_names[i] for i in potential_sources if (i in source_names)]
        suggested_sources = list(set(suggested_sources))
        return ','.join(suggested_sources)
    return ''
