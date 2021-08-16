from app import app
import flask


@app.route('/portfolio')
def index():
    # portfolio page
    return flask.render_template('porfolio.html')
