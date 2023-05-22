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


def oh_code_to_member(code):
    '\n    Exchange code for token, use this to create and return OpenHumansMember.\n    If a matching OpenHumansMember exists, update and return it.\n    '
    if (settings.OPENHUMANS_CLIENT_SECRET and settings.OPENHUMANS_CLIENT_ID and code):
        data = {'grant_type': 'authorization_code', 'redirect_uri': '{}/complete'.format(settings.OPENHUMANS_APP_BASE_URL), 'code': code}
        req = requests.post('{}/oauth2/token/'.format(settings.OPENHUMANS_OH_BASE_URL), data=data, auth=requests.auth.HTTPBasicAuth(settings.OPENHUMANS_CLIENT_ID, settings.OPENHUMANS_CLIENT_SECRET))
        data = req.json()
        if ('access_token' in data):
            oh_memberdata = api.exchange_oauth2_member(data['access_token'])
            oh_id = oh_memberdata['project_member_id']
            oh_username = oh_memberdata['username']
            try:
                oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
                logger.debug('Member {} re-authorized.'.format(oh_id))
                oh_member.access_token = data['access_token']
                oh_member.refresh_token = data['refresh_token']
                oh_member.token_expires = OpenHumansMember.get_expiration(data['expires_in'])
            except OpenHumansMember.DoesNotExist:
                oh_member = OpenHumansMember.create(oh_id=oh_id, oh_username=oh_username, access_token=data['access_token'], refresh_token=data['refresh_token'], expires_in=data['expires_in'])
                logger.debug('Member {} created.'.format(oh_id))
            oh_member.save()
            return oh_member
        elif ('error' in req.json()):
            logger.debug('Error in token exchange: {}'.format(req.json()))
        else:
            logger.warning('Neither token nor error info in OH response!')
    else:
        logger.error('OH_CLIENT_SECRET or code are unavailable')
    return None
