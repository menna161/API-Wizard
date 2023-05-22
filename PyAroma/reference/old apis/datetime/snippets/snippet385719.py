import boto3
import sys
import argparse
import ast
import urllib.request, urllib.error, urllib.parse
from subprocess import call
import time
from datetime import datetime
import shlex


def get_ec2instanceid():
    try:
        response = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
    except:
        sys.exit(('%s I am not running in EC2. Aborting!!' % datetime.now().strftime('%H:%M:%S %D')))
    instanceid = response.read()
    return instanceid
