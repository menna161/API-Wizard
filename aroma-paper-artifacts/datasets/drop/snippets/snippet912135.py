import boto3
import logging
import psycopg2
from botocore.exceptions import ClientError
from psycopg2.extensions import AsIs
from cfn_resource_provider import ResourceProvider


def drop(self):
    if (self.with_database and self.db_exists()):
        self.drop_database()
    if self.role_exists():
        self.drop_user()
