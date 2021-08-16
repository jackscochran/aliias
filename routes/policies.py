from app import app
import flask

@app.route('/policies')
def policies():
    # policies details
    return flask.render_template('policies.html')
