import os, unittest, threading, subprocess, json, tempfile, os
import wsgiref.validate
import wsgiref.simple_server
import cherrypy, urllib.request, urllib.parse, urllib.error, requests
import gnubg
import webapp as gw
import common as gc
import gnubg.webapp


def test_registration_nonmatching_passwords(self):
    username = '__test123__'
    password = '__test123__'
    out = requests.post((SERVER_URL + '/register'), data={'username': username, 'password': password, 'password_again': (password + ' ')})
    self.assertNotEqual(out.status_code, 200)
