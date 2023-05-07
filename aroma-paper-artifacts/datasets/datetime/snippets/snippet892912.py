import argparse
import copy
import datetime
import logging
import matplotlib as mpl
import multiprocessing
import numpy as np
import os
from pathlib import Path
import shutil
import tensorflow as tf
import time
import functions.reading as reading
import functions.general_utils as gut
import functions.setting.setting_utils as su
import functions.network as network
import functions.tf_utils as tfu


def backup_script(setting):
    '\n    This script does\n    1. Update the current_experiment name based on stage and deform_exp name.\n    2. Make a backup of the whole code\n    3. Start logging.\n    :param setting\n    :return setting\n    '
    date_now = datetime.datetime.now()
    network_name = ''
    if ('crop' in setting['NetworkDesign']):
        network_name = setting['NetworkDesign'].rsplit('_', 1)[0]
    if ('decimation' in setting['NetworkDesign']):
        network_name = ('dec' + setting['NetworkDesign'][(- 1)])
    if ('unet' in setting['NetworkDesign']):
        network_name = ('unet' + setting['NetworkDesign'][(- 1)])
    current_experiment = (((((((('{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}'.format(date_now.year, date_now.month, date_now.day, date_now.hour, date_now.minute, date_now.second) + '_') + setting['DataExpDict'][0]['deform_exp']) + '_') + setting['AGMode']) + '_S') + str(setting['stage'])) + '_') + network_name)
    setting['current_experiment'] = current_experiment
    if (not os.path.isdir(su.address_generator(setting, 'ModelFolder'))):
        os.makedirs(su.address_generator(setting, 'ModelFolder'))
    shutil.copy(Path(__file__), su.address_generator(setting, 'ModelFolder'))
    shutil.copytree((Path(__file__).parent / Path('functions')), (Path(su.address_generator(setting, 'ModelFolder')) / Path('functions')))
    gut.logger.set_log_file(su.address_generator(setting, 'LogFile'))
    return setting
