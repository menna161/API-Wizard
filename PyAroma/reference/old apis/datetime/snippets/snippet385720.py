import boto3
import sys
import argparse
import ast
import urllib.request, urllib.error, urllib.parse
from subprocess import call
import time
from datetime import datetime
import shlex


def main():
    parser = argparse.ArgumentParser(description='SQS Lifecycle hook consumer and trigger')
    parser.add_argument('-q', '--queue', required=True, help='Queue resource.')
    parser.add_argument('-s', '--state', action='store', choices=['LAUNCHING', 'TERMINATING'], required=True, help='Indicates if the consumer is waiting for LAUNCHING or TERMINATING state')
    parser.add_argument('-g', '--group', required=True, help='Auto Scaling Group Name')
    parser.add_argument('-H', '--hookName', required=True, help='Life Cycle Hook Name')
    parser.add_argument('-e', '--execute', required=True, help='The filepath of the triggered script')
    parser.add_argument('-w', '--wait', default=60, type=int, help='Time between query loops in seconds (default: 60)')
    arg = parser.parse_args()
    if (arg.state == 'LAUNCHING'):
        state = 'autoscaling:EC2_INSTANCE_LAUNCHING'
    elif (arg.state == 'TERMINATING'):
        state = 'autoscaling:EC2_INSTANCE_TERMINATING'
    cmd_args = shlex.split(arg.execute)
    print(('%s Getting EC2 instance ID' % datetime.now().strftime('%H:%M:%S %D')))
    ec2instanceid = get_ec2instanceid()
    print(('%s Listening for %s SQS messages using long polling' % (datetime.now().strftime('%H:%M:%S %D'), ec2instanceid)))
    while 1:
        (sqs_msg, sqs_receipt_handle) = sqs_get_msg(arg.queue)
        if (sqs_msg['LifecycleTransition'] == 'autoscaling:TEST_NOTIFICATION'):
            print(('%s Tests message consumed' % datetime.now().strftime('%H:%M:%S %D')))
        elif (sqs_msg['LifecycleTransition'] == False):
            print(('%s There are no messages in the queue. Sleeping and trying again' % datetime.now().strftime('%H:%M:%S %D')))
        elif ((sqs_msg['LifecycleTransition'] == state) and (sqs_msg['EC2InstanceId'] == ec2instanceid)):
            sqs_delete_msg(arg.queue, sqs_receipt_handle)
            print(('%s %s hook message received' % (datetime.now().strftime('%H:%M:%S %D'), arg.state)))
            print(('%s Executing filepath' % datetime.now().strftime('%H:%M:%S %D')))
            call(cmd_args)
            print(('%s Completing lifecyle action' % datetime.now().strftime('%H:%M:%S %D')))
            as_client = boto3.client('autoscaling')
            response = as_client.complete_lifecycle_action(LifecycleHookName=arg.hookName, AutoScalingGroupName=arg.group, LifecycleActionToken=sqs_msg['LifecycleActionToken'], LifecycleActionResult='CONTINUE', InstanceId=ec2instanceid)
        time.sleep(arg.wait)
