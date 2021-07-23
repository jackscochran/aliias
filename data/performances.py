import mongoengine

class Performance(mongoengine.Document):
    ticker = mongoengine.StringField()
    date = mongoengine.StringField(required=True)
    price = mongoengine.FloatField(required=True)
    market_cap = mongoengine.FloatField()
    eps = mongoengine.FloatField()

    meta = {
        'db_alias': 'core',
        'collection': 'performances',
        'indexes': [
            {'fields': ('ticker', 'date'), 'unique': True}
        ]
    }