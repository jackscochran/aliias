import mongoengine

class User(mongoengine.Document):
    first_name = mongoengine.StringField()
    last_name = mongoengine.StringField()
    password_hash = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True, unique=True)
    paymentInfo = mongoengine.DictField()

    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }