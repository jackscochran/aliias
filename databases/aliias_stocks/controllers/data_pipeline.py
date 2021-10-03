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

    Quote Data: This collects today's quote data for all companies in the database on

    collect sp 500: Scrapes and ads all companies on the S&P 500 index into ALIIAS's database
"""

# Standard libary imports
import datetime
import os
import sys

# Third party imports -- None

# Local application imports
from ..adaptors import yahoo_portal as yahoo_portal
from ..adaptors import financial_period as financial_period_adaptor
from ..adaptors import quote as quote_adaptor
from ..adaptors import daily_price as daily_price_adaptor
from ..adaptors import evaluation as evaluation_adaptor
from ..adaptors import company as company_adaptor
from ..adaptors import earnings_date as earnings_date_adaptor
from ..adaptors import portfolio as portfolio_adaptor
from ..adaptors import evaluator as evaluator_adaptor
from ..helpers import timeline as timeline


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

    if len(price_object) != 0:
        price = price_object[0]['value']
        daily_price_adaptor.add_price(ticker, date, price)
        return price
    else:
        daily_price_adaptor.add_price(ticker, date, -1)
        return None

def collect_historical_price_data(ticker, start_date):
    today = str(datetime.date.today())
    half_year_ago = timeline.change_months(today, -6)

    if start_date > half_year_ago: # scrape prices from at least 6 months ago
        start_date = half_year_ago

    for price in yahoo_portal.extract_historical_price_data(ticker, start_date, today):
        daily_price_adaptor.add_price(
            ticker=ticker,
            date=price['date'],
            price=price['value']
        )

def initiate(ticker, company_name, date):
    company_adaptor.add_company(ticker, company_name)
    collect_historical_price_data(ticker, date)
    collect_and_save_quote(ticker)
    collect_and_save_financials(ticker)
    evaluator_adaptor.evaluate(ticker, date, 'modelOne')

# ----------- MAIN FUNCTIONS ---------- #

def collect_earnings(date):
    tickers = []
    
    count = 0
    print('scraping ' + date + ' on yahoo earnings calender...' )
    companies = [company for company in yahoo_portal.earnings_on(date) if company[0][-1].upper != 'F']

    # add new earnings calender date to the datebase
    tickers = [company[0] for company in companies]
    earnings_date_adaptor.add_earnings_date(tickers, date) # update to add ticker each time they have their data collected
    print('earnings calender scrape complete') 
    print('scraping and saving ticker data...')
    
    for company in companies:
        ticker, company_name = company
        count += 1
        print(company_name + '(' + ticker + ') - ' + str(count) + ' / ' + str(len(companies)))#display progress
        company_adaptor.add_company(ticker, company_name)
        collect_historical_price_data(ticker, date)
        collect_and_save_quote(ticker)
        collect_and_save_financials(ticker)
        evaluator_adaptor.evaluate(ticker, date, 'modelOne')

    print('Earnings Calender scrape completed. ' + str(count) + ' Tickers collected')

    print('challenging current portfolios')
    portfolio_adaptor.get_current_board().challenge()

def collect_ticker_prices(date):
    print('Collecting Prices for tickers in database')
    print('Collecting price for: ')
    count = 0
    for ticker in company_adaptor.get_all_tickers():
        count +=1 
        print(ticker + ' ' + str(count))
        if not daily_price_adaptor.exists(ticker, date):
            collect_and_save_price(ticker, date)

def collect_quote_data():
    print('Collecting quote data for tickers in database')
    print('Collecting quote data for: ')
    date = str(datetime.date.today())
    count = 0
    for ticker in company_adaptor.get_all_tickers():
        count +=1 
        print(ticker + ' ' + str(count))
        if not quote_adaptor.exists(ticker, date):
            collect_and_save_quote(ticker)

def collect_sp500():
    sp500 = yahoo_portal.get_sp500()
    for i in range(len(sp500)):
        company_name = sp500["Security"][i]
        ticker = sp500["Symbol"][i]
        print(company_name + '(' + ticker + ') - ' + str(i) + ' / ' + str(len(sp500)))#display progress
        initiate(ticker, company_name, str(datetime.date.today()))