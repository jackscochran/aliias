import mongoengine

class Quote(mongoengine.Document):
    ticker = mongoengine.StringField(required=True)
    date = mongoengine.StringField(required=True)
    data = mongoengine.DictField()

    meta = {
        'db_alias': 'core',
        'collection': 'quotes',
        'indexes': [
            {'fields': ('ticker', 'date'), 'unique': True}
        ]
    }