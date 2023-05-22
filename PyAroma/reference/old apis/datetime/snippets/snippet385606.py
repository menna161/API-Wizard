import argparse
import boto3
import sys
import re
import os
import time
import json
import logging
from datetime import datetime
from collections import defaultdict


def main(period, config_file='config.json'):
    log_setup()
    config = read_config(config_file, config_defaults)
    if config['log_file']:
        log_setup(config['log_file'])
    if config.get('aws_profile_name'):
        boto3.setup_default_session(profile_name=(config['aws_profile_name'] or 'default'))
    stats = {'total_vols': 0, 'total_errors': 0, 'snap_deletes': 0, 'snap_creates': 0, 'snap_errors': 0}
    date_suffix = datetime.today().strftime(now_format[period])
    log.info('Started taking %ss snapshots at %s', period, datetime.today().strftime('%d-%m-%Y %H:%M:%S'))
    ec2_region = (config['ec2_region_name'] or None)
    try:
        ec2 = boto3.resource('ec2', region_name=ec2_region)
        vols = get_vols(ec2_resource=ec2, tag_name=config['tag_name'], tag_value=config['tag_value'], tag_type=config['tag_type'], running_only=config['running_only'])
        for vol in vols:
            log.info('Processing volume %s:', vol.id)
            stats['total_vols'] += 1
            description = ('%(period)s_snapshot %(vol_id)s_%(period)s_%(date_suffix)s by snapshot script at %(date)s' % {'period': period, 'vol_id': vol.id, 'date_suffix': date_suffix, 'date': datetime.today().strftime('%d-%m-%Y %H:%M:%S')})
            if (not config['skip_create']):
                try:
                    log.info(">> Creating snapshot for volume %s: '%s'", vol.id, description)
                    current_snap = vol.create_snapshot(Description=description)
                    if (vol.tags is not None):
                        current_snap.create_tags(Tags=vol.tags)
                    stats['snap_creates'] += 1
                except Exception as err:
                    stats['snap_errors'] += 1
                    log.error(('Unexpected error making snapshot:' + str(sys.exc_info()[0])))
                    log.error(err)
                    pass
            if (not config['skip_delete']):
                for del_snap in calc_rotate(config, vol.snapshots.all(), period):
                    log.info('>> Deleting snapshot %s', del_snap.description)
                    try:
                        del_snap.delete()
                        stats['snap_deletes'] += 1
                    except Exception as err:
                        stats['snap_errors'] += 1
                        log.error(('Unexpected error deleting snapshot:' + str(sys.exc_info()[0])))
                        log.error(err)
                        pass
            time.sleep(3)
    except Exception as err:
        stats['total_errors'] += 1
        log.critical(("Can't access volume list:" + str(sys.exc_info()[0])))
        log.critical(err)
    return dump_stats(stats, config['arn'])
