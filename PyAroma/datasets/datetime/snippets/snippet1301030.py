import datetime
import glob
import io
import os
import zmq
from zmq.utils.strtypes import bytes, unicode, b, u


def create_certificates(key_dir, name, metadata=None):
    'Create zmq certificates.\n    \n    Returns the file paths to the public and secret certificate files.\n    '
    (public_key, secret_key) = zmq.curve_keypair()
    base_filename = os.path.join(key_dir, name)
    secret_key_file = '{0}.key_secret'.format(base_filename)
    public_key_file = '{0}.key'.format(base_filename)
    now = datetime.datetime.now()
    _write_key_file(public_key_file, _cert_public_banner.format(now), public_key)
    _write_key_file(secret_key_file, _cert_secret_banner.format(now), public_key, secret_key=secret_key, metadata=metadata)
    return (public_key_file, secret_key_file)
