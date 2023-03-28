import boto3
import botocore
from botocore.client import Config
from xml.dom import minidom
import ast
import os
import logging
import time
import datetime, sys, json, urllib.request, urllib.error, urllib.parse, re


def sendAnonymousData(config, vgwTags, region_id, vpn_connections):
    if (config['SENDDATA'] == 'Yes'):
        log.debug('Sending Anonymous Data')
        dataDict = {}
        postDict = {}
        dataDict['region'] = region_id
        dataDict['vpn_connections'] = vpn_connections
        if (vgwTags[config['HUB_TAG']] == config['HUB_TAG_VALUE']):
            dataDict['status'] = 'create'
        else:
            dataDict['status'] = 'delete'
        dataDict['preferred_path'] = vgwTags.get(config.get('PREFERRED_PATH_TAG', 'none'), 'none')
        dataDict['version'] = '3'
        postDict['Data'] = dataDict
        postDict['TimeStamp'] = str(datetime.datetime.now())
        postDict['Solution'] = 'SO0001'
        postDict['UUID'] = config['UUID']
        url = 'https://metrics.awssolutionsbuilder.com/generic'
        data = json.dumps(postDict)
        data_utf8 = data.encode('utf-8')
        log.info(data)
        headers = {'content-type': 'application/json; charset=utf-8', 'content-length': len(data_utf8)}
        req = urllib.request.Request(url, data_utf8, headers)
        rsp = urllib.request.urlopen(req)
        rspcode = rsp.getcode()
        content = rsp.read()
        log.debug('Response from APIGateway: %s, %s', rspcode, content)
