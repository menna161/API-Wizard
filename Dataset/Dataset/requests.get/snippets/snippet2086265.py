import os, unittest, threading, subprocess, json, tempfile, os
import wsgiref.validate
import wsgiref.simple_server
import cherrypy, urllib.request, urllib.parse, urllib.error, requests
import gnubg
import webapp as gw
import common as gc
import gnubg.webapp


def test_access(self):
    out = requests.get(SERVER_URL)
    self.assertEqual(out.status_code, 200)
