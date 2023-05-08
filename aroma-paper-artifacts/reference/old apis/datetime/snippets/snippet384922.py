import boto3
import datetime
import json
import time
import decimal
from botocore.client import ClientError
from boto3 import resource
from boto3.dynamodb.conditions import Key
import logging
import subprocess
from urllib.parse import urlparse
import timecode
from timecode import Timecode
import xmltodict
import logging
import os
import traceback


def lambda_handler(event, context):
    print(json.dumps(event))
    tsevent = int(datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp())
    try:
        MEDIAINFOTABLE = os.environ['MediainfoTable']
        MEDIAINFOTABLETTL = os.environ['MediainfoTableTTL']
        MEDIAINFO_RETENTION_PERIOD = ((3600 * 24) * int(MEDIAINFOTABLETTL))
        for input in event['detail']['inputDetails']:
            s3_path = input['uri']
            urlp = urlparse(s3_path)
            key = urlp[2]
            key = key.lstrip('/')
            bucket = urlp[1]
            signed_url = get_signed_url(SIGNED_URL_EXPIRATION, bucket, key)
            logger.info('Signed URL: {}'.format(signed_url))
            print(((('bucket and key ' + bucket) + ' ') + key))
            xml_output = subprocess.check_output(['./mediainfo', '--full', '--output=XML', signed_url])
            print(xml_output)
            json_output = xmltodict.parse(xml_output)
            input['mediainfo'] = json_output['Mediainfo']
        job_input_info = event['detail']
        job_input_info['timestamp'] = tsevent
        job_input_info['timestampTTL'] = (tsevent + MEDIAINFO_RETENTION_PERIOD)
        s = json.dumps(job_input_info, cls=DecimalEncoder)
        job_input_info = json.loads(s, parse_float=decimal.Decimal)
        table = DYNAMO_CLIENT.Table(MEDIAINFOTABLE)
        response = table.put_item(Item=job_input_info)
        print(json.dumps(response, cls=DecimalEncoder))
    except Exception as e:
        print('An error occured {}'.format(e))
        traceback.print_stack()
        raise
    else:
        return True
