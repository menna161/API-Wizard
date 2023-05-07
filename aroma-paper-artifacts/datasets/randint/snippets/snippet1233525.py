import random
from string import ascii_lowercase
import netaddr
from oslo_log import log as logging
from tempest import config
from tempest.lib.common.utils import data_utils


def rand_mx_recordset(zone_name, pref=None, host=None, **kwargs):
    if (pref is None):
        pref = str(random.randint(0, 65535))
    if (host is None):
        host = rand_zone_name(prefix='mail', suffix=('.' + zone_name))
    data = '{0} {1}'.format(pref, host)
    return rand_recordset_data('MX', zone_name, records=[data], **kwargs)
