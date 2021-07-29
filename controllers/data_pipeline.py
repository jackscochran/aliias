from data.companies import Company
import adaptors.yahoo_portal as yahoo_portal
import adaptors.stock_adaptor as db_adaptor
import evaluators.logical_model as logical_model
import datetime
import os


# ---------- HELPER FUNCTIONS --------- #

def collect_and_save_financials(ticker):
    for period in yahoo_portal.extract_financials(ticker):
        db_adaptor.add_financialPeriod(period)

def collect_and_save_quote(ticker):
    db_adaptor.add_quote(yahoo_portal.extract_quote_data(ticker))

def collect_and_save_price(ticker):
    db_adaptor.add_price(ticker, str(datetime.date.today()),yahoo_portal.get_price(ticker))

def evaluate_logical_model(ticker):
    today = str(datetime.date.today())
    inputs = logical_model.get_data(ticker, today)
    db_adaptor.add_evaluation(
        ticker,
        today,
        logical_model.rate(inputs),
        logical_model.EVALUATOR_NAME,
        inputs
        ) 

# ----------- MAIN FUNCTIONS ---------- #

def collect_earnings(day):

    db_adaptor.setup_network_connection(os.environ.get('DB_NAME'))

    tickers = []
    count = 0
    print('scraping ' + day + ' on yahoo earnings calender...' )
    companies = yahoo_portal.earnings_on(day)
    print('earnings calender scrape complete')
    print('scraping and saving ticker data...')
    for company in companies:
        count += 1
        print(company[1] + '(' + company[0] + ') - ' + str(count) + ' / ' + str(len(companies)))#display progress
        db_adaptor.add_company(company[0], company[1])
        collect_and_save_price(company[0])
        collect_and_save_quote(company[0])
        collect_and_save_financials(company[0])
        evaluate_logical_model(company[0])

    # add new earnings calender date to the datebase
    tickers = [company[0] for company in companies]
    db_adaptor.add_earnings_date(tickers, day)  

def daily_evaluation():
    pass

def iterate_date_range(start, end):
    
    start = start.split('-')
    start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    end = end.split('-')
    end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))

    while start_date < end_date:
        # collect_earnings(str(start_date))
        print(start_date)
        start_date += datetime.timedelta(days=1)





    
