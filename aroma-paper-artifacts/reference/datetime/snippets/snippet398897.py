from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from builtins import object
from concurrent import futures
from random import shuffle
import abc
import atexit
import datetime
import logging
import os
import platform
import subprocess
import time
import grpc
import rqd.compiled_proto.report_pb2
import rqd.compiled_proto.report_pb2_grpc
import rqd.compiled_proto.rqd_pb2_grpc
import rqd.rqconstants
import rqd.rqexceptions
import rqd.rqdservicers
import rqd.rqutil


def _serializeChildrenProcs(self):
    ' Collect and serialize children proc stats for protobuf\n            Convert to Kilobytes:\n            * RSS (Resident set size) measured in pages\n            * Statm size measured in pages\n            * Stat size measured in bytes\n\n        :param data: dictionary\n        :return: serialized children proc host stats\n        :rtype: rqd.compiled_proto.report_pb2.ChildrenProcStats\n        '
    childrenProc = rqd.compiled_proto.report_pb2.ChildrenProcStats()
    for (proc, values) in self.childrenProcs.items():
        procStats = rqd.compiled_proto.report_pb2.ProcStats()
        procStatFile = rqd.compiled_proto.report_pb2.Stat()
        procStatmFile = rqd.compiled_proto.report_pb2.Statm()
        procStatFile.pid = proc
        procStatFile.name = (values['name'] if values['name'] else '')
        procStatFile.state = values['state']
        procStatFile.vsize = values['vsize']
        procStatFile.rss = values['rss']
        procStatmFile.size = values['statm_size']
        procStatmFile.rss = values['statm_rss']
        procStats.stat.CopyFrom(procStatFile)
        procStats.statm.CopyFrom(procStatmFile)
        procStats.cmdline = ' '.join(values['cmd_line'])
        startTime = (datetime.datetime.now() - datetime.timedelta(seconds=values['start_time']))
        procStats.start_time = startTime.strftime('%Y-%m-%d %H:%M%S')
        childrenProc.children.extend([procStats])
    return childrenProc
