from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import object
import datetime
import logging
import os
import platform
import random
import signal
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import rqd.compiled_proto.host_pb2
import rqd.compiled_proto.report_pb2
import rqd.rqconstants
import rqd.rqexceptions
import rqd.rqmachine
import rqd.rqnetwork
import rqd.rqnimby
import rqd.rqutil


def __writeFooter(self):
    "Writes frame's log footer"
    self.endTime = time.time()
    self.frameInfo.runTime = int((self.endTime - self.startTime))
    try:
        print('', file=self.rqlog)
        print(('=' * 59), file=self.rqlog)
        print('RenderQ Job Complete\n', file=self.rqlog)
        print(('%-20s%s' % ('exitStatus', self.frameInfo.exitStatus)), file=self.rqlog)
        print(('%-20s%s' % ('exitSignal', self.frameInfo.exitSignal)), file=self.rqlog)
        if self.frameInfo.killMessage:
            print(('%-20s%s' % ('killMessage', self.frameInfo.killMessage)), file=self.rqlog)
        print(('%-20s%s' % ('startTime', time.ctime(self.startTime))), file=self.rqlog)
        print(('%-20s%s' % ('endTime', time.ctime(self.endTime))), file=self.rqlog)
        print(('%-20s%s' % ('maxrss', self.frameInfo.maxRss)), file=self.rqlog)
        print(('%-20s%s' % ('maxUsedGpuMemory', self.frameInfo.maxUsedGpuMemory)), file=self.rqlog)
        print(('%-20s%s' % ('utime', self.frameInfo.utime)), file=self.rqlog)
        print(('%-20s%s' % ('stime', self.frameInfo.stime)), file=self.rqlog)
        print(('%-20s%s' % ('renderhost', self.rqCore.machine.getHostname())), file=self.rqlog)
        print(('%-20s%s' % ('maxrss (KB)', self.frameInfo.maxRss)), file=self.rqlog)
        for child in sorted(self.frameInfo.childrenProcs.items(), key=(lambda item: item[1]['start_time'])):
            print(('\t%-20s%s' % (child[1]['name'], child[1]['rss'])), file=self.rqlog)
            print(('\t%-20s%s' % ('start_time', datetime.timedelta(seconds=child[1]['start_time']))), file=self.rqlog)
            print(('\t%-20s%s' % ('cmdline', ' '.join(child[1]['cmd_line']))), file=self.rqlog)
        print(('=' * 59), file=self.rqlog)
    except Exception as e:
        log.critical('Unable to write footer: %s due to %s at %s', self.runFrame.log_dir_file, e, traceback.extract_tb(sys.exc_info()[2]))
