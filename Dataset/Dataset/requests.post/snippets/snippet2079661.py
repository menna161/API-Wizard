import os
import json
import datetime
import requests
from django.core.mail import EmailMultiAlternatives, send_mass_mail, get_connection
from django.template.loader import render_to_string
from rest_framework import exceptions
from pyplan.pyplan.common.baseService import BaseService
from pyplan.pyplan.company_preference.models import CompanyPreference
from pyplan.pyplan.preference.models import Preference
from pyplan.pyplan.common.email.models import EmailQueue
from pyplan.pyplan.common.email.classes.email import Email
from pyplan.pyplan.common.email.classes.eEmailType import eEmailType


def _post(self, url, data):
    response = requests.post(url=url, data=data)
    response.raise_for_status()
    return response.text
