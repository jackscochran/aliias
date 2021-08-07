import mongoengine
import datetime

class Evaluation(mongoengine.Document):
    ticker = mongoengine.StringField(required=True)
    evaluator_name = mongoengine.StringField(required=True)
    rating = mongoengine.FloatField(required=True)
    date = mongoengine.StringField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'evaluations',
        'indexes': [
            {'fields': ('ticker', 'evaluator_name', 'date'), 'unique': True}
        ]
    }