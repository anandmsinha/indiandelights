from .base import *
import os

DEBUG = True

TEMPLATE_DEBUG = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

INSTALLED_APPS += (
    'debug_toolbar',
)

JQUERY_URL = '/static/js/jquery.min.js'