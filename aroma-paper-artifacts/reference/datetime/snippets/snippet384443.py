from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime, timedelta
import urllib.request


def message_handler(event):

    def log_statistics(Src, Dst, Tstamp, Size, ET, roundTo):
        statbucket = ((Src + ':') + Dst)
        ts = datetime.strptime(Tstamp, timefmt)
        secs = (ts.replace(tzinfo=None) - ts.min).seconds
        rounding = (((secs + (roundTo / 2)) // roundTo) * roundTo)
        ts = (ts + timedelta(0, (rounding - secs), (- ts.microsecond)))
        timebucket = datetime.strftime(ts, timefmt)
        statbucket += (':' + timebucket)
        stat_exp_attrs = {}
        stat_update_exp = 'SET timebucket = :t, source_bucket = :o, dest_bucket = :r ADD objects :a, size :c, elapsed :d'
        stat_exp_attrs[':a'] = {'N': '1'}
        stat_exp_attrs[':c'] = {'N': Size}
        stat_exp_attrs[':d'] = {'N': ET}
        stat_exp_attrs[':t'] = {'S': timebucket}
        stat_exp_attrs[':o'] = {'S': Src}
        stat_exp_attrs[':r'] = {'S': Dst}
        try:
            response = client['ddb']['handle'].update_item(TableName=stattable, Key={'OriginReplicaBucket': {'S': statbucket}}, UpdateExpression=stat_update_exp, ExpressionAttributeValues=stat_exp_attrs)
        except Exception as e:
            print(e)
            print((('Table ' + stattable) + ' update failed'))
            raise e
        if (not (Src in initfail)):
            initfail[Src] = 'foo'
        if ((Dst != 'FAILED') and (initfail[Src] != timebucket)):
            print(((('Initializing FAILED bucket for ' + Src) + ':') + timebucket))
            statbucket = ((Src + ':FAILED:') + timebucket)
            stat_exp_attrs = {}
            stat_update_exp = 'SET timebucket = :t, source_bucket = :o, dest_bucket = :r ADD objects :a, size :c, elapsed :d'
            stat_exp_attrs[':a'] = {'N': '0'}
            stat_exp_attrs[':c'] = {'N': '1'}
            stat_exp_attrs[':d'] = {'N': '1'}
            stat_exp_attrs[':t'] = {'S': timebucket}
            stat_exp_attrs[':o'] = {'S': Src}
            stat_exp_attrs[':r'] = {'S': 'FAILED'}
            try:
                response = client['ddb']['handle'].update_item(TableName=stattable, Key={'OriginReplicaBucket': {'S': statbucket}}, UpdateExpression=stat_update_exp, ExpressionAttributeValues=stat_exp_attrs)
                initfail[Src] = timebucket
            except Exception as e:
                print(e)
                print((('Table ' + stattable) + ' update failed'))
                raise e
    if ('detail-type' in event):
        evdata = event
    elif ('Records' in event):
        if (event['Records'][0]['EventSource'] == 'aws:sns'):
            evdata = json.loads(event['Records'][0]['Sns']['Message'])
        else:
            print('Error: unrecognized event format received')
            raise Exception('Unrecognized event format')
    elif ('MessageId' in event):
        evdata = json.loads(event['Message'])
    else:
        evdata = event
    if (DEBUG > 1):
        print(json.dumps(evdata))
    if (evdata['detail']['eventName'] != 'PutObject'):
        if (DEBUG > 0):
            print((('Ignoring ' + evdata['detail']['eventName']) + ' event'))
        return
    region = evdata['region']
    bucket = evdata['detail']['requestParameters']['bucketName']
    key = evdata['detail']['requestParameters']['key']
    now = evdata['detail']['eventTime']
    ddb_exp_attrs = {}
    ddb_update_exp = 'set s3Object = :a'
    ddb_exp_attrs[':a'] = {'S': key}
    if (not (region in s3client)):
        s3client[region] = boto3.client('s3', region)
    try:
        response = s3client[region].head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if (e.response['Error']['Code'] == '403'):
            print(((('IGNORING: CRRMonitor does not have access to Object - ' + evdata['detail']['requestParameters']['bucketName']) + '/') + evdata['detail']['requestParameters']['key']))
        elif (e.response['Error']['Code'] == '404'):
            print(((('IGNORING: Object no longer exists - ' + evdata['detail']['requestParameters']['bucketName']) + '/') + evdata['detail']['requestParameters']['key']))
        else:
            print(('Unhandled ClientError ' + str(e)))
            print(json.dumps(e.response))
        return
    except Exception as e:
        print(('Unandled Exception ' + str(e)))
        print('Removing from queue / ignoring')
        return
    headers = response['ResponseMetadata']['HTTPHeaders']
    if ('x-amz-replication-status' not in headers):
        if (DEBUG > 0):
            print('Not a replicated object')
        return ()
    repstatus = headers['x-amz-replication-status']
    try:
        response = client['ddb']['handle'].describe_table(TableName=ddbtable)
    except Exception as e:
        print(e)
        print((('Table ' + ddbtable) + ' does not exist - need to create it'))
        raise e
    objsize = headers['content-length']
    ddb_update_exp += ', ObjectSize = :s'
    ddb_exp_attrs[':s'] = {'N': objsize}
    ETag = {'S': ((headers['etag'][1:(- 1)] + ':') + headers['x-amz-version-id'][1:(- 1)])}
    ddbdata = client['ddb']['handle'].get_item(TableName=ddbtable, Key={'ETag': ETag}, ConsistentRead=True)
    ddbitem = {}
    if ('Item' in ddbdata):
        ddbitem = ddbdata['Item']
        if (DEBUG > 4):
            print(('DDB record: ' + json.dumps(ddbitem, indent=2)))
    if (repstatus == 'REPLICA'):
        ddb_update_exp += ', s3Replica = :d'
        ddb_exp_attrs[':d'] = {'S': bucket}
        ddb_update_exp += ', end_datetime = :e'
        ddb_exp_attrs[':e'] = {'S': now}
        purge = (datetime.strptime(now, timefmt) - timedelta(hours=purge_thresh))
        ttl = purge.strftime('%s')
        ddb_update_exp += ', itemttl = :p'
        ddb_exp_attrs[':p'] = {'N': ttl}
        ddb_update_exp += ', replication_status = :b'
        ddb_exp_attrs[':b'] = {'S': 'COMPLETED'}
        if (('start_datetime' in ddbitem) and ('crr_rate' not in ddbitem)):
            etime = (datetime.strptime(now, timefmt) - datetime.strptime(ddbitem['start_datetime']['S'], timefmt))
            etimesecs = ((((etime.days * 24) * 60) * 60) + etime.seconds)
            crr_rate = ((int(objsize) * 8) / (etimesecs + 1))
            ddb_update_exp += ', crr_rate = :r'
            ddb_exp_attrs[':r'] = {'N': str(crr_rate)}
            ddb_update_exp += ', elapsed = :t'
            ddb_exp_attrs[':t'] = {'N': str(etimesecs)}
            log_statistics(ddbitem['s3Origin']['S'], bucket, ddbitem['start_datetime']['S'], objsize, str(etimesecs), 300)
    else:
        ddb_update_exp += ', s3Origin = :f'
        ddb_exp_attrs[':f'] = {'S': bucket}
        if ((repstatus == 'COMPLETED') or (repstatus == 'FAILED') or (repstatus == 'PENDING')):
            ddb_update_exp += ', start_datetime = :g'
            ddb_exp_attrs[':g'] = {'S': now}
            if (('end_datetime' in ddbitem) and ('crr_rate' not in ddbitem)):
                etime = (datetime.strptime(ddbitem['end_datetime']['S'], timefmt) - datetime.strptime(now, timefmt))
                etimesecs = ((((etime.days * 24) * 60) * 60) + etime.seconds)
                crr_rate = ((int(objsize) * 8) / (etimesecs + 1))
                ddb_update_exp += ', crr_rate = :r'
                ddb_exp_attrs[':r'] = {'N': str(crr_rate)}
                purge = (datetime.strptime(ddbitem['end_datetime']['S'], timefmt) - timedelta(hours=purge_thresh))
                ttl = purge.strftime('%s')
                ddb_update_exp += ', itemttl = :p'
                ddb_exp_attrs[':p'] = {'N': ttl}
                ddb_update_exp += ', elapsed = :t'
                ddb_exp_attrs[':t'] = {'N': str(etimesecs)}
                log_statistics(bucket, ddbitem['s3Replica']['S'], ddbitem['end_datetime']['S'], objsize, str(etimesecs), 300)
            elif (repstatus == 'FAILED'):
                ddb_update_exp += ', replication_status = :b'
                ddb_exp_attrs[':b'] = {'S': 'FAILED'}
                log_statistics(bucket, 'FAILED', now, '0', '1', 300)
        else:
            print(('Unknown Replication Status: ' + repstatus))
            raise Exception('Unknown Replication Status')
    try:
        response = client['ddb']['handle'].update_item(TableName=ddbtable, Key={'ETag': ETag}, UpdateExpression=ddb_update_exp, ExpressionAttributeValues=ddb_exp_attrs)
    except Exception as e:
        print(e)
        print((('Table ' + ddbtable) + ' update failed'))
        raise e
