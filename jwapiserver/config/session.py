from .env import *

SESSION = {
    'cookie_secret': SESSION_COOKIE_SECRET,
    'key_prefix': 'session',
    'cookie_name': 'SID',
    'expires_days': SESSION_EXPIRES_DAYS
}
