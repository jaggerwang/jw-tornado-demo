from .env import *

SESSION = {
    'driver': 'redis',
    'driver_settings': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': REDIS_DB
    },
    'force_persistence': True,
    'cache_driver': not DEBUG,
    'sid_name': 'SID',
    'session_lifetime': SESSION_EXPIRES_SECONDS
}
