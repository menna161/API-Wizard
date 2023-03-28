from __future__ import unicode_literals
import logging
import datetime
import sys
import uuid
import time
import functools
import uamqp
from uamqp import Message
from uamqp import authentication
from uamqp import constants
from azure.eventhub import __version__
from azure.eventhub.sender import Sender
from azure.eventhub.receiver import Receiver
from azure.eventhub.common import EventHubError, parse_sas_token
from urlparse import urlparse
from urllib import unquote_plus, urlencode, quote_plus
from base64 import b64encode, b64decode
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, unquote_plus, urlencode, quote_plus


def get_eventhub_info(self):
    "\n        Get details on the specified EventHub.\n        Keys in the details dictionary include:\n            -'name'\n            -'type'\n            -'created_at'\n            -'partition_count'\n            -'partition_ids'\n\n        :rtype: dict\n        "
    alt_creds = {'username': self._auth_config.get('iot_username'), 'password': self._auth_config.get('iot_password')}
    try:
        mgmt_auth = self._create_auth(**alt_creds)
        mgmt_client = uamqp.AMQPClient(self.mgmt_target, auth=mgmt_auth, debug=self.debug)
        mgmt_client.open()
        mgmt_msg = Message(application_properties={'name': self.eh_name})
        response = mgmt_client.mgmt_request(mgmt_msg, constants.READ_OPERATION, op_type=b'com.microsoft:eventhub', status_code_field=b'status-code', description_fields=b'status-description')
        eh_info = response.get_data()
        output = {}
        if eh_info:
            output['name'] = eh_info[b'name'].decode('utf-8')
            output['type'] = eh_info[b'type'].decode('utf-8')
            output['created_at'] = datetime.datetime.fromtimestamp((float(eh_info[b'created_at']) / 1000))
            output['partition_count'] = eh_info[b'partition_count']
            output['partition_ids'] = [p.decode('utf-8') for p in eh_info[b'partition_ids']]
        return output
    finally:
        mgmt_client.close()
