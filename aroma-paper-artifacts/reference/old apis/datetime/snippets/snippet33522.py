import datetime
import struct
import time
import sys
import os
from six import string_types, PY3
from ._common import tzname_in_python2
from .win import tzwin, tzwinlocal
from dateutil import relativedelta
from dateutil import parser
from dateutil import rrule
from dateutil.zoneinfo import gettz


def __init__(self, fileobj, filename=None):
    file_opened_here = False
    if isinstance(fileobj, string_types):
        self._filename = fileobj
        fileobj = open(fileobj, 'rb')
        file_opened_here = True
    elif (filename is not None):
        self._filename = filename
    elif hasattr(fileobj, 'name'):
        self._filename = fileobj.name
    else:
        self._filename = repr(fileobj)
    try:
        if (fileobj.read(4).decode() != 'TZif'):
            raise ValueError('magic not found')
        fileobj.read(16)
        (ttisgmtcnt, ttisstdcnt, leapcnt, timecnt, typecnt, charcnt) = struct.unpack('>6l', fileobj.read(24))
        if timecnt:
            self._trans_list = struct.unpack(('>%dl' % timecnt), fileobj.read((timecnt * 4)))
        else:
            self._trans_list = []
        if timecnt:
            self._trans_idx = struct.unpack(('>%dB' % timecnt), fileobj.read(timecnt))
        else:
            self._trans_idx = []
        ttinfo = []
        for i in range(typecnt):
            ttinfo.append(struct.unpack('>lbb', fileobj.read(6)))
        abbr = fileobj.read(charcnt).decode()
        if leapcnt:
            leap = struct.unpack(('>%dl' % (leapcnt * 2)), fileobj.read((leapcnt * 8)))
        if ttisstdcnt:
            isstd = struct.unpack(('>%db' % ttisstdcnt), fileobj.read(ttisstdcnt))
        if ttisgmtcnt:
            isgmt = struct.unpack(('>%db' % ttisgmtcnt), fileobj.read(ttisgmtcnt))
    finally:
        if file_opened_here:
            fileobj.close()
    self._ttinfo_list = []
    for i in range(typecnt):
        (gmtoff, isdst, abbrind) = ttinfo[i]
        gmtoff = (((gmtoff + 30) // 60) * 60)
        tti = _ttinfo()
        tti.offset = gmtoff
        tti.delta = datetime.timedelta(seconds=gmtoff)
        tti.isdst = isdst
        tti.abbr = abbr[abbrind:abbr.find('\x00', abbrind)]
        tti.isstd = ((ttisstdcnt > i) and (isstd[i] != 0))
        tti.isgmt = ((ttisgmtcnt > i) and (isgmt[i] != 0))
        self._ttinfo_list.append(tti)
    trans_idx = []
    for idx in self._trans_idx:
        trans_idx.append(self._ttinfo_list[idx])
    self._trans_idx = tuple(trans_idx)
    self._ttinfo_std = None
    self._ttinfo_dst = None
    self._ttinfo_before = None
    if self._ttinfo_list:
        if (not self._trans_list):
            self._ttinfo_std = self._ttinfo_first = self._ttinfo_list[0]
        else:
            for i in range((timecnt - 1), (- 1), (- 1)):
                tti = self._trans_idx[i]
                if ((not self._ttinfo_std) and (not tti.isdst)):
                    self._ttinfo_std = tti
                elif ((not self._ttinfo_dst) and tti.isdst):
                    self._ttinfo_dst = tti
                if (self._ttinfo_std and self._ttinfo_dst):
                    break
            else:
                if (self._ttinfo_dst and (not self._ttinfo_std)):
                    self._ttinfo_std = self._ttinfo_dst
            for tti in self._ttinfo_list:
                if (not tti.isdst):
                    self._ttinfo_before = tti
                    break
            else:
                self._ttinfo_before = self._ttinfo_list[0]
    laststdoffset = 0
    self._trans_list = list(self._trans_list)
    for i in range(len(self._trans_list)):
        tti = self._trans_idx[i]
        if (not tti.isdst):
            self._trans_list[i] += tti.offset
            laststdoffset = tti.offset
        else:
            self._trans_list[i] += laststdoffset
    self._trans_list = tuple(self._trans_list)
