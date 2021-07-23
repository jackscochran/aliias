from bson.json_util import default
import mongoengine
import datetime

class Evaluation(mongoengine.Document):
    ticker = mongoengine.StringField()
    evaluator = mongoengine.StringField()
    rating = mongoengine.FloatField()
    date = mongoengine.StringField()
    inputs = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'evaluations'
    }