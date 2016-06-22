# -*- coding: utf-8 -*-
import os
from .common_settings import *

DEBUG = True


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