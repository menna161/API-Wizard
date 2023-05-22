import os
import re
import sys
import math
import glob
import json
from datetime import datetime
from pypinyin import lazy_pinyin
from rapidfuzz import fuzz, process


def bean_add(self, inputs):
    if (not self.accounts):
        try:
            with open(self.settings['temp_path'], 'r') as tempfile:
                self.accounts = json.loads(tempfile.read())
        except IOError:
            self.accounts = self.bean_cache()
    params = ['from', 'to', 'payee', 'amount', 'tags', 'comment']
    values = {p: '' for p in params}
    for (p, v) in zip(params, inputs):
        if (p in params[:3]):
            matches = self.rank(v, self.accounts[p])
            if (p == params[(len(inputs) - 1)]):
                entries = []
                for m in matches:
                    account = m
                    icon = './icon.png'
                    if (p != 'payee'):
                        account_type = m.split(':')[0]
                        if (account_type in self.settings['icons']):
                            icon = self.settings['icons'][account_type]
                    elif (m in self.accounts['mapping']):
                        account = self.accounts['mapping'][m]
                    values[p] = account
                    entries.append({'title': account, 'subtitle': self.format_desc(values), 'autocomplete': account, 'valid': False, 'icon': icon})
                return entries
            else:
                account = matches[0]
                if ((p == 'payee') and (account in self.accounts['mapping'])):
                    account = self.accounts['mapping'][account]
                values[p] = account
        elif (p == 'amount'):
            values[p] = float(v)
        elif (p == 'tags'):
            values[p] = ('#' + ' #'.join(v.split('+')))
        else:
            values[p] = v
    values['date'] = datetime.now().strftime('%Y-%m-%d')
    entry = '\n'.join([self.settings['title_format'].format(**values).strip(), self.settings['body_format'].format(account=values['from'], flow=(- values['amount']), currency=self.settings['default_currency']), self.settings['body_format'].format(account=values['to'], flow=values['amount'], currency=self.settings['default_currency'])])
    return [{'title': 'New ${amount:.2f} Entry {tags}'.format(**values), 'subtitle': self.format_desc(values), 'valid': True, 'arg': entry, 'text': entry}]
