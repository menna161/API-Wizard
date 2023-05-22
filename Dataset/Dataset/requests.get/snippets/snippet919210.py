import numpy as np
import xarray as xr
from os import path, makedirs, walk, remove
from pathlib import Path
import requests
import time as pytime
from .utils import print_error_gldas
from ..ggclasses.class_GLDAS import GLDAS


def gldas_download(uid, passwd, start_date, end_date, res='1deg', source='NOAH'):
    "\n    Download the GLDAS grid data over a period defined by the start date and end date and its documentation from urs.earthdata.nasa.gov\n    If data to be downloaded are already in the download directory, the performance of download is automatically skipped.\n    Currently, only data from NOAH are feasible. Avaliable resolutions are 1deg and 0.25deg.\n\n    Usage:\n    gldas_download(uid,passwd,start_date,end_date)\n    gldas_download(uid,passwd,start_date,end_date,'0.25deg')\n\n    Inputs:\n    uid -> [str] username for logging into urs.earthdata.nasa.gov\n    passwd -> [str] password for logging into urs.earthdata.nasa.gov\n    start_date -> [str] start date for the data to be downloaded, for example, '2004-07'\n    end_date -> [str] end date for the data to be downloaded, for example, '2013-11'\n    \n    Parameters:\n    res -> [optional, default = '1deg'] Resolution of the GLDAS grid data. Avaliable options are '1deg' and '0.25deg'.\n    source -> [optional, default = 'NOAH'] Publisher of the GLDAS grid data. Currently, only 'NOAH' are feasible.\n \n    Outputs:\n    GLDAS grid data stored in the GLDAS/NOAH10 or GLDAS/NOAH025 directory\n        \n    Examples:\n    >>> uid,passwd = 'your_username','your_passwd'\n    >>> start_date,end_date = '2002-07','2019-09'\n    >>> gldas_download(uid,passwd,start_date,end_date)\n    Downloading ...  GLDAS_NOAH10_M.A200207.021.nc4 ... 210 Transfer complete\n    ...\n    ...\n    Downloading ...  GLDAS_NOAH10_M.A201909.021.nc4 ... 210 Transfer complete\n    >>>\n    >>> start_date,end_date = '2002-07','2019-09'\n    >>> gldas_download(uid,passwd,start_date,end_date,'0.25deg')\n    Downloading ...  GLDAS_NOAH025_M.A200207.021.nc4 ... 210 Transfer complete\n    ...\n    ...\n    Downloading ...  GLDAS_NOAH025_M.A201909.021.nc4 ... 210 Transfer complete\n    "
    (val_res, dir_res) = print_error_gldas(source, res)
    home = str(Path.home())
    if (not path.exists((home + '/.netrc'))):
        netrc_file = open((home + '/.netrc'), 'w')
        netrc_file.write(((('machine urs.earthdata.nasa.gov login ' + uid) + ' password ') + passwd))
        netrc_file.close()
    dir_gldas_to = (('GLDAS/' + source) + dir_res)
    if (not path.exists(dir_gldas_to)):
        makedirs(dir_gldas_to)
    num_month = (((((int(end_date[:4]) - int(start_date[:4])) * 12) + int(end_date[5:7])) - int(start_date[5:7])) + 1)
    month_list = list(np.array((np.array(start_date, dtype=np.datetime64) + np.arange(num_month)), dtype=np.str))
    server = 'https://hydro1.gesdisc.eosdis.nasa.gov'
    for (dirname, dirs, files) in walk(dir_gldas_to):
        pass
    for month in month_list:
        ym = month.replace('-', '')
        gldas_file = ((((('GLDAS_' + source) + dir_res) + '_M.A') + ym) + '.021.nc4')
        if (gldas_file not in files):
            print('Downloading ... ', gldas_file, end=' ... ')
            url = (((((((server + '/data/GLDAS/GLDAS_') + source) + dir_res) + '_M.2.1/') + ym[:4]) + '/') + gldas_file)
            result = requests.get(url)
            for idownload in range(3):
                try:
                    result.raise_for_status()
                    local_file = open(((dir_gldas_to + '/') + gldas_file), 'wb')
                    local_file.write(result.content)
                    local_file.close()
                    print((str(result.status_code) + ' Transfer complete'))
                    break
                except:
                    local_file.close()
                    remove(((dir_gldas_to + '/') + gldas_file))
                    if (idownload == 2):
                        raise Exception('Server did not respond, file download failed')
                    pytime.sleep(20)
    readme_file = 'README_GLDAS2.pdf'
    url = (((((server + '/data/GLDAS/GLDAS_') + source) + dir_res) + '_M.2.1/doc/') + readme_file)
    if (not path.exists(((dir_gldas_to + '/') + readme_file))):
        result = requests.get(url)
        doc_file = open(((dir_gldas_to + '/') + readme_file), 'wb')
        doc_file.write(result.content)
        doc_file.close()
