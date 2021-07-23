from data.financialPeriods import FinancialPeriod
from data.performances import Performance
from data.evaluations import Evaluation
import mongoengine
import datetime

class Company(mongoengine.Document):
    ticker = mongoengine.StringField(unique=True, required=True)
    company_name = mongoengine.StringField(required=True)

    def get_latest_financials(self, period):
        return self.get_financials(str(datetime.date.today()), period)

    def get_latest_performance(self):
        return self.get_financials(str(datetime.date.today()))

    def get_financials(self, date, period):
        return FinancialPeriod.objects(ticker=self.ticker, period_length=period, end_date__lte=date).order_by('-end_date').first()

    def get_performance_data(self, date):
        return Performance.objects(ticker=self.ticker, date__lte=date).order_by('-date').first()

    def get_evaluations(self):
        return Evaluation.objects(ticker=self.ticker)

    def performace(self, start, period):

        future_performance = self.get_performance_data(change_months(start, period))
        current_performance = self.get_performance_data(start)

        if future_performance:
            return future_performance.price / current_performance.price
        
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