import configparser
import json
import netifaces
import os
import subprocess
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from fritzhome.fritz import FritzBox
from netaddr import IPAddress
from core.models import Anonymous, LastCheck, Pad, Presence


def fritzbox_query(searched_macs, ignored_macs):
    config = configparser.ConfigParser()
    config.read(os.path.join(settings.BASE_DIR, 'config.ini'))
    ip = config['FritzBox']['ip']
    password = config['FritzBox']['password']
    if ((not ip) or (not password)):
        raise FritzException('ip or password not specified')
    box = FritzBox(ip, None, password)
    try:
        box.login()
    except Exception:
        raise FritzException('Login failed')
    r = box.session.get((box.base_url + '/net/network_user_devices.lua'), params={'sid': box.sid})
    try:
        table = BeautifulSoup(r.text, 'lxml').find(id='uiLanActive')
    except AttributeError:
        raise FritzException('Could not extract active devices.')
    rows = table.find_all('tr')
    present_macs = []
    anonymous_count = 0
    for row in rows:
        columns = row.find_all('td')
        if (len(columns) >= 4):
            mac = columns[3].text.upper()
            if (mac in searched_macs):
                present_macs.append(mac)
            elif (mac not in ignored_macs):
                anonymous_count += 1
    return (present_macs, anonymous_count)
