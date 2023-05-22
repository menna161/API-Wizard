import requests
import json
from datetime import datetime, timedelta


def disney_authentication():
    'Gets an authentication (access) token from Disney and returns it'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Accept-Language': 'en_US', 'Cache-Control': '0', 'Accept': 'application/json;apiversion=1', 'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive', 'Proxy-Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}
    auth = requests.get('https://disneyworld.disney.go.com/authentication/get-client-token', headers=headers, timeout=10).json()
    return (auth['access_token'], auth['expires_in'])
