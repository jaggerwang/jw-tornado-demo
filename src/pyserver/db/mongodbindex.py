from pymongo import ASCENDING

MONGODB_INDEXES = {
    'default': {
        'user': [
            [[('username', ASCENDING)], {'unique': True}],
            [[('nick', ASCENDING)], {'unique': True}],
        ],
        'file': [
            [[('uploader_id', ASCENDING)]],
        ],
    },
}
