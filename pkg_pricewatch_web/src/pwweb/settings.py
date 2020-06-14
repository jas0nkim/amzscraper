"""
Django settings for pwweb project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import configparser

APP_DATA_DIRPATH = '/usr/local/etc/pricewatch/'
APP_DIST_DIRPATH = APP_DATA_DIRPATH + 'dist/'
APP_CONFIG_FILEPATH = APP_DATA_DIRPATH + 'pricewatch.ini'

# django model statuses
SCHEDULES_JOB_STATUS_CANCELED = 0
SCHEDULES_JOB_STATUS_PENDING = 1
SCHEDULES_JOB_STATUS_RUNNING = 2
SCHEDULES_JOB_STATUS_FINISHED = 3

SCHEDULES_VERSION_STATUS_DELETED = 0
SCHEDULES_VERSION_STATUS_ADDED = 1

RESOURCES_LISTING_ITEM_STATUS_GOOD = 1000
RESOURCES_LISTING_ITEM_STATUS_INACTIVE = 1001
RESOURCES_LISTING_ITEM_STATUS_INVALID_SKU = 1002
RESOURCES_LISTING_ITEM_STATUS_SKU_NOT_IN_VARIATION = 1003
RESOURCES_LISTING_ITEM_STATUS_NO_PRICE_GIVEN = 1004
RESOURCES_LISTING_ITEM_STATUS_OUT_OF_STOCK = 1005
RESOURCES_LISTING_ITEM_STATUS_PARSING_FAILED_UNKNOWN_ERROR = 1006

RESOURCES_LISTING_ITEM_STATUS_STR_SET = {
    RESOURCES_LISTING_ITEM_STATUS_GOOD: 'Good',
    RESOURCES_LISTING_ITEM_STATUS_INACTIVE: 'Inactive',
    RESOURCES_LISTING_ITEM_STATUS_INVALID_SKU: 'Invalid SKU',
    RESOURCES_LISTING_ITEM_STATUS_SKU_NOT_IN_VARIATION: 'SKU not in variation',
    RESOURCES_LISTING_ITEM_STATUS_NO_PRICE_GIVEN: 'No price',
    RESOURCES_LISTING_ITEM_STATUS_OUT_OF_STOCK: 'Out of stock',
    RESOURCES_LISTING_ITEM_STATUS_PARSING_FAILED_UNKNOWN_ERROR: 'Parsing failed',
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    config = configparser.ConfigParser()
    config.read(APP_CONFIG_FILEPATH)
except Exception as e:
    raise Exception("Failed to get database connection information - {}".format(str(e)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['PriceWatchWeb']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config['PriceWatchWeb']['debug']
DEBUG = True

ALLOWED_HOSTS = config['PriceWatchWeb']['allowed_hosts'].split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django-rest-framework.org
    'rest_framework',

    # pwweb.* apps
    'pwweb.resources.apps.ResourcesConfig',
    'pwweb.schedules.apps.SchedulesConfig',
    'pwweb.reports.apps.ReportsConfig',
    'pwweb.frontend.apps.FrontendConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pwweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/pwweb/templates/',
        ],
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

WSGI_APPLICATION = 'pwweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'OPTIONS': {
    #         'read_default_file': '/usr/local/etc/my_pwbot.cnf', # has mysql connect information, and so on - macos
    #         # 'read_default_file': 'C:\ProgramData\MySQL\MySQL Server 8.0\my_amzscraper.ini', # has mysql connect information, and so on - windows 10
    #     },
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config['Postgres']['database'],
        'USER': config['Postgres']['user'],
        'PASSWORD': config['Postgres']['password'],
        'HOST': config['Postgres']['host'],
        'PORT': config['Postgres']['port'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{name}] {levelname} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'graypy': {
            'level': 'ERROR',
            'class': 'graypy.GELFUDPHandler',
            'formatter': 'verbose',
            'host': config['Graylog']['host'],
            'port': int(config['Graylog']['port']),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['graypy'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

LOGIN_REDIRECT_URL = 'home'

# django rest framework settings
REST_FRAMEWORK = {
    # production only
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_AUTHENTICATION_CLASSES': [

    # ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
}

## amazon.com related
AMAZON_COM_ITEM_LINK_PATTERN = r'^(https?://www.amazon.com)?/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'
AMAZON_ITEM_LINK_FORMAT = 'https://www.{}/dp/{}{}'
AMAZON_ITEM_VARIATION_LINK_POSTFIX = '/?th=1&psc=1'
## amazon.ca related
AMAZON_CA_ITEM_LINK_PATTERN = r'^(https?://www.amazon.ca)?/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'
## walmart.com related
WALMART_COM_ITEM_LINK_PATTERN = r'^(https?://www.walmart.com)?/([^/]+/[^/]+|ip)/([A-Z0-9]{8,15})(/.*$)?'
WALMART_COM_ITEM_LINK_FORMAT = 'https://www.{}/ip/{}{}'
WALMART_COM_ITEM_VARIATION_LINK_POSTFIX = '?selected=true'
## walmart.ca related
WALMART_CA_ITEM_LINK_PATTERN = r'^(https?://www.walmart.ca)?/(en|fr)/([^/]+/[^/]+|ip)/([A-Z0-9]{8,15})(/.*$)?'
WALMART_CA_ITEM_LINK_FORMAT = 'https://www.{}/en/ip/{}'
WALMART_CA_API_ITEM_PRICE_LINK_FORMAT = 'https://www.walmart.ca/api/product-page/price-offer#{}'
WALMART_CA_API_ITEM_FIND_IN_STORE_LINK = 'https://www.walmart.ca/api/product-page/find-in-store'
WALMART_CA_API_ITEM_FIND_IN_STORE_LINK_FORMAT = '{store_link}?latitude={lat}&longitude={lng}&lang=en&upc={upc}#{pid}'

## canadiantire.ca related
CANADIANTIRE_CA_ITEM_LINK_PATTERN = r'^(https?://www.canadiantire.ca)?/(en|fr)/([^/]+/[^/]+|pdp)/([\w-]*)([0-9]{7,12})p*.html[.*$]?'
CANADIANTIRE_CA_ITEM_LINK_FORMAT = 'https://www.{}/en/pdp/{}.html'
CANADIANTIRE_CA_API_STORES_LINK = 'https://api-triangle.canadiantire.ca/dss/services/v4/stores'
CANADIANTIRE_CA_API_STORES_LINK_FORMAT = '{stores_link}?lang=en&radius=1000&maxCount=12&storeType=store&lat={lat}&lng={lng}#{pid}'
CANADIANTIRE_CA_API_ITEM_PRICE_LINK = 'https://www.canadiantire.ca/ESB/PriceAvailability'
CANADIANTIRE_CA_API_ITEM_PRICE_LINK_FORMAT = '{price_link}?SKU={sku}&Store={store}&Banner=CTR&Language=E#{pid}'
