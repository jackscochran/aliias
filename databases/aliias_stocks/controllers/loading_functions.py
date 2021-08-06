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
import evaluators.model_one as model_one
import adaptors.financial_period as financial_period_adaptor
import adaptors.quote as quote_adaptor
import adaptors.daily_price as daily_price_adaptor
import adaptors.evaluation as evaluation_adaptor
import adaptors.company as company_adaptor
import adaptors.earnings_date as earnings_date_adaptor


# ---------- HELPER FUNCTIONS --------- #

    
# ----------- MAIN FUNCTIONS ---------- #

def load_price_and_evaluate_earnings():
    # collect and save all daily prices since the companies first earnings calender
    for earnings_date in earnings_date_adaptor.get_all():
        print('Earnings date: ' + earnings_date.date)
        for ticker in earnings_date.tickers:
            print('Ticker: ' + ticker)
            for price in yahoo_portal.extract_historical_price_data(ticker, earnings_date.date, str(datetime.date.today())):
                daily_price_adaptor.add_price(
                    ticker=ticker, 
                    date=price['date'], 
                    price=price['value'])

            model_one.evaluate_and_record(ticker, earnings_date.date)






    
