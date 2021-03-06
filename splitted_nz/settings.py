import os
#import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8ace3072-47a0-4910-b522-dc3601f38c35'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','localhost','farges.ddns.net','192.168.1.18']
INTERNAL_IPS = ('0.0.0.0','127.0.0.1','localhost',)

INSTALLED_APPS = [
    'splitted_nz',
    'photo_gallery',
    # 'geoloc_data',
    'geodata',
    'leaflet',
    'djgeojson',
    'material',
    'material.admin',
    'import_export',
    'imagekit',
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites'
    ]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'splitted_nz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'photo_gallery.context_processors.articles',
            ],
        },
    },
]

WSGI_APPLICATION = 'splitted_nz.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'splitted_nz',
#         'USER': 'fritzip',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

DATA_UPLOAD_MAX_NUMBER_FIELDS = 30240 

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/admin/'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'NZ'

USE_I18N = False

USE_L10N = True

# USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/1.8/howto/static-files/deployment/
# python manage.py collectstatic
#STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static/']))
STATIC_ROOT = BASE_DIR + '/static/'

MEDIA_URL = '/media/'
#MEDIA_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['media/']))
MEDIA_ROOT = BASE_DIR + '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

LEAFLET_CONFIG = {
    # 'DEFAULT_CENTER': (-43.5, 172.6),
    # 'DEFAULT_ZOOM': 7,
    # 'MIN_ZOOM': 2,
    # 'MAX_ZOOM': 19,
    'RESET_VIEW': False,
    # 'TILES': []
    # 'TILES': [('Outdoor', 'https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=868563c2a5a94440bbad18257a5d9bc1', {'attribution': '&copy; Thunderforest'})]
}