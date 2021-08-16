from app import app
import flask

@app.route('/help')
def help():
    # help page (FAQ)
    return flask.render_template('help.html')
