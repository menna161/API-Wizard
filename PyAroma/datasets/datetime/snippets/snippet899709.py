import argparse
import getpass
import json
import os
import shutil
import subprocess
import threading
import datetime
from subprocess import Popen, PIPE
import py_cui
import pyautogit.logger as LOGGER
import pyautogit.repo_select_screen as SELECT
import pyautogit.repo_control_screen as CONTROL
import pyautogit.internal_editor_screen as EDITOR
import pyautogit.settings_screen as SETTINGS
import pyautogit.metadata_manager as METADATA


def main():
    'Entry point for pyautogit. Parses arguments, and initializes the CUI\n    '
    (target, credentials, args) = parse_args()
    save_metadata = (not args['nosavemetadata'])
    debug_logging = args['debug']
    target_abs = os.path.abspath(target)
    input_type = 'repo'
    if (not is_git_repo(target)):
        input_type = 'workspace'
    if (not os.access(target, os.W_OK)):
        print('ERROR - Permission error for target {}'.format(target_abs))
        exit((- 1))
    if ((input_type == 'repo') and (not os.access(os.path.dirname(target_abs), os.W_OK))):
        print('ERROR - Permission denied for parent workspace {} of repository {}'.format(os.path.dirname(target_abs), target_abs))
        exit((- 1))
    if debug_logging:
        if (input_type == 'repo'):
            LOGGER.set_log_file_path('../.pyautogit/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]))
        else:
            LOGGER.set_log_file_path('.pyautogit/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]))
        LOGGER.toggle_logging()
        LOGGER.write('Initialized debug logging')
    root = py_cui.PyCUI(5, 4)
    if debug_logging:
        root.enable_logging(log_file_path='.pyautogit/py_cui_root.log')
    root.toggle_unicode_borders()
    _ = PyAutogitManager(root, target, input_type, save_metadata, credentials)
    LOGGER.write('Parsed args. Target location - {}'.format(target_abs))
    LOGGER.write('Initial state - {}'.format(input_type))
    LOGGER.write('Initialized manager object, starting CUI...')
    root.start()
