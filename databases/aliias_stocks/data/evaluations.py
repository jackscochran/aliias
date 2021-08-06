import mongoengine
import datetime

class Evaluation(mongoengine.Document):
    ticker = mongoengine.StringField()
    evaluator_name = mongoengine.StringField()
    rating = mongoengine.FloatField()
    date = mongoengine.StringField()
    inputs = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'evaluations'
    }