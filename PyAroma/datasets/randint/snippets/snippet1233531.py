import random
from string import ascii_lowercase
import netaddr
from oslo_log import log as logging
from tempest import config
from tempest.lib.common.utils import data_utils


def rand_ns_records():
    ns_zone = rand_zone_name()
    records = []
    for i in range(0, 2):
        records.append(('ns%s.%s' % (i, ns_zone)))
    ns_records = [{'hostname': x, 'priority': random.randint(1, 999)} for x in records]
    return ns_records
