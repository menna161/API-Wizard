from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime, timedelta
import urllib.request


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
