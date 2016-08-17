# -*- coding: utf-8 -*-
import os
from .common_settings import *


ALLOWED_HOSTS = ['indrz', 'api.indrz.com', ]

DEBUG = False
TEMPLATE_DEBUG = DEBUG

from .common_settings import *

DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'indrz', # DB name local
        'NAME': 'indrz-wu', # DB name Redhat live server
        'USER': secret_settings.db_user, # DB user name
        'PASSWORD': secret_settings.db_pwd, # DB user password
        'HOST': 'gis-neu.wu.ac.at',
        'PORT': '5432',
    }
}

POSTGIS_VERSION = ( 2, 2, 1 )


STATIC_ROOT = "/var/www/vhosts/www.indrz.com/static/"

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, 'homepage/static')

]