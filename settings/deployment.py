from .base import *

import django_heroku

ALLOWED_HOSTS = ['bloom-main.herokuapp.com']


django_heroku.settings(locals())
