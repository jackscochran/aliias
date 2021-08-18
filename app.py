import flask

import databases.aliias_web.adaptors.email as email_adaptor
import databases.aliias_web.manager as user_db_manager

import re

app = flask.Flask(__name__)

# ------------------- PAGE ROUTES ---------------- 3

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

@app.route('/register-email', methods=['POST'])
def register_email():
    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        # validate email
        #   TODO

        user_db_manager.setup_heroku_mongo_connection()

        return flask.jsonify({'email_added': email_adaptor.add_email(email)})

    return flask.jsonify({'error': True})

app.config["TEMPLATES_AUTO_RELOAD"] = True

if __name__ == "__main__":
    app.run()

