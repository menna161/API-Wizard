from Acquire.ObjectStore import string_to_decimal, string_to_datetime, list_to_string, ObjectStore, Mutex, datetime_to_string
from Acquire.Service import get_service_account_bucket
from Acquire.Accounting import DebitNote, CreditNote, Account, Accounts, Ledger, Transaction
from Acquire.Client import Cheque, PaymentError
from Acquire.Service import exception_to_string
from Acquire.Service import exception_to_string
from Acquire.Service import exception_to_string
from Acquire.Service import exception_to_string
from Acquire.Service import exception_to_string


def run(args):
    'This function is called to handle request to cash cheques. This\n       will verify that the cheque is valid and will then create\n       the debit/credit note pair for the transation. It will return\n       the CreditNote to the caller so they can see that the funds have\n       been reserved, and can receipt the transaction once goods/services\n       have been delivered.\n\n       Args:\n            args (dict): information for payment for service\n\n        Returns:\n            dict: contains status, status message and credit note if valid\n\n    '
    credit_notes = []
    try:
        cheque = args['cheque']
    except:
        raise ValueError('You must supply a cheque to be cashed!')
    try:
        cheque = Cheque.from_data(cheque)
    except Exception as e:
        from Acquire.Service import exception_to_string
        raise TypeError(('Unable to interpret the cheque.\n\nCAUSE: %s' % exception_to_string(e)))
    try:
        spend = args['spend']
    except:
        spend = None
    if (spend is not None):
        try:
            spend = string_to_decimal(spend)
        except Exception as e:
            from Acquire.Service import exception_to_string
            raise TypeError(('Unable to interpret the spend.\n\nCause: %s' % exception_to_string(e)))
    try:
        resource = str(args['resource'])
    except:
        raise ValueError('You must supply a string representing the resource that will be paid for using this cheque')
    try:
        account_uid = str(args['account_uid'])
    except:
        raise ValueError('You must supply the UID of the account to which the cheque will be cashed')
    try:
        receipt_by = args['receipt_by']
    except:
        raise ValueError('You must supply the datetime by which you promise to receipt this transaction')
    try:
        receipt_by = string_to_datetime(receipt_by)
    except Exception as e:
        from Acquire.Service import exception_to_string
        raise TypeError(('Unable to interpret the receipt_by date.\n\nCAUSE: %s' % exception_to_string(e)))
    info = cheque.read(resource=resource, spend=spend, receipt_by=receipt_by)
    try:
        description = str(args['description'])
    except:
        description = info['resource']
    authorisation = info['authorisation']
    auth_resource = info['auth_resource']
    user_guid = authorisation.user_guid()
    bucket = get_service_account_bucket()
    try:
        debit_account = Account(uid=info['account_uid'], bucket=bucket)
    except Exception as e:
        from Acquire.Service import exception_to_string
        raise PaymentError(('Cannot find the account associated with the cheque\n\nCAUSE: %s' % exception_to_string(e)))
    try:
        credit_account = Account(uid=account_uid, bucket=bucket)
    except Exception as e:
        from Acquire.Service import exception_to_string
        raise PaymentError(('Cannot find the account to which funds will be creditted:\n\nCAUSE: %s' % exception_to_string(e)))
    accounts = Accounts(user_guid=user_guid)
    if (not accounts.contains(account=debit_account, bucket=bucket)):
        raise PermissionError(("The user with UID '%s' cannot authorise transactions from the account '%s' as they do not own this account." % (user_guid, str(debit_account))))
    transaction = Transaction(value=info['spend'], description=description)
    transaction_records = Ledger.perform(transactions=transaction, debit_account=debit_account, credit_account=credit_account, authorisation=authorisation, authorisation_resource=auth_resource, is_provisional=True, receipt_by=receipt_by, bucket=bucket)
    credit_notes = []
    for record in transaction_records:
        credit_notes.append(record.credit_note())
    credit_notes = list_to_string(credit_notes)
    receipt_key = ('accounting/cashed_cheque/%s' % info['uid'])
    mutex = Mutex(receipt_key, bucket=bucket)
    try:
        receipted = ObjectStore.get_object_from_json(bucket, receipt_key)
    except:
        receipted = None
    if (receipted is not None):
        mutex.unlock()
        Ledger.refund(transaction_records, bucket=bucket)
    else:
        info = {'status': 'needs_receipt', 'creditnotes': credit_notes}
        ObjectStore.set_object_from_json(bucket, receipt_key, info)
        mutex.unlock()
    return {'credit_notes': credit_notes}
