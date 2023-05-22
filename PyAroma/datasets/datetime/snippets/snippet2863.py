import os
import json
import shutil
import urllib3
from hashlib import md5
from socket import gethostbyname
from argparse import ArgumentParser
from xml.etree import ElementTree as eTree
from datetime import datetime, timedelta
import sqlite3
import requests


def get_skey(msa, hashed_login, use_cache=True):
    '\n    Get session key from HP MSA API and and print it.\n\n    :param msa: MSA IP address and DNS name.\n    :type msa: tuple\n    :param hashed_login: Hashed with md5 login data.\n    :type hashed_login: str\n    :param use_cache: The function will try to save session key to disk.\n    :type use_cache: bool\n    :return: Session key or error code.\n    :rtype: str\n    '
    if use_cache:
        cur_timestamp = datetime.timestamp(datetime.utcnow())
        if (not USE_SSL):
            cache_data = sql_cmd('SELECT expired,skey FROM skey_cache WHERE ip="{}" AND proto="http"'.format(msa[0]))
        else:
            cache_data = sql_cmd('SELECT expired,skey FROM skey_cache WHERE dns_name="{}" AND IP ="{}" AND proto="https"'.format(msa[1], msa[0]))
        if (cache_data is not None):
            (cache_expired, cached_skey) = cache_data
            if (cur_timestamp < float(cache_expired)):
                return cached_skey
            else:
                return get_skey(msa, hashed_login, use_cache=False)
        else:
            return get_skey(msa, hashed_login, use_cache=False)
    else:
        msa_conn = (msa[1] if VERIFY_SSL else msa[0])
        url = '{}/api/login/{}'.format(msa_conn, hashed_login)
        (ret_code, sessionkey, xml) = query_xmlapi(url=url, sessionkey=None)
        if (ret_code == '1'):
            expired = datetime.timestamp((datetime.utcnow() + timedelta(minutes=30)))
            if (not USE_SSL):
                cache_data = sql_cmd('SELECT ip FROM skey_cache WHERE ip = "{}" AND proto="http"'.format(msa[0]))
                if (cache_data is None):
                    sql_cmd('INSERT INTO skey_cache VALUES ("{dns}", "{ip}", "http", "{time}", "{skey}")'.format(dns=msa[1], ip=msa[0], time=expired, skey=sessionkey))
                else:
                    sql_cmd('UPDATE skey_cache SET skey="{skey}", expired="{expired}" WHERE ip="{ip}" AND proto="http"'.format(skey=sessionkey, expired=expired, ip=msa[0]))
            else:
                cache_data = sql_cmd('SELECT dns_name, ip FROM skey_cache WHERE dns_name="{}" AND ip="{}" AND proto="https"'.format(msa[1], msa[0]))
                if (cache_data is None):
                    sql_cmd('INSERT INTO skey_cache VALUES ("{name}", "{ip}", "https", "{expired}", "{skey}")'.format(name=msa[1], ip=msa[0], expired=expired, skey=sessionkey))
                else:
                    sql_cmd('UPDATE skey_cache SET skey = "{skey}", expired = "{expired}" WHERE dns_name="{name}" AND ip="{ip}" AND proto="https"'.format(skey=sessionkey, expired=expired, name=msa[1], ip=msa[0]))
            return sessionkey
        elif (ret_code == '2'):
            return ret_code
