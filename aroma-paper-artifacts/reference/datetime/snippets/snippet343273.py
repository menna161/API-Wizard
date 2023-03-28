import archon.feeds.cryptocompare as cc
import archon.feeds.coinmarketcap as cmc
import json
import pickle
from datetime import datetime
from pymongo import MongoClient


def pull_listings():
    db = client['coinmarketcap']
    col = db.coins
    r = cmc.get_listings_all()
    now = datetime.now()
    s = now.strftime('%Y%m%d_%H%M%S')
    allkeys = ['id', 'name', 'symbol', 'slug', 'circulating_supply', 'total_supply', 'max_supply', 'date_added', 'num_market_pairs', 'tags', 'platform', 'cmc_rank', 'last_updated', 'quote']
    for x in r:
        cid = col.insert_one(x).inserted_id
        print('inserted ', cid)
