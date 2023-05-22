from urllib.parse import urljoin
from datetime import datetime
import json
import time
import requests
from tqdm.auto import tqdm
from seodeploy.lib.logging import get_logger
from seodeploy.lib.helpers import group_batcher, mp_list_map, process_page_data
from seodeploy.modules.contentking.exceptions import ContentKingAPIError


def load_report(report, config, **data):
    'Reporting class for ContentKing.\n\n        Description: Receives a report type and names parameters passed to function.\n        Requests from ContentKing Reporting API.\n\n        Reporting API Details: https://www.contentkingapp.com/support/reporting-api/\n\n        Implemented Reports:\n            * websites\n            * alerts\n            * issues\n            * segments\n            * statistics\n            * statistics:segment\n            * url\n\n        Implemented Named Parameters:\n            * id: COntentKing ID of website (string)\n            * url: URL of page to get details about. (string)\n            * per_page: How many pages to return at a time from the `pages` endpoint. Max is 500, (integer)\n\n\n        TODO:\n            * Currently there is minimal error handling.\n            * Should this be turned into a class?\n            * Need to add rate limit to generator function `get_paged_reports`.\n\n    '

    def api_reports(report, data=None):
        'Report repository for ContentKing API'
        reports = {'websites': 'websites', 'alerts': 'websites/{id}/alerts', 'issues': 'websites/{id}/issues', 'segments': 'websites/{id}/segments', 'statistics': 'websites/{id}/statistics/website', 'statistics:segment': 'websites/{id}/statistics/segment:{segment_id}', 'url': 'websites/{id}/pages?url={url}', 'pages': 'websites/{id}/pages/list'}
        return reports.get(report, '404').format(**data)

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

    def get_paged_report(report, config, data):
        'Function for handling paged reports from ContentKing API.'
        page = 1
        per_page = data.get('per_page', 100)
        while True:
            query_string = {'page': page, 'per_page': per_page}
            result = get_report(report, config, data, query_string=query_string)
            if result:
                urls = result['urls']
                (yield urls)
                time.sleep(2)
                if (len(urls) < per_page):
                    break
                page += 1
            else:
                (yield [])
                break
    paged_reports = ['pages']
    if (report in paged_reports):
        return get_paged_report(report, config, data)
    return get_report(report, config, data)
