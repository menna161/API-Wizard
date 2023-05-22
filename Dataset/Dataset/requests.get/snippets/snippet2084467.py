import getopt
import sys
import time
import webbrowser
import requests
from bs4 import BeautifulSoup


def download(show_name, quality, start_ep, end_ep, req_file, sleep_time=0.5):
    search_url = url.format(show_name, '{}')
    start_ep = int(start_ep)
    end_ep = int(end_ep)
    episodes_to_download = ((end_ep - start_ep) + 1)
    for page_number in range(1, 100):
        page_url = search_url.format(page_number)
        page_html = requests.get(page_url)
        soup = BeautifulSoup(page_html.text, 'html.parser')
        rows = soup.find_all('tr', class_='success')
        for row in rows:
            row_contents = row.findAll('a')
            links = row.find_all('td', class_='text-center')[0].find_all('a')
            magnet = ((base_url + links[0]['href']) if req_file else links[1]['href'])
            for content in row_contents:
                if (content.has_attr('title') and (show_name.upper() in content['title'].upper())):
                    row_title = content['title'].split(' ')
                    try:
                        if ((start_ep <= float(row_title[(- 2)]) <= end_ep) and (quality in row_title[(- 1)])):
                            print(('Opening: ' + content['title']))
                            webbrowser.open(magnet)
                            episodes_to_download -= 1
                            time.sleep(sleep_time)
                    except:
                        pass
        if ((soup.find('li', class_='active') is None) or (page_number != int(soup.find('li', class_='active').text)) or (episodes_to_download == 0)):
            break
    print('Complete.')
    if (episodes_to_download > 0):
        print('{} episode(s) could not be loaded.'.format(episodes_to_download))
