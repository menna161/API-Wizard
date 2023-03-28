from __future__ import division
import datetime
import logging
import time
from common_util import dict_key_by_value
from i2c_conn import I2CConn
from retrying import retry


def xyz_buffer(self, decimals=4, limit=128, interrupt_timestamp=None):
    '\n        Read out and calculate accelerometer data from FIFO buffer until empty or limit reached.\n        '
    ret = []
    status = self.fifo_status()
    stats = self._stats.setdefault('buffer', {})
    stats['await_readout'] = status['sample_count']
    if status['overflowed']:
        stats['overflow'] = (stats.get('overflow', 0) + 1)
    if status['watermark_reached']:
        stats['watermark'] = (stats.get('watermark', 0) + 1)
    if (interrupt_timestamp == None):
        log.warning('No interrupt timestamp given as reference - uses current timestamp which can give an inaccurate offset')
        interrupt_timestamp = datetime.datetime.utcnow()
    count = 0
    while True:
        res = self.xyz(decimals=decimals, empty_readout=FIFO_EMPTY_XYZ)
        if (not res):
            if DEBUG:
                log.debug('FIFO buffer is empty after {:} XYZ readout(s)'.format(count))
            break
        count += 1
        timestamp = (interrupt_timestamp - datetime.timedelta(milliseconds=(((self._fifo_watermark or 32) - count) * (1000 / self._data_rate))))
        res['_stamp'] = timestamp.isoformat()
        res['_type'] = 'xyz'
        ret.append(res)
        if (limit and (count >= limit)):
            log.warning('FIFO buffer readout limit of {:} reached - this may indicate that more data is being produced than can be handled'.format(limit))
            break
    stats['last_readout'] = count
    stats['total_readout'] = (stats.get('total_readout', 0) + count)
    return ret
