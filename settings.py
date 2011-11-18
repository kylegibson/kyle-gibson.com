import sys
from path import path

PROJECT_ROOT = path(__file__).abspath().dirname()
sys.path.append(PROJECT_ROOT / 'apps')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

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

STATIC_ROOT = PROJECT_ROOT / "assets"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '_@snir48qagdu2__bbfv9r!2pib+yw9(w01(f--@vix0d_l!#c'

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

ROOT_URLCONF = 'kylegibson.urls'

TEMPLATE_DIRS = (
    PROJECT_ROOT / "apps",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
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
