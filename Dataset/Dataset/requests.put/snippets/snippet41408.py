import boto3
import datetime
import json
import time
import decimal
from boto3 import resource
import logging
import os
import traceback
import elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
import http.client
from botocore.vendored import requests
from requests_aws4auth import AWS4Auth


def send(event, context, responseStatus, responseData, physicalResourceId):
    responseUrl = event['ResponseURL']
    responseBody = {'Status': responseStatus, 'Reason': ('See the details in CloudWatch Log Stream: ' + context.log_stream_name), 'PhysicalResourceId': (physicalResourceId or context.log_stream_name), 'StackId': event['StackId'], 'RequestId': event['RequestId'], 'LogicalResourceId': event['LogicalResourceId'], 'Data': responseData}
    json_responseBody = json.dumps(responseBody)
    print(('Response body:\n' + json_responseBody))
    headers = {'content-type': '', 'content-length': str(len(json_responseBody))}
    try:
        response = requests.put(responseUrl, data=json_responseBody, headers=headers)
        print(('Status code: ' + response.reason))
    except Exception as e:
        print(('send(..) failed executing requests.put(..): ' + str(e)))
    return
