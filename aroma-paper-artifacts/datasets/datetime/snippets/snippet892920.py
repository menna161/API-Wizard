import argparse
import datetime
import json
import logging
from pathlib import Path
import shutil
import functions.elastix_python as elx
import functions.general_utils as gut
import functions.landmarks_utils as lu
import functions.network as network
import functions.registration as reg
import functions.setting.setting_utils as su
from functions.setting.experiment_setting import load_network_multi_stage_from_predefined


def initialize(current_experiment, stage_list, folder_script='functions'):
    parser = argparse.ArgumentParser(description='read where_to_run')
    parser.add_argument('--where_to_run', '-w', help='This is an optional argument, you choose between "Auto" or "Cluster". The default value is "Auto"')
    args = parser.parse_args()
    where_to_run = args.where_to_run
    setting = su.initialize_setting(current_experiment=current_experiment, where_to_run=where_to_run)
    date_now = datetime.datetime.now()
    backup_number = '{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}'.format(date_now.year, date_now.month, date_now.day, date_now.hour, date_now.minute, date_now.second)
    backup_root_folder = (su.address_generator(setting, 'result_step_folder', stage_list=stage_list) + 'CodeBackup/')
    backup_folder = (((backup_root_folder + 'backup-') + str(backup_number)) + '/')
    gut.logger.set_log_file((backup_folder + 'log.txt'), short_mode=True)
    shutil.copy(Path(__file__), (Path(backup_folder) / Path(__file__).name))
    shutil.copytree((Path(__file__).parent / Path(folder_script)), (Path(backup_folder) / Path(folder_script)))
    return (setting, backup_folder)
