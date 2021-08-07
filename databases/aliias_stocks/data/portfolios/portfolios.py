import mongoengine

class Portfolio(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    date_created = mongoengine.StringField(required=True) 
    tickers = mongoengine.ListField(mongoengine.StringField())
    version = mongoengine.IntField(required=True)

    meta = {
        'allow_inheritance': True, 
        'db_alias': 'core', 
        'collection': 'portfolios',
        'indexes': [
            {'fields': ('name', 'version'), 'unique': True}
        ]
    }