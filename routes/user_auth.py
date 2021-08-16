from app import app
import flask

@app.route('/sign-on')
def sign_on():
    # handls sign up and log in
    return flask.render_template('sign_on.html')

@app.route('/logout')
def logout():
    pass