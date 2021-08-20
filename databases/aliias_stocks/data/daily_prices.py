import mongoengine

class DailyPrice(mongoengine.Document):
    ticker = mongoengine.StringField(required=True)
    date = mongoengine.StringField(required=True)
    price = mongoengine.FloatField()

    meta = {
        'db_alias': 'core',
        'collection': 'dailyPrices',
        'indexes': [
            {'fields': ('ticker', 'date'), 'unique': True}
        ]
    }