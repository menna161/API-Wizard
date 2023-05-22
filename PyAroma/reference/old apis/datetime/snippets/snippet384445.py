from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime, timedelta
import urllib.request


def send_anonymous_usage_metric(metric_data={}):
    try:
        if ((type(metric_data) is not dict) or (not dict)):
            raise Exception('Invalid metric_data passed to send_anonymous_usage_metric')
        metric_endpoint = 'https://metrics.awssolutionsbuilder.com/generic'
        metric_payload = {'Solution': 'SO0022', 'UUID': ANONYMOUS_SOLUTION_ID, 'Version': VERSION_ID, 'Timestamp': str(datetime.utcnow()), 'Data': metric_data}
        data = bytes(json.dumps(metric_payload), 'utf-8')
        headers = {'Content-Type': 'application/json'}
        print(f'Sending anonymous usage metric: {str(metric_payload)}')
        req = urllib.request.Request(url=metric_endpoint, data=data, method='POST', headers=headers)
        with urllib.request.urlopen(req) as f:
            print(f'Anonymous usage metric send status: {f.status}')
    except Exception as e:
        print(f'Exception while sending anonymous usage metric: {e}')
