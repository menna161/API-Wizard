from flask import Flask, redirect, session, request, render_template, url_for, flash, jsonify, send_file, make_response
from helpers.s3 import S3
from helpers.constants import Constants
from helpers.githubuser import GithubUser, PublicGithubUser
from helpers.githubbot import GithubBot
from helpers.sources.osenv import OSConstants
from helpers.sources.mongo import MongoConstants
from helpers.extensions import LanguageExtensions
import os, time, datetime


def cached(response_data, since, expires=86400):
    response = make_response(response_data)
    response.headers['Last-Modified'] = since
    response.headers['Expires'] = (since + datetime.timedelta(seconds=expires))
    if (expires > 0):
        response.headers['Cache-Control'] = 'public, max-age={}'.format(expires)
    else:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    return response
