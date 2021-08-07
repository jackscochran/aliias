import mongoengine

class Evaluator(mongoengine.Document):
    name = mongoengine.StringField(required=True, unique=True)
    date_created = mongoengine.StringField(required=True)

    meta = {
        'allow_inheritance': True, 
        'db_alias': 'core', 
        'collection': 'evaluators'
    }