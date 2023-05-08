from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import map
import datetime
import re
import os
from datetime import datetime
import time
import socket
import signal
import yaml
from qtpy import QtGui
from qtpy import QtCore
from qtpy import QtWidgets
import opencue.wrappers.frame
import cuegui.AbstractDockWidget
import cuegui.AbstractTreeWidget
import cuegui.AbstractWidgetItem
import cuegui.Action
import cuegui.Constants
import cuegui.JobMonitorTree
import cuegui.Logger
import cuegui.MenuActions
import cuegui.Style
import cuegui.Utils


def getBuildTimes(self, job, layers=None):
    'Return a dictionary with layer names as keys, and build tiems as\n         values.\n         '
    results = {}
    if (not layers):
        layers = job.getLayers()
    for layer in layers:
        if isinstance(layer, str):
            layer = job.getLayer(layer)
        if ('preprocess' in layer.name()):
            continue
        built_frames = []
        cores = 0
        cores_list = []
        fs = opencue.search.FrameSearch()
        fs.states = [opencue.wrappers.frame.Frame().FrameState(3)]
        frames = layer.getFrames(fs)
        if (not frames):
            fs.states = [opencue.wrappers.frame.Frame().FrameState(2)]
            frames = layer.getFrames(fs)
        for frame in frames:
            frame_cores = float(frame.lastResource.split('/')[1])
            if (frame_cores != cores):
                if (frame_cores not in cores_list):
                    built_frames.append((frame, frame_cores))
                    cores_list.append(frame_cores)
        build_times = []
        for (frame, cores) in built_frames:
            log_lines = self.getLog(job, frame)
            for line in log_lines:
                if ('[kat] Building scene done.' in line):
                    line = line.replace('[INFO BatchMain]:  ', '')
                    build_time = line.split()[0]
                    (hours, minutes, seconds) = build_time.split(':')
                    seconds = int(seconds)
                    seconds += (int(minutes) * 60)
                    seconds += (int(hours) * 360)
                    build_times.append(seconds)
            if build_times:
                avg = (sum(build_times) / len(build_times))
                seconds = int((avg % 60))
                minutes = int(((avg / 60) % 60))
                hours = int((avg / 3600))
                results[layer.name()] = (layer, datetime.time(hours, minutes, seconds))
    return results
