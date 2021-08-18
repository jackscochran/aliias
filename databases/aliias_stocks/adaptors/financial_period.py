"""
A database adaptor module that hosts functions to
interact with the financial periods collection in the 
mondoDB database
"""

from ..data import financial_periods

def add_financialPeriod(financials):

    period = financial_periods.FinancialPeriod.objects(ticker=financials['ticker'], period_length=financials['period'], end_date=financials['end_date']).first()

    if not period: # add new period to database
        period = financial_periods.FinancialPeriod()
        period.ticker = financials['ticker']
        period.period_length = financials['period']
        period.end_date = financials['end_date']

        period.incomeStatement = financials['incomeStatement']
        period.balanceSheet = financials['balanceSheet']
        period.cashflowStatement = financials['cashflowStatement']
        period.save()
