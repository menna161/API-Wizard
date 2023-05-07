from urllib.parse import urljoin
from datetime import datetime
import json
import time
import requests
from tqdm.auto import tqdm
from seodeploy.lib.logging import get_logger
from seodeploy.lib.helpers import group_batcher, mp_list_map, process_page_data
from seodeploy.modules.contentking.exceptions import ContentKingAPIError


def _check_results(paths, config=None, data=None):
    'Loads path data from ContentKing and returns cleaned data report.\n\n       Checks to see if the latest crawl timestamp is more recent than when this process started.\n\n    Parameters\n    ----------\n    paths: list\n        List of paths to check.\n    config: class\n        Configuration class.\n    data: dict\n        Meta data containing host information.\n\n    Returns\n    -------\n    list\n        List of page data.\n\n    '
    unchecked = paths.copy()
    results = []
    break_counter = BreakCounter()
    while unchecked:
        path = unchecked.pop(0)
        url = urljoin(data['host'], path)
        try:
            url_data = load_report('url', config, id=data['site_id'], url=url)
            if (url_data and (data['time_col'] in url_data)):
                last_check = datetime.fromisoformat(url_data[data['time_col']]).astimezone(data['time_zone'])
                time_delta = (data['start_time'] - last_check).total_seconds()
                if (time_delta < 0):
                    result = {'path': path, 'page_data': parse_url_data(url_data), 'error': None}
                    results.append(result)
                else:
                    break_counter(path)
                    unchecked.append(path)
            else:
                error = 'Invalid response from API URL report.'
                _LOG.error(error)
                result = {'path': path, 'page_data': None, 'error': error}
                results.append(result)
        except Exception as e:
            error = ('Unknown Error: ' + str(e))
            _LOG.error(error)
            result = {'path': path, 'page_data': None, 'error': error}
            results.append(result)
    return results
