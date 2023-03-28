import uuid as _uuid
from copy import copy as _copy
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import Refund as _Refund
from Acquire.Accounting import Account as _Account
from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import CreditNote as _CreditNote
from Acquire.Accounting import PairedNote as _PairedNote
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import Receipt as _Receipt
from Acquire.Accounting import Account as _Account
from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import CreditNote as _CreditNote
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import PairedNote as _PairedNote
from Acquire.Accounting import Account as _Account
from Acquire.Identity import Authorisation as _Authorisation
from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import CreditNote as _CreditNote
from Acquire.Accounting import Transaction as _Transaction
from Acquire.Accounting import PairedNote as _PairedNote
from Acquire.Accounting import Receipt as _Receipt
from Acquire.Accounting import Refund as _Refund
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import TransactionState as _TransactionState
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Accounting import LedgerError
from Acquire.ObjectStore import ObjectStore as _ObjectStore
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Accounting import UnbalancedLedgerError
from Acquire.Accounting import UnbalancedLedgerError
from Acquire.Accounting import UnbalancedLedgerError


@staticmethod
def perform(transaction=None, transactions=None, debit_account=None, credit_account=None, authorisation=None, authorisation_resource=None, is_provisional=False, receipt_by=None, bucket=None):
    "Perform the passed transaction(s) between 'debit_account' and\n           'credit_account', recording the 'authorisation' for this\n           transaction. If 'is_provisional' then record this as a provisional\n           transaction (liability for the debit_account, future unspendable\n           income for the 'credit_account'). Payment won't actually be taken\n           until the transaction is 'receipted' (which may be for less than\n           (but not more than) then provisional value, and which must take\n           place before 'receipt_by' (which will default to one week in\n           the future if not supplied - the actual time is encoded\n           in the returned TransactionRecords). Returns the (already\n           recorded) TransactionRecord.\n\n           Note that if several transactions are passed, then they must all\n           succeed. If one of them fails then they are immediately refunded.\n\n           Args:\n                transactions (list) : List of Transactions to process\n                debit_account (Account): Account to debit\n                credit_account (Account): Account to credit\n                authorisation (Authorisation): Authorisation for\n                the transactions\n                is_provisional (bool, default=False): Whether the transactions\n                are provisional\n                receipt_by (datetime, default=None): Date by which transactions\n                must be receipted\n                bucket (dict): Bucket to load data from\n\n            Returns:\n                list: List of TransactionRecords\n\n        "
    from Acquire.Accounting import Account as _Account
    from Acquire.Identity import Authorisation as _Authorisation
    from Acquire.Accounting import DebitNote as _DebitNote
    from Acquire.Accounting import CreditNote as _CreditNote
    from Acquire.Accounting import Transaction as _Transaction
    from Acquire.Accounting import PairedNote as _PairedNote
    if (not isinstance(debit_account, _Account)):
        raise TypeError('The Debit Account must be of type Account')
    if (not isinstance(credit_account, _Account)):
        raise TypeError('The Credit Account must be of type Account')
    if (not isinstance(authorisation, _Authorisation)):
        raise TypeError('The Authorisation must be of type Authorisation')
    if is_provisional:
        is_provisional = True
    else:
        is_provisional = False
    if (transactions is None):
        transactions = []
    elif isinstance(transactions, _Transaction):
        transactions = [transactions]
    if (transaction is not None):
        transactions.insert(0, transaction)
    t = []
    for transaction in transactions:
        if (not isinstance(transaction, _Transaction)):
            raise TypeError('The Transaction must be of type Transaction')
        if (transaction.value() >= 0):
            t.append(transaction)
    transactions = t
    if (bucket is None):
        from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
        bucket = _get_service_account_bucket()
    debit_notes = []
    try:
        for transaction in transactions:
            debit_notes.append(_DebitNote(transaction=transaction, account=debit_account, authorisation=authorisation, authorisation_resource=authorisation_resource, is_provisional=is_provisional, receipt_by=receipt_by, bucket=bucket))
            if (is_provisional and (receipt_by is None)):
                receipt_by = debit_notes[0].receipt_by()
    except Exception as e:
        credit_notes = []
        debit_error = str(e)
        try:
            for debit_note in debit_notes:
                debit_account._rescind_note(debit_note, bucket=bucket)
        except Exception as e:
            from Acquire.Accounting import UnbalancedLedgerError
            raise UnbalancedLedgerError(('We have an unbalanced ledger as it was not possible to refund a multi-part refused credit (%s): Credit refusal error = %s. Refund error = %s' % (str(debit_note), str(debit_error), str(e))))
        raise e
    credit_notes = {}
    has_error = False
    credit_error = Exception()
    for debit_note in debit_notes:
        try:
            credit_note = _CreditNote(debit_note, credit_account, bucket=bucket)
            credit_notes[debit_note.uid()] = credit_note
        except Exception as e:
            has_error = True
            credit_error = e
            break
    if has_error:
        try:
            for credit_note in credit_notes.values():
                credit_account._delete_note(credit_note, bucket=bucket)
        except Exception as e:
            from Acquire.Accounting import UnbalancedLedgerError
            raise UnbalancedLedgerError(('We have an unbalanced ledger as it was not possible to credit a multi-part debit (%s): Credit refusal error = %s. Refund error = %s' % (debit_notes, str(credit_error), str(e))))
        try:
            for debit_note in debit_notes:
                debit_account._delete_note(debit_note, bucket=bucket)
        except Exception as e:
            from Acquire.Accounting import UnbalancedLedgerError
            raise UnbalancedLedgerError(('We have an unbalanced ledger as it was not possible to credit a multi-part debit (%s): Credit refusal error = %s. Refund error = %s' % (debit_notes, str(credit_error), str(e))))
        raise credit_error
    try:
        paired_notes = _PairedNote.create(debit_notes, credit_notes)
    except Exception as e:
        for debit_note in debit_notes:
            try:
                debit_account._delete_note(debit_note, bucket=bucket)
            except:
                pass
        for credit_note in credit_notes:
            try:
                credit_account._delete_note(credit_note, bucket=bucket)
            except:
                pass
        raise e
    return Ledger._record_to_ledger(paired_notes, is_provisional, bucket=bucket)
