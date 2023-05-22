import asyncio
import logging
import os
import re
import time
import requests
from trivia.game import TriviaGame
from trivia.models import Player, commit, db_session


def send_pushover(message):
    app_token = os.getenv('PUSHOVER_APP_TOKEN')
    user_token = os.getenv('PUSHOVER_USER_TOKEN')
    if ((app_token is not None) and (user_token is not None)):
        logger.info(f'Notifying admin: {message}.')
        url = f'https://api.pushover.net/1/messages.json'
        requests.post(url, data={'token': app_token, 'user': user_token, 'message': message})
