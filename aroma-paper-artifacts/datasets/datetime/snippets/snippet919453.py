import os, ast, json
from datetime import datetime, timedelta
import dns.resolver


def __save_json(self, term_type, data):
    d = (datetime.today() - timedelta(days=2))
    save_path = './data/json_files/{}'.format(d.strftime('%Y-%m-%d'))
    if (not os.path.exists(save_path)):
        os.makedirs(save_path)
    f = open('{directory}/{term}'.format(directory=save_path, term=term_type), 'w+')
    f.write(json.dumps(data))
    f.close()
