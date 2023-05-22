import json
import locale
import logging
from datetime import datetime
import requests
from PIL import Image, ImageFont


def ISOtoHuman(self, date: str, language: str):
    'Return the provided ISO8601 timestamp in human-readable format.'
    try:
        locale.setlocale(locale.LC_ALL, language)
    except locale.Error:
        log.warn(f'Unsupported locale configured, using system default')
    try:
        return datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %-d, %Y')
    except ValueError:
        try:
            return datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %#d, %Y')
        except Exception as e:
            log.error(self, f'Failed to convert to human-readable time, {e}')
