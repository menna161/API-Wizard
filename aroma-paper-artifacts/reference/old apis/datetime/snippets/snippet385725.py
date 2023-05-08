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


def main():
    parser = argparse.ArgumentParser(description='A tool to make mongodb backups on Amazon')
    parser.add_argument('-m', '--method', help='Backup method. Dump if none is provided', choices=['dump', 'snapshot'], default='dump')
    parser.add_argument('-u', '--user', help='Mongodb user (optional)')
    parser.add_argument('-p', '--password', help='Mongodb password (optional)')
    parser.add_argument('-H', '--host', default='localhost:27017', help='Mongodb host: <hostname>:<port>. By default: localhost:27017')
    parser.add_argument('-d', '--database', help='For the dump method: The database to backup (all if not provided)')
    parser.add_argument('-c', '--collection', help="For the dump method: The collection to backup. Requires '-d' option")
    parser.add_argument('-e', '--exclude_collection', help="For the dump method: The collection to exclude from backup. Requires '-d' option")
    parser.add_argument('-o', '--out', default='dump', help='For the dump method: The output directory for dumped files')
    parser.add_argument('-n', '--number', type=int, default=7, help='Number of copies to retain')
    parser.add_argument('-b', '--bucket', help='For the dump method: Amazon s3 bucket.')
    parser.add_argument('-P', '--prefix', help='For the dump method: For grouped objects aka s3 folders, provide the prefix key')
    parser.add_argument('-v', '--volume_id', nargs='+', type=str, help='For the snapshot method: Provide the data and journal volume_id list to snapshot: If data and journal resides in a separate volumes, both volumes are required.')
    parser.add_argument('--no_journal', action='store_true', help='For the snapshot method: If pressent,  the instance is either running without journaling or has the journal files on a separate volume, you must flush all writes to disk and lock the database to prevent writes during the backup process.')
    parser.add_argument('-r', '--region', help='Specify an alternate region to override                               the one defined in the .aws/credentials file')
    arg = parser.parse_args()
    if (arg.user and (not arg.password)):
        parser.error('You provided a user but not a password')
    if (arg.password and (not arg.user)):
        parser.error('You provided a password but not a user')
    if ((arg.prefix is not None) and (arg.prefix[(- 1):] == '/')):
        arg.prefix = ('%s' % arg.prefix[:(- 1)])
    if (arg.exclude_collection and (not arg.database)):
        parser.error('--exclude_collection requires --database')
    if (arg.collection and (not arg.database)):
        parser.error('--collection requires --database')
    if arg.region:
        client = boto3.client('ec2')
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
        if (arg.region not in regions):
            sys.exit('ERROR: Please, choose a valid region.')
    if (arg.method == 'dump'):
        print('Method: dump')
        mongodump_path = distutils.spawn.find_executable('mongodump')
        if (mongodump_path is not None):
            print(('mongodump path: %s' % mongodump_path))
        else:
            print('mongodump path: not found!')
            sys.exit(1)
        dump(arg.host, arg.database, arg.collection, arg.exclude_collection, arg.user, arg.password, arg.out)
        s3 = boto3.resource('s3')
        if arg.prefix:
            objects = s3.Bucket(name=arg.bucket).objects.filter(Prefix=arg.prefix)
        else:
            objects = s3.Bucket(name=arg.bucket).objects.filter()
        print('Filelist on the S3 bucket:')
        filedict = {}
        for object in objects:
            if object.key.startswith(((arg.prefix + '/dump-') + arg.database)):
                print(object.key)
                filedict.update({object.key: object.last_modified})
        print('Creating the tarball:')
        tarball_name = ('%s-%s.tar.gz' % (arg.out, datetime.strftime(datetime.now(), '%Y-%m-%d-%H%M%S')))
        tarball_cmd = ('tar -czvf %s %s' % (tarball_name, arg.out))
        tarball_output = subprocess.check_output(tarball_cmd, shell=True)
        print(tarball_output)
        print('Removing temporary dump files...')
        shutil.rmtree(arg.out)
        remote_file = ('%s/%s' % (arg.prefix, os.path.basename(tarball_name)))
        print(('Uploading %s to Amazon S3...' % tarball_name))
        s3_client = boto3.client('s3')
        s3.meta.client.upload_file(tarball_name, arg.bucket, remote_file)
        print('Removing temporary local tarball...')
        os.remove(tarball_name)
        prefix = (arg.prefix + '/')
        sorted_filedict = sorted(list(filedict.items()), key=operator.itemgetter(1))
        for item in sorted_filedict[0:(len(sorted_filedict) - arg.number)]:
            print(('Deleting file from S3: %s' % item[0]))
            object = s3.Object(arg.bucket, item[0]).delete()
    if (arg.method == 'snapshot'):
        print('Method: EBS snapshot')
        if ((arg.method == 'snapshot') and (not arg.volume_id)):
            parser.error('The snapshot method requires --volume_id')
        if (len(arg.volume_id) == 1):
            fsyncLock = False
            if (not arg.volume_id[0].startswith('vol-')):
                parser.error('Incorrent volume_id')
            volumes_dict = {'data': arg.volume_id[0]}
            if (arg.no_journal is not None):
                fsyncLock = arg.no_journal
            if (fsyncLock == True):
                print(('  fsyncLock: %s' % fsyncLock))
                if (arg.user and (not arg.password)):
                    parser.error('You provided a user but not a password')
                if (arg.password and (not arg.user)):
                    parser.error('You provided a password but not a user')
            else:
                print(('  fsyncLock: %s' % fsyncLock))
            print(('  Volume: %s' % arg.volume_id[0]))
        if (len(arg.volume_id) == 2):
            if (arg.user and (not arg.password)):
                parser.error('You provided a user but not a password')
            if (arg.password and (not arg.user)):
                parser.error('You provided a password but not a user')
            if ((not arg.volume_id[0].startswith('vol-')) or (not arg.volume_id[1].startswith('vol-'))):
                parser.error('Incorrent volume_id')
            volumes_dict = {'data': arg.volume_id[0], 'journal': arg.volume_id[1]}
            fsyncLock = True
            print(('  fsyncLock: %s' % fsyncLock))
            print(('  Volumes: %s, %s' % (arg.volume_id[0], arg.volume_id[1])))
        if (fsyncLock == True):
            try:
                lockres = fsync('lock', arg.host, arg.user, arg.password)
                print(('  Lock result: %s' % lockres))
            except Exception as e:
                print(('  An error ocurred: %s' % e))
        snapshots = create_snapshot(arg.region, volumes_dict)
        print(('  waiting for %s to complete' % snapshots))
        try:
            client = boto3.client('ec2', region_name=arg.region)
            waiter = client.get_waiter('snapshot_completed')
            waiter.wait(SnapshotIds=snapshots)
        except botocore.exceptions.WaiterError as e:
            print(e.message)
        try:
            lockres = fsync('unlock', arg.host, arg.user, arg.password)
            print(('  Lock result: %s' % lockres))
        except Exception as e:
            print(('  An error ocurred: %s' % e))
