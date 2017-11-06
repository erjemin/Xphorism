# -*- coding: utf-8 -*-
"""
Django settings for  project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#%c&f7*18tr9o5j@&8lvj&luf3fv%=!tj+-2%dljzt^4fav!ab'

# SECURITY WARNING: don't run with debug turned on in production!
if (socket.gethostname() == 'T201') or \
   (socket.gethostname() == 'fatal1ty') or \
   (socket.gethostname() == "E-SIEMENS"):
    # DEBUG = TEMPLATE_DEBUG = True
    DEBUG = True
else:
    # DEBUG = TEMPLATE_DEBUG = False
    DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',            # Allow domain and subdomains
    'localhost',
    '192.168.1.11',         # для консольного тестирования через manager.py
    'x.cube2.ru',           # деплой
]

# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# sys.path.append(os.path.join(BASE_DIR, 'Xphorism'))

ADMINS = (
    ('Sergey Erjemin', 'erjemin@gmail.com'),
    # ('еще кто-то', 'e-serg@mail.ru'),
)

#########################################
# настройки для почтового сервера
EMAIL_HOST  = 'smtp.mail.ru' # SMTP server
EMAIL_PORT  = 2525 # для SSL/https
EMAIL_HOST_USER = u'что-то@что-то.ru' # login if requared or ''
EMAIL_HOST_PASSWORD = u'ОЧенЬ_Секретный_Пароль'       # password
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True

EMAIL_SUBJECT_PREFIX = 'Xphorism ERR: ' # префикс email-аллертов для оповещений об ошибках и необработанных исключениях
SITE_ID = 1
DEFAULT_INDEX_TABLESPACE = ''
# MANAGERS будут извещены о "битых" ссылках.
MANAGERS = ADMINS

# test (инструкция появилась в django 1.7
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'Xphorism',
    'app',
    'django.contrib.humanize',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # для управления  X-Frame-Options в HTTP-заголовках
]

X_FRAME_OPTIONS = 'ALLOW' # разрешить отображение во фрейме через X-Frame-Options в HTTP-заголовке

ROOT_URLCONF = 'Xphorism.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #    'django_jinja.loaders.AppLoader',
            #    'django_jinja.loaders.FileSystemLoader',
            # ]
        },
    },
]

WSGI_APPLICATION = 'Xphorism.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'ru-RU'         # <--------- RUSSIAN
TIME_ZONE = 'Europe/Moscow'     # <--------- RUSSIAN (MOSCOW)
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if (socket.gethostname() == 'T201') or \
        (socket.gethostname() == 'fatal1ty') or \
        (socket.gethostname() == "E-SIEMENS"):
    # накстройки для разработческих машинок.
    STATIC_BASE_PATH = 'C:/Users/Sergei/Cloud_Mail.ru/PRJ/PRJ Aphorism/Xphorism/public/static'
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        STATIC_BASE_PATH + '/js',
        STATIC_BASE_PATH + '/img',
        STATIC_BASE_PATH + '/fonts',
        STATIC_BASE_PATH + '/css',
        STATIC_BASE_PATH + '/svg',
    )
    MY_SITE_ROOT = 'C:/Users/Sergei/Cloud_Mail.ru/PRJ/PRJ Aphorism/Xphorism/'
    MEDIA_ROOT = 'C:/Users/Sergei/Cloud_Mail.ru/PRJ/PRJ Aphorism/Xphorism/public/media'
    # MEDIA_ROOT  = os.path.dirname(BASE_DIR) + '/media/'
    # настройки WYSIWYG-редактора
    # REDACTOR_UPLOAD = 'public/media/'  # папка для upload файлов WYSIWYG-редактора
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',        # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',             # Set to empty string for default. Not used with sqlite3.
            'NAME': 'django_xphorism',  # Not used with sqlite3.
            'USER': 'udb_xphorism',            # Not used with sqlite3.
            'PASSWORD': '!2#4%6&8',     # Not used with sqlite3.
            # 'OPTIONS': { 'autocommit': True, }
        }
    }
elif (socket.gethostname() == 'debian01'):
    # настройки для микросервера E450
    STATIC_ROOT = '/home/eserg/x.cube2.ru/public/static'
    MEDIA_ROOT  = '/home/eserg/x.cube2.ru/public/public/media/'
    MY_SITE_ROOT= '/home/eserg/x.cube2.ru/public/'
    STATIC_BASE_PATH = STATIC_ROOT
    STATICFILES_DIRS = (
        STATIC_BASE_PATH + '/js',
        STATIC_BASE_PATH + '/img',
        STATIC_BASE_PATH + '/fonts',
        STATIC_BASE_PATH + '/css',
        STATIC_BASE_PATH + '/svg',
    )
    # REDACTOR_UPLOAD = 'public/media/'  # папка для upload файлов WYSIWYG-редактора
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',        # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',             # Set to empty string for default. Not used with sqlite3.
            'NAME': 'django_xphorism',  # Not used with sqlite3.
            'USER': 'udb_xphorism',     # Not used with sqlite3.
            'PASSWORD': '!2#4%6&8',     # Not used with sqlite3.

        }
    }
else:
    STATIC_ROOT = os.path.dirname(BASE_DIR) + '/public/static/'
    MEDIA_ROOT = os.path.dirname(BASE_DIR) + '/public/media/'
    MY_SITE_ROOT = os.path.dirname(BASE_DIR) + '/public/'
    STATIC_BASE_PATH = STATIC_ROOT
    REDACTOR_UPLOAD = ''  # папка для upload файлов WYSIWYG-редактора
    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases
    DATABASES = {
        'default': {
            # для SQLite3
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db_oknardia.sqlite3'),
            # для MySQL
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',             # Set to empty string for default. Not used with sqlite3.
            'NAME': 'django_xphorism',  # Not used with sqlite3.
            'USER': 'udb_xphorism',     # Not used with sqlite3.
            'PASSWORD': '!2#4%6&8',     # Not used with sqlite3.

        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# подключить дополнительные переменные необходимые для текущего приложения (если они есть)
# try:
#     from Xphorism.settings_app import *
# except Exception as e:
#     pass
#  ___    ____      _              _____         _ _              _____             _
# | | |  |    \ ___| |_ _ _ ___   |_   _|___ ___| | |_ ___ ___   |  _  |___ ___ ___| |
# |_  |  |  |  | -_| . | | | . |    | | | . | . | | . | .'|  _|  |   __| .'|   | -_| |
#   |_|  |____/|___|___|___|_  |    |_| |___|___|_|___|__,|_|    |__|  |__,|_|_|___|_|
#                          |___|
INTERNAL_IPS = ['127.0.0.1', '::1']
INSTALLED_APPS += [ 'debug_toolbar' ]
MIDDLEWARE += [ 'debug_toolbar.middleware.DebugToolbarMiddleware' ]
DEBUG_TOOLBAR_PANELS = [
#    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
     ]
# DEBUG_TOOLBAR_CONFIG = {
#         'EXCLUDE_URLS': ('/admin',), # не работает, но в разработке есть...
#         'INTERCEPT_REDIRECTS': False,
#     }