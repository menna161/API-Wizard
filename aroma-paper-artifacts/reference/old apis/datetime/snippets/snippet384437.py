from __future__ import print_function
import json
import boto3
import os
import logging
from datetime import datetime, timedelta


def lambda_handler(event, context):

    def save_item(item):
        print(('Save Item' + json.dumps(item)))
        try:
            response = client['firehose']['handle'].put_record(DeliveryStreamName=kinesisfirestream, Record={'Data': (json.dumps(item) + '\n')})
        except Exception as e:
            print(e)
            print(((('Error saving ' + item['ETag']['S']) + ' from ') + ddbtable))
            raise e

    def post_stats(item):
        print(((('Posting statistics to CloudWatch for ' + item['source_bucket']['S']) + ' time bucket ') + item['timebucket']['S']))
        ts = item['timebucket']['S']
        if (item['dest_bucket']['S'] == 'FAILED'):
            try:
                client['cw']['handle'].put_metric_data(Namespace='CRRMonitor', MetricData=[{'MetricName': 'FailedReplications', 'Dimensions': [{'Name': 'SourceBucket', 'Value': item['source_bucket']['S']}], 'Timestamp': ts, 'Value': int(item['objects']['N'])}])
            except Exception as e:
                print(e)
                print('Error creating CloudWatch metric FailedReplications')
                raise e
        else:
            try:
                client['cw']['handle'].put_metric_data(Namespace='CRRMonitor', MetricData=[{'MetricName': 'ReplicationObjects', 'Dimensions': [{'Name': 'SourceBucket', 'Value': item['source_bucket']['S']}, {'Name': 'DestBucket', 'Value': item['dest_bucket']['S']}], 'Timestamp': ts, 'Value': int(item['objects']['N'])}])
            except Exception as e:
                print(e)
                print('Error creating CloudWatch metric')
                raise e
            try:
                client['cw']['handle'].put_metric_data(Namespace='CRRMonitor', MetricData=[{'MetricName': 'ReplicationSpeed', 'Dimensions': [{'Name': 'SourceBucket', 'Value': item['source_bucket']['S']}, {'Name': 'DestBucket', 'Value': item['dest_bucket']['S']}], 'Timestamp': ts, 'Value': (((int(item['size']['N']) * 8) / 1024) / (int(item['elapsed']['N']) + 1))}])
            except Exception as e:
                print(e)
                print('Error creating CloudWatch metric')
                raise e
        print(('Statistics posted to ' + ts))
        try:
            client['ddb']['handle'].delete_item(TableName=stattable, Key={'OriginReplicaBucket': {'S': ((((item['source_bucket']['S'] + ':') + item['dest_bucket']['S']) + ':') + ts)}})
            print(('Purged statistics date for ' + ts))
        except Exception as e:
            print(e)
            print(('Error purging from ' + ts))
            raise e

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
    ts = datetime.utcnow()
    secs = (ts.replace(tzinfo=None) - ts.min).seconds
    rounding = (((secs - (roundTo / 2)) // roundTo) * roundTo)
    ts = (ts + timedelta(0, (rounding - secs), (- ts.microsecond)))
    statbucket = datetime.strftime(ts, timefmt)
    print(('Logging from ' + statbucket))
    try:
        client['ddb']['handle'].describe_table(TableName=stattable)
    except Exception as e:
        print(e)
        print((('Table ' + stattable) + ' does not exist - need to create it'))
        raise e
    eav = {':stats': {'S': statbucket}}
    try:
        response = client['ddb']['handle'].scan(TableName=stattable, ExpressionAttributeValues=eav, FilterExpression='timebucket <= :stats', ConsistentRead=True)
    except Exception as e:
        print(e)
        print((('Table ' + ddbtable) + ' scan failed'))
        raise e
    if (len(response['Items']) == 0):
        print(('WARNING: No stats bucket found for ' + statbucket))
    for i in response['Items']:
        post_stats(i)
    while ('LastEvaluatedKey' in response):
        try:
            response = client['ddb']['handle'].scan(TableName=ddbtable, FilterExpression='timebucket <= :stats', ExpressionAttributeValues=eav, ExclusiveStartKey=response['LastEvaluatedKey'], ConsistentRead=True)
        except Exception as e:
            print(e)
            print((('Table ' + ddbtable) + ' scan failed'))
            raise e
        for i in response['Items']:
            post_stats(i)
    if (stream_to_kinesis == 'Yes'):
        firehose(ts)
