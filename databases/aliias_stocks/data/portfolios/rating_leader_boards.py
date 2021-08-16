import data.portfolios.portfolios as portfolios
import mongoengine
import adaptors.evaluation as evaluation_adaptor
import datetime

class RatingLeaderBoard(portfolios.Portfolio):
    evaluator_name = mongoengine.StringField(required=True)
    total_evaluations = mongoengine.IntField()

    def challenge(self):
        challengers = evaluation_adaptor.get_top_evaluations(
            evaluator_name = self.evaluator_name,
            n = 25
        )

        new_tickers = [challenger.ticker for challenger in challengers]

        for i in range(len(new_tickers)):
            if len(self.tickers) == 0 or new_tickers[i] != self.tickers[i]:
                new_board = RatingLeaderBoard()
                new_board.name = self.name
                new_board.tickers = new_tickers
                new_board.version = self.version + 1
                new_board.date_created = str(datetime.date.today())
                new_board.evaluator_name = self.evaluator_name
                new_board.total_evaluations = evaluation_adaptor.total_evaluations(self.evaluator_name)
                new_board.save()  
                return

    
