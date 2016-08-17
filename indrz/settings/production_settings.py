# -*- coding: utf-8 -*-
import os
from .common_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG


STATIC_ROOT = "/var/www/vhosts/www.indrz.com/static/"

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, 'homepage/static')

]