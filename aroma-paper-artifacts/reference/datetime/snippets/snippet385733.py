import sys
import argparse
import boto3
import time
from datetime import datetime
import socket
import urllib2
import urllib.request, urllib.error, urllib.parse


def main():
    parser = argparse.ArgumentParser(description='Delete host record from AWS Route53 zone')
    parser.add_argument('--HostedZoneId', required=True, help='The ID of the hosted zone where the new resource record will be added.')
    parser.add_argument('--dryrun', action='store_true', help="Shows what is going to be done but doesn't change anything actually")
    arg = parser.parse_args()
    hostname = socket.gethostname()
    private_ip = get_private_ip()
    public_dns = get_public_dns_hostname()
    client = boto3.client('route53')
    zone = client.get_hosted_zone(Id=arg.HostedZoneId)
    fqdn = ((hostname + '.') + zone['HostedZone']['Name'])
    date = datetime.now().strftime('%H:%M:%S %D')
    sys.stdout.write(('%s: deleting CNAME %s -> %s' % (date, fqdn, public_dns)))
    sys.stdout.flush()
    if (arg.dryrun is False):
        del_hostname_record(arg.HostedZoneId, public_dns, fqdn, private_ip)
