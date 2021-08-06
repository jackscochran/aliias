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

def collect_and_save_financials(ticker):
    try:
        for period in yahoo_portal.extract_financials(ticker):
            financial_period_adaptor.add_financialPeriod(period)
    except:
        print('error collecting financials for stock ' + ticker)
        return

def collect_and_save_quote(ticker):
    quote_adaptor.add_quote(yahoo_portal.extract_quote_data(ticker))

def collect_and_save_price(ticker, date):
    price_object = yahoo_portal.extract_historical_price_data(ticker, date, date)

    if len(price_object) == 0:
        price = yahoo_portal.get_price(ticker)
    else:
        price = price_object[0]['value']
    daily_price_adaptor.add_price(ticker, date, price)

def collect_historical_price_data(ticker, start_date, end_date):
    for price in yahoo_portal.extract_historical_price_data(ticker, start_date, end_date):
        daily_price_adaptor.add_price(
            ticker=ticker,
            date=price['date'],
            price=price['value']
        )

# ----------- MAIN FUNCTIONS ---------- #

def collect_earnings(date):
    tickers = []
    count = 0
    print('scraping ' + date + ' on yahoo earnings calender...' )
    companies = [company for company in yahoo_portal.earnings_on(date) if company[0][-1].upper != 'F']
    print('earnings calender scrape complete')
    print('scraping and saving ticker data...')
    for company in companies:
        ticker, company_name = company
        count += 1
        print(company_name + '(' + ticker + ') - ' + str(count) + ' / ' + str(len(companies)))#display progress
        company_adaptor.add_company(ticker, company_name)
        collect_historical_price_data(ticker, date, str(datetime.date.today()))
        collect_and_save_quote(ticker)
        collect_and_save_financials(ticker)
        model_one.evaluate_and_record(ticker, date)

    print('Earnings Calender scrape completed. ' + str(count) + ' Tickers collected')
    # add new earnings calender date to the datebase
    tickers = [company[0] for company in companies]
    earnings_date_adaptor.add_earnings_date(tickers, date)  

def collect_ticker_prices(date):
    print('Collecting Prices for tickers in database')
    print('Collecting price for: ')
    for ticker in company_adaptor.get_all_tickers():
        print(ticker)
        if not daily_price_adaptor.exists(ticker, date):
            collect_and_save_price(ticker, date)

def iterate_date_range(start, end):
    
    start = start.split('-')
    start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    end = end.split('-')
    end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))

    while start_date < end_date:
        # collect_ticker_prices(str(start_date))
        collect_earnings(str(start_date))
        start_date += datetime.timedelta(days=1)





    
