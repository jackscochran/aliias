"""
A database adaptor module that hosts functions to
interact with the evalutation collection in the 
mondoDB database
"""

from data import evaluations 

def add_evaluation(ticker, date, rating, evaluator_name):
    ticker = ticker.upper()

    evaluation = evaluations.Evaluation.objects(ticker=ticker, date=date, evaluator_name=evaluator_name).first()

    if not evaluation: # create new evaluation entry if one does not already exist
        evaluation = evaluations.Evaluation()
        evaluation.ticker = ticker
        evaluation.date = date
        evaluation.evaluator_name = evaluator_name
        
    evaluation.rating = rating
    evaluation.save() 

def get_top_evaluations(evaluator_name, n):
    top_evaluations = evaluations.Evaluation.objects(evaluator_name=evaluator_name).order_by('-rating')[:n] 
        
    return top_evaluations



