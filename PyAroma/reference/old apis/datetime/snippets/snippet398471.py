from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import map
import datetime
import re
import weakref
from qtpy import QtGui
from qtpy import QtCore
from qtpy import QtWidgets
import opencue
import cuegui.AbstractDockWidget
import cuegui.Action
import cuegui.Constants
import cuegui.JobMonitorTree
import cuegui.Logger
import cuegui.Utils


def restoreJobIds(self, jobIds):
    'Restore monitored jobs from previous saved state\n        Only load jobs that have a timestamp less than or equal to the time a job lives on the farm\n        (jobs are moved to historical database)\n\n        :param jobIds: monitored jobs ids and their timestamp from previous working state\n                       (loaded from config.ini file)\n                       ex: [("Job.f156be87-987a-48b9-b9da-774cd58674a3", 1612482716.170947),...\n        :type jobIds: list[tuples]\n        '
    today = datetime.datetime.now()
    limit = (JOB_RESTORE_THRESHOLD_LIMIT if (len(jobIds) > JOB_RESTORE_THRESHOLD_LIMIT) else len(jobIds))
    msg = 'Unable to load previously loaded job since it was moved to the historical database: {0}'
    try:
        for (jobId, timestamp) in jobIds[:limit]:
            loggedTime = datetime.datetime.fromtimestamp(timestamp)
            if ((today - loggedTime).days <= JOB_RESTORE_THRESHOLD_DAYS):
                try:
                    self.jobMonitor.addJob(jobId, timestamp)
                except opencue.EntityNotFoundException:
                    logger.info(msg, jobId)
    except ValueError:
        for jobId in jobIds[:limit]:
            try:
                self.jobMonitor.addJob(jobId)
            except opencue.EntityNotFoundException:
                logger.info(msg, jobId)
