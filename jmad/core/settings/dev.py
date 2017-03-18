# include from settings/base.py
from .base import *
from core.helpers import get_secret


# DEBUG CONFIGURATION
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# END DEBUG CONFIGURATION


# APPLICATIONS CONFIGURATION
INSTALLED_APPS += []

# END APPLICATIONS CONFIGURATION


# DATABASE CONFIGURATION
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DATABASE_NAME', SITE_DIR),
        'USER': get_secret('DATABASE_USER', SITE_DIR),
        'PASSWORD': get_secret('DATABASE_PASSWORD', SITE_DIR),
        'HOST': 'localhost',
        'PORT': '',
    }
}
# END DATABASE CONFIGURATION


# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# END EMAIL CONFIGURATION


