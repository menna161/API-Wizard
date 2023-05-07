import logging
from datetime import datetime
from toolz import partition_all
import ujson as json
from hive.db.adapter import Db
from hive.utils.normalize import rep_log10, vests_amount
from hive.utils.timer import Timer
from hive.utils.account import safe_profile_metadata
from hive.utils.unique_fifo import UniqueFIFO
from hive.indexer.community import Community, START_DATE


@classmethod
def _cache_accounts(cls, accounts, steem, trx=True):
    'Fetch all `accounts` and write to db.'
    timer = Timer(len(accounts), 'account', ['rps', 'wps'])
    for name_batch in partition_all(1000, accounts):
        cached_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        timer.batch_start()
        batch = steem.get_accounts(name_batch)
        timer.batch_lap()
        sqls = [cls._sql(acct, cached_at) for acct in batch]
        DB.batch_queries(sqls, trx)
        timer.batch_finish(len(batch))
        if (trx or (len(accounts) > 1000)):
            log.info(timer.batch_status())
