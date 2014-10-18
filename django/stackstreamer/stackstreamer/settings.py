"""
Django settings for stackstreamer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, os.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2i$3o(9&o4z45^=h#eml*u)34yv=z!22y8db9^c5(r5*bvb22o'

VIEWER_SECRET_KEY = 'r2o4rRGWnOhH8Nm38rAAE2F8DZztHpOHVOUSOouUw+M'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)


ALLOWED_HOSTS = []

is_volumetric = 'volumetric' in os.uname()
is_aeolos = 'aeolos' in os.uname()
is_stackstreamer = 'stackstreamer' in os.uname()
is_test = 'test' in os.uname()
is_demo = 'demo' in os.uname()

DATA_PATH = '/data/'
MEDIA_ROOT = '/web/django/media/'
MEDIA_URL = '/media/' 
VIEWER_URL = ''
if is_stackstreamer:
    VIEWER_URL = 'http://torres.stackstreamer.com/viewer/viewer.html'
elif is_test:
    VIEWER_URL = 'http://test.stackstreamer.com/viewer/viewer.html'
elif is_demo:
    VIEWER_URL = 'http://demo.stackstreamer.com/viewer/viewer.html'
# Application definition

INSTALLED_APPS = (
    'stackstreamer',
    'stackorg',
    'exportroi',
    'annotations',
    'tastypie',
    'sorl.thumbnail',
    'djcelery',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'stackstreamer.urls'

WSGI_APPLICATION = 'stackstreamer.wsgi.application'

BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
STATIC_ROOT = '/web/django/static'
