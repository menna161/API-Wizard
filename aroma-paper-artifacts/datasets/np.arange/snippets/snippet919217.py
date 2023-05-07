import numpy as np
from os import path, remove, walk, makedirs
from ftplib import FTP
from datetime import date, timedelta
from gzip import GzipFile
import time as pytime
from .utils import print_error_grace
from ..ggclasses.class_GSM import GSM


def gsm_average(gsm_list):
    "\n    Combine the (deaveraged) GSM solution from multiple institutions into an integrated one. The combined solution\n    is defined as the average of these solutions.\n    \n    Usage: \n    comb_gsm = GSM_average([csr_gsm,gfz_gsm,jpl_gsm])\n\n    Inputs:\n    gsm_list -> [str list] The list of instance of GSM class for multiple institutions.\n            \n    Outputs:\n    comb_gsm -> the instance of GSM class for combined GSM solutions\n        \n    Examples:\n    >>> csr_gsm = read_gsm('CSR',96,start_date='2002-05',end_date='2019-07')\n    >>> gfz_gsm = read_gsm('GFZ',96,end_date='2019-06')\n    >>> jpl_gsm = read_gsm('JPL',96,start_date='2002-06')\n    >>> comb_gsm = gsm_average([csr_gsm.deaverage(),gfz_gsm.deaverage(),jpl_gsm.deaverage()])\n    >>> print(comb_gsm.title)\n    Combined Deaveraged GRACE & GRACE-FO Geopotential Coefficients CSR RL06, GFZ RL06, JPL RL06\n    >>> print(comb_gsm.institution)\n    UT-AUSTIN/CSR, GFZ German Research Centre for Geosciences, NASA/JPL\n    "
    n = len(gsm_list)
    (dic_shc, dic_shc_std) = ([], [])
    (shc, shc_std) = ([], [])
    gsm_keys = {}.keys()
    for i in range(1, n):
        if (gsm_list[i].degree_order != gsm_list[0].degree_order):
            raise Exception('Degree and order for gsm in gsm list are not identical.')
    dim = (gsm_list[0].degree_order + 1)
    for j in range(n):
        if (gsm_list[j].mean_equator_radius == '6.3781364600E+06 m'):
            ratio_r = (float(gsm_list[j].mean_equator_radius.partition('m')[0]) / 6378136.3)
            ratio_rl = np.array([(ratio_r ** l) for l in range(dim)])[(:, None)]
            ratio_gm = (float(gsm_list[j].earth_gravity_param.partition('m3/s2')[0]) / 398600441500000.0)
            dic_shc.append(dict(zip(gsm_list[j].solution_month, ((gsm_list[j].shc * ratio_rl) * ratio_gm))))
            dic_shc_std.append(dict(zip(gsm_list[j].solution_month, ((gsm_list[j].shc_std * ratio_rl) * ratio_gm))))
        dic_shc.append(dict(zip(gsm_list[j].solution_month, gsm_list[j].shc)))
        dic_shc_std.append(dict(zip(gsm_list[j].solution_month, gsm_list[j].shc_std)))
        gsm_keys = (gsm_keys | dic_shc[j].keys())
    gsm_keys = np.sort(list(gsm_keys))
    nan_matrix = np.full((2, dim, dim), np.nan)
    none_matrix = np.full((2, dim, dim), None)
    for key in gsm_keys:
        (temp1, temp2, temp3) = ([], [], [])
        for k in range(n):
            temp1.append(dic_shc[k].get(key, nan_matrix))
            temp2.append((dic_shc_std[k].get(key, nan_matrix) ** 2))
            temp3.append((dic_shc[k].get(key) != none_matrix).any())
        m = np.count_nonzero(temp3)
        shc.append(np.nanmean(temp1, axis=0))
        shc_std.append(np.sqrt((np.nanmean(temp2, axis=0) / m)))
    (shc, shc_std) = (np.array(shc), np.array(shc_std))
    start_date = np.sort([gsm_list[k].info['time_coverage_start'] for k in range(n)])[0]
    end_date = np.sort([gsm_list[k].info['time_coverage_end'] for k in range(n)])[(- 1)]
    num_month = (((((int(end_date[:4]) - int(start_date[:4])) * 12) + int(end_date[5:7])) - int(start_date[5:7])) + 1)
    month_list = np.array((np.array(start_date, dtype=np.datetime64) + np.arange(num_month)), dtype=np.str)
    solution_month = list(gsm_keys)
    solution_counts = len(solution_month)
    missing_solution_flag = (~ np.in1d(month_list, solution_month))
    missing_month_list = month_list[missing_solution_flag]
    missing_month_counts = len(missing_month_list)
    info = gsm_list[0].info.copy()
    title = gsm_list[0].info['title']
    info['permanent_tide'] = 'inclusive'
    if (gsm_list[0].background_gravity == 'Average of monthly solutions'):
        info['background_gravity'] = 'Average of monthly solutions'
    else:
        info['background_gravity'] = 'GGM05C'
    info['earth_gravity_param'] = '3.9860044150E+14 m3/s2'
    info['mean_equator_radius'] = '6.3781363000E+06 m'
    info['title'] = ('Combined ' + title.replace(title[(- 9):(- 5)], ''))
    info['summary'] = (info['summary'].partition('product.')[0] + 'product.')
    info['time_coverage_start'] = start_date
    info['time_coverage_end'] = end_date
    info['total_month'] = month_list
    info['total_month_counts'] = num_month
    info['solution_month'] = solution_month
    info['solution_counts'] = solution_counts
    info['missing_month'] = missing_month_list
    info['missing_month_counts'] = missing_month_counts
    info['missing_solution_flag'] = missing_solution_flag
    info['unused_days'] = 'Invalid'
    info['date_issued'] = 'Invalid'
    for k in range(1, n):
        info['institution'] = ((info['institution'] + ', ') + gsm_list[k].info['institution'])
    return GSM(info, shc, shc_std)
