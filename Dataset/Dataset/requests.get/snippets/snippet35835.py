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


def search_jss(self):
    '\n        Search the JAMF server for FWPM Control script, strip out and categorize keyfile.\n        '
    self.logger.info(('%s: activated' % inspect.stack()[0][3]))
    try:
        jss_search_url = (self.jamf_hostname.get() + '/JSSResource/scripts')
        headers = {'Accept': 'application/json'}
        response = requests.get(url=jss_search_url, headers=headers, auth=requests.auth.HTTPBasicAuth(self.jamf_username.get(), self.jamf_password.get()))
        script_list = response.json()
    except requests.exceptions.HTTPError as this_error:
        self.logger.error(('http error %s: %s\n' % (response.status_code, this_error)))
        if (response.status_code == 400):
            self.logger.error('HTTP code {}: {}'.format(response.status_code, 'Request error.'))
        elif (response.status_code == 401):
            self.logger.error('HTTP code {}: {}'.format(response.status_code, 'Authorization error.'))
        elif (response.status_code == 403):
            self.logger.error('HTTP code {}: {}'.format(response.status_code, 'Permissions error.'))
        elif (response.status_code == 404):
            self.logger.error('HTTP code {}: {}'.format(response.status_code, 'Resource not found.'))
    for item in script_list['scripts']:
        if ('FWPM Control' in item['name']):
            target_id = item['id']
    script_url = ((self.jamf_hostname.get() + '/JSSResource/scripts/id/') + str(target_id))
    headers = {'Accept': 'application/json'}
    response = requests.get(url=script_url, headers=headers, auth=requests.auth.HTTPBasicAuth(self.jamf_username.get(), self.jamf_password.get()))
    response_json = response.json()
    if (response.status_code != 200):
        self.logger.info(('%i returned.' % response.code))
        return
    working_output = response_json['script']['script_contents'].split('\n')
    self.previous_keys = []
    for line in working_output:
        if (("'previous':" in line) and ('#' not in line)):
            try:
                contents = re.findall("\\s*\\'previous\\': \\[(.*)\\]", line)
                if contents:
                    in_contents = contents[0].split(', ')
                    in_contents = [i for i in in_contents if i]
                    for item in in_contents:
                        subitem = item.split('"')
                        subitem = [i for i in subitem if i]
                        subitem = [i for i in subitem if (i != ',')]
                        if subitem:
                            self.previous_keys.append(subitem[0])
            except Exception as exception_message:
                self.logger.error(('%s: Unknown error. [%s]' % (inspect.stack()[0][3], exception_message)))
        elif (("'new':" in line) and ('#' not in line)):
            try:
                contents = re.findall("\\s*\\'new\\': (.*)", line)
                if contents:
                    if (len(contents) == 1):
                        contents = contents[0]
                    else:
                        quit()
                    subitem = contents.split('"')
                    subitem = [i for i in subitem if i]
                    self.current_key = subitem[0]
            except Exception as exception_message:
                self.logger.error(('%s: Unknown error. [%s]' % (inspect.stack()[0][3], exception_message)))
    try:
        self.calculate_hash()
        self.status_string.set('Keys loaded successfully.')
        self.keys_loaded_string.set('Keys copied to memory.')
    except Exception as exception_message:
        self.logger.error(exception_message)
        self.flush_keys()
