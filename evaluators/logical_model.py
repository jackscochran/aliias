from data.performances import Performance
from data.companies import Company
import services.stock_adaptor as db_adaptor
import datetime

EVALUATOR_NAME = 'Logical'

# -------- EVALUATION FUNCTIONS -------- #

def rate(data):

    inputs = {
        'netIncome': {
            'value': data[0].get('netIncome', 1),
            'over': True,
            'standard': 0,
            'weighting': 3.14049035430264
        },
        'ROA': {
            'value': (data[0].get('ebit', 1)/data[0].get('totalAssets', 1))-(data[1].get('ebit', 1)/data[1].get('totalAssets', 1)),
            'over': True,
            'standard': 0,
            'weighting': 3.35787341867148
        },
        'sharesOutstanding': {
            'value': -data[0].get('shareIssuance', 1)-data[0].get('shareBuyback', 1)+data[1].get('shareIssuance', 1)+data[1].get('shareBuyback', 1),
            'over': False,
            'standard': 00000000000000000000000000000000000000000000000000000000.1, #less than or equal to zero
            'weighting': 9.89330948577594
        },
        'earningsYield': {
            'value': data[0].get('eps', 1)/data[0].get('sharePrice', 1),
            'over': True,
            'standard': 0.06,
            'weighting': 8.59360955585488
        },
        'increaseDaysSalesOutstanding': {
            'value': data[0].get('netReceivables', 1)/data[0].get('revenue', 1) - data[1].get('netReceivables', 1)/data[1].get('revenue', 1) + data[1].get('netReceivables', 1)/data[1].get('revenue', 1) - data[2].get('netReceivables', 1)/data[2].get('revenue', 1),
            'over': False,
            'standard': 0,
            'weighting': 2.17412921827518
        },
        'declinesInDepreciation': { # unsure if good or bad
            'value': (data[0].get('depreciation', 1)-data[1].get('depreciation', 1))+(data[1].get('depreciation', 1)-data[2].get('depreciation', 1)),
            'over': True,
            'standard': 0,
            'weighting': 11.8823215821384
        },
        'retainedEarningsToTotalAssets': {
            'value': data[0].get('retainedEarnings', 1)/data[0].get('totalAssets', 1),
            'over': False,
            'standard': 1,
            'weighting': 1.12945471301263
        },
        'operatingCashflow': {
            'value': data[0].get('operatingCashflow', 1),
            'over': True,
            'standard': 0,
            'weighting': 4.95404940943786
        },
        'ltDebtVsAssets': { # formula needs checking
            'value': (data[0].get('longTermDebt', 1)/data[0].get('totalAssets', 1))-(data[2].get('longTermDebt', 1)/data[2].get('totalAssets', 1)), 
            'over': False,
            'standard': 0,
            'weighting': 0.432216733067582
        },
        'grossMargins': { # formula needs checking
            'value': ((data[0].get('operatingIncome', 1)/data[0].get('revenue', 1))-(data[2].get('operatingIncome', 1)/data[2].get('revenue', 1))),
            'over': True,
            'standard': 0,
            'weighting': 0.408198164601095
        },
        'returnOnCapital': { # need checking
            'value': (data[0].get('ebit', 1)/data[0].get('marketCap', 1))-(data[2].get('ebit', 1)/data[2].get('marketCap', 1)),
            'over': True,
            'standard': 0.01,
            'weighting': 3.86967413358317
        },
        'growingDaysSalesOfInventory': {
            'value': ((data[0].get('revenue', 1)/data[0].get('inventory', 1))- (data[2].get('revenue', 1)/data[2].get('inventory', 1))),
            'over': True,
            'standard': 0,
            'weighting': 1.200997551491
        },
        'salesToAssets': {
            'value': data[0].get('revenue', 1) / data[0].get('totalAssets', 1),
            'over': False,
            'standard': 1,
            'weighting': 3.60114685180111
        },
        'returnOnTotalAssets': {
            'value': data[0].get('ebit', 1) / data[0].get('totalAssets', 1),
            'over': False,
            'standard': 0.05,
            'weighting': 14.700528329515
        },
        'qualityOfEarnings': {
            'value': data[0].get('operatingIncome', 1)-(data[0].get('revenue', 1)/data[0].get('totalAssets', 1)),
            'over': True,
            'standard': 0,
            'weighting': 4.53200718886259
        },
        'currentRatio': {
            'value': data[0].get('currentAssets', 1) / data[0].get('currentLiabilities', 1),
            'over': True,
            'standard': 0,
            'weighting': 5.31267035221777
        },
        'assetTurnover': { # check formula
            'value': ((data[0].get('revenue', 1)/data[0].get('totalAssets', 1))-(data[2].get('revenue', 1)/data[2].get('totalAssets', 1))),
            'over': True,
            'standard': 0,
            'weighting': 1.36950228222849,
        },
        'netIncomeMinusCashflow': {
            'value': data[0].get('netIncome', 1) - data[0].get('operatingCashflow', 1),
            'over': False,
            'standard': 0,
            'weighting': 3.62023341625806
        }, # check formula
        'increasingCurrentAssetsOverRevenues': {
            'value': ((data[0].get('currentAssets', 1)/data[0].get('revenue', 1))-(data[2].get('currentAssets', 1)/data[2].get('revenue', 1))),
            'over': True,
            'standard': 0,
            'weighting': 5.77809130603686
        },
        'workingCapitalToTotalAssets': {
            'value': (data[0].get('currentAssets', 1)-data[0].get('currentLiabilities', 1))/data[0].get('totalAssets', 1),
            'over': False,
            'standard': 1,
            'weighting': 6.90517210980709
        },
        'marketCapToTotalLiabilities': {
            'value': data[0].get('marketCap', 1)/data[0].get('totalLiabilities', 1),
            'over': False,
            'standard': 1,
            'weighting': 3.14432384306122
        }
    }
    
    rating = 0

    for input in inputs:
        if (inputs[input]['over'] and inputs[input]['value'] > inputs[input]['standard']) or ((not inputs[input]['over']) and inputs[input]['value'] < inputs[input]['standard']):
            rating += inputs[input]['weighting']

    return rating/10

def get_data(ticker, date):
    company = db_adaptor.get_company(ticker)

    data = [None] * 3

    performance_measurements = company.get_performance_data(date)
    
    for years_back in range(3):

        financials = company.get_financials(date, 12)

        data[years_back] = {}

        if financials:
            data[years_back] = {
                'sharePrice': performance_measurements.price,
                'marketCap': performance_measurements.market_cap,
                'revenue': financials.incomeStatement.get('totalRevenue', 1),
                'grossProfit': financials.incomeStatement.get('grossProfit', 1),
                'operatingIncome': financials.incomeStatement.get('operatingIncome', 1),
                'netIncome': financials.incomeStatement.get('netIncome', 1),
                'ebit': financials.incomeStatement.get('ebit', 1),
                'netReceivables': financials.balanceSheet.get('netReceivables', 1),
                'inventory': financials.balanceSheet.get('inventory', 1),
                'currentAssets': financials.balanceSheet.get('totalCurrentAssets', 1),
                'totalAssets': financials.balanceSheet.get('totalAssets', 1),
                'currentLiabilities': financials.balanceSheet.get('totalCurrentLiabilities', 1),
                'longTermDebt': financials.balanceSheet.get('longTermDebt', 1),
                'totalLiabilities': financials.balanceSheet.get('totalLiab', 1),
                'retainedEarnings': financials.cashflowStatement.get('retainedEarnings', 1),
                'dividends': financials.cashflowStatement.get('dividendsPaid', 1),
                'shareIssuance': financials.cashflowStatement.get('issuanceOfStock', 1),
                'shareBuyback': financials.cashflowStatement.get('repurchaseOfStock', 1),
                'operatingCashflow': financials.cashflowStatement.get('totalCashFromOperatingActivities', 1),
                'capitalExpenditure': financials.cashflowStatement.get('capitalExpenditures', 1),
                'depreciation': financials.cashflowStatement.get('depreciation', 1),
                'eps': performance_measurements.eps 
            }
            

        date = decriment_year(date)

    # remove any zeros
    for financial_year in data:
        for item in financial_year:
            if financial_year[item] == 0 or financial_year[item] == None:
                financial_year[item] = 1

    return data

def decriment_year(date):
    date = date.split('-')

    date[0] = str(int(date[0]) - 1)

    return date[0] + '-' + date[1] + '-' + date[2]
