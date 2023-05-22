import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ujson as json
from hive.conf import Conf
from hive.server.hive_api.common import get_account_id, get_community_id, valid_limit
from hive.server.common.helpers import return_error_info


def days_ago(days):
    'Get the date `n` days ago.'
    return (datetime.now() + relativedelta(days=(- days)))
