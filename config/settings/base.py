import os
import environ

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Override in production via env

env = environ.Env(
    DATABASE_URL=(str, 'postgres://mfl:mfl@localhost:5432/mfl'),
    DEBUG=(bool, True),
    FRONTEND_URL=(str, "http://localhost:8062"),
    REALTIME_INDEX=(bool, False),
    HTTPS_ENABLED=(bool, False),
    SECRET_KEY=(str, 'p!ci1&ni8u98vvd#%18yp)aqh+m_8o565g*@!8@1wb$j#pj4d8'),
    EMAIL_HOST=(str, 'localhost'),
    EMAIL_HOST_USER=(str, 487),
    EMAIL_HOST_PASSWORD=(str, 'notarealpassword'),
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_STORAGE_BUCKET_NAME=(str, ''),
    STORAGE_BACKEND=(str, ''),
    ADMINS=(str, "admin:admin@example.com,"),
    SERVER_EMAIL=(str, "root@localhost"),
    ALLOWED_HOSTS=(str, "localhost"),
    DHIS_ENDPOINT=(str, "https://hiskenya.org/"),
    DHIS_USERNAME=(str, 'kmhfl_integration'),
    DHIS_PASSWORD=(str, ''),
    DHIS_CLIENT_ID=(str, 'KMHFL'),
    DHIS_CLIENT_SECRET=(str, '65df9a025-31df-079d-14d5-a01e08ea947')
)
env.read_env(os.path.join(BASE_DIR, '.env'))

ADMINS = tuple(
    tuple(name.split(':')) for name in env('ADMINS').split(',') if name != ''
)
SERVER_EMAIL = env('SERVER_EMAIL')


DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ENV_DB = env.db()
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': ENV_DB['HOST'],
        'NAME': ENV_DB['NAME'],
        'PASSWORD': ENV_DB['PASSWORD'],
        'PORT': ENV_DB['PORT'],
        'USER': ENV_DB['USER'],
    }
}  # Env should have DATABASE_URL
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',
)

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[Master Facility List] '

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',') + ['localhost', '127.0.0.1', '0.0.0.0',''
                                                                                       '29a4-102-208-44-38.ngrok-free.app']
# ALLOWED_HOSTS = ['.locahost', ' .health.go.ke', '198.199.125.166', 'api.kmhfltest.health.go.ke']

INSTALLED_APPS = (
    'django.contrib.sites',
    'users',
    'django.contrib.admin',
    'common',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_auth',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'corsheaders',
    #'rest_framework_swagger',
    'drf_yasg',
    'django.contrib.gis',
    'reversion',
    'gunicorn',
    'debug_toolbar',
    'storages',
    'django_filters',
    'facilities',
    'data_bootstrap',
    'chul',
    'mfl_gis',
    'search',
    'reporting',
    'admin_offices',
)
# LOCAL_APPS is now just a convenience setting for the metadata API
# It is *NOT* appended to INSTALLED_APPS ( **deliberate** DRY violation )
# This was forced by the need to override rest_framework templates in common
# It is a list because order matters

LOCAL_APPS = [
    'users',
    'common',
    'facilities',
    'chul',
    'mfl_gis',
    'data_bootstrap',
    'data',
    'reporting',
    'search',
    'admin_offices',
]
# CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'if-modified-since',
    'if-none-match',
    'cache-control'
)
AUTH_USER_MODEL = 'users.MflUser'
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'  # This is INTENTIONAL
TIME_ZONE = 'Africa/Nairobi'
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False  # Turn on in production
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'common.utilities.throttling.ThrottlingBySession',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'rating': '1/day'
    },
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'users.permissions.MFLModelPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        # 'rest_framework.filters.DjangoFilterBackend',
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'common.renderers.CSVRenderer',
        'common.renderers.ExcelRenderer',
        'common.renderers.PDFRenderer'
    ),
    'EXCEPTION_HANDLER': 'exception_handler.handler.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'common.paginator.MflPaginationSerializer',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGE_SIZE': 30,
    'PAGINATE_BY_PARAM': 'page_size',
    # Should be able to opt in to see all wards at once
    'MAX_PAGINATE_BY': 150000,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DATETIME_FORMAT': 'iso-8601',
    'DATE_FORMAT': 'iso-8601',
    'TIME_FORMAT': 'iso-8601'
}
SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '3.0',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': True,
    'is_superuser': False,
    'info': {
        'contact': 'developers@savannahinformatics.com',
        'description': 'Explore the MFL v3 API',
        'license': 'MIT License',
        'licenseUrl': 'http://choosealicense.com/licenses/mit/',
        'title': 'MFL v3 API',
    },
    'doc_expansion': 'full',
}
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60  # One hour
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s: %(asctime)s [%(module)s] %(message)s'  # NOQA
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'rest_framework': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'common': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'facilities': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'users': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'data_bootstrap': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'mfl_gis': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'exception_handler': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': os.path.join(BASE_DIR, '/common/templates/'),
        'DIRS': [(os.path.join(BASE_DIR, 'common/templates')), ],
        'APP_DIRS': True,
         'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        }
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }
}
CACHE_MIDDLEWARE_SECONDS = 15  # Intentionally conservative by default

# cache for the gis views
GIS_BORDERS_CACHE_SECONDS = (60 * 60 * 24 * 366)


# django-allauth related settings
# some of these settings take into account that the target audience
# of this system is not super-savvy

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    # 'users.backends.MflUserAuthBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/api/'

SEARCH = {
    "ELASTIC_URL": "http://localhost:9200/",
    "INDEX_NAME": "mfl_index",
    "REALTIME_INDEX": env('REALTIME_INDEX'),
    "SEARCH_RESULT_SIZE": 50,
    "NON_INDEXABLE_MODELS": [
        "mfl_gis.FacilityCoordinates",
        "mfl_gis.WorldBorder",
        "mfl_gis.CountyBoundary",
        "mfl_gis.ConstituencyBoundary",
        "mfl_gis.WardBoundary",
        "mfl_gis.DrilldownView",
        "users.CustomGroup",
        "users.ProxyGroup",
        "facilities.FacilityUpdates"

    ],
    "STOP_WORDS": [
        "centre", "center", "health", "hospital", "clinic", "district",
        "sub-district", "dispensary"
    ],
    "FULL_TEXT_SEARCH_FIELDS": {

        "models": [
            {
                "name": "facility",
                "fields": [
                    "name", "county", "constituency", "ward_name",
                    "facility_services.service_name",
                    "facility_services.service_name",
                    "facility_services.category_name",
                    "facility_physical_address.town",
                    "facility_physical_address.nearest_landmark",
                    "facility_physical_address.nearest_landmark"
                ]
            }
        ]

    },

    "AUTOCOMPLETE_MODEL_FIELDS": [
        {
            "app": "facilities",
            "models": [
                {
                    "name": "facility",
                    "fields": ["name"],
                    "boost": ["name"],
                },
                {
                    "name": "owner",
                    "fields": ["name"]
                },
                {
                    "name": "OwnerType",
                    "fields": ["name"]
                },
                {
                    "name": "JobTitle",
                    "fields": ["name"]
                },
                {
                    "name": "Officer",
                    "fields": ["name"]
                },
                {
                    "name": "FacilityStatus",
                    "fields": ["name"]
                },
                {
                    "name": "FacilityType",
                    "fields": ["name"]
                },
                {
                    "name": "RegulationStatus",
                    "fields": ["name"]
                },
                {
                    "name": "Option",
                    "fields": ["name"]
                },
                {
                    "name": "ServiceCategory",
                    "fields": ["name"]
                },
                {
                    "name": "Service",
                    "fields": ["name"]
                }
            ]
        },
        {
            "app": "common",
            "models": [
                {
                    "name": "County",
                    "fields": ["name"]
                },
                {
                    "name": "Consituency",
                    "fields": ["name"]
                },
                {
                    "name": "Ward",
                    "fields": ["name"]
                },
                {
                    "name": "ContactType",
                    "fields": ["name"]
                },
                {
                    "name": "Contact",
                    "fields": ["contact"]
                },
                {
                    "name": "Town",
                    "fields": ["name"]
                },
            ]
        },
        {
            "app": "mfl_gis",
            "models": [
                {
                    "name": "GeoCodeSource",
                    "fields": ["name"]
                },
                {
                    "name": "GeoCodeMethod",
                    "fields": ["name"]
                }
            ]
        },
        {
            "app": "users",
            "models": [
                {
                    "name": "MflUser",
                    "fields": ["full_name", "email"]
                }
            ]
        }
    ]
}

OAUTH2_PROVIDER_APPLICATION_MODEL = 'users.MFLOAuthApplication'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/api/'
ACCOUNT_SESSION_REMEMBER = True

# django_rest_auth settings
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.MflUserSerializer',
    'PASSWORD_CHANGE_SERIALIZER':
        'users.serializers.MflPasswordChangeSerializer'
}

REST_AUTH = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.MflUserSerializer',
}
# django-allauth forces this atrocity on us ( true at the time of writing )
SITE_ID = 1

EXCEL_EXCEPT_FIELDS = [
    'id', 'updated', 'created', 'created_by', 'updated_by', 'active',
    'deleted', 'search', 'services', 'categories', 'is_published'
]

FRONTEND_URL = env("FRONTEND_URL")
PASSWORD_RESET_URL = "%s/#/reset_pwd_confirm/{uid}/{token}" % FRONTEND_URL

if env('HTTPS_ENABLED'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_PROXY_PROTOCOL', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://3553-102-208-44-38.ngrok-free.app',
]
CSRF_COOKIE_AGE = None
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_AGE = (7 * 24 * 60 * 60)
SECURE_BROWSER_XSS_FILTER = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
EXCEL_EXCEPT_FIELDS_FOR_PUBLIC_USERS = EXCEL_EXCEPT_FIELDS + ['lat', 'long']

# KMHFL - DHIS2 Configurations
PUSH_TO_DHIS = not DEBUG
DHIS_ENDPOINT = env('DHIS_ENDPOINT')
DHIS_USERNAME = env('DHIS_USERNAME')
DHIS_PASSWORD = env('DHIS_PASSWORD')
DHIS_CLIENT_ID = env('DHIS_CLIENT_ID')
DHIS_CLIENT_SECRET = env('DHIS_CLIENT_SECRET')

# Upgrade additions
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
