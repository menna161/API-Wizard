import os
import sys
import yaml
import logging
from string import Template
import datetime
import smtplib
from email.message import EmailMessage
import boto3
from botocore.exceptions import ClientError
from docopt import docopt
from passwordgenerator import pwgenerator
import awsorgs
from awsorgs.utils import *
from awsorgs.spec import *
from awsorgs.reports import *


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)
