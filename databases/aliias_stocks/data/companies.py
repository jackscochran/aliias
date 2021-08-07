"""
This module represents the companies collection 
data object model
"""

# Standard libary imports
import datetime
import helpers.timeline as timeline

# Third party imports 
import mongoengine

# Local application imports
import data.financial_periods as financial_periods
import data.daily_prices as daily_prices
import data.evaluations as evaluations
import data.quotes as quotes


class Company(mongoengine.Document):
    ticker = mongoengine.StringField(unique=True, required=True)
    company_name = mongoengine.StringField(required=True)

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

    def revenue_growth(self, start, period):

        future_financials = self.get_financials(timeline.change_months(start, period), period)
        current_financials = self.get_financials(start, period)

        if future_financials != current_financials:
            future_revenue = future_financials.incomeStatement.get('totalRevenue', None)
            current_revenue = current_financials.incomeStatement.get('totalRevenue', None)

            if future_revenue:
                return future_revenue/current_revenue

        return None  

    meta = {
        'db_alias': 'core',
        'collection': 'companies'
    }
