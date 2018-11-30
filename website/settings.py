"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7+f*q&6@bznk#9-!8mrf+@5xxtusg*_-7y72r*l17(omwvdg+2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['s713ff3n.pythonanywhere.com']#iwedb.tk

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'import_export',
    'wind_farms',
    'django_tables2',
    'django_filters',
    'crispy_forms',
    'widget_tweaks',
    'player',
    'phonenumber_field',
    'graphos',
    'turbine',
    'projects',
    'account',
    'dal',
    'dal_select2',
    'django.contrib.admin',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'website.urls'

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

WSGI_APPLICATION = 'website.wsgi.application'

if DEBUG:

    INTERNAL_IPS = ['127.0.0.1']#, '10.0.0.21']
    MIDDLEWARE_CLASSES += (
       'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
       'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
	    'debug_toolbar.panels.timer.TimerPanel',
	    'debug_toolbar.panels.settings.SettingsPanel',
	    'debug_toolbar.panels.headers.HeadersPanel',
	    'debug_toolbar.panels.request.RequestPanel',
	    'debug_toolbar.panels.sql.SQLPanel',
	    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
	    'debug_toolbar.panels.templates.TemplatesPanel',
	    'debug_toolbar.panels.cache.CachePanel',
	    'debug_toolbar.panels.signals.SignalsPanel',
	    'debug_toolbar.panels.logging.LoggingPanel',
	    'debug_toolbar.panels.redirects.RedirectsPanel',
      #'debug_toolbar.panels.version.VersionDebugPanel',
      'debug_toolbar.panels.sql.SQLPanel',
      #'debug_toolbar.panels.timer.TimerDebugPanel',
      #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
      #'debug_toolbar.panels.templates.TemplatesPanel',
    )

    #DEBUG_TOOLBAR_CONFIG = {
    #       'INTERCEPT_REDIRECTS': False,
    #   }

    SHOW_TOOLBAR_CALLBACK = True

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'S713FF3N$default',
        'USER': 'S713FF3N',
        'PASSWORD': 'osna2166',
        'HOST': 'S713FF3N.mysql.pythonanywhere-services.com',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    #('de', _('German')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

IMPORT_EXPORT_USE_TRANSACTIONS = True

CRISPY_TEMPLATE_PACK = 'bootstrap'

GEOPOSITION_GOOGLE_MAPS_API_KEY = ''

from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('polls:home')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

EMAIL_HOST = "smtp.deutsche-windtechnik.com"#"smtp.gmail.com"
EMAIL_HOST_USER = "success-map@deutsche-windtechnik.com"#"stefschroedter@gmail.com"
EMAIL_HOST_PASSWORD = "Weltmeister@2018!"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "success-map@deutsche-windtechnik.com"

<<<<<<< HEAD
#AUTH_USER_MODEL = 'account.User'
=======
#AUTH_USER_MODEL = 'account.User'
>>>>>>> d7b98305b0c34c31a0569f26c2129e78a0d929ad
