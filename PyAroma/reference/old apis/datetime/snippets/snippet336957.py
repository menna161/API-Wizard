import datetime
import filecmp
import os
import time
from framework.utils.reporterutils.LoggingUtil import LoggingController


def get_LatestFile(self):
    pro_path = self.get_project_path()
    rpath = 'TestResult\\Reports'
    result_dir = os.path.join(pro_path, rpath)
    l = os.listdir(result_dir)
    st = l.sort(key=(lambda fn: (os.path.getmtime(((result_dir + '\\') + fn)) if (not os.path.isdir(((result_dir + '\\') + fn))) else 0)))
    d = datetime.datetime.fromtimestamp(os.path.getmtime(((result_dir + '\\') + l[(- 1)])))
    fname = l[(- 1)]
    fpath = os.path.join(result_dir, fname)
    self.__logger.debug(('last file is ::' + fpath))
    time_end = time.mktime(d.timetuple())
    self.__logger.debug(('time_end:%s' % time_end))
    return (fpath, fname, result_dir)
