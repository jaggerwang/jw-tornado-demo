import pymongo

MONGODB_INDEXES = {
    'default': {
        'user': [
            [[('username', pymongo.ASCENDING)], {'unique': True}],
            [[('nickname', pymongo.ASCENDING)], {'unique': True}],
        ],
    },
}
