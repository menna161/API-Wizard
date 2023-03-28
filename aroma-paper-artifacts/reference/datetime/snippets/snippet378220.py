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
