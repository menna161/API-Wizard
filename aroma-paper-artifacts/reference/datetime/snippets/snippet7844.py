import pytest
import random
import datetime
from threading import Thread, RLock
from Acquire.Accounting import Account, Transaction, TransactionRecord, Ledger, Receipt, Refund, create_decimal, Balance, Accounts
from Acquire.Identity import Authorisation
from Acquire.ObjectStore import get_datetime_now
from Acquire.Crypto import PrivateKey, get_private_key
from Acquire.Service import get_service_account_bucket, is_running_service, push_is_running_service, pop_is_running_service
from freezegun import freeze_time


@pytest.fixture(scope='session')
def account2(bucket):
    if (not have_freezetime):
        return None
    with freeze_time(start_time) as _frozen_datetime:
        now = get_datetime_now()
        assert (start_time == now)
        push_is_running_service()
        accounts = Accounts(user_guid=account2_user)
        account = Account(name='Testing Account', description='This is a second testing account', group_name=accounts.name())
        uid = account.uid()
        assert (uid is not None)
        assert (account.balance() == Balance())
        account.set_overdraft_limit(account2_overdraft_limit)
        assert (account.get_overdraft_limit() == account2_overdraft_limit)
        pop_is_running_service()
    return account
