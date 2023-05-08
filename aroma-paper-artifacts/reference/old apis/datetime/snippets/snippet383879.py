import boto3
import os
import sys
import traceback
import datetime
import time


def delete_expired_snapshots(ec2):
    try:
        print('Scanning for snapshots with tags ({})'.format(global_key_to_tag_on))
        snapshots_to_consider = response = ec2.describe_snapshots(Filters=[{'Name': 'tag-key', 'Values': [global_key_to_tag_on]}])['Snapshots']
    except:
        if ('OptInRequired' in str(sys.exc_info())):
            print('  Region not activated for this account, skipping...')
            return
        else:
            raise
    today_date = time.strptime(datetime.datetime.now().strftime('%m-%d-%Y'), '%m-%d-%Y')
    if (len(snapshots_to_consider) == 0):
        return
    print('  Found {} snapshots to consider...'.format(len(snapshots_to_consider)))
    for snapshot in snapshots_to_consider:
        print('  Found snapshot to consider: {}'.format(snapshot['SnapshotId']))
        print('                  For Volume: {}'.format(snapshot['VolumeId']))
        try:
            delete_after = [t.get('Value') for t in snapshot['Tags'] if (t['Key'] == 'DeleteAfter')][0]
        except:
            print('Unable to find when to delete this image after, skipping...')
            continue
        print('                Delete After: {}'.format(delete_after))
        delete_date = time.strptime(delete_after, '%m-%d-%Y')
        if (today_date < delete_date):
            print('This item is too new, skipping...')
            continue
        if dry_run:
            print('DRY_RUN, would have deleted snapshot : {}'.format(snapshot['SnapshotId']))
        else:
            print('       === DELETING SNAPSHOT: {}'.format(snapshot['SnapshotId']))
            try:
                deleteSnapshotResponse = ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            except Exception as e:
                print('Unable to delete snapshot: {}'.format(e))
