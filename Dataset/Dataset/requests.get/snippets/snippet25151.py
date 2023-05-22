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


def download_notebook_oh(notebook_url):
    notebook_content = requests.get(notebook_url).content
    return notebook_content
