# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + os.sep
__author__ = ('hughson.simon@gmail.com (Hughson Simon)')
# Activate django-dbindexer for the default database
#DATABASES['native'] = DATABASES['default']
#DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'


import os
if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
    os.getenv('SETTINGS_MODE') == 'prod'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': 'saltwaterfishdb:saltwaterfish2',
            'NAME': 'saltwaterfishnew_db',
        }
    }
else:
    # Running in development, so use a local MySQL database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
			'NAME': 'newdatabase',
            #'NAME': 'saltwaterfish',
        }
    }
SETTINGS_MODE='prod' 
SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'
#SETTINGS_MODE='prod' python manage.py syncdb
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
	'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangotoolbox',
    'autoload',
    'dbindexer',
	'admin',
	

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
	#'pagination',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
	'django.contrib.sessions.middleware.SessionMiddleware',
    'autoload.middleware.AutoloadMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	#'pagination.middleware.PaginationMiddleware',
)
MEDIA_ROOT = 'assets/'
MEDIA_URL = 'assets/'
STATIC_URL = '/misc'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
    'django.core.context_processors.request',
    'django.core.context_processors.media',
	'django.contrib.messages.context_processors.messages',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

LOGOUT_URL = '/logout'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
	#'django.template.loaders.eggs.Loader',
	#'django.template.loaders.app_directories.load_template_source',
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

PAYPAL_URL  = 'https://www.sandbox.paypal.com/us/cgi-bin/webscr'
PAYPAL_MERCHANT_EMAIL = 'swfmerchant@expertsden.com'
if(os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine')):
    
    CALLBACK_URL = 'http://saltwaterfish-com.appspot.com/checkoutcallback'
    PAYPAL_CANCEL_URL = 'http://saltwaterfish-com.appspot.com/viewcart'
else:
    CALLBACK_URL = 'http://localhost:8000/checkoutcallback'
    PAYPAL_CANCEL_URL = 'http://localhost:8000/viewcart'
 

AUTHORIZENET_API_LOGIN_ID = "2SzzM45p"
AUTHORIZENET_API_PASSWORD = "425hScrL9qHX37g3"
TEST_MODE = False  # Change it to False when transaction has to record in Sandbox Instance. You will get Transaction ID.
TEST_MODE_URL = True # Boolean Value for Authorize.net to call Production URL or Sandbox URL.

