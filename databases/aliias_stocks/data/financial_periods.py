import mongoengine

class FinancialPeriod(mongoengine.Document):
    ticker = mongoengine.StringField(required=True)
    period_length = mongoengine.IntField(required=True)
    end_date = mongoengine.StringField(required=True)
    incomeStatement = mongoengine.DictField()
    balanceSheet = mongoengine.DictField()
    cashflowStatement = mongoengine.DictField()

    meta = {
        'db_alias': 'core',
        'collection': 'financialPeriods',
        'indexes': [
            {'fields': ('ticker', 'period_length', 'end_date'), 'unique': True}
        ]
    }