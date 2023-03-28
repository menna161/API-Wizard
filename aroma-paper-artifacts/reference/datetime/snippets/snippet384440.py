from __future__ import print_function
import json
import boto3
import os
import logging
from datetime import datetime, timedelta


def firehose(ts):
    begts = (ts - timedelta(minutes=5))
    arch_beg = begts.strftime(timefmt)
    arch_end = ts.strftime(timefmt)
    eav = {':archbeg': {'S': arch_beg}, ':archend': {'S': arch_end}}
    print(('Reading from ' + ddbtable))
    try:
        response = client['ddb']['handle'].scan(TableName=ddbtable, ExpressionAttributeValues=eav, FilterExpression='end_datetime >= :archbeg and end_datetime < :archend', Limit=1000)
    except Exception as e:
        print(e)
        print((('Table ' + ddbtable) + ' scan failed'))
        raise e
    print(((((('Archiving items from ' + ddbtable) + ' beg>=') + arch_beg) + ' end=') + arch_end))
    for i in response['Items']:
        save_item(i)
    while ('LastEvaluatedKey' in response):
        response = client['ddb']['handle'].scan(TableName=ddbtable, FilterExpression='end_datetime >= :archbeg and end_datetime < :archend', ExpressionAttributeValues=eav, ExclusiveStartKey=response['LastEvaluatedKey'], Limit=1000)
        for i in response['Items']:
            print(('Items LastEvaluated ' + i['ETag']['S']))
            save_item(i)
