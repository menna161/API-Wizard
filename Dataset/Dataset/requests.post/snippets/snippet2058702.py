import datetime
import glob
import json
import logging
import mimetypes
import ntpath
import os
from pprint import pformat
import googleapiclient.http
import requests
from django.conf import settings
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.client import GoogleCredentials


def publishResult(result, topic, retain):
    url = settings.HA_MQTT_PUBLISH_URL
    data = {'payload': json.dumps(result), 'topic': topic, 'retain': retain}
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', 'Authorization': ('Bearer ' + settings.HA_TOKEN)}
    response = requests.post(url, data=data_json, headers=headers)
    logging.debug(pformat(response))
