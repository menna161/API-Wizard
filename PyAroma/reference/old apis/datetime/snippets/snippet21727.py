import logging
import os
import time
from datetime import datetime
import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
import libtmux
from box.management.commands.run_box import start_sensor_in_tmux
from box.models import BoxSettings
from box.utils.dir_handling import build_tmp_dir_name
from data.models import TmuxStatus
from data.time_utils import sleep_until_interval_is_complete


def monitor_tmux_windows(tmux_session):
    'Monitor if tmux windows are doing fine. For now, only the sensor, can add others later.'
    box_id = BoxSettings.objects.last().box_id
    timezone = pytz.timezone(settings.TIME_ZONE)
    status = True
    tmux_window = tmux_session.find_where({'window_name': 'sensor'})
    if (tmux_window is None):
        status = False
        logger.info('Cannot find the "sensor" tmux window. Assuming sensor is not running...')
    tmux_pane = tmux_window.list_panes()[0]
    last_message = tmux_pane.cmd('capture-pane', '-p').stdout[(- 1)]
    if (last_message == 'sleeping a bit...'):
        status = False
        logger.info('The sensor seems to be off (process is sleeping and will try again) ...')
    TmuxStatus.objects.update_or_create(box_id=box_id, sensor_status=status, time_stamp=timezone.localize(datetime.now()))
