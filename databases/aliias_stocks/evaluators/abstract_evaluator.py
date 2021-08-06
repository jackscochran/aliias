"""
This abstract class is used as an interface for any
evaluators added to the system. All evaluators will extend 
and impliment this class
"""
# Standard libary imports
import datetime

# Third party imports
import mongoengine

# Local application imports
import data.evaluations as evaluations

class Evaluator(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    version = mongoengine.IntField(required=True, min_value=0)
    date_created = mongoengine.StringField(required=True)

    def create_new_version(self):
        self.date_created = str(datetime.date.today())
        self.version = 1
        self.save()
        return self

    # process and create evaulation for ticker
    def evaluate_ticker(self, ticker):
        return


    # helper methods

    def load_ticker_data(self):
        return

    def rate_current_data(self):
        return


    meta = {
        'allow_inheritance': True, 
        'db_alias': 'core', 
        'collection': 'evaluators'
    }
