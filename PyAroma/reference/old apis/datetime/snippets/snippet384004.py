import sys
import argparse
import datetime
from awscfnctl import CfnControl


def main():
    rc = 0
    args = arg_parse()
    region = args.region
    instance_state = args.instance_state
    inst_info_all = list()
    client = CfnControl(region=region)
    for (inst, info) in client.get_instance_info(instance_state=instance_state).items():
        inst_info = list()
        inst_info.append(inst)
        for (k, v) in info.items():
            if isinstance(v, datetime.datetime):
                v = str(v)[:(- 6)]
            inst_info.append(v)
        inst_info_all.append(inst_info)
    print
    print_header()
    print((155 * '-'))
    print('\n'.join(('{:<20} {:<20} {:<20.20}  {:<30}  {:<15}  {:<7}  {:<15}  {:<20}'.format(*i) for i in Sort(inst_info_all))))
    print
    return rc
