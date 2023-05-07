from __future__ import division
from __future__ import print_function
from builtins import str
from past.utils import old_div
import argparse
import datetime
import getpass
import json
import logging
import re
import time
from prettytable import PrettyTable
from vspk import v6 as vsdk


def main():
    '\n    Main function to handle vcenter vm names and the mapping to a policy group\n    '
    args = get_args()
    debug = args.debug
    extended = args.extended
    json_output = args.json_output
    log_file = None
    if args.logfile:
        log_file = args.logfile
    nuage_enterprise = args.nuage_enterprise
    nuage_host = args.nuage_host
    nuage_port = args.nuage_port
    nuage_password = None
    if args.nuage_password:
        nuage_password = args.nuage_password
    nuage_username = args.nuage_username
    time_difference = args.time_difference
    verbose = args.verbose
    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s %(message)s', level=log_level)
    logger = logging.getLogger(__name__)
    time_check = re.compile('^([0-9]+)([m|h|d]?)$')
    time_matches = time_check.match(time_difference)
    if (time_matches is None):
        logger.critical(('The time indication %s is an invalid value, exiting' % time_difference))
        return 1
    time_diff = int(float(time_matches.group(1)))
    if (time_matches.group(2) == 'm'):
        logger.debug('Found m in the time difference, multiplying integer by 60')
        time_diff *= 60
    elif (time_matches.group(2) == 'h'):
        logger.debug('Found h in the time difference, multiplying integer by 3600')
        time_diff *= 3600
    elif (time_matches.group(2) == 'd'):
        logger.debug('Found d in the time difference, multiplying integer by 86400')
        time_diff *= 86400
    logger.debug(('Time difference set to %s seconds' % time_diff))
    if (nuage_password is None):
        logger.debug('No command line Nuage password received, requesting Nuage password from user')
        nuage_password = getpass.getpass(prompt=('Enter password for Nuage host %s for user %s: ' % (nuage_host, nuage_username)))
    try:
        logger.info(('Connecting to Nuage server %s:%s with username %s' % (nuage_host, nuage_port, nuage_username)))
        nc = vsdk.NUVSDSession(username=nuage_username, password=nuage_password, enterprise=nuage_enterprise, api_url=('https://%s:%s' % (nuage_host, nuage_port)))
        nc.start()
    except Exception as e:
        logger.error(('Could not connect to Nuage host %s with user %s and specified password' % (nuage_host, nuage_username)))
        logger.critical(('Caught exception: %s' % str(e)))
        return 1
    if json_output:
        logger.debug('JSON output enabled, not setting up an output table')
        json_object = []
    elif extended:
        logger.debug('Setting up extended output table')
        pt = PrettyTable(['Enterprise', 'Timestamp', 'Date/Time', 'Type', 'Entity', 'Entity parent', 'Extended info'])
    else:
        logger.debug('Setting up basic output table')
        pt = PrettyTable(['Enterprise', 'Timestamp', 'Date/Time', 'Type', 'Entity', 'Entity parent'])
    unix_check_time = (time.time() - time_diff)
    logger.debug(('Gathering all events from after UNIX timestamp %s' % unix_check_time))
    for ent in nc.user.enterprises.get():
        logger.debug(('Gathering events for enterprise %s' % ent.name))
        for event in ent.event_logs.get(filter=("eventReceivedTime >= '%s'" % int((unix_check_time * 1000)))):
            logger.debug(('Found event of type %s with timestamp %s' % (event.type, event.event_received_time)))
            clean_time = datetime.datetime.fromtimestamp(int(old_div(event.event_received_time, 1000))).strftime('%Y-%m-%d %H:%M:%S')
            if json_output:
                json_dict = {'Enterprise': ent.name, 'Timestamp': event.event_received_time, 'Date/Time': clean_time, 'Type': event.type, 'Entity': event.entity_type, 'Entity parent': event.entity_parent_type}
                if extended:
                    json_dict['Extended info'] = event.entities
                json_object.append(json_dict)
            elif extended:
                pt.add_row([ent.name, event.event_received_time, clean_time, event.type, event.entity_type, event.entity_parent_type, json.dumps(event.entities)])
            else:
                pt.add_row([ent.name, event.event_received_time, clean_time, event.type, event.entity_type, event.entity_parent_type])
    logger.debug('Printing output')
    if json_output:
        print(json.dumps(json_object, sort_keys=True, indent=4))
    else:
        print(pt.get_string(sortby='Timestamp'))
    return 0
