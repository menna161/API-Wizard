import requests
from dao.es_dao import es_connect
import re
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from elasticsearch import helpers

if (__name__ == '__main__'):
    import time
    from datetime import datetime
    from bs4 import BeautifulSoup
    from elasticsearch import helpers
    ct = datetime.now()
    es = es_connect()
    st = time.time()
    data_source = run_spider()
    transformer(data_source)
    print(ct)
    print('time used:{}'.format((time.time() - st)))
