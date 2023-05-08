import re, time
import database_auth
import archiveis
import datetime


def update_tweet(id):
    sql = (((('update mimic_tweets set erased = 1, 7c0_tweeted = 1, timestamp_erased = "' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '" where idTweets = "') + id) + '";')
    db = database_auth.conecta_banco()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except Exception as E:
        print(E)
    db.commit()
    db.close()
