from ..evaluators import model_one
from ..evaluators import lenny
from ..data import evaluators

import datetime

def add_evaluator(name, weightings):
    evaluator = evaluators.RegressionModel()
    evaluator.name = name
    evaluator.date_created = str(datetime.date.today())
    evaluator.weightings = weightings
    evaluator.save()

def evaluate(ticker, date, evaluator_name): # only supports model one for now
    if evaluators.Evaluator.objects(name=evaluator_name).first() is None:
        if evaluator_name == 'modelOne':
            add_evaluator(evaluator_name, model_one.get_weightings())

        # if evaluator_name == 'modelTwo':
        #     add_evaluator(evaluator_name, model_two.get_weightings())

        if evaluator_name == 'lenny':
            add_evaluator(evaluator_name, lenny.get_weightings())

    if evaluator_name == 'modelOne':
        model_one.evaluate_ticker(ticker, date)

    if evaluator_name == 'lenny':
        lenny.evaluate_ticker(ticker, date)
