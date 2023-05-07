import os
import pickle
from datetime import datetime


def __init__(self, bot):
    self.total = {}
    for k in bot.total:
        self.total[k] = bot.total[k]
    self.blocked_actions = {}
    for k in bot.blocked_actions:
        self.blocked_actions[k] = bot.blocked_actions[k]
    self.start_time = bot.start_time
    self.date = datetime.now()
    self.total_requests = bot.api.total_requests
