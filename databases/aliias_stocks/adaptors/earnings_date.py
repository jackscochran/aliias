"""
A database adaptor module that hosts functions to
interact with the earnings dates collection in the 
mondoDB database
"""

from ..data import earnings_dates

def add_earnings_date(tickers, date):

    earnings_date = earnings_dates.EarningsDate.objects(date=date).first()

    if earnings_date:
        for ticker in tickers:
            if ticker not in earnings_date.tickers:
                earnings_date.tickers.append(ticker)

    else:
        earnings_date = earnings_dates.EarningsDate()
        earnings_date.date = date
        earnings_date.tickers = tickers

    earnings_date.save()

def get_earnings_date(date):
    return earnings_dates.EarningsDate.objects(date=date).first()

def get_all():
    return earnings_dates.EarningsDate.objects