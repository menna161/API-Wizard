import time
import re
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from afterhours.utils import Settings, formatoutput, clean_df
from utils import Settings, formatoutput, clean_df


def secure_all_pages(self):
    '\n        iterate over all pages of price information for after hours trading,\n            secure data and store in pandas dataframe. Columns incude:\n                Time: datetime object of time stamps from trading\n                Price: price of trade\n                Volume: volume of shares\n                Ticker: Ticker symbol of stock\n\n        :return: cleaned dataframe containing\n        '
    if (not self.soup.find('table', {'id': Settings.settings['pricetable']})):
        raise ValueError('{} market data not available for {}'.format(self.typeof, self.ticker))
    table = self.soup.find('table', {'id': Settings.settings['pricetable']}).findAll('td')
    times = [datetime.strptime('{}-{}-{} {}'.format(self.month, self.day, self.year, rec.text), '%m-%d-%Y %H:%M:%S') for rec in table[::3]]
    prices = [float(Settings.price_finder.search(rec.text).group(0)) for rec in table[1::3]]
    volumes = [rec.text.replace(',', '') for rec in table[2::3]]
    tmpdf = pd.DataFrame({'Time': times, 'Price': prices, 'Volume': volumes})
    tmpdf['Ticker'] = self.ticker
    self.df = self.df.append(tmpdf)
    next_page_tag = self.soup.find('a', {'id': Settings.settings['nextpage']})
    if (next_page_tag and next_page_tag.has_attr('href')):
        next_page_link = next_page_tag['href']
        next_soup = BeautifulSoup(requests.get(next_page_link).content, 'html.parser')
        self.soup = next_soup
        self.secure_all_pages()
    else:
        self.soup = self.init
        self.df.drop_duplicates(keep='first', inplace=True)
        self.df = clean_df(self.df)
    return self.df
