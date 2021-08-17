import unittest
import controllers.data_pipeline as data_pipeline
import manager as db_manager
import adaptors.earnings_date as earnings_date_adaptor
import adaptors.company as company_adaptor
import adaptors.daily_price as daily_price_adaptor
import adaptors.evaluation as evaluation_adaptor
import controllers.loading_functions as loading_functions
import datetime
import controllers.analytics as analytics
import adaptors.portfolio as portfolio_adaptor

DATE = '2021-01-01'
db_manager.setup_network_connection('aliias')
# portfolio_adaptor.get_current_board().challenge()


# data_pipeline.collect_earnings(DATE)
# print(analytics.calculate_correlation(2500, 6))
print(analytics.get_portfolio_performance_ratings(6))

# class EarningsDateScrape(unittest.TestCase):
    
#     # run process and test results
#     def test_earnings_date_existance(self):
#         self.earnings_date = earnings_date_adaptor.get_earnings_date(DATE)
#         self.assertIsNotNone(self.earnings_date)

#     def test_list_length(self):
#         self.assertEqual(len(self.earnings_date.tickers), 27)

#     def test_document_date(self):
#         self.assertEqual(DATE, self.earnings_date.date)

#     def test_stock_existence(self):
#         self.assertIn('SCR', self.earnings_date.tickers)
#         self.assertIn('CAG', self.earnings_date.tickers)
#         self.assertIn('GS', self.earnings_date.tickers)
#         self.assertIn('PEP', self.earnings_date.tickers)
#         self.assertIn('TIEMF', self.earnings_date.tickers)

#     def test_ticker_data_collection(self):
#         for ticker in self.earnings_date.ticker:
#             self.assertIsNotNone(daily_price_adaptor.get_price(
#                 ticker=ticker, 
#                 date=DATE
#                 ))
#             company = company_adaptor.get_company(ticker)
#             self.assertIsNotNone(company.get_financials(DATE), 12)
#             self.assertIsNotNone(company.get_financials(DATE), 3)
#             self.assertIsNone(company.get_financials(DATE), 2)

#     def test_evaluation(self):
        
#         for ticker in self.earnings_date.ticker:
#             company = company_adaptor.get_company(ticker)
#             self.assertIsNotNone(company.get_latest_evaluation())
#             self.assertIsNotNone(company.get_latest_evaluation().rating)
#             self.assertEqual(len(company.get_evaluations()), 20) # no evaluation for foreign stocks

# class EarningsDatePricesScrape(unittest.TestCase):

#     def test_earnings_date_price_scrape(self):
#         loading_functions.load_price_and_evaluate_earnings()

if __name__ == '__main__':
    unittest.main()
    
