"""
Default settings for project to create a new enviornment extends this file.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ozyh=iu^77^puy)jjxnry20#w$d&jy(%6!&o6n2n@iv6w(uf6('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.home',
    'apps.product',
    'apps.partners',
    'imagekit',
    'django_pickling', # for fast serialization and deserialization of django models.
    'bootstrapform',
    'mptt'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'indiandelights.urls'

WSGI_APPLICATION = 'indiandelights.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

AUTH_USER_MODEL = 'home.AppUser'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# General
APPEND_SLASH = True

# Error pages
handler404 = 'apps.home.views.not_found'
handler500 = 'apps.home.views.internal_server_error'

# Settings for imagekit - we want all images to be in one folder
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
IMAGEKIT_CACHEFILE_DIR = 'cache'
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.hash'

LOG_FOLDER = os.path.join(PROJECT_DIR, 'logs')
# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s.%(msecs)d %(name)s-%(levelname)s (%(filename)s:%(lineno)s %(funcName)s)]: %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_FOLDER, 'apps.log'),
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'apps.product': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'apps.home': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'apps.partners': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}