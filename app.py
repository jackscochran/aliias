import flask

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
    return flask.render_template('portfolio.html')

@app.route('/help')
def help():
    # Porfolio page
    return flask.render_template('help.html')

@app.route('/about')
def about():
    # Porfolio page
    return flask.render_template('about.html')

@app.route('/register')
def register():
    # Porfolio page
    return flask.render_template('register.html')

@app.route('/search')
def search():
    # Porfolio page
    return flask.render_template('search.html') 

@app.route('/error')
def error():
    # error page
    
    return flask.render_template('error.html')

# ------------------- API ROUTES ---------------- 3

@app.route('/api/register-email', methods=['POST'])
def register_email():
    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        # validate email
        #   TODO

        user_db_manager.setup_heroku_mongo_connection()

        return flask.jsonify({'email_added': email_adaptor.add_email(email)})

    return flask.jsonify({'error': True})

@app.route('/api/get-portfolio', methods=['POST'])
def get_portfolio():

    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'POST':
        portfolio = portfolio_adaptor.get_portfolio(flask.request.form.get('name'), flask.request.form.get('version'))
        return flask.jsonify({'date_created': portfolio.date_created, 'tickers': portfolio.tickers})

    return flask.jsonify({'error': True})

@app.route('/api/portfolio-company', methods=['POST'])
def portfolio_company_date():

    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'POST':
        company_data = company_adaptor.company_data_list_format(flask.request.form.get('ticker'))
        return flask.jsonify(company_data)

    return flask.jsonify({'error': True})

@app.route('/api/all-company-prices', methods=['POST'])
def all_company_prices():
    
    stock_db_manager.setup_heroku_mongo_connection()

    if flask.request.method == 'POST':
        prices = price_adaptor.all_company_prices(flask.request.form.get('ticker'))
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
            '3m': price_adaptor.get_price(ticker, timeline.change_months(date, -3)),
            '6m': price_adaptor.get_price(ticker, timeline.change_months(date, -6)),
            '1y': price_adaptor.get_price(ticker, timeline.change_months(date, -12)),
            '5y': price_adaptor.get_price(ticker, timeline.change_months(date, -60)),
            'rated': price_adaptor.get_price(ticker, date_rated)
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
            '5y': 0
        }

        threeMonthCount = sixMonthCount = oneYearCount = fiveYearCount = 0
        for ticker in portfolio_adaptor.get_portfolio(name, version).tickers:
            
            current_price = price_adaptor.get_price(ticker, date)
             
            
            entry_price = price_adaptor.get_price(ticker, timeline.change_months(date, -3))
            if entry_price is not None:
                threeMonthCount += 1
                performance['3m'] += (current_price - entry_price) / entry_price

            
            entry_price = price_adaptor.get_price(ticker, timeline.change_months(date, -6))
            if entry_price is not None:
                sixMonthCount += 1
                performance['6m'] += (current_price - entry_price) / entry_price

            entry_price = price_adaptor.get_price(ticker, timeline.change_months(date, -12))
            if entry_price is not None:
                oneYearCount += 1
                performance['1y'] += (current_price - entry_price) / entry_price

            entry_price = price_adaptor.get_price(ticker, timeline.change_months(date, -60))
            if entry_price is not None:
                fiveYearCount += 1
                performance['5y'] += (current_price - entry_price) / entry_price

        performance['3m'] = round(performance['3m'] / threeMonthCount * 100, 2)
        performance['6m'] = round(performance['6m'] / sixMonthCount * 100, 2)
        performance['1y'] = round(performance['1y'] / oneYearCount * 100, 2)
        performance['5y'] = round(performance['5y'] / fiveYearCount * 100, 2)

        return flask.jsonify(performance)

    return flask.jsonify({'error': True})
    
# ------------------- RUNNER FUNCTION ---------------- #

if __name__ == "__main__":
    app.run()

