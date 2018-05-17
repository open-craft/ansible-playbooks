import getpass

LTI_CLIENT_KEY = u'{{ LPD_LTI_CLIENT_KEY }}'
LTI_CLIENT_SECRET = u'{{ LPD_LTI_CLIENT_SECRET }}'
PASSWORD_GENERATOR_NONCE = u'{{ LPD_PASSWORD_GENERATOR_NONCE }}'

DB_NAME = u'{{ LPD_DB_NAME }}'
DB_USERNAME = u'{{ LPD_DB_USERNAME }}'
DB_PASSWORD = u'{{ LPD_DB_PASSWORD }}'
DB_HOST = u'{{ LPD_DB_HOST }}'

DEBUG = False

ALLOWED_HOSTS = ['{{ LPD_SERVER_DOMAIN }}']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_SCHEME', 'https')

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': DB_NAME,
       'USER': DB_USERNAME,
       'PASSWORD': DB_PASSWORD,
       'HOST': DB_HOST
   }
}

if getpass.getuser() == '{{ LPD_USER_NAME }}':
    # Change log paths only for production requests
    LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_debug_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{{ LPD_LOG_DIR }}/debug.log',
        },
        'file_test_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '{{ LPD_LOG_DIR }}/test.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file_debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_lti_tool_provider.views': {
            'handlers': ['file_debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'lpd.views': {
            'handlers': ['file_debug_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'lpd.tests': {
            'handlers': ['file_test_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

STATIC_ROOT="{{ LPD_STATICFILES_ROOT }}"
STATIC_URL="/static/"

MEDIA_ROOT="{{ LPD_MEDIA_ROOT }}"
MEDIA_URL="/media/"
