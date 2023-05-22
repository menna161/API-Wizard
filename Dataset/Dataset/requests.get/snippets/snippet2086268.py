import os, unittest, threading, subprocess, json, tempfile, os
import wsgiref.validate
import wsgiref.simple_server
import cherrypy, urllib.request, urllib.parse, urllib.error, requests
import gnubg
import webapp as gw
import common as gc
import gnubg.webapp


@classmethod
def tearDownClass(cls):
    cls.done_serving = True
    requests.get(SERVER_URL)
    process = get_launched_mysql_process()
    process.stdin.write((('DROP DATABASE ' + cls.DB_NAME) + ';\n'))
    process.stdin.close()
    process.wait()
