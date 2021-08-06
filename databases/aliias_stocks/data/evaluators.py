import mongoengine

class Evaluator(mongoengine.Document):
    name = mongoengine.StringField()

    meta = {
        'db_alias': 'core',
        'collection': 'evaluators'
    }