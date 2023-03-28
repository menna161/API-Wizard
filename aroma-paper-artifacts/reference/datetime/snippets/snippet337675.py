import pdb
import os
from time import sleep
from shutil import rmtree
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction
import datetime
import time
import os
from glob import glob


def main():
    user = os.environ['USER']
    news_cache_search_path = '/Users/{}/Library/Developer/CoreSimulator/Devices/{}/data/Containers/Data/Application/*/Library/Caches/News'.format(user, udid)
    try:
        news_cache_path = glob(news_cache_search_path)[0]
        wipe_app_data_folder(news_cache_path)
    except:
        print("Couldn't find cache folder")
    if (not os.path.exists(output_folder)):
        os.makedirs(output_folder)
    print('Opening app...')
    try:
        driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', desired_capabilities={'app': APP_PATH, 'deviceName': device_name_and_os, 'udid': udid, 'automationName': 'XCUITest', 'platformName': 'iOS', 'platformVersion': device_os, 'noReset': True, 'locationServicesEnabled': True, 'gpsEnabled': True})
    except:
        print('Error! You probably need to start appium!')
        exit()
    time_st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    date_st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    sleep(6)
    try:
        top_stories = get_top_stories(driver)
        top_links = links_from_strings(top_stories)
        top_line = (('{},'.format(time_st) + ','.join(top_links)) + '\n')
        print('Top: {}'.format(top_line))
        top_file_path = '{}/top-{}.csv'.format(output_folder, date_st)
        with open(top_file_path, 'a') as out:
            out.write(top_line)
        print('Scrolling to trending stories...')
        trending_stories = get_trending_stories(driver)
        trending_links = links_from_strings(trending_stories)
        trending_line = (('{},'.format(time_st) + ','.join(trending_links)) + '\n')
        print('Trending: {}'.format(trending_line))
        trending_file_path = '{}/trending-{}.csv'.format(output_folder, date_st)
        with open(trending_file_path, 'a') as out:
            out.write(trending_line)
    except:
        print('Problem at time {}'.format(time_st))
    driver.close_app()
    driver.quit()
