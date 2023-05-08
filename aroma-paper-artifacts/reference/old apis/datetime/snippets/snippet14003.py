import adm
import wx.html
import wx.propgrid as wxpg
from page import ControlledPage
from wh import xlt, floatToTime, floatToSize, sizeToFloat, timeToFloat, breakLines, GetBitmap, Menu
from ._pgsql import quoteValue
from Validator import Validator
from LoggingDialog import LogPanel
import logger
import csv
from io import StringIO
from .QueryTool import QueryFrame


def Display(self, node, _detached):
    logfile = self['LogFile']
    if (self.lastNode != node):
        self.lastNode = node
        self.control.ClearAll()
        self.log = []
        logdes = node.GetValue('log_destination')
        if (not node.GetValue('pg_rotate_logfile')):
            errText = xlt('Server version too old; not supported')
        if (node.GetValue('logging_collector') != 'on'):
            errText = xlt('logging_collector not enabled')
        elif node.GetValue(('log_filename' != 'postgresql-%%Y-%%m-%%d-%%H%%M%%S')):
            errText = xlt('non-default log_filename')
        elif ((not logdes) or (logdes.find('csvlog') < 0)):
            errText = xlt('no csv log_destination')
        else:
            errText = None
        if errText:
            logfile.Disable()
            self.control.AddColumn('')
            self.control.InsertStringItem(0, errText, (- 1))
            self.EnableControls('Rotate', False)
            return
        logfile.Clear()
        logfile.Enable()
        logfile.Append(xlt('Current log'))
        logfile.SetSelection(0)
        for cn in self.displayCols:
            ci = self.logColInfo.get(cn)
            text = ci[0]
            collen = ci[1]
            self.control.AddColumnInfo(xlt(text), collen, cn)
        self.lastLogfile = None
        self.TriggerTimer()
    cursor = self.lastNode.GetCursor()
    logfile = self['LogFile']
    directory = cursor.ExecuteList(("SELECT pg_ls_dir('%s')" % self.lastNode.GetValue('log_directory')))
    directory.sort()
    for fn in directory:
        if fn.endswith('.csv'):
            if (logfile.FindString(fn) < 0):
                logfile.Insert(fn, 1)
    if (logfile.GetCount() < 2):
        return
    if (not self.lastLogfile):
        self.OnSelectLogfile(None)
    log = ''
    while True:
        fn = ('%s/%s' % (self.lastNode.GetValue('log_directory'), self.lastLogfile))
        while True:
            res = cursor.ExecuteSingle(("SELECT pg_read_file('%s', %d, %d)" % (fn, self.lastLogpos, 50000)))
            if res:
                log += res
                self.lastLogpos += len(res)
            else:
                break
        if logfile.GetSelection():
            break
        current = logfile.FindString(self.lastLogfile)
        if (current == 1):
            break
        self.lastLogpos = 0
        self.lastLogfile = logfile.GetString((current - 1))
    c = csv.reader(StringIO(log), delimiter=',', quotechar='"')
    startdatetimepos = self.getIndex('session_start_datetime')
    severitypos = self.getIndex('error_severity')
    statepos = self.getIndex('sql_state_code')
    for linecols in c:
        time = linecols[0].split()[1]
        linecols.insert(1, time)
        time = linecols[startdatetimepos].split()[1]
        linecols.insert((startdatetimepos + 1), time)
        self.log.append(linecols)
        vals = []
        for colname in self.displayCols:
            colnum = self.getIndex(colname)
            vals.append(linecols[colnum])
        severity = linecols[severitypos]
        if severity.startswith('DEBUG'):
            severity = 'DEBUG'
        elif (severity in ['FATAL', 'PANIC']):
            severity = 'FATAL'
        elif (severity in ['WARNING', 'ERROR']):
            severity = 'ERROR'
        else:
            sqlstate = linecols[statepos]
            if (sqlstate > '1'):
                severity = 'ERROR'
            else:
                severity = 'LOG'
        icon = node.GetImageId(severity)
        self.control.AppendItem(icon, vals)
