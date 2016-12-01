import os

from .main import *

LOGGING = {
    'version': 1,
    'incremental': False,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "%(levelname)s %(asctime)s %(pathname)s %(lineno)d \
%(funcName)s \"%(message)s\""
        },
        'simple': {
            'format': "%(levelname)s %(asctime)s \"%(message)s\""
        },
        'raw': {
            'format': "%(asctime)s %(message)s"
        },
    },
    'handlers': {
        'null': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.NullHandler",
        },
        'console': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.StreamHandler",
            'formatter': "simple"
        },
        'app': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.FileHandler",
            'filename': os.path.join(LOG_PATH, "app.log"),
            'formatter': "verbose",
        },
        'command': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.FileHandler",
            'filename': os.path.join(LOG_PATH, "command.log"),
            'formatter': "verbose",
        },
        'tornado_access': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.FileHandler",
            'filename': os.path.join(LOG_PATH, "tornado_access.log"),
            'formatter': "simple"
        },
        'tornado_error': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.FileHandler",
            'filename': os.path.join(LOG_PATH, "tornado_error.log"),
            'formatter': "simple"
        },
        'request': {
            'level': LOGGING_HANDLER_LEVEL,
            'class': "logging.FileHandler",
            'filename': os.path.join(LOG_PATH, "request.log"),
            'formatter': "raw"
        },
    },
    'loggers': {
        'app': {
            'handlers': ["app"],
            'level': LOGGING_LOGGER_LEVEL,
            'propagate': False
        },
        'command': {
            'handlers': ["command", "console"],
            'level': LOGGING_LOGGER_LEVEL,
            'propagate': False
        },
        'tornado.access': {
            'handlers': ["tornado_access"],
            'level': LOGGING_LOGGER_LEVEL
        },
        'tornado.application': {
            'handlers': ["tornado_error"],
            'level': LOGGING_LOGGER_LEVEL
        },
        'tornado.general': {
            'handlers': ["tornado_error"],
            'level': LOGGING_LOGGER_LEVEL
        },
        'request': {
            'handlers': ["request"],
            'level': LOGGING_LOGGER_LEVEL,
            'propagate': False
        },
    }
}
