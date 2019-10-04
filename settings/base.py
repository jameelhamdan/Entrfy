import os
import neomodel.config as neo4j
import mongoengine
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'this_is_a_secret_key_please_keep_it_very_secret')

# Expiration in days
TOKEN_EXPIRATION_PERIOD = 14

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

NEOMODEL_CYPHER_DEBUG = 1

ALLOWED_HOSTS = ['127.0.0.1']
APPEND_SLASH = False

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'auth',
    'main',
    'chat',
]

MIDDLEWARE = [
    # Must be at top
    'auth.backend.middleware.AuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}


# Internationalization
LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'UTC'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'neo4j': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# neomodel_install_labels manage.py auth.models --db bolt://neo4j:1234@localhost:7687
NEO4J_DATABASE_URL = os.environ.get('NEO4J_DATABASE_URL', '')
neo4j.DATABASE_URL = NEO4J_DATABASE_URL

# mongodb connection
MONGO_DATABASE_URL = os.environ.get('MONGO_DATABASE_URL', '')
mongoengine.connect('mongo_db', host=MONGO_DATABASE_URL, alias='default')
