from pycfn_custom_resource.lambda_backed import CustomResource
import boto3
from botocore.client import Config
from zipfile import ZipFile
import urllib
import os
import string
import shutil
import ast
import paramiko
import crypt
import binascii
import logging
import uuid
import json
import datetime
import re


def SendAnonymousData(AnonymousData):
    log.info('Sending anonymous data')
    TimeNow = datetime.datetime.utcnow().isoformat()
    TimeStamp = str(TimeNow)
    AnonymousData['TimeStamp'] = TimeStamp
    data = json.dumps(AnonymousData)
    log.info('Data: %s', data)
    data_utf8 = data.encode('utf-8')
    url = 'https://metrics.awssolutionsbuilder.com/generic'
    headers = {'content-type': 'application/json; charset=utf-8', 'content-length': len(data_utf8)}
    req = urllib.request.Request(url, data_utf8, headers)
    rsp = urllib.request.urlopen(req)
    rspcode = rsp.getcode()
    content = rsp.read()
    log.info('Response from APIGateway: %s, %s', rspcode, content)
    return data
