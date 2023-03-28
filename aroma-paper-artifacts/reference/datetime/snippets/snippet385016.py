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


def print_expiration_time(aws_expiration):
    remaining = (aws_expiration - datetime.datetime.now(tz=pytz.utc))
    print(('Temporary credentials will expire in %s.' % remaining), file=sys.stderr)
