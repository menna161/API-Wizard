import re
import textwrap
import warnings
from datetime import datetime
from urllib.request import urlopen, Request
from astropy import time as atime
from astropy.utils.console import color_print, _color_text
from . import get_sun
from bs4 import BeautifulSoup
import astropy


def horoscope(birthday, corrected=True, chinese=False):
    '\n    Enter your birthday as an `astropy.time.Time` object and\n    receive a mystical horoscope about things to come.\n\n    Parameter\n    ---------\n    birthday : `astropy.time.Time` or str\n        Your birthday as a `datetime.datetime` or `astropy.time.Time` object\n        or "YYYY-MM-DD"string.\n    corrected : bool\n        Whether to account for the precession of the Earth instead of using the\n        ancient Greek dates for the signs.  After all, you do want your *real*\n        horoscope, not a cheap inaccurate approximation, right?\n\n    chinese : bool\n        Chinese annual zodiac wisdom instead of Western one.\n\n    Returns\n    -------\n    Infinite wisdom, condensed into astrologically precise prose.\n\n    Notes\n    -----\n    This function was implemented on April 1.  Take note of that date.\n    '
    from bs4 import BeautifulSoup
    today = datetime.now()
    err_msg = 'Invalid response from celestial gods (failed to load horoscope).'
    headers = {'User-Agent': 'foo/bar'}
    special_words = {'([sS]tar[s^ ]*)': 'yellow', '([yY]ou[^ ]*)': 'magenta', '([pP]lay[^ ]*)': 'blue', '([hH]eart)': 'red', '([fF]ate)': 'lightgreen'}
    if isinstance(birthday, str):
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
    if chinese:
        zodiac_sign = _get_zodiac(birthday.year)
        url = 'https://www.horoscope.com/us/horoscopes/yearly/{}-chinese-horoscope-{}.aspx'.format(today.year, zodiac_sign)
        summ_title_sfx = f'in {today.year}'
        try:
            res = Request(url, headers=headers)
            with urlopen(res) as f:
                try:
                    doc = BeautifulSoup(f, 'html.parser')
                    item = doc.find(id='overview')
                    desc = item.getText()
                except Exception:
                    raise CelestialError(err_msg)
        except Exception:
            raise CelestialError(err_msg)
    else:
        birthday = atime.Time(birthday)
        if corrected:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                zodiac_sign = get_sun(birthday).get_constellation().lower()
            zodiac_sign = _CONST_TO_SIGNS.get(zodiac_sign, zodiac_sign)
            if (zodiac_sign not in _VALID_SIGNS):
                raise HumanError('On your birthday the sun was in {}, which is not a sign of the zodiac.  You must not exist.  Or maybe you can settle for corrected=False.'.format(zodiac_sign.title()))
        else:
            zodiac_sign = get_sign(birthday.to_datetime())
        url = f'http://www.astrology.com/us/horoscope/daily-overview.aspx?sign={zodiac_sign}'
        summ_title_sfx = 'on {}'.format(today.strftime('%Y-%m-%d'))
        res = Request(url, headers=headers)
        with urlopen(res) as f:
            try:
                doc = BeautifulSoup(f, 'html.parser')
                item = doc.find('span', {'class': 'date'})
                desc = item.parent.getText()
            except Exception:
                raise CelestialError(err_msg)
    print(('*' * 79))
    color_print('Horoscope for {} {}:'.format(zodiac_sign.capitalize(), summ_title_sfx), 'green')
    print(('*' * 79))
    for block in textwrap.wrap(desc, 79):
        split_block = block.split()
        for (i, word) in enumerate(split_block):
            for re_word in special_words.keys():
                match = re.search(re_word, word)
                if (match is None):
                    continue
                split_block[i] = _color_text(match.groups()[0], special_words[re_word])
        print(' '.join(split_block))
