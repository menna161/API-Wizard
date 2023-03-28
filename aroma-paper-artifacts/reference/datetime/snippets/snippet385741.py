import sys
import argparse
import boto3
import re
import time
from datetime import datetime
import urllib2
import urllib.request, urllib.error, urllib.parse


def main():
    parser = argparse.ArgumentParser(description='AWS Route53 hostname managment for Autoscaled EC2 Instances')
    parser.add_argument('--HostedZoneId', required=True, help='The ID of the hosted zone where the new resource record will be added.')
    parser.add_argument('--HostStr', required=True, help='The host string used to build the new name')
    parser.add_argument('--rangeSize', type=int, default=10, help='The maximun number to be assigned. The first available will be used')
    parser.add_argument('--dryrun', action='store_true', help="Shows what is going to be done but doesn't change anything actually")
    arg = parser.parse_args()
    available_hostname = get_available_hostname(arg.HostedZoneId, arg.HostStr, arg.rangeSize)
    private_ip = get_private_ip()
    public_dns = get_public_dns_hostname()
    date = datetime.now().strftime('%H:%M:%S %D')
    sys.stdout.write(('%s: creating CNAME %s -> %s' % (date, available_hostname, public_dns)))
    sys.stdout.flush()
    if (arg.dryrun is False):
        set_hostname_record(arg.HostedZoneId, public_dns, available_hostname, private_ip)
