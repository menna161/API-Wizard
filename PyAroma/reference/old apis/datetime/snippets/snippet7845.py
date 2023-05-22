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


def test_temporal_transactions(account1, account2, bucket):
    if (not have_freezetime):
        return
    zero = create_decimal(0)
    balance1 = zero
    balance2 = zero
    final_balance1 = zero
    final_balance2 = zero
    liability1 = zero
    liability2 = zero
    receivable1 = zero
    receivable2 = zero
    random_dates = []
    now = get_datetime_now()
    for i in range(0, 50):
        if (i == 0):
            s = '2019-01-20 20:59:59.092627+00:00'
            r = datetime.datetime.fromisoformat(s)
        else:
            r = (start_time + (random.random() * (now - start_time)))
        while (((r.minute == 59) and (r.second >= 58)) or ((r.minute == 0) and (r.second == 0) and (r.microsecond < 10))):
            r = (r + datetime.timedelta(seconds=1))
        random_dates.append(r)
    random_dates.sort()
    random_dates.sort()
    provisionals = []
    for (i, transaction_time) in enumerate(random_dates):
        with freeze_time(transaction_time) as _frozen_datetime:
            now = get_datetime_now()
            assert (transaction_time == now)
            is_provisional = (random.randint(0, 3) <= 2)
            transaction = Transaction((25 * random.random()), ('test transaction %d' % i))
            if random.randint(0, 1):
                debit_account = account1
                credit_account = account2
                if is_provisional:
                    liability1 += transaction.value()
                    receivable2 += transaction.value()
                else:
                    balance1 -= transaction.value()
                    balance2 += transaction.value()
                final_balance1 -= transaction.value()
                final_balance2 += transaction.value()
            else:
                debit_account = account2
                credit_account = account1
                if is_provisional:
                    receivable1 += transaction.value()
                    liability2 += transaction.value()
                else:
                    balance1 += transaction.value()
                    balance2 -= transaction.value()
                final_balance1 += transaction.value()
                final_balance2 -= transaction.value()
            auth = Authorisation(resource=transaction.fingerprint(), testing_key=testing_key, testing_user_guid=debit_account.group_name())
            records = Ledger.perform(transaction=transaction, debit_account=debit_account, credit_account=credit_account, authorisation=auth, is_provisional=is_provisional, bucket=bucket)
            for record in records:
                assert (record.datetime() == now)
            if is_provisional:
                for record in records:
                    provisionals.append((credit_account, record))
            elif (random.randint(0, 3) <= 2):
                balance1 = Balance(balance=balance1, liability=liability1, receivable=receivable1)
                balance2 = Balance(balance=balance2, liability=liability2, receivable=receivable2)
                assert (account1.balance() == balance1)
                assert (account2.balance() == balance2)
                for (credit_account, record) in provisionals:
                    credit_note = record.credit_note()
                    auth = Authorisation(resource=credit_note.fingerprint(), testing_key=testing_key, testing_user_guid=credit_account.group_name())
                    receipted_value = create_decimal((random.random() * float(credit_note.value())))
                    delta_value = (credit_note.value() - receipted_value)
                    Ledger.receipt(Receipt(credit_note=credit_note, receipted_value=receipted_value, authorisation=auth), bucket=bucket)
                    if (credit_note.debit_account_uid() == account1.uid()):
                        final_balance1 += delta_value
                        final_balance2 -= delta_value
                    else:
                        final_balance2 += delta_value
                        final_balance1 -= delta_value
                assert (account1.balance() == Balance(balance=final_balance1))
                assert (account2.balance() == Balance(balance=final_balance2))
                provisionals = []
                balance1 = final_balance1
                balance2 = final_balance2
                liability1 = zero
                liability2 = zero
                receivable1 = zero
                receivable2 = zero
    balance1 = Balance(balance=balance1, liability=liability1, receivable=receivable1)
    balance2 = Balance(balance=balance2, liability=liability2, receivable=receivable2)
    assert (account1.balance() == balance1)
    assert (account2.balance() == balance2)
    for (credit_account, record) in provisionals:
        credit_note = record.credit_note()
        auth = Authorisation(resource=record.credit_note().fingerprint(), testing_key=testing_key, testing_user_guid=credit_account.group_name())
        receipted_value = create_decimal((random.random() * float(credit_note.value())))
        delta_value = (credit_note.value() - receipted_value)
        Ledger.receipt(Receipt(credit_note=credit_note, authorisation=auth, receipted_value=receipted_value), bucket=bucket)
        if (credit_note.debit_account_uid() == account1.uid()):
            final_balance1 += delta_value
            final_balance2 -= delta_value
        else:
            final_balance2 += delta_value
            final_balance1 -= delta_value
    assert (account1.balance() == Balance(balance=final_balance1))
    assert (account2.balance() == Balance(balance=final_balance2))
