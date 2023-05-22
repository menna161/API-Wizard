from __future__ import division
from __future__ import print_function
import base64
import ConfigParser
import hashlib
import inspect
import json
import os
import platform
import plistlib
import pwd
import re
import socket
import subprocess
import sys
import tkFileDialog
import tkSimpleDialog
import ttk
from Tkinter import Tk, N, E, S, W, StringVar, IntVar, PhotoImage, HORIZONTAL
import logging
import pexpect
import requests
import mount_shares_better as msb


def slack_message(self, message, icon, msg_type):
    '\n        Sends slack messages.\n        '
    if self.logger:
        self.logger.info(('%s: activated' % inspect.stack()[0][3]))
    slack_info_channel = False
    slack_error_channel = False
    if (self.config_options['slack']['use_slack'] and self.config_options['slack']['slack_info_url']):
        slack_info_channel = True
    if (self.config_options['slack']['use_slack'] and self.config_options['slack']['slack_error_url']):
        slack_error_channel = True
    if (slack_error_channel and (msg_type == 'error')):
        slack_url = self.config_options['slack']['slack_error_url']
    elif slack_info_channel:
        slack_url = self.config_options['slack']['slack_info_url']
    else:
        return
    payload = {'text': message, 'username': ('Skeleton Key ' + self.master_version), 'icon_emoji': ':old_key:'}
    response = requests.post(slack_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    self.logger.info(('Response: ' + str(response.text)))
    self.logger.info(('Response code: ' + str(response.status_code)))
