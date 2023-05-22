import boto3
import os
import sys
import traceback
import datetime
import time


def backup_tagged_instances_in_region(ec2):
    print('Scanning for instances with tags ({})'.format(','.join(tags_to_find)))
    try:
        reservations = ec2.describe_instances(Filters=[{'Name': 'tag-key', 'Values': tags_to_find}])['Reservations']
    except:
        if ('OptInRequired' in str(sys.exc_info())):
            print('  Region not activated for this account, skipping...')
            return
        else:
            raise
    instance_reservations = [[i for i in r['Instances']] for r in reservations]
    instances = []
    for instance_reservation in instance_reservations:
        for this_instance in instance_reservation:
            if (this_instance['State']['Name'] != 'terminated'):
                instances.append(this_instance)
    if (len(instances) == 0):
        return
    print('  Found {} instances to backup...'.format(len(instances)))
    for instance in instances:
        print('  Instance: {}'.format(instance['InstanceId']))
        try:
            instance_name = [t.get('Value') for t in instance['Tags'] if (t['Key'] == 'Name')][0]
        except:
            instance_name = instance['InstanceId']
        print('      Name: {}'.format(instance_name))
        try:
            retention_days = [int(t.get('Value')) for t in instance['Tags'] if (t['Key'] == 'Retention')][0]
        except:
            retention_days = default_retention_time
        print('      Time: {} days'.format(retention_days))
        if dry_run:
            print('DRY_RUN: Would have created an AMI...')
            print('   InstanceId : {}'.format(instance['InstanceId']))
            print('   Name       : {}'.format('{}-backup-{}'.format(instance_name, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f'))))
        else:
            try:
                image = ec2.create_image(InstanceId=instance['InstanceId'], Name='{}-backup-{}'.format(instance_name, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')), Description='Automatic Backup of {} from {}'.format(instance_name, instance['InstanceId']), NoReboot=True, DryRun=False)
                print('       AMI: {}'.format(image['ImageId']))
                delete_fmt = (datetime.date.today() + datetime.timedelta(days=retention_days)).strftime('%m-%d-%Y')
                instance['Tags'].append({'Key': 'DeleteAfter', 'Value': delete_fmt})
                instance['Tags'].append({'Key': 'OriginalInstanceID', 'Value': instance['InstanceId']})
                instance['Tags'].append({'Key': global_key_to_tag_on, 'Value': 'true'})
                finaltags = []
                for (index, item) in enumerate(instance['Tags']):
                    if item['Key'].startswith('aws:'):
                        print("Modifying internal aws tag so it doesn't fail: {}".format(item['Key']))
                        finaltags.append({'Key': 'internal-{}'.format(item['Key']), 'Value': item['Value']})
                    else:
                        finaltags.append(item)
                response = ec2.create_tags(Resources=[image['ImageId']], Tags=finaltags)
            except:
                print('Failure trying to create image or tag image.  See/report exception below')
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
