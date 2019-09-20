from .base import *

import django_heroku

ALLOWED_HOSTS = ['entrfy-main.herokuapp.com']


django_heroku.settings(locals())
