import mongoengine
import datetime

class Email(mongoengine.Document):
    email_string = mongoengine.StringField(required=True, unique=True)
    date_added = mongoengine.StringField(required=True, default=str(datetime.date.today()))

    meta = {
        'db_alias': 'web',
        'collection': 'emails'
    }