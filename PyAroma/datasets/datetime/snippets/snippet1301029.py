import datetime
import glob
import io
import os
import zmq
from zmq.utils.strtypes import bytes, unicode, b, u


def _write_key_file(key_filename, banner, public_key, secret_key=None, metadata=None, encoding='utf-8'):
    'Create a certificate file'
    if isinstance(public_key, bytes):
        public_key = public_key.decode(encoding)
    if isinstance(secret_key, bytes):
        secret_key = secret_key.decode(encoding)
    with io.open(key_filename, 'w', encoding='utf8') as f:
        f.write(banner.format(datetime.datetime.now()))
        f.write(u('metadata\n'))
        if metadata:
            for (k, v) in metadata.items():
                if isinstance(k, bytes):
                    k = k.decode(encoding)
                if isinstance(v, bytes):
                    v = v.decode(encoding)
                f.write(u('    {0} = {1}\n').format(k, v))
        f.write(u('curve\n'))
        f.write(u('    public-key = "{0}"\n').format(public_key))
        if secret_key:
            f.write(u('    secret-key = "{0}"\n').format(secret_key))
