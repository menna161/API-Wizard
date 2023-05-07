from urllib.parse import urljoin
from datetime import datetime
import json
import time
import requests
from tqdm.auto import tqdm
from seodeploy.lib.logging import get_logger
from seodeploy.lib.helpers import group_batcher, mp_list_map, process_page_data
from seodeploy.modules.contentking.exceptions import ContentKingAPIError


def run_check_results(sample_paths, start_time, time_zone, config):
    'Monitors paths that were pinged for updated timestamp. Compares allowed differences.\n\n    Parameters\n    ----------\n    sample_paths: list\n        List of paths to check.\n    start_time: datetime\n        When the difftest was started.\n    time_zone: pytz.timezone\n        Default timezone to keep times the same.\n    config: class\n        Module configuration class.\n\n    Returns\n    -------\n    dict\n        Page Data dict.\n\n    '
    batches = group_batcher(sample_paths, list, config.contentking.BATCH_SIZE, fill=None)
    prod_data = {'start_time': start_time, 'time_zone': time_zone, 'site_id': config.contentking.PROD_SITE_ID, 'host': config.contentking.PROD_HOST, 'time_col': config.contentking.TIME_COL}
    stage_data = {'start_time': start_time, 'time_zone': time_zone, 'site_id': config.contentking.STAGE_SITE_ID, 'host': config.contentking.STAGE_HOST, 'time_col': config.contentking.TIME_COL}
    prod_result = []
    stage_result = []
    for batch in tqdm(batches, desc='Checking crawl status of URLs'):
        prod_result.extend(mp_list_map(batch, _check_results, config=config, data=prod_data))
        stage_result.extend(mp_list_map(batch, _check_results, config=config, data=stage_data))
        time.sleep(config.contentking.BATCH_WAIT)
    page_data = process_page_data(sample_paths, prod_result, stage_result, config.contentking)
    return page_data
