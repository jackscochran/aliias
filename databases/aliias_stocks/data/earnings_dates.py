import mongoengine

class EarningsDate(mongoengine.Document):
    tickers = mongoengine.ListField(mongoengine.StringField())
    date = mongoengine.StringField(unique=True, required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'earningsDates'
    }