from data.financialPeriods import FinancialPeriod
from data.dailyPrices import DailyPrice
from data.evaluations import Evaluation
from data.quotes import Quote
import mongoengine
import datetime

class Company(mongoengine.Document):
    ticker = mongoengine.StringField(unique=True, required=True)
    company_name = mongoengine.StringField(required=True)

    def get_latest_financials(self, period):
        return self.get_financials(str(datetime.date.today()), period)

    def get_latest_quote_data(self):
        return self.get_financials(str(datetime.date.today()))

    def get_financials(self, date, period):
        return FinancialPeriod.objects(ticker=self.ticker, period_length=period, end_date__lte=date).order_by('-end_date').first()

    def get_quote_data(self, date):
        return Quote.objects(ticker=self.ticker, date__lte=date).order_by('-date').first()

    def get_evaluations(self):
        return Evaluation.objects(ticker=self.ticker)

    def get_price(self, date):
        return DailyPrice.objects(ticker=self.ticker, date=date).first()

    def performace(self, start, period):

        future_value = self.get_price(change_months(start, period))
        current_value = self.get_price(start)

        if future_value:
            return future_value.price / current_value.price
        
        return None

    def revenue_growth(self, start, period):

        future_financials = self.get_financials(change_months(start, period), period)
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

def change_months(date, months):
    date = date.split('-')

    date[0] = str(int(date[0]) + int(months/12))
    date[1] = str(int(date[1]) + months%12)

    return date[0] + '-' + date[1] + '-' + date[2]