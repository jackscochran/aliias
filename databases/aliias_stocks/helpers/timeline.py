import datetime
from dateutil.relativedelta import relativedelta
import calendar

def change_months(date, months):
    start = date.split('-')
    start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    return str(start_date + relativedelta(months=months))
