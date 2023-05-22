from acs.models import AcsBaseModel
from lxml import etree
import requests
from defusedxml.lxml import fromstring
from os import urandom
from collections import OrderedDict
import logging
from random import choice
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from acs.response import get_soap_xml_object
from acs.utils import run_ssh_command, get_value_from_parameterlist
from acs.conf import acs_settings


def acs_http_connection_request(self):
    url = self.acs_connection_request_url
    if ((not url) or (not self.acs_connectionrequest_password)):
        logger.error('unable to make a connectionrequest without url or credentials')
        return False
    try:
        return requests.get(url, auth=requests.auth.HTTPBasicAuth(self.acs_connectionrequest_username, self.acs_connectionrequest_password))
    except requests.exceptions.ConnectionError as E:
        logger.exception(('got exception %s while running HTTP request' % E))
        return False
