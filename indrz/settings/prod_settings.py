# -*- coding: utf-8 -*-
import os
from settings.common_settings import *


ALLOWED_HOSTS = ['campus.wu.ac.at', 'gis-neu.ac.at', ]

DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'indrz', # DB name local
        'NAME': 'indrz-wu', # DB name Redhat live server
        'USER': secret_settings.db_user, # DB user name
        'PASSWORD': secret_settings.db_pwd, # DB user password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

POSTGIS_VERSION = ( 2, 2, 1 )

WU_IP_STARTSWITH = "137.208."
LOCALHOST_URL = "http://gis-neu.wu.ac.at/"  # http://campus.wu.ac.at


STATIC_ROOT = "/opt/django-deploy/indrz/static/"

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, 'homepage/static'),
    os.path.join(BASE_DIR, 'static/admin'),
    os.path.join(BASE_DIR, 'static/gis')

]

MEDIA_URL = "/media/"
MEDIA_ROOT = "/opt/django-deploy/indrz/media"
UPLOAD_POI_DIR = MEDIA_ROOT + '/poi-icons/'