import logging
import requests
import xmltodict
from dateutil.parser import parse
from django.utils import timezone
from pagseguro.forms import PagSeguroItemForm
from pagseguro.settings import CHECKOUT_URL, NOTIFICATION_URL, PAGSEGURO_EMAIL, PAGSEGURO_TOKEN, PAYMENT_URL, SESSION_URL, TRANSACTION_URL
from pagseguro.signals import checkout_realizado, checkout_realizado_com_erro, checkout_realizado_com_sucesso, notificacao_recebida, NOTIFICATION_STATUS


def get_transaction(self, transaction_id):
    response = requests.get((self.transaction_url + '/{}'.format(transaction_id)), params={'email': self.base_params['email'], 'token': self.base_params['token']})
    if (response.status_code == 200):
        root = xmltodict.parse(response.text)
        transaction = root['transaction']
        data = {'transaction': transaction, 'status_code': response.status_code, 'success': True, 'date': timezone.now()}
    else:
        data = {'status_code': response.status_code, 'message': response.text, 'success': False, 'date': timezone.now()}
    logger.debug('operation=api_get_transaction, transaction_id={}, data={!r}, response_status={}'.format(transaction_id, data, response.status_code))
    return data
