import flask
import math
import datetime
import databases.aliias_web.adaptors.email as email_adaptor
import databases.aliias_stocks.adaptors.portfolio as portfolio_adaptor
import databases.aliias_stocks.adaptors.company as company_adaptor
import databases.aliias_stocks.adaptors.daily_price as price_adaptor
import databases.aliias_stocks.manager as stock_db_manager
import databases.aliias_web.manager as user_db_manager
import databases.aliias_stocks.helpers.timeline as timeline

import re

# ------------------- APP CONFIG -------------------#

app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


# ------------------- PAGE ROUTES ---------------- #

@app.route('/')
def index():
    # home page
    return flask.render_template('index.html')

@app.route('/portfolio')
def portfolio():
    # Porfolio page
    return flask.render_template('register.html')

@app.route('/help')
def help():
    # help page
    return flask.render_template('help.html')

@app.route('/about')
def about():
    # about page
    return flask.render_template('about.html')

@app.route('/contact-us')
def contact():
    # contact-us page
    return flask.render_template('contact-us.html')

@app.route('/search')
def search():
    # search page
    return flask.render_template('search.html') 

@app.route('/error')
def error():
    # error page
    
    return flask.render_template('error.html')

@app.route('/privacy-policy')
def privacy():
    # privacy policy
    return flask.render_template('privacy-policy.html')

@app.route('/stocks/<ticker>')
def company(ticker):
    stock_db_manager.setup_heroku_mongo_connection()
    date = str(datetime.date.today())
    company = company_adaptor.get_company(ticker)
    quote_data = company.get_quote_data(date)

    clean_quote_data = {}

    for data_point in quote_data.data:
        if data_point == 'firstYearTargetEst':
            continue
        clean_label = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', data_point).capitalize()
        clean_quote_data[clean_label] = quote_data.data[data_point]

    return flask.render_template('company.html', company=company, price=company.get_price(date), quote_data=clean_quote_data)

# ------------------- API ROUTES ---------------- #

@app.route('/api/register-email', methods=['POST'])
def register_email():
    if flask.request.method == 'POST':
        email = flask.request.form.get('email').lower()
        # validate email
        #   TODO

        user_db_manager.setup_heroku_mongo_connection()

        return flask.jsonify({'email_added': email_adaptor.add_email(email)})

    return flask.jsonify({'error': True})

@app.route('/api/get-portfolio', methods=['GET'])
def get_portfolio():

    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        portfolio = portfolio_adaptor.get_portfolio(flask.request.args.get('name'), flask.request.args.get('version'))
        return flask.jsonify({'date_created': portfolio.date_created, 'tickers': portfolio.tickers})

    return flask.jsonify({'error': True})

@app.route('/api/portfolio-company', methods=['GET'])
def portfolio_company_date():

    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        company_data = company_adaptor.company_data_list_format(flask.request.args.get('ticker'))
        return flask.jsonify(company_data)

    return flask.jsonify({'error': True})

@app.route('/api/all-company-prices', methods=['GET'])
def all_company_prices():
    
    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        prices = price_adaptor.all_company_prices(flask.request.args.get('ticker'))
        return flask.jsonify([{'price': price.price, 'date': price.date} for price in prices])

    return flask.jsonify({'error': True})

@app.route('/api/company-performance', methods=['GET'])
def company_price():
    
    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        ticker = flask.request.args.get('ticker')
        date = flask.request.args.get('date')
        date_rated = company_adaptor.get_company(ticker).get_evaluation(date).date
        return flask.jsonify({
            'current': price_adaptor.get_price(ticker, date),
            '3m': price_adaptor.get_weekday_price(ticker, timeline.change_months(date, -3)),
            '6m': price_adaptor.get_weekday_price(ticker, timeline.change_months(date, -6)),
            '1y': price_adaptor.get_weekday_price(ticker, timeline.change_months(date, -12)),
            'rated': price_adaptor.get_weekday_price(ticker, date_rated)
        })

    return flask.jsonify({'error': True})
    
@app.route('/api/portfolio-performance', methods=['GET'])
def portfolio_performance():
    
    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        name = flask.request.args.get('name')
        version = flask.request.args.get('version')
        date = flask.request.args.get('date')

        performance = {
            '3m': 0,
            '6m': 0,
            '1y': 0,
            'sinceCreation': 0
        }

        print(performance)

        threeMonthCount = sixMonthCount = oneYearCount = sinceCreationCount = 0

        portfolio = portfolio_adaptor.get_portfolio(name, version)
        for ticker in portfolio.tickers:
            
            current_price = price_adaptor.get_price(ticker, date)
            
            entry_price = price_adaptor.get_weekday_price(ticker, timeline.change_months(date, -3))
            if entry_price is not None:
                threeMonthCount += 1
                performance['3m'] += (current_price - entry_price) / entry_price

            
            entry_price = price_adaptor.get_weekday_price(ticker, timeline.change_months(date, -6))
            if entry_price is not None:
                sixMonthCount += 1
                performance['6m'] += (current_price - entry_price) / entry_price

            entry_price = price_adaptor.get_weekday_price(ticker, timeline.change_months(date, -12))
            if entry_price is not None:
                oneYearCount += 1
                performance['1y'] += (current_price - entry_price) / entry_price

            entry_price = price_adaptor.get_weekday_price(ticker, portfolio.date_created)
            if entry_price is not None and not math.isnan(entry_price):
                sinceCreationCount += 1
                performance['sinceCreation'] += (current_price - entry_price) / entry_price

        if threeMonthCount > 0:
            performance['3m'] = round(performance['3m'] / threeMonthCount * 100, 2)

        if sixMonthCount > 0:
            performance['6m'] = round(performance['6m'] / sixMonthCount * 100, 2)

        if oneYearCount > 0:
            performance['1y'] = round(performance['1y'] / oneYearCount * 100, 2)

        print('------------')
        print(performance)
        print(sinceCreationCount)
        if sinceCreationCount > 0:
            performance['sinceCreation'] = round(performance['sinceCreation'] / sinceCreationCount * 100, 2)


        return flask.jsonify(performance)

    return flask.jsonify({'error': True})
    
@app.route('/api/search-stock', methods=['GET'])
def search_stock():
    
    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        query = flask.request.args.get('query')

        responseDict = {
            'results': company_adaptor.search(query, 20)
        }

        return flask.jsonify(responseDict)

    return flask.jsonify({'error': True})

@app.route('/api/historical-prices')
def historical_prices():
    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'GET':
        ticker = flask.request.args.get('ticker')
        dates = []
        prices = []
        for price in price_adaptor.get_historical_prices(ticker, months_back=6):
            dates.append(price.date)
            prices.append(price.price)


        return flask.jsonify(
            {
                'results': {
                    'dates': dates,
                    'prices': prices
                }
            }
        
        )

# ------------------- RUNNER FUNCTION ---------------- #

if __name__ == "__main__":
    app.run()

