"""
A database adaptor module that hosts functions to
interact with the portfolios collection in the 
mondoDB database
"""

from ..data.portfolios import rating_leader_boards
from ..data.portfolios import portfolios
import datetime

def get_portfolio():
    return

def get_leader_board(evaluator_name, date):
    return rating_leader_boards.RatingLeaderBoard.objects(evaluator_name=evaluator_name, date_created__lte = date).order_by('-version').first()

def get_current_board():
    board = get_leader_board('modelOne', str(datetime.date.today()))
    
    if board is None:
        board = create_leader_board('InitialPortfolio', 'modelOne')

    return board

def create_leader_board(name, evaluator_name):
    new_board = rating_leader_boards.RatingLeaderBoard()
    new_board.name = name
    new_board.evaluator_name = evaluator_name
    new_board.version = portfolios.Portfolio.objects(name=name).count()
    return new_board

# ---------- Website functions ------ #
