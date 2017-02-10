from pymongo import ReadPreference

MONGODB = {
    'default': {
        'host': 'mongodb',
        'port': 27017,
        'maxPoolSize': 1000,
        'tz_aware': True,
        'socketTimeoutMS': None,
        'connectTimeoutMS': 1000,
        'w': 1,
        'wtimeout': 10000,
        'j': False,
        'name': 'pyserver',
        'auth': None,
        'replicaSet': None,
        'read_preference': ReadPreference.PRIMARY,
    },
}
