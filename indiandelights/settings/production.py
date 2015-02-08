from .base import *
import os


SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [
    '.flavood.com',
    '.flavood.com.'
]

CONN_MAX_AGE = 60

TEMPLATE_LOADERS = (
    'django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ),
)