from __future__ import print_function
from builtins import input
import argparse
import datetime
import os
import sys
import boto3.session
import botocore
import botocore.exceptions
import botocore.session
import pytz
from six import PY2
from six.moves import configparser
from six.moves import shlex_quote
from ._version import VERSION


def use_testing_credentials(args, credentials):
    print('Skipping AWS API calls because AWSMFA_TESTING_MODE is set.', file=sys.stderr)
    fake_expiration = (datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(minutes=5))
    fake_credentials = {'AccessKeyId': credentials.get(args.identity_profile, 'aws_access_key_id'), 'SecretAccessKey': credentials.get(args.identity_profile, 'aws_secret_access_key'), 'SessionToken': '420', 'Expiration': fake_expiration}
    print_expiration_time(fake_expiration)
    update_credentials_file(args.aws_credentials, args.target_profile, args.identity_profile, credentials, fake_credentials)
