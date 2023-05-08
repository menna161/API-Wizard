import abc
import csv
import functools
import logging
from enum import Enum, unique
from . import constants


def perform_bulk_api_pass(self, query):
    date_time_fields = [f for f in self.field_scope if (self.context.get_field_map(self.sobjectname)[f]['type'] == 'datetime')]
    for result in self.context.connection.bulk_api_query(self.sobjectname, query, date_time_fields, self.get_option('bulk-api-poll-interval')):
        self.store_result(result)
