"""
A database adaptor module that hosts functions to
interact with the daily pirces collection in the 
mondoDB database
"""
import math

from ..data import daily_prices
from ..controllers import data_pipeline
from ..helpers import timeline

def add_price(ticker, date, price):
    daily_price =  daily_prices.DailyPrice.objects(ticker=ticker, date=date).first()
    
    if not daily_price:
        daily_price = daily_prices.DailyPrice()
        daily_price.ticker = ticker
        daily_price.date = date
        daily_price.price = price
        daily_price.save()


    if daily_price.price == -1:
        daily_price.price = price
        daily_price.save()

def get_price(ticker, date):
    price = daily_prices.DailyPrice.objects(ticker=ticker, date__lte=date).order_by('-date').first()

    if price is None:
        return price

    return price.price

def get_weekday_price(ticker, date):
    #if weekend, find nearest monday
    if timeline.weekday(date) == 6:
        date = timeline.change_days(date, 1)
    elif timeline.weekday(date) == 5:
        date = timeline.change_days(date, 2)
    price = daily_prices.DailyPrice.objects(ticker=ticker, date=date).first()

    if price is None:
        price = data_pipeline.collect_and_save_price(ticker, date) 
    else:
        price = price.price

    if math.isnan(price): # stock holiday - set to wednesday
        if timeline.weekday(date) == 0: # monday
            date = timeline.change_days(date, 2)
        elif timeline.weekday(date) == 1: # tuesday
            date = timeline.change_days(date, 1)
        elif timeline.weekday(date) == 3: # wednesday - set to tuesday
            date = timeline.change_days(date, -1)
        elif timeline.weekday(date) == 1: #thursday
            date = timeline.change_days(date, -1)
        elif timeline.weekday(date) == 1: # friday
            date = timeline.change_days(date, -2)

        price = daily_prices.DailyPrice.objects(ticker=ticker, date=date).first()
    

        if price is None:
            price = data_pipeline.collect_and_save_price(ticker, date) 
        else:
            price = price.price

    return price


def exists(ticker, date):
    return daily_prices.DailyPrice.objects(ticker=ticker, date=date).first() is not None

