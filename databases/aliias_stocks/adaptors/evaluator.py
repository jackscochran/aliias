from ..evaluators import model_one
from ..data import evaluators

import datetime

def add_evaluator(name):
    evaluator = evaluators.RegressionModel()
    evaluator.name = name
    evaluator.date_created = str(datetime.date.today())
    evaluator.weightings = model_one.WEIGHTINGS
    evaluator.save()

def evaluate(ticker, date, evaluator_name): # only supports model one for now
    if evaluators.Evaluator.objects(name=evaluator_name).first() is None:
        add_evaluator(evaluator_name)

    if evaluator_name == 'modelOne':
        model_one.evaluate_ticker(ticker, date)

