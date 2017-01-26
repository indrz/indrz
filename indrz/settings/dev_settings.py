# -*- coding: utf-8 -*-
import os
from .common_settings import *

DEBUG = True

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, 'homepage/static')

]

WU_IP_STARTSWITH = "137.208."
LOCALHOST_URL = "http://localhost:8000/"

DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'indrz-wu', # DB name
        'USER': secret_settings.db_user, # DB user name
        'PASSWORD': secret_settings.db_pwd, # DB user password
        'HOST': 'gis-neu.wu.ac.at',
        'PORT': '5432',
    }
}


# django-debug-toolbar
# ------------------------------------------------------------------------------
# MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar', )
# INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
#
# DEBUG_TOOLBAR_CONFIG = {
#     'DISABLE_PANELS': [
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#     ],
#     'SHOW_TEMPLATE_CONTEXT': True,
# }
# DATABASES = {
#     'default': {
#         # Postgresql with PostGIS
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'indrz-wu', # DB name
#         'USER': secret_settings.db_user, # DB user name
#         'PASSWORD': secret_settings.db_pwd, # DB user password
#         'HOST': 'localhost',
#         'PORT': '5434',
#     }
# }

if os.path.isdir('../logs'):
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
