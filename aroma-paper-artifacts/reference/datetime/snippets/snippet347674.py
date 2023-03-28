import argparse
import boolean
import datetime
from dateutil.parser import parse as dateparse
import hashlib
import logging
import os
import re
import sys


def get_sids(self, kvpair, negate=False):
    'Get a list of all SIDs for passed in key-value pair.\n\n        :param kvpair: key-value pair\n        :type kvpair: string, required\n        :param negate: returns the inverse of the result (i.e. all SIDs not matching the ``kvpair``), defaults to `False`\n        :type negate: boolean, optional\n        :returns: list of matching SIDs\n        :rtype: list\n        :raises: `AristotleException`\n        '
    (k, v) = [e.strip() for e in kvpair.split(' ', 1)]
    retarray = []
    rangekeys = ['sid', 'cve', 'cvss_v2_base', 'cvss_v2_temporal', 'cvss_v3_base', 'cvss_v3_temporal', 'created_at', 'updated_at']
    if ((k in rangekeys) and (v.startswith('<') or v.startswith('>')) and (v not in ['<all>', '<any>'])):
        if (len(v) < 2):
            print_error("Invalid value '{}' for key '{}'.".format(v, k), fatal=True)
        if (k == 'cve'):
            try:
                offset = 1
                if (v[1] == '='):
                    offset += 1
                cmp_operator = v[:offset]
                cve_val = v[offset:].strip()
                print_debug('cmp_operator: {}, cve_val: {}'.format(cmp_operator, cve_val))
                retarray = [s for s in [s2 for s2 in self.metadata_dict.keys() if (k in self.metadata_dict[s2]['metadata'].keys())] for val in self.metadata_dict[s]['metadata'][k] if (self.cve_compare(left_val=val, right_val=cve_val, cmp_operator=cmp_operator) and ((not self.metadata_dict[s]['disabled']) or self.include_disabled_rules))]
            except Exception as e:
                print_error("Unable to process key '{}' value '{}' (as CVE number):\n{}".format(k, v, e), fatal=True)
        elif (k in ['created_at', 'updated_at']):
            try:
                lbound = datetime.datetime.min
                ubound = datetime.datetime.max
                offset = 1
                if v.startswith('<'):
                    if (v[offset] == '='):
                        offset += 1
                    ubound = dateparse(v[offset:].strip())
                    ubound += datetime.timedelta(microseconds=(offset - 1))
                else:
                    if (v[offset] == '='):
                        offset += 1
                    lbound = dateparse(v[offset:].strip())
                    lbound -= datetime.timedelta(microseconds=(offset - 1))
                print_debug('lbound: {}\nubound: {}'.format(lbound, ubound))
                retarray = [s for s in [s2 for s2 in self.metadata_dict.keys() if (k in self.metadata_dict[s2]['metadata'].keys())] for val in self.metadata_dict[s]['metadata'][k] if (((dateparse(val) < ubound) and (dateparse(val) > lbound)) and ((not self.metadata_dict[s]['disabled']) or self.include_disabled_rules))]
            except Exception as e:
                print_error("Unable to process '{}' value '{}' (as datetime):\n{}".format(k, v, e), fatal=True)
        else:
            try:
                lbound = float('-inf')
                ubound = float('inf')
                offset = 1
                if v.startswith('<'):
                    if (v[offset] == '='):
                        offset += 1
                    ubound = float(v[offset:].strip())
                    ubound += (float(offset) - 1.0)
                else:
                    if (v[offset] == '='):
                        offset += 1
                    lbound = float(v[offset:].strip())
                    lbound -= (float(offset) - 1.0)
                print_debug('lbound: {}\nubound: {}'.format(lbound, ubound))
                retarray = [s for s in [s2 for s2 in self.metadata_dict.keys() if (k in self.metadata_dict[s2]['metadata'].keys())] for val in self.metadata_dict[s]['metadata'][k] if (((float(val) < float(ubound)) and (float(val) > float(lbound))) and ((not self.metadata_dict[s]['disabled']) or self.include_disabled_rules))]
            except Exception as e:
                print_error("Unable to process '{}' value '{}' (as float):\n{}".format(k, v, e), fatal=True)
    elif (k not in self.keys_dict.keys()):
        print_warning("metadata key '{}' not found in ruleset".format(k))
    elif (v in ['<all>', '<any>']):
        retarray = [s for val in self.keys_dict[k].keys() for s in self.keys_dict[k][val] if ((not self.metadata_dict[s]['disabled']) or self.include_disabled_rules)]
    elif (v not in self.keys_dict[k]):
        print_warning("metadata key-value pair '{}' not found in ruleset".format(kvpair))
        retarray = []
    else:
        retarray = [s for s in self.keys_dict[k][v] if ((not self.metadata_dict[s]['disabled']) or self.include_disabled_rules)]
    if negate:
        retarray = list((frozenset(self.get_all_sids()) - frozenset(retarray)))
    return list(set(retarray))
