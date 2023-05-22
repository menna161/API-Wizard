import random
from string import ascii_lowercase
import netaddr
from oslo_log import log as logging
from tempest import config
from tempest.lib.common.utils import data_utils


def rand_soa_records(number_of_records=2):
    return ['{} {} {} {} {} {}.'.format('{}.{}.{}'.format(rand_string(3), rand_string(7), rand_string(3)), random.randint(1000000000, 2020080302), random.randint(3000, 7200), random.randint(1000, 3600), random.randint(1000000, 1209600), random.randint(1000, 3600)) for i in range(0, number_of_records)]
