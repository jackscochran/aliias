import evaluators.model_one as model_one
import data.evaluators as evaluators

import datetime

def add_evaluator(name):
    evaluator = evaluators.Evaluator()
    evaluator.name = name
    evaluator.date_created = str(datetime.date.today())
    evaluator.save()

def evaluate(ticker, date, evaluator_name): # only supports model one for now
    if evaluators.Evaluator.objects(name=evaluator_name).first() is None:
        add_evaluator(evaluator_name)

    if evaluator_name == 'modelOne':
        model_one.evaluate_ticker(ticker, date)