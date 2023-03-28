import boto3
import os
import sys
import traceback
import datetime
import time


def delete_expired_amis(ec2):
    try:
        print('Scanning for AMIs with tags ({})'.format(global_key_to_tag_on))
        amis_to_consider = response = ec2.describe_images(Filters=[{'Name': 'tag-key', 'Values': [global_key_to_tag_on]}], Owners=['self'])['Images']
    except:
        if ('OptInRequired' in str(sys.exc_info())):
            print('  Region not activated for this account, skipping...')
            return
        else:
            raise
    today_date = time.strptime(datetime.datetime.now().strftime('%m-%d-%Y'), '%m-%d-%Y')
    if (len(amis_to_consider) == 0):
        return
    print('  Found {} amis to consider...'.format(len(amis_to_consider)))
    for ami in amis_to_consider:
        print('  Found AMI to consider: {}'.format(ami['ImageId']))
        try:
            delete_after = [t.get('Value') for t in ami['Tags'] if (t['Key'] == 'DeleteAfter')][0]
        except:
            print('Unable to find when to delete this image after, skipping...')
            continue
        print('           Delete After: {}'.format(delete_after))
        delete_date = time.strptime(delete_after, '%m-%d-%Y')
        if (today_date < delete_date):
            print('This item is too new, skipping...')
            continue
        if dry_run:
            print('DRY_RUN, would have deleted ami : {}'.format(ami['ImageId']))
            for snapshot in [i['Ebs']['SnapshotId'] for i in ami['BlockDeviceMappings'] if ('Ebs' in i)]:
                print('DRY_RUN, would have deleted volume snapshot {}'.format(ami['ImageId'], snapshot))
        else:
            print(' === DELETING AMI : {}'.format(ami['ImageId']))
            try:
                amiResponse = ec2.deregister_image(ImageId=ami['ImageId'])
            except Exception as e:
                print('Unable to delete AMI: {}'.format(e))
            for snapshot in [i['Ebs']['SnapshotId'] for i in ami['BlockDeviceMappings'] if ('Ebs' in i)]:
                print(' === DELETING AMI {} SNAPSHOT : {}'.format(ami['ImageId'], snapshot))
                try:
                    result = ec2.delete_snapshot(SnapshotId=snapshot)
                except Exception as e:
                    print('Unable to delete snapshot: {}'.format(e))
