import datetime
import sys

# Local application imports
import databases.aliias_stocks.manager as stock_db_manager
import databases.aliias_stocks.controllers.data_pipeline as data_pipeline
import databases.aliias_stocks.controllers.loading_functions as loading_functions


if __name__ == '__main__':
    
    command = sys.argv[1]

    stock_db_manager.setup_heroku_mongo_connection()

    if command == 'earnings_calender':
        if len(sys.argv) > 2:
            date = sys.argv[2]
        else:
            date = str(datetime.date.today() - datetime.timedelta(days=1))

        data_pipeline.collect_earnings(date)

    if command == 'collect_ticker_prices':
        if len(sys.argv) > 2:
            date = sys.argv[2]
        else:
            date = str(datetime.date.today() - datetime.timedelta(days=1))

        data_pipeline.collect_ticker_prices(date)

    if command == 'collect_quote_data':
        data_pipeline.collect_quote_data()

    if command == 'load_price_and_evaluate_earnings':
        loading_functions.load_price_and_evaluate_earnings()
