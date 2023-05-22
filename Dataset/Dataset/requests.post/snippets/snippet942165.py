import requests
import logging
import json
import os


def search_query(self, query):
    params = self.build_search_query_params(query)
    r = requests.post(self.api_url, json=params, headers=self.request_headers, verify=PowerThesaurus.VERIFY_SSL)
    self.logger.debug('search_query: {} {}'.format(r.status_code, r.url))
    r.raise_for_status()
    return self.parse_search_query_response(r.json())
