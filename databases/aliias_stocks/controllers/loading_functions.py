""" 
The data pipeline module is used to host functions
and commands that feed data from the web into the 
database on a recurring basis. 

The main commands are:
    Earings Calender: This scrapes the tickers, and 
    all their related data from yahoo finance and stores
    it into the aliias cloud database

    Daily Prices: This collects today's price for all 
    companies in the database
"""

# Standard libary imports
import datetime
import os
import sys

# Third party imports -- None

# Local application imports
import adaptors.yahoo_portal as yahoo_portal
import manager as db_manager
import adaptors.evaluator as evaluator_adaptor
import adaptors.financial_period as financial_period_adaptor
import adaptors.quote as quote_adaptor
import adaptors.daily_price as daily_price_adaptor
import adaptors.evaluation as evaluation_adaptor
import adaptors.company as company_adaptor
import adaptors.earnings_date as earnings_date_adaptor
import helpers.timeline as timeline
import adaptors.portfolio as portfolio_adaptor

# ---------- HELPER FUNCTIONS --------- #

    
# ----------- MAIN FUNCTIONS ---------- #

def load_price_and_evaluate_earnings():
    # collect and save all daily prices since the companies first earnings calender
    for earnings_date in earnings_date_adaptor.get_all():
        if earnings_date.date in ['2021-07-29', '2021-07-30', '2021-08-02']:
            continue
        print('Earnings date: ' + earnings_date.date)
        for ticker in earnings_date.tickers:
            print('Ticker: ' + ticker)
            for price in yahoo_portal.extract_historical_price_data(ticker, timeline.change_months(str(datetime.date.today()), -6), str(datetime.date.today())):
                daily_price_adaptor.add_price(
                    ticker=ticker, 
                    date=price['date'], 
                    price=price['value'])

            evaluator_adaptor.evaluate(ticker, earnings_date.date, 'modelOne')

    portfolio_adaptor.get_current_board().challenge()






    
