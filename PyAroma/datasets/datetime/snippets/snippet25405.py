from pathlib import Path
import pandas as pd
from pptx import Presentation
from spx_data_update import UpdateSP500Data
from option_utilities import read_feather, write_feather
from urllib.request import urlretrieve
from pptx.util import Inches
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT as PP_ALIGN
import pandas_datareader.data as web
import os


def get_hfr(feather_name, csv_file_path, update_funds=True):
    db_directory = (UpdateSP500Data.DATA_BASE_PATH / 'xl')
    if update_funds:
        rows_to_skip = list(range(0, 2))
        headers = ['Date', 'Index Name', 'Index Code', 'Return', 'Index Value']
        df = pd.read_csv((db_directory / csv_file_path), skiprows=rows_to_skip, squeeze=True, names=headers, engine='python')
        index_codes = df['Index Code'].unique()
        all_hfr_list = []
        for index_code in index_codes[:(- 1)]:
            idx = (df['Index Code'] == index_code)
            hfr = df[idx].copy()
            hfr['Date'] = hfr['Date'].apply(pd.to_datetime)
            hfr = hfr.set_index(['Date'])
            hfr = hfr.reindex(hfr.index.sort_values())
            hfr_index = hfr['Index Value'].rename(hfr['Index Name'].unique()[0])
            all_hfr_list.append(hfr_index)
        hfr_df = pd.concat(all_hfr_list, axis=1)
        write_feather(hfr_df, ((UpdateSP500Data.DATA_BASE_PATH / 'feather') / feather_name))
    hfr_df = read_feather(((UpdateSP500Data.DATA_BASE_PATH / 'feather') / feather_name))
    return hfr_df
