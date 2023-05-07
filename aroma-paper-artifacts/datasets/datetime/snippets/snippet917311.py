import boto3
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import urllib
import urllib.request
import logging


def parse_temp_redshift_credentials(self, rs_creds: dict) -> tuple:
    " Return the user credentials as a tuple, with the username html safe\n        by changing any spaces the +'s\n\n        Args:\n            rs_creds (dict): The Redshift credentials returned by boto\n                Format is:\n                    DbUser (str): Database user for Redshift\n                    DbPassword (str): Password for the database user for Redshift\n                    Expiration (datetime): The date and time when the password expires\n\n        Returns:\n            Tuple of creds, format of:\n                DbUser (str): Database user for Redshift, html escaped\n                DbPassword (str): Password for the database user for Redshift\n        "
    username = rs_creds['DbUser']
    username = urllib.parse.quote_plus(username)
    pwd = rs_creds['DbPassword']
    return (username, pwd)
