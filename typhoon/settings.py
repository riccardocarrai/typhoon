"""
Django settings for typhoon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bnwe+jlr_!ehxaxaxwb#57=q1x_zdw2q!w6jkdytu=nt$x&!v@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prodotti',
    'anagrafiche',
    'catalogo',
    'catalogo.templatetags',
    'widget_tweaks',
    'django_bootstrap_breadcrumbs',
    'merged_inlines',


)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'typhoon.urls'

WSGI_APPLICATION = 'typhoon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
    #'default': {
     #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
      #  'NAME': 'typhoon1',
       # 'USER': 'riccardocarrai',
        #'PASSWORD': '9212Mistic',
        #'HOST': ''
    #}
#}

#DATABASES = {
 #       'default': {
  #              'ENGINE': 'django.db.backends.mysql',
   #             'NAME': 'typhoon',
    #            'USER': 'administrator',
     #           'PASSWORD': 'IronEagles0803',
      #		'OPTIONS': {
       #   		 "init_command": "SET storage_engine=MyISAM",
   		# }
	 #}
#}

DATABASES = {
    'default':{
       'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : os.path.join(BASE_DIR, 'typhoon.db')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'it-it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


STATIC_URL = '/static/'
#STATICFILES_DIRS = (('static', os.path.join(BASE_DIR, 'static')),)
#STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__),'static'),)
STATICFILES_DIRS = (os.path.join(BASE_DIR,  'static'),)
TEMPLATE_DIRS =(BASE_DIR+'/static/templates/',)
MEDIA_ROOT=(BASE_DIR+'/static/media/')
STATIC_ROOT = '/var/www/typhoon/static/'