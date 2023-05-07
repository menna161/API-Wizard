import argparse
import codecs
import datetime
import json
import os
import sys
import time
import subprocess
from xml.dom.minidom import parseString
from instagram_private_api import ClientError
from instagram_private_api import Client
import urllib.request as urllib
from instagram_private_api import Client, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError, __version__ as client_version
import urllib as urllib
import sys
from instagram_private_api import Client, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError, __version__ as client_version


def get_media_story(user_to_check, user_id, ig_client, taken_at=False, no_video_thumbs=False, hq_videos=False):
    global download_dest
    if (hq_videos and command_exists('ffmpeg')):
        print('[I] Downloading high quality videos enabled. Ffmpeg will be used.')
        print(('-' * 70))
    elif (hq_videos and (not command_exists('ffmpeg'))):
        print('[W] Downloading high quality videos enabled but Ffmpeg could not be found. Falling back to default.')
        hq_videos = False
        print(('-' * 70))
    try:
        try:
            feed = ig_client.user_story_feed(user_id)
        except Exception as e:
            print(('[W] An error occurred trying to get user feed: ' + str(e)))
            return
        try:
            feed_json = feed['reel']['items']
            open('feed_json.json', 'w').write(json.dumps(feed_json))
        except TypeError as e:
            print('[I] There are no recent stories to process for this user.')
            return
        list_video_v = []
        list_video_a = []
        list_video = []
        list_image = []
        list_video_new = []
        list_image_new = []
        for media in feed_json:
            if (not taken_at):
                taken_ts = None
            elif media.get('imported_taken_at'):
                imported_taken_at = media.get('imported_taken_at', '')
                if (imported_taken_at > 10000000000):
                    imported_taken_at /= 1000
                taken_ts = ((datetime.datetime.utcfromtimestamp(media.get('taken_at', '')).strftime('%Y-%m-%d_%H-%M-%S') + '__') + datetime.datetime.utcfromtimestamp(imported_taken_at).strftime('%Y-%m-%d_%H-%M-%S'))
            else:
                taken_ts = datetime.datetime.utcfromtimestamp(media.get('taken_at', '')).strftime('%Y-%m-%d_%H-%M-%S')
            is_video = (('video_versions' in media) and ('image_versions2' in media))
            if ('video_versions' in media):
                if hq_videos:
                    video_manifest = parseString(media['video_dash_manifest'])
                    video_period = video_manifest.documentElement.getElementsByTagName('Period')
                    representations = video_period[0].getElementsByTagName('Representation')
                    video_url = representations[0].getElementsByTagName('BaseURL')[0].childNodes[0].nodeValue
                    audio_element = representations.pop()
                    if (audio_element.getAttribute('mimeType') == 'audio/mp4'):
                        audio_url = audio_element.getElementsByTagName('BaseURL')[0].childNodes[0].nodeValue
                    else:
                        audio_url = 'noaudio'
                    list_video_v.append([video_url, taken_ts])
                    list_video_a.append(audio_url)
                else:
                    list_video.append([media['video_versions'][0]['url'], taken_ts])
            if ('image_versions2' in media):
                if ((is_video and (not no_video_thumbs)) or (not is_video)):
                    list_image.append([media['image_versions2']['candidates'][0]['url'], taken_ts])
        if hq_videos:
            print('[I] Downloading video stories. ({:d} stories detected)'.format(len(list_video_v)))
            print(('-' * 70))
            for (index, video) in enumerate(list_video_v):
                filename = video[0].split('/')[(- 1)]
                if taken_at:
                    try:
                        final_filename = (video[1] + '.mp4')
                    except:
                        final_filename = (filename.split('.')[0] + '.mp4')
                        (print('[E] Could not determine timestamp filename for this file, using default: ') + final_filename)
                else:
                    final_filename = (filename.split('.')[0] + '.mp4')
                save_path_video = ((download_dest + '/stories/{}/'.format(user_to_check)) + final_filename.replace('.mp4', '.video.mp4'))
                save_path_audio = save_path_video.replace('.video.mp4', '.audio.mp4')
                save_path_final = save_path_video.replace('.video.mp4', '.mp4')
                if (not os.path.exists(save_path_final)):
                    print('[I] ({:d}/{:d}) Downloading video: {:s}'.format((index + 1), len(list_video_v), final_filename))
                    try:
                        download_file(video[0], save_path_video)
                        if (list_video_a[index] == 'noaudio'):
                            has_audio = False
                        else:
                            has_audio = True
                            download_file(list_video_a[index], save_path_audio)
                        ffmpeg_binary = os.getenv('FFMPEG_BINARY', 'ffmpeg')
                        if has_audio:
                            cmd = [ffmpeg_binary, '-loglevel', 'fatal', '-y', '-i', save_path_video, '-i', save_path_audio, '-c:v', 'copy', '-c:a', 'copy', save_path_final]
                        else:
                            cmd = [ffmpeg_binary, '-loglevel', 'fatal', '-y', '-i', save_path_video, '-c:v', 'copy', '-c:a', 'copy', save_path_final]
                        fnull = None
                        exit_code = subprocess.call(cmd, stdout=fnull, stderr=subprocess.STDOUT)
                        if (exit_code != 0):
                            print("[W] FFmpeg exit code not '0' but '{:d}'.".format(exit_code))
                            os.remove(save_path_video)
                            if has_audio:
                                os.remove(save_path_audio)
                            return
                        else:
                            os.remove(save_path_video)
                            if has_audio:
                                os.remove(save_path_audio)
                            list_video_new.append(save_path_final)
                    except Exception as e:
                        print(('[W] An error occurred while iterating HQ video stories: ' + str(e)))
                        exit(1)
                else:
                    print('[I] Story already exists: {:s}'.format(final_filename))
        else:
            print('[I] Downloading video stories. ({:d} stories detected)'.format(len(list_video)))
            print(('-' * 70))
            for (index, video) in enumerate(list_video):
                filename = video[0].split('/')[(- 1)]
                if taken_at:
                    try:
                        final_filename = (video[1] + '.mp4')
                    except:
                        final_filename = (filename.split('.')[0] + '.mp4')
                        (print('[E] Could not determine timestamp filename for this file, using default: ') + final_filename)
                else:
                    final_filename = (filename.split('.')[0] + '.mp4')
                save_path = ((download_dest + '/stories/{}/'.format(user_to_check)) + final_filename)
                if (not os.path.exists(save_path)):
                    print('[I] ({:d}/{:d}) Downloading video: {:s}'.format((index + 1), len(list_video), final_filename))
                    try:
                        download_file(video[0], save_path)
                        list_video_new.append(save_path)
                    except Exception as e:
                        print(('[W] An error occurred while iterating video stories: ' + str(e)))
                        exit(1)
                else:
                    print('[I] Story already exists: {:s}'.format(final_filename))
        print(('-' * 70))
        print('[I] Downloading image stories. ({:d} stories detected)'.format(len(list_image)))
        print(('-' * 70))
        for (index, image) in enumerate(list_image):
            filename = image[0].split('/')[(- 1)].split('?', 1)[0]
            if taken_at:
                try:
                    final_filename = (image[1] + '.jpg')
                except:
                    final_filename = (filename.split('.')[0] + '.jpg')
                    (print('[E] Could not determine timestamp filename for this file, using default: ') + final_filename)
            else:
                final_filename = (filename.split('.')[0] + '.jpg')
            save_path = ((download_dest + '/stories/{}/'.format(user_to_check)) + final_filename)
            if (not os.path.exists(save_path)):
                print('[I] ({:d}/{:d}) Downloading image: {:s}'.format((index + 1), len(list_image), final_filename))
                try:
                    download_file(image[0], save_path)
                    list_image_new.append(save_path)
                except Exception as e:
                    print(('[W] An error occurred while iterating image stories: ' + str(e)))
                    exit(1)
            else:
                print('[I] Story already exists: {:s}'.format(final_filename))
        if ((len(list_image_new) != 0) or (len(list_video_new) != 0)):
            print(('-' * 70))
            print((((('[I] Story downloading ended with ' + str(len(list_image_new))) + ' new images and ') + str(len(list_video_new))) + ' new videos downloaded.'))
        else:
            print(('-' * 70))
            print('[I] No new stories were downloaded.')
    except Exception as e:
        print(('[E] A general error occurred: ' + str(e)))
        exit(1)
    except KeyboardInterrupt as e:
        print('[I] User aborted download.')
        exit(1)
