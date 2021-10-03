"""
This module hosts functions related to configuring
and setting up connections with the external mongoDB
databases
"""
# Standard libary imports
import os

# Third party imports -- None
import mongoengine


def setup_local_connection(database):
    mongoengine.connect(db=database, alias='core', host='localhost:27017')

def setup_heroku_mongo_connection():
    mongoengine.connect(host='mongodb+srv://' + os.environ.get('DB_ACCOUNT') + ':' + os.environ.get('DB_PASSWORD') + '@realmcluster.zudeo.mongodb.net/' + os.environ.get('DB_NAME') + '?retryWrites=true&w=majority', alias='core')

def setup_network_connection(database):
    # Insert credentials here for local testing
    account_name = ''
    account_password = ''
    mongoengine.connect(host='mongodb+srv://' + account_name + ':' + account_password + '@realmcluster.zudeo.mongodb.net/' + database + '?retryWrites=true&w=majority', alias='core')


