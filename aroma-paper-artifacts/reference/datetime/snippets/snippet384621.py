from __future__ import print_function
from botocore.exceptions import ClientError
import boto3
import os
import json
import datetime
import uuid
import time
import detect


def InstanceCredentialExfiltration(event, context):
    print(('log -- Event: %s ' % json.dumps(event)))
    event['remediation'] = {}
    event['remediation']['success'] = False
    event['remediation']['title'] = 'GuardDog was unable to remediate the Instance'
    event['remediation']['description'] = 'Auto remediation was unsuccessful.  Please review the finding and remediate manaully.'
    try:
        iam = boto3.client('iam')
        ec2 = boto3.client('ec2')
        role = event['detail']['resource']['accessKeyDetails']['userName']
        time = datetime.datetime.utcnow().isoformat()
        policy = ('\n        {\n          "Version": "2012-10-17",\n          "Statement": {\n            "Effect": "Deny",\n            "Action": "*",\n            "Resource": "*",\n            "Condition": {"DateLessThan": {"aws:TokenIssueTime": "%s"}}\n          }\n        }\n        ' % time)
        iam.put_role_policy(RoleName=role, PolicyName='RevokeOldSessions', PolicyDocument=policy.replace('\n', '').replace(' ', ''))
        event['remediation']['success'] = True
        event['remediation']['title'] = ('GuardDog Successfully Removed all Active Sessions for Role: %s' % role)
        event['remediation']['description'] = 'Please follow your necessary forensic procedures.'
    except ClientError as e:
        print(e)
        print('log -- Error Auto-Remediating Finding')
    return event
