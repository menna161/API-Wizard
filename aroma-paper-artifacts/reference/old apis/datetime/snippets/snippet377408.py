import logging
import datetime
from boto.exception import EC2ResponseError
from automated_ebs_snapshots import volume_manager
from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS


def _ensure_snapshot(connection, volume, force):
    ' Ensure that a given volume has an appropriate snapshot\n\n    :type connection: boto.ec2.connection.EC2Connection\n    :param connection: EC2 connection object\n    :type volume: boto.ec2.volume.Volume\n    :param volume: Volume to check\n    :returns: None\n    '
    if ('AutomatedEBSSnapshots' not in volume.tags):
        logger.warning('Missing tag AutomatedEBSSnapshots for volume {}'.format(volume.id))
        return
    interval = volume.tags['AutomatedEBSSnapshots']
    if (volume.tags['AutomatedEBSSnapshots'] not in VALID_INTERVALS):
        logger.warning('"{}" is not a valid snapshotting interval for volume {}'.format(interval, volume.id))
        return
    snapshots = connection.get_all_snapshots(filters={'volume-id': volume.id})
    if ((not snapshots) or force):
        _create_snapshot(volume)
        return
    min_delta = (((3600 * 24) * 365) * 10)
    for snapshot in snapshots:
        timestamp = datetime.datetime.strptime(snapshot.start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        delta_seconds = int((datetime.datetime.utcnow() - timestamp).total_seconds())
        if (delta_seconds < min_delta):
            min_delta = delta_seconds
    logger.info('The newest snapshot for {} is {} seconds old'.format(volume.id, min_delta))
    if ((interval == 'hourly') and (min_delta > 3600)):
        _create_snapshot(volume)
    elif ((interval == 'daily') and (min_delta > (3600 * 24))):
        _create_snapshot(volume)
    elif ((interval == 'weekly') and (min_delta > ((3600 * 24) * 7))):
        _create_snapshot(volume)
    elif ((interval == 'monthly') and (min_delta > ((3600 * 24) * 30))):
        _create_snapshot(volume)
    elif ((interval == 'yearly') and (min_delta > ((3600 * 24) * 365))):
        _create_snapshot(volume)
    else:
        logger.info('No need for a new snapshot of {}'.format(volume.id))
