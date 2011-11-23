import sys
from path import path

PROJECT_ROOT = path(__file__).abspath().dirname().dirname()
sys.path.append(PROJECT_ROOT / 'apps')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'db/dev.db',
    }
}

TIME_ZONE = 'America/Detroit'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False # internationalization 
USE_L10N = True # Format dates to current locale
MEDIA_ROOT = '' 
MEDIA_URL = ''

#STATIC_ROOT = PROJECT_ROOT / "static"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = [PROJECT_ROOT / "static"]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

try:
    SECRET_KEY = (PROJECT_ROOT / "SECRET_KEY").bytes().strip()
except IOError:
    try:
        import string
        from random import choice
        SECRET_KEY = ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])
        (PROJECT_ROOT / "SECRET_KEY").write_bytes(SECRET_KEY)
    except IOError:
        pass

TEMPLATE_LOADERS = (
    'djaml.filesystem',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT / "apps",
    PROJECT_ROOT / "templates",
)

INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'tastypie',
    'blog',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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
