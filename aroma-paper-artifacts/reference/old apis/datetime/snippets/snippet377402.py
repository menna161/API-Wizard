from google.cloud import bigquery
from telegram.ext import Updater
import matplotlib.pyplot as plt
import numpy as np
import datetime


def main():
    updater = Updater('YOUR_TOKEN')
    updater.job_queue.run_daily(send_image, time=datetime.datetime.strptime('9:00AM', '%I:%M%p').time(), days=(0, 1, 2, 3, 4, 5, 6))
    updater.start_polling()
    updater.idle()
