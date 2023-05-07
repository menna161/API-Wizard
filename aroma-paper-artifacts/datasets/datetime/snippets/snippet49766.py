from flask import Flask, redirect, session, request, render_template, url_for, flash, jsonify, send_file, make_response
from helpers.s3 import S3
from helpers.constants import Constants
from helpers.githubuser import GithubUser, PublicGithubUser
from helpers.githubbot import GithubBot
from helpers.sources.osenv import OSConstants
from helpers.sources.mongo import MongoConstants
from helpers.extensions import LanguageExtensions
import os, time, datetime


@app.route('/pending/<path:object_key>')
def pending_view(object_key):
    response = render_template('pending.html', object_key=object_key, bucket=constants.get('AWS_BUCKET'), time=time.time())
    return cached(response, datetime.datetime.utcnow(), expires=0)
