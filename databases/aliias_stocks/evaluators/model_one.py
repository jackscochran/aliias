"""
The model-1 is the initiaal stock rating algorithm
that uses soley quanatative data
"""

# Standard libary imports
import datetime

# Third party imports

# Local application imports
from ..adaptors import company as company_adaptor
from ..adaptors import evaluation as evaluation_adaptor

EVALUATOR_NAME = 'modelOne'

def evaluate_ticker(ticker, date):
        if ticker[-1].upper() == 'F' and len(ticker) == 5: 
            # foreign stock, does not compute with model one
            return

        # load ticker data
        data = get_ticker_data(ticker, date)

        if data is None:
            return

        # rate ticker
        rating = rate(data)

        # create and save evaluation 
        evaluation_adaptor.add_evaluation(
            ticker=ticker,
            date=date,
            evaluator_name=EVALUATOR_NAME,
            rating=rating,
        )

def get_weightings():
    weightings = {
        'netIncome': 3.14049035430264,
        'ROA': 3.35787341867148,
        'sharesOutstanding': 9.89330948577594,
        'earningsYield': 8.59360955585488,
        'increaseDaysSalesOutstanding': 2.17412921827518,
        'declinesInDepreciation': 11.8823215821384,
        'retainedEarningsToTotalAssets': 1.12945471301263,
        'operatingCashflow': 4.95404940943786,
        'ltDebtVsAssets': 0.432216733067582,
        'grossMargins': 0.408198164601095,
        'returnOnCapital': 3.86967413358317,
        'growingDaysSalesOfInventory': 1.200997551491,
        'salesToAssets': 3.60114685180111,
        'returnOnTotalAssets': 14.700528329515,
        'qualityOfEarnings':  4.53200718886259,
        'currentRatio': 5.31267035221777,
        'assetTurnover': 1.36950228222849,
        'netIncomeMinusCashflow': 3.62023341625806,
        'increasingCurrentAssetsOverRevenues': 5.77809130603686,
        'workingCapitalToTotalAssets': 6.90517210980709,
        'marketCapToTotalLiabilities': 3.14432384306122
    }
    return weightings
# -------- EVALUATION FUNCTIONS -------- #

def rate(inputs):
    
    if inputs is None:
        return None
    
    rating = 0

    for input in inputs:
        if (inputs[input]['over'] and inputs[input]['value'] > inputs[input]['standard']) or ((not inputs[input]['over']) and inputs[input]['value'] < inputs[input]['standard']):
            rating += inputs[input]['weighting']

    return rating/10

def get_ticker_data(ticker, date):
    company = company_adaptor.get_company(ticker)

    data = [None] * 3

    share_price = company.get_price(date)
    if share_price is None:
        share_price = company.get_latest_price()
    
    if share_price is None:
        print('Insufficent data for rating, Could not find price data for ' + ticker + ' on or before the date ' + date)
        return

    raw_quote_data = company.get_quote_data(date)

    if raw_quote_data is None:
        raw_quote_data = company.get_latest_quote_data()

    if raw_quote_data is None:
        print('Insufficent data for rating, Could not find quote data for ' + ticker + ' on or before the date ' + date)
        return

    quote_data = {
        'market_cap': raw_quote_data.data.get('marketCap', 1),
        'eps': raw_quote_data.data.get('epsTtm', 1)
    }

    for years_back in range(3):

        financials = company.get_financials(date, 12)
        if financials == None:
            print('Insufficent data for rating, Could not find financials for ' + ticker + ' on or before the date ' + date)
            return None

        data[years_back] = {}

        if financials:
            data[years_back] = {
                'sharePrice': share_price.price,
                'marketCap': quote_data['market_cap'],
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
                'eps': quote_data['eps'] 
            }
            

        date = decriment_year(date)

    # remove any zeros
    for financial_year in data:
        for item in financial_year:
            if financial_year[item] == 0 or financial_year[item] == None:
                financial_year[item] = 1


    weightings = get_weightings()
    inputs = {
        'netIncome': {
            'value': data[0].get('netIncome', 1),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('netIncome', 0) 
        },
        'ROA': {
            'value': (data[0].get('ebit', 1)/data[0].get('totalAssets', 1))-(data[1].get('ebit', 1)/data[1].get('totalAssets', 1)),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('ROA', 0) 
        },
        'sharesOutstanding': {
            'value': -data[0].get('shareIssuance', 1)-data[0].get('shareBuyback', 1)+data[1].get('shareIssuance', 1)+data[1].get('shareBuyback', 1),
            'over': False,
            'standard': 00000000000000000000000000000000000000000000000000000000.1, #less than or equal to zero
            'weighting': weightings.get('sharesOutstanding', 0) 
        },
        'earningsYield': {
            'value': data[0].get('eps', 1)/data[0].get('sharePrice', 1),
            'over': True,
            'standard': 0.06,
            'weighting': weightings.get('earningsYield', 0) 
        },
        'increaseDaysSalesOutstanding': {
            'value': data[0].get('netReceivables', 1)/data[0].get('revenue', 1) - data[1].get('netReceivables', 1)/data[1].get('revenue', 1) + data[1].get('netReceivables', 1)/data[1].get('revenue', 1) - data[2].get('netReceivables', 1)/data[2].get('revenue', 1),
            'over': False,
            'standard': 0,
            'weighting': weightings.get('increaseDaysSalesOutstanding', 0) 
        },
        'declinesInDepreciation': { # unsure if good or bad
            'value': (data[0].get('depreciation', 1)-data[1].get('depreciation', 1))+(data[1].get('depreciation', 1)-data[2].get('depreciation', 1)),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('declinesInDepreciation', 0) 
        },
        'retainedEarningsToTotalAssets': {
            'value': data[0].get('retainedEarnings', 1)/data[0].get('totalAssets', 1),
            'over': False,
            'standard': 1,
            'weighting': weightings.get('retainedEarningsToTotalAssets', 0) 
        },
        'operatingCashflow': {
            'value': data[0].get('operatingCashflow', 1),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('operatingCashflow', 0) 
        },
        'ltDebtVsAssets': { # formula needs checking
            'value': (data[0].get('longTermDebt', 1)/data[0].get('totalAssets', 1))-(data[2].get('longTermDebt', 1)/data[2].get('totalAssets', 1)), 
            'over': False,
            'standard': 0,
            'weighting': weightings.get('ltDebtVsAssets', 0) 
        },
        'grossMargins': { # formula needs checking
            'value': ((data[0].get('operatingIncome', 1)/data[0].get('revenue', 1))-(data[2].get('operatingIncome', 1)/data[2].get('revenue', 1))),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('grossMargins', 0) 
        },
        'returnOnCapital': { # need checking
            'value': (data[0].get('ebit', 1)/data[0].get('marketCap', 1))-(data[2].get('ebit', 1)/data[2].get('marketCap', 1)),
            'over': True,
            'standard': 0.01,
            'weighting': weightings.get('returnOnCapital', 0) 
        },
        'growingDaysSalesOfInventory': {
            'value': ((data[0].get('revenue', 1)/data[0].get('inventory', 1))- (data[2].get('revenue', 1)/data[2].get('inventory', 1))),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('growingDaysSalesOfInventory', 0) 
        },
        'salesToAssets': {
            'value': data[0].get('revenue', 1) / data[0].get('totalAssets', 1),
            'over': False,
            'standard': 1,
            'weighting': weightings.get('salesToAssets', 0)
        },
        'returnOnTotalAssets': {
            'value': data[0].get('ebit', 1) / data[0].get('totalAssets', 1),
            'over': False,
            'standard': 0.05,
            'weighting': weightings.get('returnOnTotalAssets', 0)
        },
        'qualityOfEarnings': {
            'value': data[0].get('operatingIncome', 1)-(data[0].get('revenue', 1)/data[0].get('totalAssets', 1)),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('qualityOfEarnings', 0)
        },
        'currentRatio': {
            'value': data[0].get('currentAssets', 1) / data[0].get('currentLiabilities', 1),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('currentRatio', 0) 
        },
        'assetTurnover': { # check formula
            'value': ((data[0].get('revenue', 1)/data[0].get('totalAssets', 1))-(data[2].get('revenue', 1)/data[2].get('totalAssets', 1))),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('assetTurnover', 0) ,
        },
        'netIncomeMinusCashflow': {
            'value': data[0].get('netIncome', 1) - data[0].get('operatingCashflow', 1),
            'over': False,
            'standard': 0,
            'weighting': weightings.get('netIncomeMinusCashflow', 0) 
        }, # check formula
        'increasingCurrentAssetsOverRevenues': {
            'value': ((data[0].get('currentAssets', 1)/data[0].get('revenue', 1))-(data[2].get('currentAssets', 1)/data[2].get('revenue', 1))),
            'over': True,
            'standard': 0,
            'weighting': weightings.get('increasingCurrentAssetsOverRevenues', 0) 
        },
        'workingCapitalToTotalAssets': {
            'value': (data[0].get('currentAssets', 1)-data[0].get('currentLiabilities', 1))/data[0].get('totalAssets', 1),
            'over': False,
            'standard': 1,
            'weighting': weightings.get('workingCapitalToTotalAssets', 0)
        },
        'marketCapToTotalLiabilities': {
            'value': data[0].get('marketCap', 1)/data[0].get('totalLiabilities', 1),
            'over': False,
            'standard': 1,
            'weighting': weightings.get('marketCapToTotalLiabilities', 0) 
        }
    }

    return inputs

# ---------- HELPER FUNCTIONS -----------#

def decriment_year(date):
    date = date.split('-')

    date[0] = str(int(date[0]) - 1)

    return date[0] + '-' + date[1] + '-' + date[2]

def increment_year(date):
    date = date.split('-')

    date[0] = str(int(date[0]) - 1)

    return date[0] + '-' + date[1] + '-' + date[2]

