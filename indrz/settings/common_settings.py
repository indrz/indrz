import os

try:
    from settings import secret_settings
except ImportError:
    from indrz.settings import secret_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = secret_settings.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [ ]


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
    'rest_framework_gis',
    'taggit',
    'mptt',
    'rest_framework_swagger',
    'rosetta',


    ##### our local indrz apps
    'api',
    # 'maps',
    'buildings',
    'routing',
    'conference',
    'poi_manager',
    'landscape',
    'homepage',
    'homepage.library',
    'homepage.kiosk'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
                 # os.path.join(BASE_DIR,  'maps/templates'),
                 os.path.join(BASE_DIR,  'poi_manager/templates'),
                 os.path.join(BASE_DIR,  'homepage/templates'),
                 os.path.join(BASE_DIR,  'homepage/library/templates'),
                 os.path.join(BASE_DIR,  'homepage/kiosk/templates'),
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
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
        'NAME': 'indrz', # DB name Redhat live server
        'USER': secret_settings.db_user, # DB user name
        'PASSWORD': secret_settings.db_pwd, # DB user password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

POSTGIS_VERSION = ( 2, 2, 0 )

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
STATIC_ROOT = "/var/www/vhosts/www.indrz.com/static/"

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
UPLOAD_POI_DIR = MEDIA_ROOT + '/poi-icons/'

ROSETTA_MESSAGES_PER_PAGE = 20
YANDEX_TRANSLATE_KEY = "trnsl.1.1.20160713T103415Z.0a117baa17b2233a.fb58b4876ab2920ea22ae0a0b55507319bb4a0db"
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True