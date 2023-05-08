import boto3
import os
import sys
import traceback
import datetime
import time


def backup_tagged_volumes_in_region(ec2):
    print('Scanning for volumes with tags ({})'.format(','.join(tags_to_find)))
    try:
        volumes = ec2.describe_volumes(Filters=[{'Name': 'tag-key', 'Values': tags_to_find}])
    except:
        if ('OptInRequired' in str(sys.exc_info())):
            print('  Region not activated for this account, skipping...')
            return
        else:
            raise
    volumes_array = []
    for volume in volumes['Volumes']:
        if (volume['State'] in ['available', 'in-use']):
            volumes_array.append(volume)
    if (len(volumes_array) == 0):
        return
    print('  Found {} volumes to backup...'.format(len(volumes_array)))
    for volume in volumes_array:
        print('  Volume ID: {}'.format(volume['VolumeId']))
        try:
            volume_name = [t.get('Value') for t in volume['Tags'] if (t['Key'] == 'Name')][0]
        except:
            volume_name = volume['VolumeId']
        try:
            instance_id = volume['Attachments'][0]['InstanceId']
        except:
            instance_id = 'No attachment'
        print('Volume Name: {}'.format(volume_name))
        print('Instance ID: {}'.format(instance_id))
        try:
            retention_days = [int(t.get('Value')) for t in volume['Tags'] if (t['Key'] == 'Retention')][0]
        except:
            retention_days = default_retention_time
        print('       Time: {} days'.format(retention_days))
        if dry_run:
            print('Backup Name: {}'.format('{}-backup-{}'.format(volume_name, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f'))))
            print('DRY_RUN: Would have created a volume backup...')
        else:
            try:
                delete_fmt = (datetime.date.today() + datetime.timedelta(days=retention_days)).strftime('%m-%d-%Y')
                tags = []
                tags.append({'Key': 'Name', 'Value': '{}-backup-{}'.format(volume_name, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f'))})
                tags.append({'Key': 'DeleteAfter', 'Value': delete_fmt})
                tags.append({'Key': 'OriginalVolumeID', 'Value': volume['VolumeId']})
                tags.append({'Key': global_key_to_tag_on, 'Value': 'true'})
                try:
                    if ('Tags' in volume):
                        for (index, item) in enumerate(volume['Tags']):
                            if item['Key'].startswith('aws:'):
                                print("Modifying internal aws tag so it doesn't fail: {}".format(item['Key']))
                                tags.append({'Key': 'internal-{}'.format(item['Key']), 'Value': item['Value']})
                            elif (item['Key'] == 'Name'):
                                pass
                            else:
                                tags.append(item)
                except:
                    pass
                snapshot = ec2.create_snapshot(Description='Automatic Backup of {} from {}'.format(volume_name, volume['VolumeId']), VolumeId=volume['VolumeId'], TagSpecifications=[{'ResourceType': 'snapshot', 'Tags': tags}])
                print('Snapshot ID: {}'.format(snapshot['SnapshotId']))
            except Exception as e:
                print('Caught exception while trying to process volume')
                pprint(e)
