"""
This module hosts functions related to configuring
and setting up connections with the external mongoDB
databases
"""
# Standard libary imports
import datetime
import os
import sys

# Third party imports -- None
import mongoengine

# Local application imports
import controllers.data_pipeline as data_pipeline
import controllers.loading_functions as loading_functions

def setup_local_connection(database):
    mongoengine.connect(db=database, alias='core', host='localhost:27017')

def setup_heroku_mongo_connection():
    mongoengine.connect(host='mongodb+srv://' + os.environ.get('DB_ACCOUNT') + ':' + os.environ.get('DB_PASSWORD') + '@realmcluster.zudeo.mongodb.net/' + os.environ.get('DB_NAME') + '?retryWrites=true&w=majority', alias='core')

def setup_network_connection(database):
    account_name = 'webApp'
    account_password = 't3NMqHZh2Jn1gNTO'
    mongoengine.connect(host='mongodb+srv://' + account_name + ':' + account_password + '@realmcluster.zudeo.mongodb.net/' + database + '?retryWrites=true&w=majority', alias='core')


# ------------- COMMANDS -------------- # 


if __name__ == '__main__':
    
    command = sys.argv[1]


    setup_network_connection('aliias')

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

    if command == 'load_price_and_evaluate_earnings':
        loading_functions.load_price_and_evaluate_earnings()
