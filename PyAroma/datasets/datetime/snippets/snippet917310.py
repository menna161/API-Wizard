import boto3
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import urllib
import urllib.request
import logging


def get_redshift_credentials(self) -> dict:
    " Uses the boto session client to get temporary credentials to\n        connect to Redshift with.\n        If this is in ec2, it will just use the local access stuff, otherwise\n        it will use the boto session's credentials.\n\n        Returns:\n            This returns a dict of the cluster_credentials per boto's Redshift\n            Format is:\n                DbUser (str): Database user for Redshift\n                DbPassword (str): Password for the database user for Redshift\n                Expiration (datetime): The date and time when the password expires\n        "
    if self.is_ec2_flag:
        client = self.boto_session.client('redshift', region_name=self.region)
        temp_redshift_credentials = client.get_cluster_credentials(DbUser=self.iam_user, ClusterIdentifier=self.cluster_id, AutoCreate=True)
    else:
        client = self.boto_session.client('redshift', region_name=self.region, aws_access_key_id=self.aws_credentials.access_key, aws_secret_access_key=self.aws_credentials.secret_key)
        temp_redshift_credentials = client.get_cluster_credentials(DbUser=self.iam_user, ClusterIdentifier=self.cluster_id, AutoCreate=True)
    return temp_redshift_credentials
