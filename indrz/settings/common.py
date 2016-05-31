import os

try:
    from settings import secret_settings
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


SECRET_KEY = secret_settings.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['campus.wu.ac.at', ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    #### third party apps
    'rest_framework',
    'taggit',
    'mptt',


    ##### our local indrz apps
    'api',
    'maps',
    'buildings',
    'routing',
    'conference',
    'poi_manager',
    'homepage',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'indrz.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates'),
                 os.path.join(BASE_DIR,  'maps/templates'),
                 os.path.join(BASE_DIR,  'poi_manager/templates'),
                 os.path.join(BASE_DIR,  'homepage/templates'),
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            # not needed if APP_DIRS is true
            # 'loaders':[(
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',)]
        },
    },
]


WSGI_APPLICATION = 'indrz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
    'default': {
        # Postgresql with PostGIS
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'indrz', # DB name
        'USER': secret_settings.db_user, # DB user name
        'PASSWORD': secret_settings.db_pwd, # DB user password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

POSTGIS_VERSION = ( 2, 1 )

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('fr', 'French'),)

# Location of translation files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_FOLDER = 'static'
STATIC_ROOT = "/var/www/vhosts/campus.wu.ac.at/static/"

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, STATIC_FOLDER),
]

# finds all static folders in all apps
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

# LOGGING_CONFIG = None

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file_verbose': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR,  'logs/verbose.log'),
#             'formatter': 'verbose'
#         },
#         'file_debug': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR,  'logs/debug.log'),
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file_verbose'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#         'api': {
#             'handlers': ['file_debug'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'admin': {
#             'handlers': ['file_debug'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'buildings': {
#             'handlers': ['file_debug'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'routing': {
#             'handlers': ['file_debug'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'maps': {
#             'handlers': ['file_debug'],
#             'propagate': True,
#             'level': 'DEBUG',
#         }
#
#     }
# }

# import logging.config
# logging.config.dictConfig(LOGGING)