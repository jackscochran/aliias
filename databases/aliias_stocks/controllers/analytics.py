import adaptors.company as company_adaptor
import adaptors.portfolio as portfolio_adaptor
import adaptors.daily_price as price_adaptor
import evaluators.model_one as model_one
import manager
import numpy as np
import matplotlib.pyplot as plt
import helpers.timeline as timeline
import datetime
import scipy.stats as scipy_stats
import math


def get_performance(ticker, start, end):
    entry_price = price_adaptor.get_price(ticker, start)
    exit_price = price_adaptor.get_price(ticker, end)

    if entry_price is None or exit_price is None:
        return None

    return exit_price - entry_price

def calculate_correlation(input, detailed_inputs, performance_data, training_date_cap):
    input_data = []
    output_data = []

    for ticker in performance_data:
        if detailed_inputs[ticker] is None or performance_data[ticker] is None:
            continue

        data = detailed_inputs[ticker].get(input, None)
        if data is not None and not math.isnan(data['value']):
            input_data.append(data['value'])
            output_data.append(performance_data[ticker])

    if len(input_data) == 0 or len(output_data) == 0:
        return 0

    return scipy_stats.pearsonr(input_data, output_data)[0]

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
    inputs = ['netIncome',
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

