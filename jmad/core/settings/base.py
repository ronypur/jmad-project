"""
Django settings for jmad project.

The settings files are divided into three part;
base, dev, test, and prod. This method is based on
"Two Scoops of Django: Best Practices for django 1.8"
book (https://www.twoscoopspress.com/).
"""

from os.path import abspath, basename, dirname, join


# PATH CONFIGURATION
# Path for django project
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
# Path for project root
SITE_DIR = dirname(BASE_DIR)
# Site name based on project dir name
SITE_NAME = basename(BASE_DIR)
# END PATH CONFIGURATION


# SECRET CONFIGURATION
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xv)hhranl0xmdqrr+u!0a*j@9dh%e!xnbc5!)xqg4mrip)plu4'
# END SECRET CONFIGURATION


# DEBUG CONFIGURATION
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# END DEBUG CONFIGURATION


# SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
# END SITE CONFIGURATION


# APPLICATIONS CONFIGURATION
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = []

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
# END APPLICATIONS CONFIGURATION


# MIDDLEWARE CONFIGURATION
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# END MIDDLEWARE CONFIGURATION


# URL CONFIGURATION
ROOT_URLCONF = '{}.urls'.format(SITE_NAME)
# END URL CONFIGURATION


# TEMPLATE CONFIGURATION
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
            ],
        },
    },
]
# END TEMPLATE CONFIGURATION


# WSGI CONFIGURATION
WSGI_APPLICATION = 'jmad.wsgi.application'
# END WSGI CONFIGURATION


# DATABASE CONFIGURATION
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
    }
}
# END DATABASE CONFIGURATION


# AUTH CONFIGURATION
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
# END AUTH CONFIGURATION


# GENERAL CONFIGURATION
# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# END GENREAL CONFIGURATION


# STATIC FILES CONFIGURATION
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
# END STATIC FILES CONFIGURATION
