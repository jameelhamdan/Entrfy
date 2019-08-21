import os
import neomodel.config as neo4j

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a9h)a4c!vqi)z!4ne5ni@iicf!j_iz4xua6e!$o33cqm#s+z*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
NEOMODEL_CYPHER_DEBUG = 1

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'auth',
    'main',
]

MIDDLEWARE = [
    'auth.middleware.AuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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
# neomodel_install_labels manage.py auth.models --db bolt://neo4j:1234@localhost:7687
neo4j.DATABASE_URL = 'bolt://neo4j:1234@localhost:7687'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    # ],
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
