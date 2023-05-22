import atexit
import datetime
import logging
import os
import random
import signal
import time
from instabot import utils
from ..api import API
from .state.bot_state import BotState
from .state.bot_cache import BotCache
from .bot_archive import archive, archive_medias, unarchive_medias
from .bot_block import block, block_bots, block_users, unblock, unblock_users
from .bot_checkpoint import load_checkpoint, save_checkpoint
from .bot_comment import comment, comment_geotag, comment_hashtag, comment_medias, comment_user, comment_users, is_commented, reply_to_comment
from .bot_delete import delete_comment, delete_media, delete_medias
from .bot_direct import approve_pending_thread_requests, send_hashtag, send_like, send_media, send_medias, send_message, send_messages, send_photo, send_profile
from .bot_filter import check_media, check_not_bot, check_user, filter_medias
from .bot_follow import approve_pending_follow_requests, follow, follow_followers, follow_following, follow_users, reject_pending_follow_requests
from .bot_get import convert_to_user_id, get_archived_medias, get_comment, get_comment_likers, get_geotag_medias, get_geotag_users, get_hashtag_medias, get_hashtag_users, get_last_user_medias, get_link_from_media_id, get_locations_from_coordinates, get_media_commenters, get_media_comments, get_media_comments_all, get_media_id_from_link, get_media_info, get_media_likers, get_media_owner, get_messages, get_pending_follow_requests, get_pending_thread_requests, get_popular_medias, get_self_story_viewers, get_timeline_medias, get_timeline_users, get_total_hashtag_medias, get_total_user_medias, get_user_followers, get_user_following, get_user_id_from_username, get_user_info, get_user_likers, get_user_medias, get_user_reel, get_user_stories, get_user_tags_medias, get_username_from_user_id, get_your_medias, search_users, get_muted_friends
from .bot_like import like, like_comment, like_followers, like_following, like_geotag, like_hashtag, like_location_feed, like_media_comments, like_medias, like_timeline, like_user, like_users
from .bot_photo import download_photo, download_photos, upload_photo, upload_album
from .bot_stats import save_user_stats
from .bot_story import download_stories, upload_story_photo, watch_users_reels
from .bot_support import check_if_file_exists, console_print, extract_urls, read_list_from_file
from .bot_unfollow import unfollow, unfollow_everyone, unfollow_non_followers, unfollow_users
from .bot_unlike import unlike, unlike_comment, unlike_media_comments, unlike_medias, unlike_user
from .bot_video import download_video, upload_video
from pip._vendor import pkg_resources
import pkg_resources


def __init__(self, base_path=(current_path + '/config/'), whitelist_file='whitelist.txt', blacklist_file='blacklist.txt', comments_file='comments.txt', followed_file='followed.txt', unfollowed_file='unfollowed.txt', skipped_file='skipped.txt', friends_file='friends.txt', proxy=None, max_likes_per_day=random.randint(50, 100), max_unlikes_per_day=random.randint(50, 100), max_follows_per_day=random.randint(50, 100), max_unfollows_per_day=random.randint(50, 100), max_comments_per_day=random.randint(50, 100), max_blocks_per_day=random.randint(50, 100), max_unblocks_per_day=random.randint(50, 100), max_likes_to_like=random.randint(50, 100), min_likes_to_like=random.randint(50, 100), max_messages_per_day=random.randint(50, 100), filter_users=False, filter_private_users=False, filter_users_without_profile_photo=False, filter_previously_followed=False, filter_business_accounts=False, filter_verified_accounts=False, max_followers_to_follow=5000, min_followers_to_follow=10, max_following_to_follow=2000, min_following_to_follow=10, max_followers_to_following_ratio=15, max_following_to_followers_ratio=15, min_media_count_to_follow=3, max_following_to_block=2000, like_delay=random.randint(300, 600), unlike_delay=random.randint(300, 600), follow_delay=random.randint(300, 600), unfollow_delay=random.randint(300, 600), comment_delay=random.randint(300, 600), block_delay=random.randint(300, 600), unblock_delay=random.randint(300, 600), message_delay=random.randint(300, 600), stop_words=('shop', 'store', 'free'), blacklist_hashtags=['#shop', '#store', '#free'], blocked_actions_protection=True, blocked_actions_sleep=True, blocked_actions_sleep_delay=random.randint(600, 1200), verbosity=True, device=None, save_logfile=True, log_filename=None, loglevel_file=logging.DEBUG, loglevel_stream=logging.INFO, log_follow_unfollow=True):
    self.api = API(device=device, base_path=base_path, save_logfile=save_logfile, log_filename=log_filename, loglevel_file=loglevel_file, loglevel_stream=loglevel_stream)
    self.log_follow_unfollow = log_follow_unfollow
    self.base_path = base_path
    self.state = BotState()
    self.delays = {'like': like_delay, 'unlike': unlike_delay, 'follow': follow_delay, 'unfollow': unfollow_delay, 'comment': comment_delay, 'block': block_delay, 'unblock': unblock_delay, 'message': message_delay}
    self.filter_users = filter_users
    self.filter_private_users = filter_private_users
    self.filter_users_without_profile_photo = filter_users_without_profile_photo
    self.filter_business_accounts = filter_business_accounts
    self.filter_verified_accounts = filter_verified_accounts
    self.filter_previously_followed = filter_previously_followed
    self.max_per_day = {'likes': max_likes_per_day, 'unlikes': max_unlikes_per_day, 'follows': max_follows_per_day, 'unfollows': max_unfollows_per_day, 'comments': max_comments_per_day, 'blocks': max_blocks_per_day, 'unblocks': max_unblocks_per_day, 'messages': max_messages_per_day}
    self.blocked_actions_protection = blocked_actions_protection
    self.blocked_actions_sleep = blocked_actions_sleep
    self.blocked_actions_sleep_delay = blocked_actions_sleep_delay
    self.max_likes_to_like = max_likes_to_like
    self.min_likes_to_like = min_likes_to_like
    self.max_followers_to_follow = max_followers_to_follow
    self.min_followers_to_follow = min_followers_to_follow
    self.max_following_to_follow = max_following_to_follow
    self.min_following_to_follow = min_following_to_follow
    self.max_followers_to_following_ratio = max_followers_to_following_ratio
    self.max_following_to_followers_ratio = max_following_to_followers_ratio
    self.min_media_count_to_follow = min_media_count_to_follow
    self.stop_words = stop_words
    self.blacklist_hashtags = blacklist_hashtags
    self.max_following_to_block = max_following_to_block
    self.cache = BotCache()
    followed_file = os.path.join(base_path, followed_file)
    unfollowed_file = os.path.join(base_path, unfollowed_file)
    skipped_file = os.path.join(base_path, skipped_file)
    friends_file = os.path.join(base_path, friends_file)
    comments_file = os.path.join(base_path, comments_file)
    blacklist_file = os.path.join(base_path, blacklist_file)
    whitelist_file = os.path.join(base_path, whitelist_file)
    self.followed_file = utils.file(followed_file)
    self.unfollowed_file = utils.file(unfollowed_file)
    self.skipped_file = utils.file(skipped_file)
    self.friends_file = utils.file(friends_file)
    self.comments_file = utils.file(comments_file)
    self.blacklist_file = utils.file(blacklist_file)
    self.whitelist_file = utils.file(whitelist_file)
    self.proxy = proxy
    self.verbosity = verbosity
    self.logger = self.api.logger
    self.logger.info((('Instabot version: ' + version) + ' Started'))
    self.logger.debug('Bot imported from {}'.format(__file__))
