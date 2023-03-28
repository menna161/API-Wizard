from telebot import TeleBot as tb
from telebot import types
import os
import config
import psutil
import glob
import subprocess
import time
import sqlite3
import hashlib
import audit_functions


@bot.message_handler(commands=['login'])
def vb_reply(message):
    try:
        a = str.replace(message.text, '/login ', '')
        MAS = a.encode('utf-8')
        hash = hashlib.md5(MAS).hexdigest()
        t = (hash,)
        conn = sqlite3.connect(config.adminBOTDB)
        c = conn.cursor()
        c.execute('SELECT login FROM users WHERE password = ?', t)
        login = c.fetchone()[0]
        t = (message.from_user.id, hash)
        c.execute("UPDATE users set last_login = datetime(CURRENT_TIMESTAMP, 'localtime'),user_chat_id = ? where password = ?", t)
        bot.send_message(message.from_user.id, ('Welcome ' + login))
        conn.commit()
        conn.close()
    except:
        bot.send_message(message.from_user.id, 'Wrong password, please enter again again')
