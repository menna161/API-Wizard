from __future__ import print_function
import logging
import requests
from bs4 import BeautifulSoup
from six.moves.urllib import parse as urlparse


def find_feeds(url, check_all=False, user_agent=None, timeout=None):
    finder = FeedFinder(user_agent=user_agent, timeout=timeout)
    url = coerce_url(url)
    text = finder.get_feed(url)
    if (text is None):
        return []
    if finder.is_feed_data(text):
        return [url]
    logging.info('Looking for <link> tags.')
    tree = BeautifulSoup(text, 'html.parser')
    links = []
    for link in tree.find_all('link'):
        if (link.get('type') in ['application/rss+xml', 'text/xml', 'application/atom+xml', 'application/x.atom+xml', 'application/x-atom+xml']):
            links.append(urlparse.urljoin(url, link.get('href', '')))
    urls = list(filter(finder.is_feed, links))
    logging.info('Found {0} feed <link> tags.'.format(len(urls)))
    if (len(urls) and (not check_all)):
        return sort_urls(urls)
    logging.info('Looking for <a> tags.')
    (local, remote) = ([], [])
    for a in tree.find_all('a'):
        href = a.get('href', None)
        if (href is None):
            continue
        if (('://' not in href) and finder.is_feed_url(href)):
            local.append(href)
        if finder.is_feedlike_url(href):
            remote.append(href)
    local = [urlparse.urljoin(url, l) for l in local]
    urls += list(filter(finder.is_feed, local))
    logging.info('Found {0} local <a> links to feeds.'.format(len(urls)))
    if (len(urls) and (not check_all)):
        return sort_urls(urls)
    remote = [urlparse.urljoin(url, l) for l in remote]
    urls += list(filter(finder.is_feed, remote))
    logging.info('Found {0} remote <a> links to feeds.'.format(len(urls)))
    if (len(urls) and (not check_all)):
        return sort_urls(urls)
    fns = ['atom.xml', 'index.atom', 'index.rdf', 'rss.xml', 'index.xml', 'index.rss']
    urls += list(filter(finder.is_feed, [urlparse.urljoin(url, f) for f in fns]))
    return sort_urls(urls)
