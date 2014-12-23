from .base import *
import os

DEBUG = True

TEMPLATE_DEBUG = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

JQUERY_URL = '/static/js/jquery.min.js'