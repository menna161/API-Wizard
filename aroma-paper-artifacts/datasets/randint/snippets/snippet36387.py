import csv
import ipaddress
import json
import logging
import random
from LatLon23 import string2latlon
from auvsi_suas.proto import interop_admin_api_pb2
from auvsi_suas.views.decorators import require_superuser
from auvsi_suas.views.json import ProtoJsonEncoder
from django import shortcuts
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import View
from google.protobuf import json_format


def post(self, request):
    context = {'server': {'ip': INTEROP_SERVER_IP, 'port': INTEROP_SERVER_PORT}, 'teams': []}
    static_min = int(ipaddress.IPv4Address(str(INTEROP_TEAM_STATIC_RANGE_MIN)))
    static_max = int(ipaddress.IPv4Address(str(INTEROP_TEAM_STATIC_RANGE_MAX)))
    static_range = (static_max - static_min)
    random.seed()
    csvreader = csv.DictReader(request.FILES['file'].read().decode().splitlines())
    for (i, row) in enumerate(csvreader):
        context['teams'].append({'university': row['University'], 'name': row['Name'], 'username': row['Username'], 'password': random.randint(1000000000.0, 10000000000.0), 'ip': str(ipaddress.IPv4Address((static_min + (i % static_range))))})
    for team in context['teams']:
        get_user_model().objects.create_user(username=team['username'], password=team['password'], first_name=team['name'][:30], last_name=team['university'][:30])
    return shortcuts.render(request, 'bulk_create_teams.html', context)
