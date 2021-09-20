import datetime
from dateutil.relativedelta import relativedelta
import calendar

def change_months(date, months):
    start = date.split('-')
    start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    return str(start_date + relativedelta(months=months))
    
def weekday(date):
    date = date.split('-')
    day = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    return day.weekday()

def change_days(date, days):
    start = date.split('-')
    start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    return str(start_date + datetime.timedelta(days=days))
