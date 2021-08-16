from app import app
import flask

@app.route('/<ticker>')
def company():
    # view detailed company information
    return flask.render_template('company.html')