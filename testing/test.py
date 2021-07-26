import unittest
import evaluators.logical_model as evaluator
import services.stock_adaptor as stock_adaptor
import controllers.data_pipeline as data_pipeline

DATABASE_NAME = 'test'

class TestEvaluators(unittest.TestCase):

    def test_rating(self):
        input = [
            {
                'sharePrice': 7,
                'marketCap': 253497904,
                'revenue': 100,
                'grossProfit': 100,
                'operatingIncome': 26752000,
                'netIncome': 19405000,
                'ebit': 1,
                'netReceivables': 268000,
                'inventory': 1,
                'currentAssets': 271294000,
                'totalAssets': 1943885000,
                'currentLiabilities': 1668286000,
                'longTermDebt': 13634000,
                'totalLiabilities': 1668286000,
                'retainedEarnings': 73194000,
                'dividends': -4280000,
                'shareIssuance': 1,
                'shareBuyback': 1,
                'operatingCashflow': -26947000,
                'capitalExpenditure': -245000,
                'depreciation': 1149000,
                'eps': 0.683
            },
            {
                'sharePrice': 7,
                'marketCap': 253497904,
                'revenue': 100,
                'grossProfit': 100,
                'operatingIncome': 27821000,
                'netIncome': 20196000,
                'ebit': 1,
                'netReceivables': 437000,
                'inventory': 1,
                'currentAssets': 151145000,
                'totalAssets': 1785381000,
                'currentLiabilities': 1500873000,
                'longTermDebt': 38247000,
                'totalLiabilities': 1545218000,
                'retainedEarnings': 58069000,
                'dividends': -3678000,
                'shareIssuance': 1,
                'shareBuyback': 1,
                'operatingCashflow': 57905000,
                'capitalExpenditure': -245000,
                'depreciation': 721000,
                'eps': 0.683
            },
            {
                'sharePrice': 7,
                'marketCap': 253497904,
                'revenue': 100,
                'grossProfit': 100,
                'operatingIncome': 25013000,
                'netIncome': 18074000,
                'ebit': 1,
                'netReceivables': 489000,
                'inventory': 1,
                'currentAssets': 142116000,
                'totalAssets': 1809130000,
                'currentLiabilities': 1537066000,
                'longTermDebt': 43154000,
                'totalLiabilities': 1585563000,
                'retainedEarnings': 41473000,
                'dividends': -3044000,
                'shareIssuance': 1,
                'shareBuyback': 1,
                'operatingCashflow': -74708000,
                'capitalExpenditure': -993000,
                'depreciation': 623000,
                'eps': 0.683
            }
        ]
        rating = 8.16
        self.assertEqual(rating, round(evaluator.rate(input), 2))

class Pipeline(unittest.TestCase):

    def test_earnings_function(self):
        data_pipeline.collect_earnings('2021-07-05')

class TestDBAdaptor(unittest.TestCase):

    def setUp(self):
        stock_adaptor.setup_network_connection(DATABASE_NAME)

    def test_company_existance(self):
        stock_adaptor.add_company('TEST', 'TEST Stock')
        self.assertIsNotNone(stock_adaptor.get_company('TEST'))

    def test_non_existance(self):
        self.assertIsNone(stock_adaptor.get_company('feoquqfh34u'))

if __name__ == '__main__':
    unittest.main()

