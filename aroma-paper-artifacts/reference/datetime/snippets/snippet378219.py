import base64
import bluenrg.codes
import bluenrg.commands
import bluenrg.events
import re
import datetime
import json
import logging
import RPi.GPIO as gpio
import time
import _strptime
from jwcrypto import jwk, jwe
from messaging import EventDrivenMessageProcessor
from common_util import fromisoformat
from threading_more import intercept_exit_signal
from bluenrg.connection import SerialConnection
from bluenrg.interface import GATTTerminalInterface


@intercept_exit_signal
def start(**settings):
    try:
        if log.isEnabledFor(logging.DEBUG):
            log.debug('Starting BLE manager with settings: {:}'.format(settings))
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(READY_PIN, gpio.OUT, initial=gpio.LOW)
        mode_handler(value='normal')
        for (key, val) in settings.get('serial_conn', {}).iteritems():
            setattr(conn, key, val)
        term_settings = settings.get('gatt_terminal', {})

        def on_authenticate(token):
            if (not ('auth_rsa_key_b64' in term_settings)):
                raise Exception('No RSA key defined in settings')
            private_key = jwk.JWK()
            private_key.import_from_pem(base64.b64decode(term_settings['auth_rsa_key_b64']))
            jwetoken = jwe.JWE()
            jwetoken.deserialize(token, key=private_key)
            decrypted_token = json.loads(jwetoken.payload)
            valid = (fromisoformat(decrypted_token['valid_from_utc']) <= datetime.datetime.utcnow() <= fromisoformat(decrypted_token['valid_to_utc']))
            return valid

        def on_execute(command, *args, **kwargs):
            if ((not term_settings.get('cmd_allow_regex', None)) or (not re.match(term_settings['cmd_allow_regex'], command))):
                raise ValueError('Command not allowed')
            res = __salt__[command](*args, **kwargs)
            return res
        iface.on_authenticate = on_authenticate
        iface.on_execute = on_execute
        try:
            iface.start()
            gpio.output(READY_PIN, gpio.HIGH)
        except:
            log.exception('Failed to start terminal interface')
        edmp.init(__salt__, __opts__, hooks=settings.get('hooks', []), workers=settings.get('workers', []), reactors=settings.get('reactors', []))
        edmp.run()
    except Exception:
        log.exception('Failed to start BLE manager')
        raise
    finally:
        log.info('Stopping BLE manager')
        gpio.output(READY_PIN, gpio.LOW)
