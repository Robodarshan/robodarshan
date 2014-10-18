"""
Django settings for robodarshan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&vu7pnsbbb8mcooj@wz(6z^)=ters+f3)dt@zx&6xyw8jj+0i#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'kombu.transport.django',
    'djcelery', 
    'accounts',
    'blog',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'robodarshan.urls'

WSGI_APPLICATION = 'robodarshan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'productiondb.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

# Media files (User Uploaded Content)

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Login Url

LOGIN_URL = '/accounts/login/'

# Custom User Model

AUTH_USER_MODEL = 'accounts.robodarshanMember'
AUTH_PROFILE_MODULE = 'accounts.Profile'

# Email smtp setup

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ghoshbinayak@gmail.com'
EMAIL_HOST_PASSWORD = 'rujufhjzhcvevjix'


# Flatpages setup
SITE_ID = 1
 

# Celery setup
BROKER_URL = "django://"
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

# Host base url
HOST_BASE_URL = "http://robodarshan.herokuapp.com/"
