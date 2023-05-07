from flask import Flask, redirect, session, request, render_template, url_for, flash, jsonify, send_file, make_response
from helpers.s3 import S3
from helpers.constants import Constants
from helpers.githubuser import GithubUser, PublicGithubUser
from helpers.githubbot import GithubBot
from helpers.sources.osenv import OSConstants
from helpers.sources.mongo import MongoConstants
from helpers.extensions import LanguageExtensions
import os, time, datetime


@app.route('/redirect/<path:object_key>')
def redirect_view(object_key):
    url = s3.get_url(object_key, constants.get('EXPIRES'), force_http=(constants.get('HTTP') == 'true'))
    response = redirect((url if url else url_for('pending_view', object_key=object_key)))
    return cached(response, datetime.datetime.utcnow(), expires=0)
