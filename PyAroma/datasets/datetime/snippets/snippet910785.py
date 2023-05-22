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
    '\n    Main function to handle statistics\n    '
    args = get_args()
    debug = args.debug
    entity_type = args.entity_type
    json_output = args.json_output
    log_file = None
    if args.logfile:
        log_file = args.logfile
    entity_name = None
    if args.entity_name:
        entity_name = args.entity_name
    nuage_enterprise = args.nuage_enterprise
    nuage_host = args.nuage_host
    nuage_port = args.nuage_port
    nuage_password = None
    if args.nuage_password:
        nuage_password = args.nuage_password
    nuage_username = args.nuage_username
    statistic_types = statistics_valid_types
    if args.statistic_types:
        statistic_types = args.statistic_types
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
    output_type = None
    entities = []
    output_type = entity_type.capitalize()
    search_query = (('name == "%s"' % entity_name) if entity_name else None)
    logger.debug(('Getting %ss matching the search' % output_type))
    entities = nc.user.fetcher_for_rest_name(entity_type.lower()).get(filter=search_query)
    if ((entity_type == 'VM') and entities):
        vms = entities
        entities = []
        for vm in vms:
            for vm_interface in vm.vm_interfaces.get():
                entities.append(vm_interface)
    output_fields = [output_type, 'Start timestamp', 'End timestamp', 'Start date/time', 'End date/time', '# datapoints']
    output_fields.extend(statistic_types)
    if (len(entities) == 0):
        logger.critical(('No matching entities found of type %s' % entity_type))
        return 1
    if json_output:
        logger.debug('JSON output enabled, not setting up an output table')
        json_object = []
    else:
        logger.debug('Setting up output table')
        pt = PrettyTable(output_fields)
    stat_end_time = int(time.time())
    stat_start_time = int((stat_end_time - time_diff))
    stat_metric_types_str = ','.join(statistic_types)
    entity_data_freq = 60
    for entity in entities:
        if ((entity_type != 'VM') and ('BackHaul' in entity.name)):
            logger.debug(('Found a BackHaul %s, skipping' % output_type))
            continue
        if (entity_type != 'VM'):
            logger.debug(('Looking for a statistics policy on %s %s' % (output_type, entity.name)))
            entity_stat_policies = entity.statistics_policies.get()
            if (len(entity_stat_policies) > 0):
                logger.debug(('Found at least one statistics policy on %s %s, getting data collection frequency' % (output_type, entity.name)))
                entity_data_freq = entity_stat_policies[0].data_collection_frequency
            logger.debug(('Data collection frequency for %s %s saved as %s' % (output_type, entity.name, entity_data_freq)))
        num_data_points = int(old_div(time_diff, entity_data_freq))
        logger.debug(('Collecting %s datapoints of statistics %s on %s %s from timestamp %s to timestamp %s' % (num_data_points, stat_metric_types_str, output_type, entity.name, stat_start_time, stat_end_time)))
        stats_data = entity.statistics.get_first(query_parameters={'startTime': stat_start_time, 'endTime': stat_end_time, 'numberOfDataPoints': num_data_points, 'metricTypes': stat_metric_types_str}).stats_data
        output_name = entity.name
        if (entity_type == 'VM'):
            output_name = ('%s %s' % (entity.parent.name, entity.mac))
        if json_output:
            json_dict = {output_type: output_name, 'Start timestamp': stat_start_time, 'End timestamp': stat_end_time, 'Start date/time': datetime.datetime.fromtimestamp(stat_start_time).strftime('%Y-%m-%d %H:%M:%S'), 'End date/time': datetime.datetime.fromtimestamp(stat_end_time).strftime('%Y-%m-%d %H:%M:%S'), '# datapoints': num_data_points}
            json_dict.update(stats_data)
            json_object.append(json_dict)
        else:
            row = [output_name, stat_start_time, stat_end_time, datetime.datetime.fromtimestamp(stat_start_time).strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.fromtimestamp(stat_end_time).strftime('%Y-%m-%d %H:%M:%S'), num_data_points]
            for statistic_type in statistic_types:
                row.append(stats_data[statistic_type])
            pt.add_row(row)
    logger.debug('Printing output')
    if json_output:
        print(json.dumps(json_object, sort_keys=True, indent=4))
    else:
        print(pt.get_string())
    return 0
