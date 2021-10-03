# Standard libary imports
import datetime

# Third party imports

# Local application imports
from ..adaptors import company as company_adaptor
from ..adaptors import evaluation as evaluation_adaptor


# -*-*-*-*-*- LENNY -*-*-*-*-*- #
# ---- Linear Regression to sigmoid model --------- #

def evaluate_ticker(ticker, date):

    def rate(inputs):
        pass

    def get_input_data(ticker, date):
        pass

    # get input data
    inputs = get_input_data(ticker, date)

    # rate ticker
    rating = rate(inputs)

    # create and save evaluation 
    evaluation_adaptor.add_evaluation(
        ticker=ticker,
        date=date,
        evaluator_name='lenny',
        rating=rating,
    )

def get_weightings():
    weightings = {}
    return weightings

def train(start_date, end_date):

    def load_data(start_date, end_date):
        pass

    def train_model(inputs, labels):
        pass

    def save_model(model):
        pass

def test():
    pass

