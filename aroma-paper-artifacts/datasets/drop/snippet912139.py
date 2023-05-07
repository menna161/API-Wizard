import boto3
import logging
import psycopg2
from botocore.exceptions import ClientError
from psycopg2.extensions import AsIs
from cfn_resource_provider import ResourceProvider


def delete(self):
    if (self.physical_resource_id == 'could-not-create'):
        self.success('user was never created')
    try:
        self.connect()
        self.drop()
    except Exception as e:
        return self.fail(str(e))
    finally:
        self.close()
