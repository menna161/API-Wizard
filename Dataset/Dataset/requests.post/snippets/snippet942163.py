import requests
import logging
import json
import os


def thesaurus_query(self, term_id, query_type):
    if (not term_id):
        return []
    params = self.build_thesaurus_query_params(term_id, query_type)
    r = requests.post(self.api_url, json=params, headers=self.request_headers, verify=PowerThesaurus.VERIFY_SSL)
    self.logger.debug('thesaurus_query: {} {}'.format(r.status_code, r.url))
    r.raise_for_status()
    return self.parse_thesaurus_query_response(r.json())
