from app import app
import flask

@app.route('/about')
def about():
    # about the company page
    return flask.render_template('about.html')
