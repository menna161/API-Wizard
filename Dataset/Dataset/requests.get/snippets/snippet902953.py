from urllib.parse import urljoin
from datetime import datetime
import json
import time
import requests
from tqdm.auto import tqdm
from seodeploy.lib.logging import get_logger
from seodeploy.lib.helpers import group_batcher, mp_list_map, process_page_data
from seodeploy.modules.contentking.exceptions import ContentKingAPIError


def get_report(report, config, data, query_string=None):
    'Requests report from ContenKing API'
    api_url = urljoin((config.contentking.ENDPOINT + '/'), api_reports(report, data))
    headers = {'User-Agent': 'Python CI/CD Testing', 'Authorization': 'token {}'.format(config.contentking.REPORT_API_KEY), 'Content-Type': 'application/json'}
    tries = 3
    for i in range(tries):
        try:
            options = {'url': api_url, 'params': query_string, 'headers': headers, 'timeout': config.contentking.API_TIMEOUT, 'verify': False}
            response = requests.get(api_url, params=query_string, headers=headers, timeout=config.contentking.API_TIMEOUT, verify=False)
            response.raise_for_status()
            break
        except requests.exceptions.Timeout as err:
            _LOG.error(str(err))
            time.sleep(((i + 1) * 10))
        except requests.exceptions.ConnectionError as err:
            _LOG.error(str(err))
            time.sleep(((i + 1) * 10))
        except requests.exceptions.HTTPError as err:
            api_message = response.json()['message']
            _LOG.error('{} ({})'.format(str(err), api_message))
            break
        except Exception as err:
            _LOG.error(('Unspecified ContentKing Error:' + str(err)))
            _LOG.error(('API Request Options:' + json.dumps(options, indent=2)))
            raise ContentKingAPIError(str(err))
    if (response and (response.status_code == 200)):
        return response.json()
    return None
