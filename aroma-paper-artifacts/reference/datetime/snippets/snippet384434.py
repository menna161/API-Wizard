from __future__ import print_function
import boto3
import os
from datetime import datetime, timedelta


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
