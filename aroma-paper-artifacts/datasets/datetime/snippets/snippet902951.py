from urllib.parse import urljoin
from datetime import datetime
import json
import time
import requests
from tqdm.auto import tqdm
from seodeploy.lib.logging import get_logger
from seodeploy.lib.helpers import group_batcher, mp_list_map, process_page_data
from seodeploy.modules.contentking.exceptions import ContentKingAPIError


def run_contentking(sample_paths, start_time, time_zone, config):
    'Main function that kicks off ContentKing Processing.\n\n    Parameters\n    ----------\n    sample_paths: list\n        List of paths to check.\n    start_time: datetime\n        When the difftest was started.\n    time_zone: pytz.timezone\n        Default timezone to keep times the same.\n    config: class\n        Module configuration class.\n\n    Returns\n    -------\n    dict\n        Page Data dict.\n\n    '
    run_path_pings(sample_paths, config)
    page_data = run_check_results(sample_paths, start_time, time_zone, config)
    return page_data
