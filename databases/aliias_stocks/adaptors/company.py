"""
A database adaptor module that hosts functions to
interact with the companies collection in the 
mondoDB database
"""

from ..data import companies
import random
import datetime
# ----------- ADDER(also setter) FUNCTIONS--------- #

def add_company(ticker, name):
    ticker = ticker.upper()

    entry = get_company(ticker)

    if not entry: # add new company to database
        entry = companies.Company()
        entry.ticker = ticker

    entry.company_name = name
    entry.save()


# ----------- GETTER FUNCTIONS ----------- #

def get_company(ticker):
    return companies.Company.objects(ticker=ticker).first()

def get_financials(ticker, period):                                                                                                         
    return get_company(ticker).get_latest_financials(period)

def get_all_tickers():
    return [company.ticker for company in companies.Company.objects]

def get_all_companies():
    return companies.Company.objects

def get_n_companies(n):
    return companies.Company.objects[:n]

def get_n_random_companies(n):
    n_companies = []
    indexes_used = []
    company_objects = get_all_companies()
    for i in range(n):
        index = random.randint(0, len(company_objects))
        indexes_used.append(index)
        n_companies.append(companies.Company.objects[index])

    return n_companies

# ---------- Website functions ------ #

def company_data_list_format(ticker):

    date = str(datetime.date.today())

    company = get_company(ticker)
    evaluation = company.get_evaluation(date)
    price = company.get_price(date)

    company_data = {
        'ticker': ticker,
        'fullName': company.company_name,
        'rating': evaluation.rating,
        'dateRated': evaluation.date,
        'price': price.price,
    }

    return company_data

def search(query, n):

    results = {}

    ticker_matches = companies.Company.objects(ticker__icontains=query)[:n]

    for company in ticker_matches:
        results[company.ticker] = company.company_name

    name_matches = companies.Company.objects(company_name__icontains=query)[:n]

    for company in name_matches:
        if company.ticker not in results.keys():
            results[company.ticker] = company.company_name

    return results