import json, requests
import datetime
import os

API_KEY = os.environ.get('API_KEY') 

# -------- MAIN FUNCTIONS ---------#

def earnings_calender(start_date, end_date):
    # collect all companies included on yahoo's earnings calender for the given range

        # adapt inputs into datatime objects
        date_from = int(datetime.datetime.strptime(start_date, '%Y-%m-%d' ).timestamp() * 1000)
        date_to = int(datetime.datetime.strptime(end_date, '%Y-%m-%d' ).timestamp() * 1000 + 86400000)
        print(date_from)
        print(date_to)
        companies = earnings_API(date_from, date_to)
        print(companies)
        return [(company['ticker'], company['companyShortName']) for company in companies['finance']['result']]

def extract_financials(ticker):

    response = stock_API("https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials", ticker)

    financialPeriods = []

    # get yearly financials
    
    max_years = len(response['incomeStatementHistory']['incomeStatementHistory'])
    
    for i in range(max_years):
        financialPeriods.append({
            'ticker': ticker,
            'period': 12,
            'end_date': response['incomeStatementHistory']['incomeStatementHistory'][i]['endDate']['fmt'],
            'incomeStatement': cleanFinancialData(response['incomeStatementHistory']['incomeStatementHistory'][i]),
            'balanceSheet': cleanFinancialData(response['balanceSheetHistory']['balanceSheetStatements'][i]),
            'cashflowStatement': cleanFinancialData(response['cashflowStatementHistory']['cashflowStatements'][i])
        })
            

    # get quarterly financials
    
    max_quarters = len(response['incomeStatementHistoryQuarterly']['incomeStatementHistory'])

    for i in range(max_quarters):
        financialPeriods.append({
            'ticker': ticker,
            'period': 3,
            'end_date': response['incomeStatementHistoryQuarterly']['incomeStatementHistory'][i]['endDate']['fmt'],
            'incomeStatement': cleanFinancialData(response['incomeStatementHistoryQuarterly']['incomeStatementHistory'][i]),
            'balanceSheet': cleanFinancialData(response['balanceSheetHistoryQuarterly']['balanceSheetStatements'][i]),
            'cashflowStatement': cleanFinancialData(response['cashflowStatementHistoryQuarterly']['cashflowStatements'][i])
        })
            

    return financialPeriods

def extract_performance(ticker):
    response = stock_API("https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary", ticker)

    performance = {
        'date': str(datetime.date.today()),
        'price': response['price']['regularMarketPrice'].get('raw', None),
        'eps': response['defaultKeyStatistics']['trailingEps'].get('raw', None),
        'market_cap': response['summaryDetail']['marketCap'].get('raw', None),
    }

    return performance

# -------- HELPER FUNCTIONS -------#

def stock_API(url, ticker):

    headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params={"symbol": ticker}).text
    return json.loads(response)

def earnings_API(date_from, date_to):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-earnings"

    querystring = {"region":"US","startDate":date_from,"endDate":date_to}

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return json.loads(response.text)

def cleanFinancialData(data):

    clean_data = data

    for item in data:
        if item != 'maxAge':
            clean_data[item] = data[item].get('raw', None)

    return clean_data