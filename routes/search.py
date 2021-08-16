from app import app
import flask


@app.route('/search')
def search():
    # search page to find company data
    return flask.render_template('search.html')

# ----------------- search APIs ----------------- #

def search(query):
    # must accept either ticker or company name
    # return name and ticker of company most similar to query string
    pass

def search_results(query):
    # must accept either ticker or company name
    # check if user is logged in
    # return all needed details of company most similar to query string
    pass
