from __main__ import app
import flask

@app.route('/')
def index():
    # home page
    return flask.render_template('index.html')