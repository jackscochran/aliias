from data.companies import Company
import services.yahoo_portal as yahoo_portal
import services.stock_adaptor as db_adaptor
import evaluators.logical_model as logical_model
import datetime
import os

EVALUATION_FREQUENCY = os.environ.get('EVALUATION_FREQUENCY') # times per years

# ---------- HELPER FUNCTIONS --------- #

def measure_financials(ticker):
    for period in yahoo_portal.extract_financials(ticker):
        db_adaptor.add_financialPeriod(period)

def measure_performance(ticker):
    db_adaptor.add_performance(ticker, yahoo_portal.extract_performance(ticker))

# ----------- MAIN FUNCTIONS ---------- #

def collect_earnings(day):

    db_adaptor.setup_network_connection(os.environ.get('DB_NAME'))

    tickers = []
    print('getting tickers...')
    companies = yahoo_portal.earnings_calender(day, day)

    print('extracting financials for:')

    for company in companies:
        print(company)
        db_adaptor.add_company(company[0], company[1])
        measure_financials(company[0])

    
    tickers = [company[0] for company in companies]

    # add new earnings calender date to the datebase
    
    db_adaptor.add_earnings_date(tickers, day)

    evaluation_period = 1/EVALUATION_FREQUENCY * 12 # in months

    performance_tickers = [] # any ticker whos last performance check was an evaluation period ago

    # for day in range(startDay, endDay):
    #     performance_tickers.append(Company.objects('if company.last_evaluation.date == startDay - evaluationPeriod'))

    tickers += performance_tickers
    print('Gathering Stock performance and evaluating for:')

    for ticker in tickers:
        print(ticker)
        measure_performance(ticker)
        today = str(datetime.date.today())
        inputs = logical_model.get_data(ticker, today)
        db_adaptor.add_evaluation(
            ticker,
            today,
            logical_model.rate(inputs),
            logical_model.EVALUATOR_NAME,
            inputs
            ) 

    # check performance stocks and test how they are doing compared to their evaluation 

    for ticker in performance_tickers:
        # check_performance(ticker) <= Not yet implimented
        break

def iterate_date_range(start, end):
    
    start = start.split('-')
    start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    end = end.split('-')
    end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))

    while start_date < end_date:
        # collect_earnings(str(start_date))
        print(start_date)
        start_date += datetime.timedelta(days=1)





    
