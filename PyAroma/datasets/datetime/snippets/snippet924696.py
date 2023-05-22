import argparse
import datetime
import os
import sys
import time
from instabot import Bot


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-u', type=str, help='username')
    parser.add_argument('-p', type=str, help='password')
    parser.add_argument('-proxy', type=str, help='proxy')
    parser.add_argument('-message', type=str, nargs='?', help='message text', default='Hi, thanks for reaching me')
    args = parser.parse_args()
    bot = Bot()
    bot.login(username=args.u, password=args.p, proxy=args.proxy)
    start_time = datetime.datetime.utcnow()
    while True:
        try:
            new_followers = get_recent_followers(bot, start_time)
        except ValueError as err:
            print(err)
            time.sleep(RETRY_DELAY)
            continue
        if new_followers:
            print('Found new followers. Count: {count}'.format(count=len(new_followers)))
        for follower in new_followers:
            print('New follower: {}'.format(follower['username']))
            bot.send_message(args.message, str(follower['user_id']))
        start_time = datetime.datetime.utcnow()
        time.sleep(DELAY)
