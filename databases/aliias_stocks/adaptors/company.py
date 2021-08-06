"""
A database adaptor module that hosts functions to
interact with the companies collection in the 
mondoDB database
"""

from data.companies import Company


# ----------- ADDER(also setter) FUNCTIONS--------- #

def add_company(ticker, name):
    ticker = ticker.upper()

    entry = get_company(ticker)

    if not entry: # add new company to database
        entry = Company()
        entry.ticker = ticker

    entry.company_name = name
    entry.save()


# ----------- GETTER FUNCTIONS ----------- #

def get_company(ticker):
    return Company.objects(ticker=ticker).first()

def get_financials(ticker, period):                                                                                                         
    return get_company(ticker).get_latest_financials(period)

def get_all_companies():
    return Company.objects

def get_all_tickers():
    return [company.ticker for company in Company.objects]