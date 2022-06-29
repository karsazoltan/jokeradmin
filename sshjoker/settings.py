"""
Django settings for sshjoker project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from json import loads
from os.path import join, abspath, dirname
from pathlib import Path
from shutil import which

from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

PUBLIC_URL = 'joker.cloud.bme.hu/'
SITE_NAME = 'jokeradmin'
FROM_EMAIL = 'noreply@joker.cloud.bme.hu'

EMAIL_HOST_USER = 'jokermail@cloud.bme.hu'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_HOST = 'posta.ik.bme.hu'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = FROM_EMAIL
EMAIL_FOOTER = '\n\n -------------------------------------------- \n Kérem, erre az üzenetre ne válaszoljon - JOKER ' \
               'GÉPHÁZ '

KEYDIR = ''
# KEYDIR = '/usr/local/keys/'
# KEYDIR = '/home1/karsa/keys' #sudo crontab */2 * * * * cp -a /home1/karsa/keys/. /etc/ssh/authorized_keys/
# KEYDIR = '/etc/ssh/authorized_keys/'

MAXKEYNUM = 5

ROOT_GROUP = 'adm'
# ROOT_GROUP = 'root'
# ROOT_GROUP = 'wheel'

HOME_DIRECTORY = '/home1/'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

# redirect uname user to login page
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'joker.cloud.bme.hu',
    '127.0.0.1',
    'localhost'
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jokerauth',
    'projects',
    'users',
    'rest_framework',
    'djangosaml2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangosaml2.middleware.SamlSessionMiddleware'
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'users.backend.ModifiedSaml2Backend',
)

# BASE_DIR = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(BASE_DIR)
remote_metadata = join(SITE_ROOT, 'bme-metadata.xml')
required_attrs = loads('["niifPersonOrgID", "mail", "sn", "givenName"]')
optional_attrs = loads('{}')

SAML_CONFIG = {
    'xmlsec_binary': which('xmlsec1'),
    'entityid': PUBLIC_URL + 'saml2/metadata/',
    'attribute_map_dir': join(SITE_ROOT, 'attribute-maps'),
    'service': {
        'sp': {
            'name': SITE_NAME,
            'endpoints': {
                'assertion_consumer_service': [
                    ('https://' + PUBLIC_URL + 'saml2/acs/', BINDING_HTTP_POST),
                ],
                'single_logout_service': [
                    ('https://' + PUBLIC_URL + 'saml2/ls/', BINDING_HTTP_REDIRECT),
                ],
            },
            'required_attributes': required_attrs,
            'optional_attributes': optional_attrs,
            'want_response_signed': False,
        },
    },
    'metadata': {'local': [remote_metadata], },
    'key_file': join(SITE_ROOT, 'samlcert.key'),  # private part
    'cert_file': join(SITE_ROOT, 'samlcert.pem'),  # public part
    'encryption_keypairs': [{
        'key_file': join(SITE_ROOT, 'samlcert.key'),  # private part
        'cert_file': join(SITE_ROOT, 'samlcert.pem'),  # public part
    }]
}

SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = loads(
    '{"mail": ["email"], "sn": ["last_name"], '
    '"niifPersonOrgID": ["username"], "givenName": ["first_name"]}')
SAML_ORG_ID_ATTRIBUTE = 'niifPersonOrgID'

ROOT_URLCONF = 'sshjoker.urls'

# LOGIN_URL = 'https://login.bme.hu/Shibboleth.sso/Login'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sshjoker.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'jokeradmin',
#         'USER': os.environ['DB_USER'],
#         'PASSWORD': os.environ['DB_PASS'],
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
# CELERY_BROKER_URL = os.environ['BROKER_URL']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Budapest'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = '/var/www/html/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
