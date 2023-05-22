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


def reached_limit(self, key):
    current_date = datetime.datetime.now()
    passed_days = (current_date.date() - self.start_time.date()).days
    if (passed_days > 0):
        self.reset_counters()
    return ((self.max_per_day[key] - self.total[key]) <= 0)
