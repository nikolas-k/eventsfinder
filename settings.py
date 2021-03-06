from djangoappengine.settings_base import *
import os

DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alejandro Saucedo', 'axsauze@gmail.com'),
)

MANAGERS = ADMINS

#Use email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'wakeuproulette@gmail.com'
EMAIL_HOST_PASSWORD = 'wakeup!!'

ALLOWED_HOSTS = [ '.events-finder.appspot.com/']

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# Use optimizations
USE_I18N = True

# Django should format dates
USE_L10N = True

# Application is not timezone aware
USE_TZ = False

APPEND_SLASH = True

# Media files
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'media'))
MEDIA_URL = '/media/'
MAX_UPLOAD_SIZE = 20971520
CONTENT_TYPES = ['image/jpeg', 'image/png']

# Static Files
STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



INSTALLED_APPS = (
    'django.contrib.admin',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djangotoolbox',
    'autoload',
    'dbindexer',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',

    'eventsfinder',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nqc8l#-7^n-$v^ls=v%t#1pq&j(i__heue^xvjhdt=om5!98#!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    "eventsfinder.ef_context.in_prod",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'eventsfinder.urls'

TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'templates'))
)
