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


def onetime_passwd_expired(log, user, login_profile, hours):
    'Test if initial one-time-only password is expired'
    if (login_profile and login_profile.password_reset_required):
        log.debug(('now: %s' % utcnow().isoformat()))
        log.debug(('ttl: %s' % datetime.timedelta(hours=hours)))
        log.debug(('delta: %s' % (utcnow() - login_profile.create_date)))
        return ((utcnow() - login_profile.create_date) > datetime.timedelta(hours=hours))
    return False
