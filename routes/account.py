from app import app
import flask

@app.route('/account')
def account_settings():
    # view and edit account settings
    return flask.render_template('account.html')


# ------------- User Account API's ------------- #

def account_info():
    # get/set account information in dict
    pass

def cancel_account():
    pass

def cancel_subscription():
    pass
