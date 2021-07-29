import json, requests
import datetime
import os
import yahoo_fin.stock_info as yf_stock_info
from yahoo_fin import news as yf_news

# -------- MAIN FUNCTIONS ---------#

def earnings_on(date):
    response = yf_stock_info.get_earnings_for_date(date)
    return [(company['ticker'], company['companyshortname']) for company in response]

def extract_financials(ticker):

    financials = yf_stock_info.get_financials(ticker)

    formatted_financial_periods = []

    yearly_income_statements = financials['yearly_income_statement'].to_dict()
    yearly_balance_sheets = financials['yearly_balance_sheet'].to_dict()
    yearly_cash_flow = financials['yearly_cash_flow'].to_dict()

    for end_date_time_stamp in yearly_income_statements:
        formatted_financial_periods.append({
            'ticker': ticker,
            'period': 12,
            'end_date': str(end_date_time_stamp).split(' ')[0],
            'incomeStatement': yearly_income_statements[end_date_time_stamp],
            'balanceSheet': yearly_balance_sheets[end_date_time_stamp],
            'cashflowStatement': yearly_cash_flow[end_date_time_stamp]
        })

    quarterly_income_statements = financials['quarterly_income_statement'].to_dict()
    quarterly_balance_sheets = financials['quarterly_balance_sheet'].to_dict()
    quarterly_cash_flow = financials['quarterly_cash_flow'].to_dict()

    for end_date_time_stamp in quarterly_income_statements:
        formatted_financial_periods.append({
            'ticker': ticker,
            'period': 3,
            'end_date': str(end_date_time_stamp).split(' ')[0],
            'incomeStatement': quarterly_income_statements[end_date_time_stamp],
            'balanceSheet': quarterly_balance_sheets[end_date_time_stamp],
            'cashflowStatement': quarterly_cash_flow[end_date_time_stamp]
        })

    return formatted_financial_periods

def extract_quote_data(ticker):
    
    quote_data = yf_stock_info.get_quote_table(ticker)

    # remove unnessary data
    quote_data.pop('symbol', None)

    # rename variables to camelCase and reformat data
    quote_data['firstYearTargetEst'] = quote_data.pop('1y Target Est')
    quote_data['fiftyTwoWeekRange'] = quote_data.pop('52 Week Range')
    quote_data['ask'] = quote_data.pop('Ask')
    quote_data['betaFiveYearMonthly'] = quote_data.pop('Beta (5Y Monthly)')
    quote_data['bid'] = quote_data.pop('Bid')
    quote_data['daysRange'] = quote_data.pop("Day's Range")
    quote_data['epsTtm'] = quote_data.pop('EPS (TTM)')
    quote_data['earningsDate'] = quote_data.pop('Earnings Date')
    quote_data['exDividendDate'] = quote_data.pop('Ex-Dividend Date')
    quote_data['forwardDividendAndYield'] = quote_data.pop('Forward Dividend & Yield')
    quote_data['marketCap'] = convert_currency(quote_data.get('Market Cap', None))
    quote_data['open'] = quote_data.pop('Open')
    quote_data['peRatioTtm'] = quote_data.pop('PE Ratio (TTM)')
    quote_data['previous'] = quote_data.pop('Previous Close')
    quote_data['quotePrice'] = quote_data.pop('Quote Price')
    quote_data['volume'] = quote_data.pop('Volume')
    quote_data['avgVolume'] = quote_data.pop('Avg. Volume', None)

    quote = {
        'ticker': ticker,
        'date': str(datetime.date.today()),
        'data': quote_data
    }
    
    return quote

def get_price(ticker):
    return yf_stock_info.get_live_price(ticker) 

def get_rss_news(ticker):
    return yf_news.get_yf_rss(ticker)

# ------------ Helper Functions -------------- #

def convert_currency(amount):

    if not amount:
        return amount

    value = float(amount[:-1])

    aplifiers = {
        'G': 1000,
        'M': 1000000,
        'B': 1000000000,
        'T': 1000000000000
    }

    return value * aplifiers.get(amount[-1])
