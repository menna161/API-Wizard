import numpy as np
from os import path, remove, walk, makedirs
from ftplib import FTP
from datetime import date, timedelta
from gzip import GzipFile
import time as pytime
from .utils import print_error_grace
from ..ggclasses.class_GSM import GSM


def parse_gsm_file(filename, lmax):
    "\n    Parse the GRACE GSM Level-2 file.\n\n    Usage: \n    info,cilm,cilm_std = parse_gsm_file(filename,lmax)\n\n    Inputs:\n    filename -> [str] filename of the GRACE GSM solution;\n    lmax -> [int] the maximum degree to read; \n        \n    Outputs:\n    info -> [dictionary] detailed information for GRACE GSM solutions\n    cilm -> [float array] Dimensionless SHCs with shape of (2, lmax + 1, lmax + 1);\n    cilm_std -> [float array] Dimensionless SHCs stds with shape of (2, lmax + 1, lmax + 1)\n        \n    Examples:\n    >>> info,cilm,cilm_std = parse_gsm_file('GFZ/RL06_96/GSM-2_2016221-2016247_GRAC_GFZOP_BB01_0600',179)\n    >>> info,cilm,cilm_std = parse_gsm_file('JPL/RL06_60/GSM-2_2003060-2003090_GRAC_JPLEM_BA01_0600',30) \n    "
    info = {'degree_order': lmax}
    with open(filename, 'r', errors='ignore') as f:
        for line in f:
            if ('# End of YAML header' in line):
                break
            words = [word.strip() for word in line.split(':')]
            if (words[0] == 'degree'):
                info['max_degree'] = int(words[1])
            elif (words[0] == 'order'):
                info['max_order'] = int(words[1])
            elif (words[0] == 'normalization'):
                info['normalization'] = words[1]
            elif (words[0] == 'permanent_tide_flag'):
                info['permanent_tide'] = words[1].split()[0]
            elif (words[0] == 'value'):
                if ((words[1] == '3.9860044150E+14') or (words[1] == '3.9860044150e+14')):
                    info['earth_gravity_param'] = (words[1] + ' m3/s2')
                elif ((words[1] == '6.3781363000E+06') or (words[1] == '6.3781363000e+06')):
                    info['mean_equator_radius'] = (words[1] + ' m')
                    info['background_gravity'] = 'GGM05C'
                elif ((words[1] == '6.3781364600E+06') or (words[1] == '6.3781364600e+06')):
                    info['mean_equator_radius'] = (words[1] + ' m')
                    info['background_gravity'] = 'EIGEN-6C4'
                else:
                    raise Exception('unknown background gravity model')
            elif (words[0] == 'title'):
                info['title'] = words[1]
            elif (words[0] == 'summary'):
                info['summary'] = words[1]
            elif (words[0] == 'institution'):
                info['institution'] = words[1]
            elif (words[0] == 'processing_level'):
                info['processing_level'] = words[1]
            elif (words[0] == 'product_version'):
                info['product_version'] = words[1]
            elif (words[0] == 'time_coverage_start'):
                info['time_coverage_start'] = ((((words[1] + ':') + words[2]) + ':') + words[3])
            elif (words[0] == 'time_coverage_end'):
                info['time_coverage_end'] = ((((words[1] + ':') + words[2]) + ':') + words[3])
            elif (words[0] == 'unused_days'):
                info['unused_days'] = words[1].strip('[ ]').split(', ')
            elif (words[0] == 'date_issued'):
                info['date_issued'] = ((((words[1] + ':') + words[2]) + ':') + words[3])
            else:
                pass
        cilm = np.zeros((2, (lmax + 1), (lmax + 1)))
        cilm_std = np.zeros_like(cilm)
        cilm[(0, 0, 0)] = 1
        for line in f:
            words = line.replace('D', 'E').split()
            (l, m) = (int(words[1]), int(words[2]))
            if (m > lmax):
                break
            if (l > lmax):
                continue
            value_cs = [float(words[3]), float(words[4])]
            value_cs_std = [float(words[5]), float(words[6])]
            cilm[(:, l, m)] = value_cs
            cilm_std[(:, l, m)] = value_cs_std
    f.close()
    return (info, cilm, cilm_std)
