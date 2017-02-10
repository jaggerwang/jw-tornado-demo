from pymongo import ASCENDING

MONGODB_INDEXES = {
    'default': {
        'user': [
            [[('username', ASCENDING)], {'unique': True}],
            [[('nickname', ASCENDING)], {'unique': True}],
        ],
    },
}
