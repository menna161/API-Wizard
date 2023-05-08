import boto3
import botocore
import sys
import argparse
import subprocess
import shutil
import os
from datetime import datetime
import operator
import distutils.spawn
from pymongo import MongoClient
from pymongo import errors


def create_snapshot(RegionName, volumes_dict):
    dtime = datetime.now()
    client = boto3.client('ec2', region_name=RegionName)
    successful_snapshots = dict()
    for snapshot in volumes_dict:
        try:
            response = client.create_snapshot(Description='Crated by aws-scripts/mongodb_backup.py ', VolumeId=volumes_dict[snapshot], TagSpecifications=[{'ResourceType': 'snapshot', 'Tags': [{'Key': 'aws-scripts:mongodb_backup.py:managed', 'Value': 'true'}, {'Key': 'Name', 'Value': dtime}]}], DryRun=False)
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            snapshot_id = response['SnapshotId']
            if (status_code == 200):
                successful_snapshots[snapshot] = snapshot_id
            else:
                print(('status code: %s' % status_code))
        except Exception as e:
            exception_message = ((((('There was error in creating snapshot ' + snapshot) + ' with volume id ') + volumes_dict[snapshot]) + ' and error is: \n') + str(e))
    if (len(successful_snapshots) == 1):
        print(('  Snapshots: %s ' % successful_snapshots['data']))
        snap_ids = [successful_snapshots['data']]
    if (len(successful_snapshots) == 2):
        print(('  Snapshots: %s, %s ' % (successful_snapshots['data'], successful_snapshots['journal'])))
        snap_ids = [successful_snapshots['data'], successful_snapshots['journal']]
    return snap_ids
