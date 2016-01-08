"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import environ

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG
# ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')e-_u9#$xfu5(uw!izbq!yu+dtf1*ce5@7w42p^ro*i-+)$yy%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.tweet-search2.herokuapp.com',  
    '127.0.0.1', 
    'localhost', 
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'django.contrib.humanize',
    'social.apps.django_app.default',
    'south',
    'tags',
    'app',
    'home',
    'gnip_search'
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Uncomment for Heroku
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='sqlite://tweet-search.db')
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "static"),
)

# security: http://django-secure.readthedocs.org/en/latest/index.html
SECURE_HSTS_SECONDS = 31536000 
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# security: https://django-csp.readthedocs.org/en/latest/configuration.html#policy-settings
CSP_DEFAULT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", 'www.google-analytics.com', )
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", 'www.google-analytics.com', 'ajax.googleapis.com', )
CSP_FRAME_SRC = ("'self'", )
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", 'fonts.googleapis.com', )
CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com', )

SOCIAL_AUTH_LOGIN_URL          = '/login'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home'
SOCIAL_AUTH_LOGIN_ERROR_URL    = '/login-error/'

LOGIN_URL = '/login/twitter'

# Get your Twitter key/secret from https://apps.twitter.com/
SOCIAL_AUTH_TWITTER_KEY = environ.get('CONSUMER_KEY')               # Twitter API Consumer Key
SOCIAL_AUTH_TWITTER_SECRET = environ.get('CONSUMER_SECRET')         # Twitter API Consumer Secret

TWITTER_ACCESS_TOKEN = environ.get('ACCESS_TOKEN')                  # Twitter API Access Token
TWITTER_ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')    # Twitter API Access Secret

GNIP_USERNAME = environ.get('GNIP_USERNAME')                         # Gnip username
GNIP_PASSWORD = environ.get('GNIP_PASSWORD')                         # Gnip password
GNIP_SEARCH_ENDPOINT = environ.get('GNIP_SEARCH_ENDPOINT')                  # Gnip search endpoint


