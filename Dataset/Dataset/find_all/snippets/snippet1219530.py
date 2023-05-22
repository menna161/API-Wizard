import base64
import datetime
import random
import re
import time
from email.utils import make_msgid
import shortuuid
import spintax
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.db.utils import IntegrityError
from django.urls import reverse
from faker import Faker
from .utils import is_blacklisted
from .utils import parse_email_address
from .utils import parse_forwarded_message


def strip_html(html):
    'Strip all tags from an HTML string.'
    soup = BeautifulSoup(html, features='html.parser')
    for br in soup.find_all('br'):
        br.replace_with(('\n' + br.text))
    return soup.text
