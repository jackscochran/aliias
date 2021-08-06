"""
A database adaptor module that hosts functions to
interact with the quotes collection in the 
mondoDB database
"""

from data import quotes

def add_quote(company_quote):
    if company_quote is None:
        return None

    quote = quotes.Quote.objects(date=company_quote.get('date'), ticker=company_quote.get('ticker', None)).first()

    if not quote:  # add new period to database
        quote = quotes.Quote()
        quote.ticker = company_quote.get('ticker', None)
        quote.date = company_quote.get('date', None)
    
        quote.data = company_quote.get('data', None)
        quote.save()
