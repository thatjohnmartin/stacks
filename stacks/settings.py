import os

STACKS_ROOT = os.environ['STACKS_ROOT']
IS_LOCAL = 'STACKS_LOCAL' in os.environ

DEBUG = int(os.environ.get('STACKS_DEBUG', IS_LOCAL))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('John Martin', 'john@lonepixel.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'stacks',                      # Or path to database file if using sqlite3.
        'USER': 'stacksuser',                      # Not used with sqlite3.
        'PASSWORD': 'stacksuser',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': os.environ.get('STACKS_CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache' if IS_LOCAL else 'django.core.cache.backends.memcached.MemcachedCache'),
        'LOCATION': os.environ.get('STACKS_CACHE_LOCATION', '' if IS_LOCAL else '127.0.0.1:11211'),
        'TIMEOUT': 0,
    }
}

ALLOWED_HOSTS = [
    '.stcks.net'
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/var/stacks/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%%u-6vvmop1@cxqetfbyeg%7g8^k7v#xyb0z+c$6(a7zb0jk6h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'stacks.django_jinja.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'stacks.www.middleware.site_resolver.SiteResolverMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'stacks.urls'

TEMPLATE_DIRS = ()

JINJA2_TEMPLATE_DIRS = (
    os.path.join(STACKS_ROOT, "stacks/www/templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'stacks.www',
    'social_auth',
    'taggit',
    'compressor',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/start/'
LOGIN_ERROR_URL = '/login-error/'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter')

TWITTER_CONSUMER_KEY = 'KGWgTDLPg3srd4BA5zaEg'
TWITTER_CONSUMER_SECRET = 'TAREqhMLY9Q3wqdtZxKaksmREjjGu1hEgH45srLkSsc'

FLICKR_API_KEY = 'bd6c2ce4a4d1cd5252aa4f1f6b645100'
FLICKR_API_SECRET = '37f2aa730149f69c'

ENABLE_SCRAPER_CACHE = int(os.environ.get('STACKS_ENABLE_SCRAPER_CACHE', 1))

COMPRESS_ENABLED = os.environ.get('STACKS_COMPRESS_ENABLED', 0)
COMPRESS_ROOT = '/var/stacks'
COMPRESS_OUTPUT_DIR = 'cache'

COMPRESS_PRECOMPILERS = (
    ('text/less', '/usr/local/bin/lessc {infile} {outfile}'),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
)

LOG_FILE = os.environ.get('STACKS_LOG_ROOT', '/var/log/stacks/app.log')
ENABLE_SQL_LOGGING = int(os.environ.get('STACKS_ENABLE_SQL_LOGGING', 0))
ENABLE_CACHE_LOGGING = int(os.environ.get('STACKS_ENABLE_CACHE_LOGGING', 0))

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
        },
        'null': {
            'level': 'DEBUG',
            'class':'django.utils.log.NullHandler',
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if not ENABLE_SQL_LOGGING:
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['null'],  # Quiet by default!
        'propagate': False,
        'level':'DEBUG',
    }

# configure logging
import logging
from django.conf import settings

# logging level is INFO on production, DEBUG if local install
LOG_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
LOG_FORMAT = '%(asctime)s %(process)d %(filename)s(%(lineno)d): %(levelname)s %(message)s'

logging.basicConfig(filename=settings.LOG_FILE, filemode='a', level=LOG_LEVEL, format=LOG_FORMAT)