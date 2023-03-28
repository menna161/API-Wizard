from oom import *
from oom.decode import get_hexstr, mod_id
from datetime import datetime
import sys


def iop(port, fileflag):
    if (port.port_type == 0):
        return
    vendor_name = oom_get_keyvalue(port, 'VENDOR_NAME').replace(' ', '_')[0:8]
    outfilename = (vendor_name + '_')
    vendor_sn = oom_get_keyvalue(port, 'VENDOR_SN').replace(' ', '_')
    outfilename += (vendor_sn + '_EEPROMdecode_')
    dt = datetime.now()
    dateformat = '%Y%m%d%H%M%S'
    timestr = dt.strftime(dateformat)
    outfilename += (timestr + '.txt')
    if (fileflag == '-f'):
        sys.stdout = open(outfilename, 'w+')
    print('')
    print(('Port: %s' % port.port_name))
    print(('%s %s module' % (oom_get_keyvalue(port, 'VENDOR_NAME'), mod_id(port.port_type))))
    print(('Part Number: %s  Serial Number: %s' % (oom_get_keyvalue(port, 'VENDOR_PN'), oom_get_keyvalue(port, 'VENDOR_SN'))))
    print(outfilename)
    print('')
    keys = port.fmap['SERIAL_ID']
    print('SERIAL_ID Keys:')
    for key in sorted(keys):
        val = oom_get_keyvalue(port, key)
        decoder = port.mmap[key][1]
        if ((decoder == 'get_bytes') or (decoder == 'get_cablespec')):
            valstr = get_hexstr(val)
        else:
            valstr = str(val)
        print(('%s: %s' % (key, valstr)))
    print('')
    vend_specific = ''
    if ((port.port_type == 3) or (port.port_type == 11)):
        vend_specific = get_hexstr(oom_get_keyvalue(port, 'VENDOR_SPECIFIC_96'))
    if ((port.port_type == 13) or (port.port_type == 17)):
        vend_specific = get_hexstr(oom_get_keyvalue(port, 'VENDOR_SPECIFIC_224'))
    print(('Vendor Specific: ' + vend_specific))
    print('')
    if ((port.port_type == 3) or (port.port_type == 11)):
        print('I2C Address A0h, bytes 0-127, in hex')
        print_block_hex(oom_get_memory_sff(port, 160, 0, 0, 128), 0)
        print('')
        print('I2C Address A2h, bytes 0-127, in hex')
        print_block_hex(oom_get_memory_sff(port, 162, 0, 0, 128), 0)
    if ((port.port_type == 13) or (port.port_type == 17)):
        print('I2C Address A0h, bytes 0-127, in hex')
        print_block_hex(oom_get_memory_sff(port, 160, 0, 0, 128), 0)
        print('')
        print('I2C Address A0h, page 0, bytes 128-255, in hex')
        print_block_hex(oom_get_memory_sff(port, 160, 0, 128, 128), 0)
    keys = port.mmap
    print('All Keys:')
    print('')
    for key in sorted(keys):
        val = oom_get_keyvalue(port, key)
        decoder = port.mmap[key][1]
        if ((decoder == 'get_bytes') or (decoder == 'get_cablespec')):
            valstr = get_hexstr(val)
        else:
            valstr = str(val)
        print(('%s: %s' % (key, valstr)))
