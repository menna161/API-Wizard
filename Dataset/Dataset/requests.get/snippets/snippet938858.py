import logging
import requests
import xmltodict
from dateutil.parser import parse
from django.utils import timezone
from pagseguro.forms import PagSeguroItemForm
from pagseguro.settings import CHECKOUT_URL, NOTIFICATION_URL, PAGSEGURO_EMAIL, PAGSEGURO_TOKEN, PAYMENT_URL, SESSION_URL, TRANSACTION_URL
from pagseguro.signals import checkout_realizado, checkout_realizado_com_erro, checkout_realizado_com_sucesso, notificacao_recebida, NOTIFICATION_STATUS


def get_notification(self, notification_id):
    response = requests.get((self.notification_url + '/{}'.format(notification_id)), params={'email': self.base_params['email'], 'token': self.base_params['token']})
    if (response.status_code == 200):
        root = xmltodict.parse(response.text)
        transaction = root['transaction']
        notificacao_recebida.send(sender=self, transaction=transaction)
        status = transaction['status']
        if (status in NOTIFICATION_STATUS):
            signal = NOTIFICATION_STATUS[status]
            signal.send(sender=self, transaction=transaction)
    logger.debug('operation=api_get_notification, notification_id={}, response_body={}, response_status={}'.format(notification_id, response.text, response.status_code))
    return response
