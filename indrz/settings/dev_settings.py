# -*- coding: utf-8 -*-
import os
from .common_settings import *

DEBUG = True


DATABASES = {
    'default': {
        # Postgresql 9.5 with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'indrz-wu', # DB name
        'USER': 'indrz-wu', # DB user name
        'PASSWORD': 'air', # DB user password
        'HOST': 'localhost',
        'PORT': '5434',
    }
}

POSTGIS_VERSION = ( 2, 2, 2 )


LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file_verbose': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,  'logs/verbose.log'),
            'formatter': 'verbose'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,  'logs/debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file_verbose'],
            'propagate': True,
            'level':'DEBUG',
        },
        'api': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'admin': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'buildings': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'routing': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'maps': {
            'handlers': ['file_debug'],
            'propagate': True,
            'level': 'DEBUG',
        }

    }
}

import logging.config
logging.config.dictConfig(LOGGING)