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
        'formatters': {
            'timestamped': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
        },
        'handlers': {
            'file_debug_log': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '{{ LPD_LOG_DIR }}/debug.log',
                'formatter': 'timestamped',
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

STATIC_ROOT = "{{ LPD_STATICFILES_ROOT }}"
STATIC_URL = "/static/"

MEDIA_ROOT = "{{ LPD_MEDIA_ROOT }}"
MEDIA_URL = "/media/"

# List of knowledge component IDs for which LDA model calculates probabilities.
# The order of the components must match exactly the order in which probabilities are returned by LDA model.
# E.g. If LDA model returns [0.2, 0.8] and GROUP_KCS are equal to ['kc_id_1', 'kc_id_2'],
# then 0.2 will be interpreted as the probability of a learner belonging to the knowledge component (group)
# identified by 'kc_id_1', and 0.8 will be interpreted as the probability of the learner
# belonging to the knowledge component (group) identified by 'kc_id_2'.
GROUP_KCS = {{ LPD_GROUP_KCS }}

# Domain of the Open edX instance that this LPD deployment is connected to
OPENEDX_INSTANCE_DOMAIN = '{{ LPD_OPENEDX_INSTANCE_DOMAIN }}'
# URL of the Adaptive Engine deployment that this LPD deployment is connected to
ADAPTIVE_ENGINE_URL = '{{ LPD_ADAPTIVE_ENGINE_URL }}'
# Auth token for requests to Adaptive Engine deployment that this LPD deployment is connected to
ADAPTIVE_ENGINE_TOKEN = '{{ LPD_ADAPTIVE_ENGINE_TOKEN}}'
