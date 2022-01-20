from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fa_*+n_#92(-c#cht2eexo-z(=5alcp+1#d3yw@t97ys#xf1t*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SHOPIFY_API_KEY = '65cdfeaa66aba266d5f37b2ecf831fb3'
SHOPIFY_API_SECRET = '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'

# Application definition

INSTALLED_APPS = [
    'orderprocessing.apps.OrderprocessingConfig',
    'slackbot.apps.SlackbotConfig',
    'shopify_app.apps.ShopifyAppConfig',
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'reports.apps.ReportsConfig',
    'warehouse.apps.WarehouseConfig',
    'dashboard.apps.DashboardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shopify_app.middleware.LoginProtection',
]

ROOT_URLCONF = 'stockroom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'stockroom/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'warehouse.context_processors.all_warehouse',
            ],
        },
    },
]

WSGI_APPLICATION = 'stockroom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stockroomdb',
        'USER': 'postgres',
        'PASSWORD': 'basedata',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'stockroom/static')
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SLACK API Configurations
# ----------------------------------------------
# use your keys
VERIFICATION_TOKEN = 'tKDQ9EHwBZpcDCiFxSoBPY6H'
OAUTH_ACCESS_TOKEN = 'xoxp-1160741229927-2927562415123-2913192058551-146963152d0243cb325b588f1d52fd36'
CLIENT_ID = '1160741229927.2951481346768'
CLIENT_SECRET = '32310bd8d3e8db0763ac037f96b268fa'
BOT_USER_ACCESS_TOKEN = 'xoxb-1160741229927-2930106095572-IR0auNuQUDvjoUSdwd34ZQTq'


try:
    from .local_settings import *
except ImportError:
    pass
