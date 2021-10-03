from ..adaptors import company as company_adaptor
from ..adaptors import portfolio as portfolio_adaptor
from ..adaptors import daily_price as price_adaptor
from ..evaluators import model_one as model_one
from ..helpers import timeline as timeline
from .. import manager as db_manager
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import datetime
import scipy.stats as spicy_stats
import math

# establish database connection
db_manager.setup_network_connection('aliias')

def get_performance(ticker, start, end):
    entry_price = price_adaptor.get_weekday_price(ticker, start)
    exit_price = price_adaptor.get_weekday_price(ticker, end)

    if entry_price is None or exit_price is None:
        return None

    return (exit_price - entry_price)/entry_price

def calculate_correlation(input, detailed_inputs, performance_data, training_date_cap):
    input_data = []
    output_data = []

    for ticker in performance_data:
        if detailed_inputs[ticker] is None or performance_data[ticker] is None or math.isnan(performance_data[ticker]):
            continue

        data = detailed_inputs[ticker].get(input, None)
        if data is not None and not math.isnan(data['value']):
            input_data.append(data['value'])
            output_data.append(performance_data[ticker])

    if len(input_data) == 0 or len(output_data) == 0:
        return 0

    return spicy_stats.pearsonr(input_data, output_data)[0]

def create_weightings(sample_size, entry_date, exit_date):


    # collect training tickers
    tickers = [company.ticker for company in company_adaptor.get_n_companies(sample_size)]
    
    detailed_inputs = {}

    # gather performance data for time frame
    performance = {}
    for ticker in tickers:
        print(ticker)
        performance[ticker] = get_performance(ticker, entry_date, exit_date)
        detailed_inputs[ticker] = model_one.get_ticker_data(ticker, entry_date)

    # list desired training inputs
    inputs = [    
        'netIncome',
        'ROA',
        'sharesOutstanding',
        'earningsYield',
        'increaseDaysSalesOutstanding',
        'declinesInDepreciation',
        'retainedEarningsToTotalAssets',
        'operatingCashflow',
        'ltDebtVsAssets',
        'grossMargins',
        'returnOnCapital',
        'growingDaysSalesOfInventory',
        'salesToAssets',
        'returnOnTotalAssets',
        'qualityOfEarnings',
        'currentRatio',
        'assetTurnover',
        'netIncomeMinusCashflow',
        'increasingCurrentAssetsOverRevenues',
        'workingCapitalToTotalAssets',
        'marketCapToTotalLiabilities'
    ]

    correlations = {}

    # populate correlation variable with correlations to inputs
    for input in inputs:
        correlations[input] = calculate_correlation(input, detailed_inputs, performance, entry_date)

    # normalize correlations into weightings
    weightings = {}
    correlation_sum = sum(correlations.values())

    for input in correlations:
        weightings[input] = correlations[input]/correlation_sum * 100

    return weightings

def collect_and_save_plots(sample_size, entry_date, exit_date):
    # collect training tickers
    tickers = [company.ticker for company in company_adaptor.get_n_companies(sample_size)]
    
    detailed_inputs = {}

    # gather data for time frame
    count = 0
    for ticker in tickers:
        count += 1
        print(ticker + ' - ' + str(count) + '/' + str(sample_size))
        if ticker[-1].upper() == 'F' and len(ticker) == 5:
            print('skip...')
            continue
        
        detailed_inputs[ticker] = model_one.get_ticker_data(ticker, entry_date)

    # list desired training inputs

    input_data_frame = {
        'ticker': [],
        'netIncome': [],
        'ROA': [],
        'sharesOutstanding': [],
        'earningsYield': [],
        'increaseDaysSalesOutstanding': [],
        'declinesInDepreciation': [],
        'retainedEarningsToTotalAssets': [],
        'operatingCashflow': [],
        'ltDebtVsAssets': [],
        'grossMargins': [],
        'returnOnCapital': [],
        'growingDaysSalesOfInventory': [],
        'salesToAssets': [],
        'returnOnTotalAssets': [],
        'qualityOfEarnings': [],
        'currentRatio': [],
        'assetTurnover': [],
        'netIncomeMinusCashflow': [],
        'increasingCurrentAssetsOverRevenues': [],
        'workingCapitalToTotalAssets': [],
        'marketCapToTotalLiabilities': [],
        'futurePerformance': []
    }

    boolean_data_frame = {
        'ticker': [],
        'netIncome': [],
        'ROA': [],
        'sharesOutstanding': [],
        'earningsYield': [],
        'increaseDaysSalesOutstanding': [],
        'declinesInDepreciation': [],
        'retainedEarningsToTotalAssets': [],
        'operatingCashflow': [],
        'ltDebtVsAssets': [],
        'grossMargins': [],
        'returnOnCapital': [],
        'growingDaysSalesOfInventory': [],
        'salesToAssets': [],
        'returnOnTotalAssets': [],
        'qualityOfEarnings': [],
        'currentRatio': [],
        'assetTurnover': [],
        'netIncomeMinusCashflow': [],
        'increasingCurrentAssetsOverRevenues': [],
        'workingCapitalToTotalAssets': [],
        'marketCapToTotalLiabilities': [],
        'futurePerformance': []
    }

    count = 0
    for ticker in detailed_inputs:
        print(str(count) + '/' + str(sample_size))
        if detailed_inputs[ticker] is None:
            continue

        for input in input_data_frame:

            if input == 'ticker':
                input_data_frame[input].append(ticker)
                boolean_data_frame[input].append(ticker)
                continue

            if input == 'futurePerformance':
                input_data_frame[input].append(get_performance(ticker, entry_date, exit_date))
                boolean_data_frame[input].append(get_performance(ticker, entry_date, exit_date))
                continue

            boolean_data_frame[input].append((detailed_inputs[ticker][input]['over'] and detailed_inputs[ticker][input]['value'] > detailed_inputs[ticker][input]['standard']) or (not detailed_inputs[ticker][input]['over'] and detailed_inputs[ticker][input]['value'] < detailed_inputs[ticker][input]['standard']))

            input_data_frame[input].append(detailed_inputs[ticker][input]['value'])
                
    pd.DataFrame(data=input_data_frame).to_csv('databases/excel/absolute_inputs.csv')
    pd.DataFrame(data=boolean_data_frame).to_csv('databases/excel/boolean_inputs.csv')

    
