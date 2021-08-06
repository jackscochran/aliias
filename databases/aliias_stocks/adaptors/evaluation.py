"""
A database adaptor module that hosts functions to
interact with the evalutation collection in the 
mondoDB database
"""

from data import evaluations 

def add_evaluation(ticker, date, rating, evaluator_name, inputs):
    ticker = ticker.upper()

    evaluation = evaluations.Evaluation.objects(ticker=ticker, date=date, evaluator_name=evaluator_name).first()

    if not evaluation: # create new evaluation entry if one does not already exist
        evaluation = evaluations.Evaluation()
        evaluation.ticker = ticker
        evaluation.date = date
        evaluation.evaluator_name = evaluator_name
        
    evaluation.rating = rating
    evaluation.inputs = inputs
    evaluation.save() 


def get_portfolio():

    num_of_results = 25
    portfolio = []
    
    top_ratings = evaluations.Evaluation.objects().order_by('-rating')
    for evaluation in top_ratings:
        if len(portfolio) >= num_of_results:
            break

        if evaluation not in portfolio:
            portfolio.append(evaluation.ticker)

    return portfolio
