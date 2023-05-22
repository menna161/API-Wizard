import fcntl
import json
import mock
import os
import re
import subprocess
import time
from datetime import datetime
from optparse import OptionParser
from ansible.compat import selectors
from ansible.errors import AnsibleError
from ansible.plugins.loader import connection_loader
from logzero import logger


def main():
    global SSHCMD
    parser = OptionParser()
    parser.add_option('--iterations', type=int, default=10)
    parser.add_option('--controlpersist', action='store_true')
    parser.add_option('--selectors', action='store_true')
    parser.add_option('--use_plugin', action='store_true')
    parser.add_option('--vcount', type=int, default=None)
    parser.add_option('--debug', action='store_true')
    parser.add_option('--hostname', default=None)
    parser.add_option('--username', default=None)
    parser.add_option('--keyfile', default=None)
    parser.add_option('--command', default=None)
    (options, args) = parser.parse_args()
    if (not options.debug):
        logger.setLevel('INFO')
    if (not options.use_plugin):
        validate_control_socket(SSHCMD)
        if (not options.controlpersist):
            SSHCMD = remove_control_persist(SSHCMD)
        if options.hostname:
            SSHCMD = set_hostname(SSHCMD, options.hostname)
        if options.username:
            SSHCMD = set_username(SSHCMD, options.username)
        if options.keyfile:
            SSHCMD = set_keyfile(SSHCMD, options.keyfile)
        if (options.vcount is not None):
            SSHCMD = set_vcount(SSHCMD, count=options.vcount)
        if (options.command is not None):
            SSHCMD[(- 1)] = ('/bin/sh -c "%s"' % options.command)
        logger.info(SSHCMD)
    durations = []
    for x in range(0, options.iterations):
        logger.info(('iteration %s' % x))
        start = datetime.now()
        if options.use_plugin:
            (rc, so, se) = run_ssh_exec(command=options.command, hostname=options.hostname, username=options.username, keyfile=options.keyfile)
        else:
            (rc, so, se) = run_ssh_cmd(SSHCMD, hostname=options.hostname, username=options.username, use_selectors=options.selectors)
        stop = datetime.now()
        durations.append((stop - start))
        stats = extract_speeed_from_stdtout(se)
        logger.info('transfer stats ...')
        for (k, v) in stats.items():
            for (k2, v2) in v.items():
                logger.info(('%s.%s = %s' % (k, k2, v2)))
        logger.info(('rc: %s' % rc))
        logger.info(('so:%s' % so.strip()))
        if (rc != 0):
            logger.error(se)
            logger.error(('sshcmd: %s' % ' '.join(SSHCMD)))
    durations = [x.total_seconds() for x in durations]
    logger.info('durations ...')
    for (idx, x) in enumerate(durations):
        logger.info(('%s. %s' % (idx, x)))
    logger.info(('duration min: %s' % min(durations)))
    logger.info(('duration max: %s' % max(durations)))
    avg = (sum(durations) / float(len(durations)))
    logger.info(('duration avg: %s' % avg))
