from app import app
import flask

@app.route('/pricing')
def pricing():
    # pricing and plans page
    return flask.render_template('pricing.html')
