import numpy as np
import xarray as xr
from os import path, makedirs, walk, remove
from pathlib import Path
import requests
import time as pytime
from .utils import print_error_gldas
from ..ggclasses.class_GLDAS import GLDAS


def read_gldas(start_date=None, end_date=None, res='1deg', source='NOAH'):
    "\n    Read the GLDAS files into a GLDAS class instance. Before calling this program, it is recommended to be able to download all the GLDAS data needed using the program gldas_download.\n    \n    Usage:\n    gldas = read_gldas()\n    gldas = read_gldas('2008-07','2018-12')\n    gldas = read_gldas(start_date = '2010-01')\n    gldas = read_gldas(end_date = '2018-12',res = '0.25deg')\n\n    Inputs:\n    \n    Parameters:\n    start_date: [optional, str, default = None] start date for the data to be read, for example, '2004-07'. If None, there is no limit on the start date.\n    end_date: [optional, str, default = None] end date for the data to be read, for example, '2004-07'. If None, there is no limit on the end date. \n    If both start date and end_date are None, all files in the storage directory will be read.\n\n    Outputs:\n    gldas -> GLDAS class instance\n        \n    Examples: \n    >>> gldas = read_gldas()\n    >>> print(gldas.title)\n    GLDAS2.1 LIS land surface model output monthly mean\n    >>> print(gldas.solution_counts)\n    210\n    >>> print(gldas.institution)\n    NASA GSFC\n    >>>\n    >>> gldas = read_gldas('2008-07','2018-12')\n    >>> print(gldas.time_coverage_start)\n    2008-07\n    >>> print(gldas.time_coverage_end)\n    2018-12\n    >>> print(gldas.solution_counts)\n    126\n    "
    (val_res, dir_res) = print_error_gldas(source, res)
    (filelist, filelist_interval) = ([], [])
    (gldas_dates, gldas_dates_interval) = ([], [])
    date_issued = []
    data = []
    info = {}
    file_dir = (('GLDAS/' + source) + dir_res)
    for (dirname, dirs, files) in walk(file_dir):
        pass
    files = np.sort(files)
    for filename in files:
        if filename.endswith('.nc4'):
            filelist.append(path.join(dirname, filename))
            gldas_dates.append(((filename[(- 14):(- 10)] + '-') + filename[(- 10):(- 8)]))
    num_solutions = len(gldas_dates)
    if (start_date is None):
        start_date = gldas_dates[0]
    if (end_date is None):
        end_date = gldas_dates[(- 1)]
    num_month = (((((int(end_date[:4]) - int(start_date[:4])) * 12) + int(end_date[5:7])) - int(start_date[5:7])) + 1)
    month_list = np.array((np.array(start_date, dtype=np.datetime64) + np.arange(num_month)), dtype=np.str)
    for i in range(num_solutions):
        if (gldas_dates[i] in month_list):
            gldas_dates_interval.append(gldas_dates[i])
            filelist_interval.append(filelist[i])
    solution_month = gldas_dates_interval
    solution_counts = len(solution_month)
    missing_solution_flag = (~ np.in1d(month_list, solution_month))
    missing_month_list = month_list[missing_solution_flag]
    missing_month_counts = len(missing_month_list)
    for filename in filelist_interval:
        datum = xr.open_dataset(filename)
        date_issued.append(datum.history[17:27])
        data.append(datum)
    (lons, lats) = (datum['lon'], datum['lat'])
    info['title'] = datum.title
    info['summary'] = datum.comment
    info['resolution'] = res
    info['degree_order'] = (int((90 / float(res.strip('deg')))) - 1)
    info['max_degree'] = info['max_order'] = info['degree_order']
    info['institution'] = datum.institution
    info['time_coverage_start'] = start_date
    info['time_coverage_end'] = end_date
    info['total_month'] = month_list
    info['total_month_counts'] = num_month
    info['solution_month'] = solution_month
    info['solution_counts'] = solution_counts
    info['missing_month'] = missing_month_list
    info['missing_month_counts'] = missing_month_counts
    info['missing_solution_flag'] = missing_solution_flag
    info['missing_value'] = datum.missing_value
    info['tavg'] = 'past 3-hour average'
    info['acc'] = 'past 3-hour accumulation'
    info['inst'] = 'instantaneous'
    info['date_issued'] = date_issued
    info['filter'] = 'none'
    return GLDAS(info, lons, lats, data)
