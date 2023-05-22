import numpy as np
from os import path, remove, walk, makedirs
from ftplib import FTP
from datetime import date, timedelta
from gzip import GzipFile
import time as pytime
from .utils import print_error_grace
from ..ggclasses.class_GSM import GSM


def read_gsm(source='CSR', D=60, lmax=None, start_date=None, end_date=None, RL='RL06'):
    '\n    Read the GRACE GSM Level-2 files. Before calling this program, it is recommended to be able to download all the GRACE GSM data needed using the program GSM_download.\n    \n    Usage: \n    xxx_gsm = read_gsm(source,D,lmax,start_date,end_date)\n\n    Parameters:\n    source -> [optional, str, default = \'CSR\'] source of the GRACE Level-2 solutions; vailable sources are CSR, GFZ, JPL\n    D -> [optional, int, default = 60] degree of the GRACE Level-2 solutions. Avaliable options are 60 or 96\n    lmax -> [optional, int, default = None] degree to be read; it should be any positive integer. if None, lmax = D\n    start_date -> [optional, str, default = None] start date of the data to be read. If None, there is no limit on the start date.\n    end_date -> [optional, str, default = None] end date of the data to be read. If None, there is no limit on the end date.\n    RL -> [optional, str, default = \'RL06\'] release of the GRACE Level-2 solutions; currently only RL06 is available\n\n    Outputs:\n    xxx_gsm -> instance of GSM class\n        \n    Examples:\n    >>> csr_gsm = read_gsm(\'CSR\',96)\n    >>> print(CSR_GSM.degree_order)\n    96\n    >>> print(csr_gsm.max_degree,csr_gsm.max_order)\n    96 96\n    >>> print(csr_gsm.normalization)\n    fully normalized\n    >>> print(csr_gsm.earth_gravity_param)\n    3.9860044150E+14 m3/s2\n    >>> print(csr_gsm.mean_equator_radius)\n    6.3781363000E+06 m\n    >>> print(csr_gsm.background_gravity)\n    GGM05C\n    >>> print(csr_gsm.title)\n    GRACE Geopotential Coefficients CSR RL06\n    >>> print(csr_gsm.summary)\n    Spherical harmonic coefficients representing an estimate of the mean gravity field of Earth during the specified timespan derived from GRACE mission measurements. These coefficients represent the full magnitude of land hydrology, ice, and solid Earth processes. Further, they represent atmospheric and oceanic processes not captured in the accompanying GAC product. The 0th and 1st degree terms are excluded from CSR level-2.\n    >>> print(CSR_GSM.institution)\n    UT-AUSTIN/CSR\n    >>> print(csr_gsm.processing_level)\n    2\n    >>> print(csr_gsm.product_version)\n    RL06\n    >>> print(csr_gsm.time_coverage_start)\n    2002-04\n    >>> print(csr_gsm.time_coverage_end)\n    2017-06\n    >>> print(csr_gsm.solution_counts)\n    163\n    >>> print(csr_gsm.total_month_counts)\n    183\n    >>> print(csr_gsm.missing_month)\n    [\'2002-06\' \'2002-07\' \'2003-06\' \'2011-01\' \'2011-06\' \'2012-05\' \'2012-10\'\n     \'2013-03\' \'2013-08\' \'2013-09\' \'2014-02\' \'2014-07\' \'2014-12\' \'2015-07\'\n     \'2015-10\' \'2015-11\' \'2016-04\' \'2016-09\' \'2016-10\' \'2017-02\']\n    >>> print(CSR_GSM.missing_month_counts)\n    20\n    >>> print(csr_gsm.unused_days)\n    [\'2002-04-10\', \'2002-04-11\', \'2002-04-28\', \'2002-05-07\', \'2002-05-08\', \'2002-05-14\', \'2002-08-28\', \'2002-09-27\', \'2002-11-26\', \'2002-12-15\', \'2003-01-22\', \'2003-01-24\', \'2003-01-26\', \'2003-01-27\', \'2003-01-29\', \'2003-01-30\', \'2003-02-08\', \'2003-02-26\', \'2003-03-06\', \'2003-09-21\', \'2003-11-24\', \'2003-12-04\', \'2004-05-24\', \'2004-05-25\', \'2004-05-26\', \'2004-12-09\', \'2004-12-10\', \'2004-12-11\', \'2004-12-16\', \'2005-03-14\', \'2005-03-15\', \'2005-03-16\', \'2005-12-03\', \'2005-12-04\', \'2005-12-09\', \'2005-12-10\', \'2005-12-11\', \'2005-12-12\', \'2005-12-13\', \'2006-03-26\', \'2006-12-24\', \'2006-12-25\', \'2006-12-26\', \'2007-01-12\', \'2007-01-13\', \'2007-01-17\', \'2007-04-12\', \'2007-06-13\', \'2007-11-15\', \'2007-11-16\', \'2007-11-22\', \'2007-11-23\', \'2008-04-21\', \'2010-03-18\', \'2011-12-14\', \'2011-12-15\', \'2011-12-16\', \'2011-12-24\', \'2012-12-07\', \'2012-12-08\', \'2013-12-25\', \'2013-12-26\', \'2013-12-27\', \'2014-11-16\', \'2015-07-07\', \'2015-07-08\', \'2015-07-09\', \'2015-07-10\', \'2015-07-11\', \'2015-07-12\', \'2016-12-01\', \'2016-12-02\', \'2016-12-03\', \'2017-01-01\', \'2017-05-01\', \'2017-05-02\', \'2017-06-04\']\n    >>> print(CSR_GSM.SHC.shape,CSR_GSM.SHC_std.shape)\n    >>> (163, 2, 97, 97) (163, 2, 97, 97)\n    >>> gfz_gsm = read_gsm(\'GFZ\',96, 179, \'2007-05\',\'2012-05\')\n    >>> print(gfz_gsm.info)\n    {\'degree_order\': 179, \'max_degree\': 96, \'max_order\': 96, \'normalization\': \'fully normalized\', \'permanent_tide\': \'exclusive\', \'earth_gravity_param\': \'3.9860044150E+14 m3/s2\', \'mean_equator_radius\': \'6.3781364600E+06 m\', \'background_gravity\': \'EIGEN-6C4\', \'title\': \'GRACE Geopotential GSM Coefficients GFZ RL06\', \'summary\': "Spherical harmonic coefficients representing an estimate of Earth\'s mean gravity field during the specified timespan derived from GRACE mission measurements. These coefficients represent the full magnitude of land hydrology, ice, and solid Earth processes. Further, they represent atmospheric and oceanic processes not captured in the accompanying GAC product.", \'institution\': \'GFZ German Research Centre for Geosciences\', \'processing_level\': \'2\', \'product_version\': \'6.0\', \'time_coverage_start\': \'2007-05\', \'time_coverage_end\': \'2012-05\', \'unused_days\': [\'2007-06-13\', \'2007-11-15\', \'2007-11-22\', \'2007-11-23\', \'2008-04-21\', \'2008-04-22\', \'2010-03-18\', \'2011-12-14\', \'2011-12-15\', \'2011-12-16\'], \'date_issued\': [\'2018-09-26\', \'2018-09-27\', \'2018-08-02\'], \'solution_counts\': 58, \'total_month_counts\': 61, \'missing_month\': array([\'2011-01\', \'2011-06\', \'2012-05\'], dtype=\'<U7\'), \'missing_month_counts\': 3}\n    >>> print(gfz_gsm.SHC.shape,gfz_gsm.SHC_std.shape)\n    (58, 2, 180, 180) (58, 2, 180, 180)\n    >>> jpl_gsm = read_gsm(\'JPL\',60,30,\'2010-01\')\n    >>> print(jpl_gsm.info)\n    {\'degree_order\': 30, \'max_degree\': 60, \'max_order\': 60, \'normalization\': \'fully normalized\', \'permanent_tide\': \'inclusive\', \'earth_gravity_param\': \'3.9860044150e+14 m3/s2\', \'mean_equator_radius\': \'6.3781363000e+06 m\', \'background_gravity\': \'GGM05C\', \'title\': \'GRACE Geopotential Coefficients JPL RL06\', \'summary\': "Spherical harmonic coefficients representing an estimate of Earth\'s mean gravity field during the specified timespan derived from GRACE mission measurements.  These coefficients represent the full magnitude of land hydrology, ice, and solid Earth processes.  Further, they represent atmospheric and oceanic processes not captured in the accompanying GAC product.", \'institution\': \'NASA/JPL\', \'processing_level\': \'2\', \'product_version\': \'6.0\', \'time_coverage_start\': \'2010-01\', \'time_coverage_end\': \'2017-06\', \'unused_days\': [\'2010-06-15\', \'2010-06-17\', \'2010-06-18\', \'2010-06-19\', \'2010-06-20\', \'2010-06-21\', \'2010-06-22\', \'2010-06-23\', \'2012-12-07\', \'2012-12-08\', \'2013-06-12\', \'2013-12-25\', \'2013-12-26\', \'2013-12-27\', \'2015-07-07\', \'2015-07-08\', \'2015-07-09\', \'2015-07-10\', \'2015-07-11\', \'2015-07-12\', \'2015-12-31\', \'2016-01-20\', \'2016-05-25\'], \'date_issued\': [\'2018-05-20\', \'2018-08-19\'], \'solution_counts\': 73, \'total_month_counts\': 90, \'missing_month\': array([\'2011-01\', \'2011-06\', \'2012-05\', \'2012-10\', \'2013-03\', \'2013-08\',\n     \'2013-09\', \'2014-02\', \'2014-07\', \'2014-12\', \'2015-07\', \'2015-10\',\n     \'2015-11\', \'2016-04\', \'2016-09\', \'2016-10\', \'2017-02\'], dtype=\'<U7\'), \'missing_month_counts\': 17}\n    >>> print(jpl_gsm.SHC.shape,jpl_gsm.SHC_std.shape)\n    (73, 2, 31, 31) (73, 2, 31, 31)  \n    '
    print_error_grace(source, D, RL)
    if (lmax is None):
        lmax = D
    (filelist, filelist_interval) = ([], [])
    (gsm_dates, gsm_dates_interval) = ([], [])
    (shc, shc_std) = ([], [])
    (unused_days, date_issued) = ([], [])
    file_dir = ((((('GRACE/' + source) + '/') + RL) + '_') + str(D))
    for (dirname, dirs, files) in walk(file_dir):
        pass
    files = np.sort(files)
    for filename in files:
        if ('GSM' in filename):
            filelist.append(path.join(dirname, filename))
            gsm_date = parse_gsm_filename(filename)
            gsm_dates.append(((gsm_date['start']['year'] + '-') + gsm_date['start']['month']))
    num_solutions = len(gsm_dates)
    for i in range((num_solutions - 1)):
        if (gsm_dates[(i + 1)] == gsm_dates[i]):
            gsm_dates[(i + 1)] = str((np.array(gsm_dates[(i + 1)], dtype=np.datetime64) + 1))
    if (start_date is None):
        start_date = gsm_dates[0]
    if (end_date is None):
        end_date = gsm_dates[(- 1)]
    num_month = (((((int(end_date[:4]) - int(start_date[:4])) * 12) + int(end_date[5:7])) - int(start_date[5:7])) + 1)
    month_list = np.array((np.array(start_date, dtype=np.datetime64) + np.arange(num_month)), dtype=np.str)
    for i in range(num_solutions):
        if (gsm_dates[i] in month_list):
            gsm_dates_interval.append(gsm_dates[i])
            filelist_interval.append(filelist[i])
    solution_month = gsm_dates_interval
    solution_counts = len(solution_month)
    missing_solution_flag = (~ np.in1d(month_list, solution_month))
    missing_month_list = month_list[missing_solution_flag]
    missing_month_counts = len(missing_month_list)
    for filename in filelist_interval:
        (info, cilm, cilm_std) = parse_gsm_file(filename, lmax)
        unused_days.append(info['unused_days'])
        date_issued.append(info['date_issued'][:10])
        shc.append(cilm)
        shc_std.append(cilm_std)
    (shc, shc_std) = (np.array(shc), np.array(shc_std))
    info['time_coverage_start'] = start_date
    info['time_coverage_end'] = end_date
    info['total_month'] = month_list
    info['total_month_counts'] = num_month
    info['solution_month'] = solution_month
    info['solution_counts'] = solution_counts
    info['missing_month'] = missing_month_list
    info['missing_month_counts'] = missing_month_counts
    info['missing_solution_flag'] = missing_solution_flag
    info['unused_days'] = unused_days
    info['date_issued'] = date_issued
    info['title'] = info['title'].replace('GRACE-FO', 'GRACE & GRACE-FO')
    info['summary'] = info['summary'].replace('GRACE-FO', 'GRACE & GRACE-FO')
    info['equi_material'] = 'Water'
    info['filter'] = 'none'
    return GSM(info, shc, shc_std)
