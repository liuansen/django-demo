# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rp2pkz^a2lwv!^hmt3$kit)1w20svk+$uidasigf%yy0q@ok4a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'thunder/templates')
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_mobile.context_processors.flavour',
            ],
            'loaders':(
                ('django_mobile.loader.CachedLoader', (
                    'django_mobile.loader.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                    # 'django.template.loaders.eggs.Loader',
                )),
            ),
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'oauth2_provider',
    'django_mobile',
    'accounts',
    'common',
    'we_media',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'thunder.urls'

WSGI_APPLICATION = 'thunder.wsgi.application'

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thunder',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {'charset': 'utf8mb4',
                    'init_command': "SET sql_mode = 'STRICT_TRANS_TABLES', innodb_strict_mode = 1"},
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'critical': '10/hour',  # 同一个ip，调用api次数限制
        'traffic_exchange': '10/hour',
        'mobile_captcha': '10/hour',
        'check_mobile': '10/hour',
    },
    'DEFAULT_PAGINATION_CLASS':
        'common.utils.CustomPaginationSerializer',
    'PAGE_SIZE': 20,                 # Default to 10
    'page_size_query_param': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'max_page_size': 100,            # Maximum limit allowed when using `?page_size=xxx`.
    'UNICODE_JSON': False,
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
}


from rest_framework.fields import DateTimeField


def to_representation(self, value):
    from rest_framework.settings import api_settings
    from django.utils import six
    if not value:
        return None

    output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

    if output_format is None or isinstance(value, six.string_types):
        return value

    return value.strftime(output_format)
DateTimeField.to_representation = to_representation


SWAGGER_SETTINGS = {
    "SUPPORTED_SUBMIT_METHODS": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'DOC_EXPANSION': 'None',
    'APIS_SORTER': 'alpha',
    'JSON_EDITOR': True,
    'SHOW_REQUEST_HEADERS': True,
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected/')

# 自定义User models字段
AUTH_USER_MODEL = 'accounts.User'
DEFAULT_CHARSET = 'utf-8'

ENABLE_ENCRYPTION = True

try:
    from local_settings import *
except ImportError:
    pass
