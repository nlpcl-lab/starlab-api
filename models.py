import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class APIAccessLog(db.Document):

    key = db.StringField()
    ip = db.StringField()
    input = db.StringField()
    output = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [
            'key',
        ]
    }
