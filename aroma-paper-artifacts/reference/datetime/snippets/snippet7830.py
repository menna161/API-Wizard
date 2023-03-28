import pytest
import random
import datetime
from Acquire.Accounting import Account, Transaction, TransactionRecord, Accounts, Ledger, Receipt, Refund, create_decimal, Balance
from Acquire.Identity import Authorisation, ACLRule
from Acquire.Service import get_service_account_bucket, push_is_running_service, pop_is_running_service, is_running_service
from Acquire.Crypto import PrivateKey, get_private_key
from Acquire.ObjectStore import get_datetime_now


def test_transactions(random_transaction, bucket):
    (transaction, account1, account2) = random_transaction
    starting_balance1 = account1.balance()
    starting_balance2 = account2.balance()
    authorisation = Authorisation(resource=transaction.fingerprint(), testing_key=testing_key, testing_user_guid=account1.group_name())
    records = Ledger.perform(transaction=transaction, debit_account=account1, credit_account=account2, authorisation=authorisation, is_provisional=False, bucket=bucket)
    assert (len(records) == 1)
    record = records[0]
    ending_balance1 = account1.balance()
    ending_balance2 = account2.balance()
    assert (ending_balance1 == (starting_balance1 - transaction))
    assert (ending_balance2 == (starting_balance2 + transaction))
    assert (record.debit_account_uid() == account1.uid())
    assert (record.credit_account_uid() == account2.uid())
    debit_note = record.debit_note()
    credit_note = record.credit_note()
    assert (debit_note.account_uid() == account1.uid())
    assert (credit_note.account_uid() == account2.uid())
    assert (not debit_note.is_provisional())
    assert (not credit_note.is_provisional())
    assert (debit_note.value() == transaction.value())
    assert (credit_note.value() == transaction.value())
    now = get_datetime_now()
    assert (debit_note.datetime() < now)
    assert (credit_note.datetime() < now)
    assert (debit_note.datetime() <= credit_note.datetime())
    assert_packable(debit_note)
    assert_packable(credit_note)
    authorisation = Authorisation(resource=credit_note.fingerprint(), testing_key=testing_key, testing_user_guid=account2.group_name())
    refund = Refund(credit_note, authorisation)
    assert (not refund.is_null())
    assert (refund.authorisation() == authorisation)
    assert (refund.value() == transaction.value())
    assert (refund.credit_note() == credit_note)
    assert_packable(refund)
    rrecords = Ledger.refund(refund)
    assert (len(rrecords) == 1)
    rrecord = rrecords[0]
    assert (not rrecord.is_null())
    assert_packable(rrecord)
    assert (not rrecord.is_provisional())
    assert rrecord.is_direct()
    assert (rrecord.get_refund_info() == refund)
    assert rrecord.is_refund()
    assert (rrecord.original_transaction() == transaction)
    assert record.is_direct()
    record.reload()
    assert record.is_refunded()
    assert (rrecord.original_transaction_record() == record)
    ending_balance1 = account1.balance()
    ending_balance2 = account2.balance()
    assert (ending_balance1.liability() == starting_balance1.liability())
    assert (ending_balance2.receivable() == starting_balance2.receivable())
    assert (starting_balance1.balance() == ending_balance1.balance())
    assert (starting_balance2.balance() == ending_balance2.balance())
    assert (starting_balance2.liability() == ending_balance2.liability())
    assert (starting_balance1.receivable() == ending_balance1.receivable())
