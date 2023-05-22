import argparse
import datetime
import os
import sys
import time
from instabot import Bot


def get_recent_followers(bot, from_time):
    followers = []
    ok = bot.api.get_recent_activity()
    if (not ok):
        raise ValueError('failed to get activity')
    activity = bot.api.last_json
    for feed in [activity['new_stories'], activity['old_stories']]:
        for event in feed:
            if event.get('args', {}).get('text', '').endswith('started following you.'):
                follow_time = datetime.datetime.utcfromtimestamp(event['args']['timestamp'])
                if (follow_time < from_time):
                    continue
                followers.append({'user_id': event['args']['profile_id'], 'username': event['args']['profile_name'], 'follow_time': follow_time})
    return followers
