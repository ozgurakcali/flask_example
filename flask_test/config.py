#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


class Config(object):
    DEBUG = False
    PORT = 5000
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, '../flask-test.sqlite')


class Development(Config):
    SECRET_KEY = '05fb5bd20d648695a4b2796631a38e5307ca4ecbfc3db793'
    DEBUG = True


class Production(Config):
    SECRET_KEY = '4732b7281d9ba1e4411ba03b1c3bd927130ded246f28c645'


class Testing(Config):
    SECRET_KEY = 'd64ad70f1372c3819cd7f9e3e5550ce2f3aea44ed0a63484'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.PROJECT_ROOT, '../unit-tests.sqlite')
    TESTING = True
