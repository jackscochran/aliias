"""
A database adaptor module that hosts functions to
interact with the daily pirces collection in the 
mondoDB database
"""

from data import daily_prices

def add_price(ticker, date, price):
    daily_price =  daily_prices.DailyPrice.objects(ticker=ticker, date=date).first()
    
    if not daily_price:
        daily_price = daily_prices.DailyPrice()
        daily_price.ticker = ticker
        daily_price.date = date

        daily_price.price = price
        daily_price.save()

def get_price(ticker, date):
    return daily_prices.DailyPrice.objects(ticker=ticker, date=date).first()

def exists(ticker, date):
    return daily_prices.DailyPrice.objects(ticker=ticker, date=date).first() is not None