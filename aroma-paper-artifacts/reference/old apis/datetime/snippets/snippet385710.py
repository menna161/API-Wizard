import boto3
import argparse
import sys
from botocore.exceptions import ClientError
from rich.console import Console
from rich.table import Table
from requests import get
import random
import datetime


def main():
    parser = argparse.ArgumentParser(description='Security Groups Management')
    parser.add_argument('-n', '--name', help='Filter result by group name.')
    parser.add_argument('-l', '--gid_list', nargs='+', type=str, help='Do not filter the result. Provide a GroupIds list instead.')
    parser.add_argument('-r', '--region', help='Specify an alternate region to override                               the one defined in the .aws/credentials file')
    parser.add_argument('-s', '--show', help='Show inbound and outbound rules for the provided SG ID')
    parser.add_argument('--allow_my_public_ip', help='Modify the SSH inbound rule with your current public IP                               address inside the provided Security Group ID.')
    parser.add_argument('--security_group_rule_id', help='Modify the SSH inbound rule with your current public IP                              address inside the provided Security Group Rule ID')
    parser.add_argument('--description', default='', help='Allows you to append a string to the rule description field')
    arg = parser.parse_args()
    filter = []
    GroupIds = []
    if (arg.allow_my_public_ip and (not arg.security_group_rule_id)):
        print('The argument allow_my_public_ip requires the argument security_group_rule_id.')
        sys.exit(1)
    if arg.allow_my_public_ip:
        ec2 = boto3.client('ec2')
        ip = None
        ip_services = ['https://api.ipify.org', 'https://ifconfig.me', 'https://api.my-ip.io/ip', 'http://myexternalip.com/raw', 'http://ipwho.is/&fields=ip&output=csv']
        random.shuffle(ip_services)
        for url in ip_services:
            try:
                ip = get(url).content.decode('utf8')
                break
            except:
                print(('%s fail. Trying next...' % url))
        if (ip is None):
            print('Public IP address not found using any services')
            sys.exit(1)
        else:
            now = datetime.datetime.now()
            try:
                data = ec2.modify_security_group_rules(GroupId=arg.allow_my_public_ip, SecurityGroupRules=[{'SecurityGroupRuleId': arg.security_group_rule_id, 'SecurityGroupRule': {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIpv4': (ip + '/32'), 'Description': (((('(' + arg.description) + ') ') + now.strftime('%Y-%m-%d %H:%M:%S')) + ' by ec2-sg.py from aws-scripts')}}])
                if data:
                    rule_table = Table(title=(('Inbound Rule updated on the ' + arg.allow_my_public_ip) + ' Security Group'))
                    rule_table.add_column('SG Rule ID', style='cyan')
                    rule_table.add_column('IP Version', style='green')
                    rule_table.add_column('Type', style='green')
                    rule_table.add_column('Protocol', justify='right', style='green')
                    rule_table.add_column('Port Range', justify='right', style='green')
                    rule_table.add_column('Source', justify='right', style='green')
                    rule_table.add_column('Description', justify='right', style='green')
                    rule_table.add_row(arg.security_group_rule_id, 'IPv4', 'SSH', 'TCP', '[red]22', (('[red]' + ip) + '/32'), (((('[white](' + arg.description) + ') ') + now.strftime('%Y-%m-%d %H:%M:%S')) + ' by ec2-sg.py from aws-scripts'))
                    console = Console()
                    console.print(rule_table)
                    sys.exit(0)
                else:
                    print('an error occurred!')
            except ClientError as e:
                print(e)
                sys.exit(0)
    if arg.name:
        filter.append({'Name': 'group-name', 'Values': [(('*' + arg.name) + '*')]})
    if arg.gid_list:
        GroupIds = arg.gid_list
    if arg.region:
        client = boto3.client('ec2')
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
        if (arg.region not in regions):
            sys.exit('ERROR: Please, choose a valid region.')
    if (not arg.show):
        list_security_groups(filter, GroupIds, arg.region)
    else:
        filter = []
        filter.append({'Name': 'group-id', 'Values': [arg.show]})
        list_security_group(filter, arg.region)
