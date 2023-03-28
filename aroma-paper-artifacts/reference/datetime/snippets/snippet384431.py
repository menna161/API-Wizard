from __future__ import print_function
import boto3
import os
from datetime import datetime, timedelta


def lambda_handler(event, context):

    def purge_item(itemkey):
        print(('Purge ETag: ' + itemkey))
        try:
            client['ddb']['handle'].delete_item(TableName=ddbtable, Key={'ETag': {'S': itemkey}})
        except Exception as e:
            print(e)
            print(((('Error purging ' + itemkey) + ' from ') + ddbtable))
            raise e

    def log_statistics(Src, Dst, Tstamp, Size, ET, roundTo):
        statbucket = ((Src + ':') + Dst)
        ts = datetime.strptime(Tstamp, timefmt)
        secs = (ts.replace(tzinfo=None) - ts.min).seconds
        rounding = (((secs + (roundTo / 2)) // roundTo) * roundTo)
        ts = (ts + timedelta(0, (rounding - secs), (- ts.microsecond)))
        statbucket += (':' + datetime.strftime(ts, timefmt))
        stat_exp_attrs = {}
        stat_update_exp = 'SET timebucket = :t, source_bucket = :o, dest_bucket = :r ADD objects :a, size :c, elapsed :d'
        stat_exp_attrs[':a'] = {'N': '1'}
        stat_exp_attrs[':c'] = {'N': Size}
        stat_exp_attrs[':d'] = {'N': ET}
        stat_exp_attrs[':t'] = {'S': datetime.strftime(ts, timefmt)}
        stat_exp_attrs[':o'] = {'S': Src}
        stat_exp_attrs[':r'] = {'S': Dst}
        try:
            client['ddb']['handle'].update_item(TableName=stattable, Key={'OriginReplicaBucket': {'S': statbucket}}, UpdateExpression=stat_update_exp, ExpressionAttributeValues=stat_exp_attrs)
        except Exception as e:
            print(e)
            print((('Table ' + stattable) + ' update failed'))
            raise e

    def process_items(items):
        for i in items:
            try:
                response = client['s3']['handle'].head_object(Bucket=i['s3Origin']['S'], Key=i['s3Object']['S'])
            except Exception as e:
                print(('Item no longer exists - purging: ' + i['ETag']['S']))
                purge_item(i['ETag']['S'])
                continue
            ddb_exp_attrs = {}
            ddb_update_exp = 'set s3Object = :a'
            ddb_exp_attrs[':a'] = {'S': i['s3Object']['S']}
            headers = response['ResponseMetadata']['HTTPHeaders']
            lastmod = datetime.strftime(response['LastModified'], timefmt)
            if (headers['x-amz-replication-status'] == 'COMPLETED'):
                print(('Completed transfer found: ' + i['ETag']['S']))
                ddb_update_exp += ', replication_status = :b'
                ddb_exp_attrs[':b'] = {'S': 'COMPLETED'}
            elif (headers['x-amz-replication-status'] == 'FAILED'):
                ddb_update_exp += ', replication_status = :b'
                ddb_exp_attrs[':b'] = {'S': 'FAILED'}
                log_statistics(i['s3Origin']['S'], 'FAILED', i['start_datetime']['S'], '0', '1', 300)
            try:
                client['ddb']['handle'].update_item(TableName=ddbtable, Key={'ETag': i['ETag']}, UpdateExpression=ddb_update_exp, ExpressionAttributeValues=ddb_exp_attrs)
            except Exception as e:
                print(e)
                print((('Table ' + ddbtable) + ' update failed'))
                raise e
    print('Checking for incomplete transfers')
    check = (datetime.utcnow() - timedelta(hours=1))
    checkstr = check.strftime(timefmt)
    eav = {':check': {'S': checkstr}, ':completed': {'S': 'COMPLETED'}}
    print(('Reading from ' + ddbtable))
    try:
        response = client['ddb']['handle'].scan(TableName=ddbtable, ExpressionAttributeValues=eav, FilterExpression='replication_status <> :completed and start_datetime < :check', Limit=1000)
    except Exception as e:
        print(e)
        print((('Table ' + ddbtable) + ' scan failed'))
        raise e
    print(('Checking for incomplete items from ' + ddbtable))
    process_items(response['Items'])
    while ('LastEvaluatedKey' in response):
        response = client['ddb']['handle'].scan(TableName=ddbtable, FilterExpression='replication_status <> :completed and start_datetime < :check', ExpressionAttributeValues=eav, ExclusiveStartKey=response['LastEvaluatedKey'], Limit=1000)
        process_items(response['Items'])
