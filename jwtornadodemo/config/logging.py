import os

from .env import *

LOGGING = {
    'version': 1,
    'incremental': False,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(lineno)d \
%(funcName)s \'%(message)s\''
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s \'%(message)s\''
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'app': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PATH_LOG, 'app.log'),
            'formatter': 'verbose',
        },
        'command': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PATH_LOG, 'command.log'),
            'formatter': 'verbose',
        },
        'tornado_access': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PATH_LOG, 'tornado_access.log'),
            'formatter': 'simple'
        },
        'tornado': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PATH_LOG, 'tornado.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['app', 'console'],
            'level': LOGGING_LOGGER_LEVEL,
            'propagate': False
        },
        'command': {
            'handlers': ['command', 'console'],
            'level': LOGGING_LOGGER_LEVEL,
            'propagate': False
        },
        'tornado.access': {
            'handlers': ['tornado_access', 'console'],
            'level': LOGGING_LOGGER_LEVEL
        },
        'tornado.application': {
            'handlers': ['tornado', 'console'],
            'level': LOGGING_LOGGER_LEVEL
        },
        'tornado.general': {
            'handlers': ['tornado', 'console'],
            'level': LOGGING_LOGGER_LEVEL
        }
    }
}
