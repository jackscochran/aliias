"""
This module represents the companies collection 
data object model
"""

# Standard libary imports
import datetime
from ..helpers import timeline

# Third party imports 
import mongoengine

# Local application imports
from ..data import financial_periods as financial_periods
from ..data import daily_prices as daily_prices
from ..data import evaluations as evaluations
from ..data import quotes as quotes


class Company(mongoengine.Document):
    ticker = mongoengine.StringField(unique=True, required=True)
    company_name = mongoengine.StringField(required=True)
    industry = mongoengine.StringField()
    sector = mongoengine.StringField()

    def get_latest_financials(self, period):
        return self.get_financials(str(datetime.date.today()), period)

    def get_latest_quote_data(self):
        return self.get_quote_data(str(datetime.date.today()))

    def get_latest_price(self):
        return self.get_price(str(datetime.date.today()))

    def get_financials(self, date, period):
        return financial_periods.FinancialPeriod.objects(ticker=self.ticker, period_length=period, end_date__lte=date).order_by('-end_date').first()

    def get_quote_data(self, date):
        return quotes.Quote.objects(ticker=self.ticker, date__lte=date).order_by('-date').first()

    def get_evaluations(self):
        return evaluations.Evaluation.objects(ticker=self.ticker)

    def get_evaluation(self, date):
        return evaluations.Evaluation.objects(ticker=self.ticker, date__lte=date).order_by('-date').first()

    def get_latest_evaluation(self):
        return evaluations.Evaluation.objects(ticker=self.ticker).order_by('-date').first()

    def get_price(self, date):
        return daily_prices.DailyPrice.objects(ticker=self.ticker, date__lte=date).order_by('-date').first()

    def performance(self, start, period):

        future_value = self.get_price(timeline.change_months(start, period))
        current_value = self.get_price(start)

        if future_value and current_value:
            return (future_value.price / current_value.price - 1)
        
        return None
 

    meta = {
        'db_alias': 'core',
        'collection': 'companies'
    }
