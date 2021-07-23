import flask
import controllers.data_pipeline as data_pipeline
import datetime

app = flask.Flask(__name__)



# ------------- Pages ------------- #

@app.route('/')
def index():
    # home page
    return flask.render_template('about.html')

@app.route('/about')
def about():
    # about page
    data_pipeline.collect_earnings(str(datetime.date.today()))
    return flask.render_template('about.html')

@app.route('/policies')
def policies():
    # policies details
    return flask.render_template('policies.html')

@app.route('/help')
def help_page():
    # page to help the user use the site and resolve any issues
    return flask.render_template('help.html')

@app.route('/search')
def search():
    # search for companies
    return flask.render_template('search.html')

@app.route('/portfolio')
def portfolio():
    # view porfolios page
    return flask.render_template('portfolio.html')

@app.route('/account')
def account_settings():
    # view and edit account settings
    return flask.render_template('account.html')

@app.route('/<ticker>')
def company():
    # view detailed company information
    return flask.render_template('company.html')

# ------------- User Authentication ------------- #

@app.route('/sign-on')
def sign_on():
    # handls sign up and log in
    return flask.render_template('sign_on.html')

@app.route('/logout')
def logout():
    pass

# ------------- User Account API's ------------- #

def account_info():
    # get/set account information in dict
    pass

def cancel_account():
    pass

def cancel_subscription():
    pass

# ------------- Company Data Apis ------------- #

def search(query):
    # must accept either ticker or company name
    # return name and ticker of company most similar to query string
    pass

def search_results(query):
    # must accept either ticker or company name
    # check if user is logged in
    # return all needed details of company most similar to query string
    pass

def portfolio():
    # return protfolio and performance for portfolio in specific category
    pass

if __name__ == "__main__":
    app.run(debug=True)

