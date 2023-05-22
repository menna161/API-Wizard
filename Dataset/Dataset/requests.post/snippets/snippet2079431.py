import datetime
import json
import os
import platform
import subprocess
import uuid
from shlex import split
from time import sleep
import requests
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from pyplan.pyplan.app_pool.models import AppPool
from pyplan.pyplan.common.baseService import BaseService
from pyplan.pyplan.common.calcEngine import CalcEngine
from pyplan.pyplan.common.logger import PyplanLogger
from pyplan.pyplan.common.redisService import RedisService
from pyplan.pyplan.external_link.models import ExternalLink
from pyplan.pyplan.modelmanager.classes.modelInfo import ModelInfo
from pyplan.pyplan.modelmanager.service import ModelManagerService
from pyplan.pyplan.usercompanies.models import UserCompany
from .classes.clientSession import ClientSession
from .functions import _getAllSessions
from .serializers import ClientSessionSerializer


def setStatistics(self, appVersion):
    try:
        if (self.client_session and self.client_session.userId):
            ping_url = 'https://ping.pyplan.com/pings/'
            home_path = os.path.expanduser('~')
            payload = {'id': str(uuid.uuid4()), 'uuid': str(self.client_session.userId), 'homePath': home_path, 'platform': platform.system(), 'myUuid': str(self.client_session.my_uuid), 'myUsername': str(self.client_session.my_username), 'firstName': str(self.client_session.userFirstName), 'lastName': str(self.client_session.userLastName), 'appVersion': appVersion}
            requests.post(url=ping_url, json=payload)
    except Exception as ex:
        print(ex)
