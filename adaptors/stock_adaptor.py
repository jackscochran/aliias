from data.companies import Company
from data.financialPeriods import FinancialPeriod
from data.quotes import Quote
from data.evaluations import Evaluation
from data.dailyPrices import DailyPrice
import mongoengine
import os
from data.earningsDates import EarningsDate


# ----------- ADDER(also setter) FUNCTIONS--------- #

def add_company(ticker, name):
    ticker = ticker.upper()

    entry = get_company(ticker)

    if not entry: # add new company to database
        entry = Company()
        entry.ticker = ticker

    entry.company_name = name
    entry.save()

def add_financialPeriod(financials):

    period = FinancialPeriod.objects(ticker=financials['ticker'], period_length=financials['period'], end_date=financials['end_date']).first()

    if not period: # add new period to database
        period = FinancialPeriod()
        period.ticker = financials['ticker']
        period.period_length = financials['period']
        period.end_date = financials['end_date']

    period.incomeStatement = financials['incomeStatement']
    period.balanceSheet = financials['balanceSheet']
    period.cashflowStatement = financials['cashflowStatement']
    period.save()

def add_quote(company_quote):

    quote = Quote.objects(date=company_quote.get('date'), ticker=company_quote.get('ticker', None)).first()

    if not quote:  # add new period to database
        quote = Quote()
        quote.ticker = company_quote.get('ticker', None)
        quote.date = company_quote.get('date', None)
    
    quote.data = company_quote.get('data', None)
    quote.save()

def add_price(ticker, date, price):
    daily_price =  DailyPrice.objects(ticker=ticker, date=date).first()
    
    if not daily_price:
        daily_price = DailyPrice()
        daily_price.ticker = ticker
        daily_price.date = date

    daily_price.price = price
    daily_price.save()

def add_evaluation(ticker, date, rating, evaluator, inputs):
    ticker = ticker.upper()

    evaluation = Evaluation.objects(ticker=ticker, date=date, evaluator=evaluator).first()

    if not evaluation: # create new evaluation entry if one does not already exist
        evaluation = Evaluation()
        evaluation.ticker = ticker
        evaluation.date = date
        evaluation.evaluator = evaluator
        
    evaluation.rating = rating
    evaluation.inputs = inputs
    evaluation.save() 

def add_earnings_date(tickers, date):

    earnings_date = EarningsDate.objects(date=date).first()

    if earnings_date:
        for ticker in tickers:
            if ticker not in earnings_date.tickers:
                earnings_date.tickers.append(ticker)

    else:
        earnings_date = EarningsDate()
        earnings_date.date = date
        earnings_date.tickers = tickers

    earnings_date.save()

# ----------- GETTER FUNCTIONS ----------- #

def get_company(ticker):
    return Company.objects(ticker=ticker).first()

def get_financials(ticker, period):                                                                                                         
    return get_company(ticker).get_latest_financials(period)

def get_all_companies():
    return Company.objects

def get_portfolio():

    num_of_results = 25
    portfolio = []
    
    top_ratings = Evaluation.objects().order_by('-rating')
    for evaluation in top_ratings:
        if len(portfolio) >= num_of_results:
            break

        if evaluation not in portfolio:
            portfolio.append(evaluation.ticker)

    return portfolio

def setup_local_connection(database):
    mongoengine.connect(db=database, alias='core', host='localhost:27017')

def setup_network_connection(db):
    mongoengine.connect(host='mongodb+srv://' + os.environ.get('DB_ACCOUNT') + ':' + os.environ.get('DB_PASSWORD') + '@realmcluster.zudeo.mongodb.net/' + db + '?retryWrites=true&w=majority', alias='core')

def get_all_tickers():
    return [company.ticker for company in Company.objects]