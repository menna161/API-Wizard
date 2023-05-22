import pytest
from datetime import datetime, timedelta
import botocore
from athena_glue_service_logs.alb import ALBRawCatalog, ALBConvertedCatalog


def return_s3_objects(*args, **kwargs):
    if ((args[0] == 'ListObjectsV2') and ('Delimiter' in args[1])):
        prefix = args[1]['Prefix']
        return {'IsTruncated': False, 'Name': 'string', 'Prefix': '/', 'Delimiter': 'string', 'MaxKeys': 10, 'KeyCount': 1, 'CommonPrefixes': [{'Prefix': ('%s/us-west-2/' % prefix)}]}
    elif ((args[0] == 'ListObjectsV2') and ('Delimiter' not in args[1])):
        two_days_ago = (datetime.utcnow() - timedelta(days=2)).date()
        prefix = args[1]['Prefix']
        two_days_ago_str = two_days_ago.strftime('%Y/%m/%d')
        return {'IsTruncated': False, 'Contents': [{'Key': ('%s/us-west-2/%s/some_data.json.gz' % (prefix, two_days_ago_str)), 'LastModified': two_days_ago, 'ETag': 'string', 'Size': 123, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}], 'Name': 'string', 'Prefix': '/', 'Delimiter': 'string', 'MaxKeys': 10, 'KeyCount': 1}
