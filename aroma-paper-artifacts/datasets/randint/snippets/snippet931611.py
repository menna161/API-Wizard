import sys
import re
import random
import time
from multiprocessing import Queue, Pool
from PIL import Image
from douyin import CrawlerScheduler
from common import debug, config, screenshot
from common.auto_adb import auto_adb
from common import apiutil
from common.compression import crop_image


def main(queue):
    '\n    main\n    :return:\n    '
    print('程序版本号：{}'.format(VERSION))
    print('激活窗口并按 CONTROL + C 组合键退出')
    debug.dump_device_info()
    screenshot.check_screenshot()
    while True:
        next_page()
        time.sleep(random.randint(1, 5))
        screenshot.pull_screenshot()
        crop_image('douyin.png', 'optimized.png', config['crop_img']['x'], config['crop_img']['y'], config['crop_img']['width'], config['crop_img']['height'])
        with open('optimized.png', 'rb') as bin_data:
            image_data = bin_data.read()
        ai_obj = apiutil.AiPlat(AppID, AppKey)
        rsp = ai_obj.face_detectface(image_data, 0)
        major_total = 0
        minor_total = 0
        if (rsp['ret'] == 0):
            beauty = 0
            for face in rsp['data']['face_list']:
                msg_log = '[INFO] gender: {gender} age: {age} expression: {expression} beauty: {beauty}'.format(gender=face['gender'], age=face['age'], expression=face['expression'], beauty=face['beauty'])
                print(msg_log)
                with Image.open('optimized.png') as im:
                    crop_img = im.crop((face['x'], face['y'], (face['x'] + face['width']), (face['y'] + face['height'])))
                    crop_img.save(((FACE_PATH + face['face_id']) + '.png'))
                is_correct_gender = ((face['gender'] < 50) if (GENDER == 'female') else (face['gender'] > 50))
                if ((face['beauty'] > beauty) and is_correct_gender):
                    beauty = face['beauty']
                if (face['age'] > GIRL_MIN_AGE):
                    major_total += 1
                else:
                    minor_total += 1
            if ((beauty > BEAUTY_THRESHOLD) and (major_total > minor_total)):
                msg = ('发现漂亮妹子\x08👀' if (GENDER == 'female') else '发现帅气小哥👀')
                print(msg)
                thumbs_up()
                follow_user()
                share_video()
                left_swipe()
                video_url = copy_link()
                queue.put(video_url)
        else:
            print(rsp)
            continue
