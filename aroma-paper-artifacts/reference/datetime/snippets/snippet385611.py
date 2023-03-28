import pytest
from unittest.mock import patch, Mock
from aws_rotate import create_new_access_key
from datetime import datetime
from botocore.exceptions import ClientError


@patch('boto3.client')
def test_returns_new_keys(mock_iam):
    '\n    The new keys should be returned\n    '
    mock_iam.return_value.create_access_key.return_value = {'AccessKey': {'UserName': 'foo.bar', 'AccessKeyId': 'MYACCESSKEYID', 'Status': 'Active', 'SecretAccessKey': 'NOTONEOFTHESE', 'CreateDate': datetime(2015, 1, 1)}}
    assert (create_new_access_key() == {'AccessKeyId': 'MYACCESSKEYID', 'SecretAccessKey': 'NOTONEOFTHESE'})
