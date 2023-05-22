from argparse import RawTextHelpFormatter
import argparse
import base64
import configparser
import hashlib
import inspect
import json
import logging
import os
import platform
import plistlib
import re
import socket
import subprocess
import sys
import pexpect
import requests


def slack_message(self, message, icon, type):
    '\n        This should not be blank.\n        '
    if self.logger:
        self.logger.info(('%s: activated' % inspect.stack()[0][3]))
    slack_info_channel = False
    slack_error_channel = False
    if (self.config_options['slack']['use_slack'] and self.config_options['slack']['slack_info_url']):
        slack_info_channel = True
    if (self.config_options['slack']['use_slack'] and self.config_options['slack']['slack_error_url']):
        slack_error_channel = True
    if (slack_error_channel and (type == 'error')):
        slack_url = self.config_options['slack']['slack_error_url']
    elif slack_info_channel:
        slack_url = self.config_options['slack']['slack_info_url']
    else:
        return
    payload = {'text': message, 'username': ('FWPM ' + self.master_version), 'icon_emoji': ':key:'}
    response = requests.post(slack_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    self.logger.info(('Response: ' + str(response.text)))
    self.logger.info(('Response code: ' + str(response.status_code)))
