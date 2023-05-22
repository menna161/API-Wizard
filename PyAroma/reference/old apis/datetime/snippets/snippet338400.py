import argparse
import os
import commands
from urllib import unquote
import datetime
import requests
from googletrans import Translator
import webbrowser


def check_update():
    now_time = datetime.datetime.today()
    (now_year, now_month, now_day) = (now_time.year, now_time.month, now_time.day)
    now_time_stamp = '{}-{}-{}'.format(now_year, now_month, now_day)
    if ((now_day % 7) == 0):
        check = open('check', 'r').read().strip()
        if (check != now_time_stamp):
            open('check', 'w').write(now_time_stamp)
            version_url = 'https://github.com/wizyoung/googletranslate.popclipext/blob/master/src/version?raw=true'
            version_response = requests.get(version_url)
            if (version_response.status_code == 200):
                remote_version_str = version_response.content
                remote_version = calc_version(remote_version_str)
                current_version_str = open('./version', 'r').read()
                current_version = calc_version(current_version_str)
                if (remote_version > current_version):
                    script = ('\'display dialog "Found a new version %s -- Your current version is %s.\n\nClick OK to download." with title "Check Update" buttons {"Cancel", "OK"} default button "OK" cancel button "Cancel"\'' % (remote_version_str, current_version_str))
                    btn_res = commands.getoutput('osascript -e {}'.format(script))
                    if btn_res.startswith('button'):
                        import webbrowser
                        webbrowser.open('https://github.com/wizyoung/googletranslate.popclipext/releases')
