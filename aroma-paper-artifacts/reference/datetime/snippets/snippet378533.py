import datetime
import logging
import salt.exceptions
import salt.utils.event
import salt.utils.jid
import time
from retrying import retry
from salt.utils.network import host_to_ips as _host_to_ips
from salt.utils.network import remote_port_tcp as _remote_port_tcp


def update_release(force=False, dry_run=False, only_retry=False):
    "\n    Update a minion to newest release by running a highstate if not already up-to-date.\n\n    Optional arguments:\n      - force (bool): Default is 'False'.\n      - dry_run (bool): Default is 'False'.\n      - only_retry (bool): Default is 'False'.\n    "
    old = __salt__['grains.get']('release', default={'id': None, 'state': None})
    if (not ('state' in old)):
        old['state'] = None
    new = {'id': __salt__['pillar.get']('latest_release_id'), 'state': None}
    if ((old['state'] == 'updated') and (old['id'] == new['id'])):
        if force:
            new['state'] = 'forcing'
        else:
            new['state'] = 'updated'
            log.info("Current release '{:}' is the latest and already updated".format(old['id']))
    else:
        if (old['state'] in ['pending', 'forcing', 'retrying', 'failed']):
            new['state'] = 'retrying'
        else:
            new['state'] = 'pending'
        log.info("Release '{:}' is pending for update".format(new['id']))
    ret = {'release': {'old': old, 'new': new}}
    if dry_run:
        return ret
    if (only_retry and (new['state'] != 'retrying')):
        if log.isEnabledFor(logging.DEBUG):
            log.debug('No failed update is pending for retry')
        return ret
    if (new['state'] in ['pending', 'forcing', 'retrying']):
        if __salt__['saltutil.is_running']('minionutil.update_release'):
            raise salt.exceptions.CommandExecutionError('Update is already running - please wait and try again later')
        if __salt__['saltutil.is_running']('state.*'):
            raise salt.exceptions.CommandExecutionError('Another state run is currently active - please wait and try again later')
        try:
            res = __salt__['schedule.disable']()
            if (not res.get('result', False)):
                log.error('Unable to disable schedule: {:}'.format(res))
            if __salt__['pillar.get']('update_release:pause_workers', default=False):
                try:
                    __salt__['obd.manage']('worker', 'pause', '*')
                except:
                    log.exception('Failed to pause all OBD workers before update')
                try:
                    __salt__['obd.file_export'](run=False)
                except:
                    log.exception('Failed to stop OBD exporter before update')
                try:
                    __salt__['acc.manage']('worker', 'pause', '*')
                except:
                    log.exception('Failed to pause all accelerometer workers before update')
            if (new['state'] == 'pending'):
                log.info("Updating release '{:}' => '{:}'".format(old['id'], new['id']))
            else:
                log.warn("{:} update of release '{:}' => '{:}'".format(new['state'].title(), old['id'], new['id']))
            res = __salt__['grains.setval']('release', new, destructive=True)
            if (not res):
                log.error("Failed to store {:} release '{:}' in grains data".format(new['state'], new['id']))
            trigger_event('system/release/{:}'.format(new['state']), data={'id': new['id']})
            try:
                __salt__['cmd.run']('wall -n "\nATTENTION ({:}):\n\nUpdate release initiated in state \'{:}\'.\nPlease do not power off the device until the update is completed.\n\n(Press ENTER to continue)"'.format(datetime.datetime.utcnow(), new['state']))
            except:
                log.exception('Failed to broadcast update release initiated notification')
            res = __salt__['saltutil.sync_all'](refresh=False)
            ret['dynamic'] = res
            res = __salt__['state.highstate']()
            if (not isinstance(res, dict)):
                raise salt.exceptions.CommandExecutionError('Failed to run highstate: {:}'.format(res))
            ret['highstate'] = res
            new['id'] = __salt__['pillar.get']('latest_release_id')
            if all((v.get('result', False) for (k, v) in ret['highstate'].iteritems())):
                log.info("Completed highstate for release '{:}'".format(new['id']))
                new['state'] = 'updated'
            else:
                log.warn("Unable to complete highstate for release '{:}'".format(new['id']))
                new['state'] = 'failed'
            res = __salt__['grains.setval']('release', new, destructive=True)
            if (not res):
                log.error("Failed to store {:} release '{:}' in grains data".format(new['state'], new['id']))
            trigger_event('system/release/{:}'.format(new['state']), data={'id': new['id']})
            try:
                __salt__['cmd.run']('wall -n "\nATTENTION ({:}):\n\nUpdate release completed in state \'{:}\'.\n\n(Press ENTER to continue)"'.format(datetime.datetime.utcnow(), new['state']))
            except:
                log.exception('Failed to broadcast update release completed notification')
        finally:
            res = __salt__['schedule.enable']()
            if (not res.get('result', False)):
                log.error('Unable to re-enable schedule: {:}'.format(res))
            if __salt__['pillar.get']('update_release:pause_workers', default=False):
                try:
                    __salt__['obd.manage']('worker', 'resume', '*')
                except:
                    log.exception('Failed to resume all OBD workers after update')
                try:
                    __salt__['acc.manage']('worker', 'resume', '*')
                except:
                    log.exception('Failed to resume all accelerometer workers after update')
    return ret
