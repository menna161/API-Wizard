import logging
import requests
import xmltodict
from dateutil.parser import parse
from django.utils import timezone
from pagseguro.forms import PagSeguroItemForm
from pagseguro.settings import CHECKOUT_URL, NOTIFICATION_URL, PAGSEGURO_EMAIL, PAGSEGURO_TOKEN, PAYMENT_URL, SESSION_URL, TRANSACTION_URL
from pagseguro.signals import checkout_realizado, checkout_realizado_com_erro, checkout_realizado_com_sucesso, notificacao_recebida, NOTIFICATION_STATUS


def checkout(self):
    self.build_params()
    headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    response = requests.post(self.checkout_url, self.params, headers=headers)
    data = {}
    if (response.status_code == 200):
        root = xmltodict.parse(response.text)
        data = {'code': root['checkout']['code'], 'status_code': response.status_code, 'date': parse(root['checkout']['date']), 'redirect_url': '{}?code={}'.format(self.redirect_url, root['checkout']['code']), 'success': True}
        checkout_realizado_com_sucesso.send(sender=self, data=data)
    else:
        data = {'status_code': response.status_code, 'message': response.text, 'success': False, 'date': timezone.now()}
        checkout_realizado_com_erro.send(sender=self, data=data)
    checkout_realizado.send(sender=self, data=data)
    logger.debug('operation=api_checkout, data={!r}'.format(data))
    return data
