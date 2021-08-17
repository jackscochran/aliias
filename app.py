import flask


app = flask.Flask(__name__)

# after creating app, import all route files
# import routes.index
# import routes.about
# import routes.account
# import routes.company
# import routes.help
# import routes.policies
# import routes.portfolio
# import routes.pricing
# import routes.search
# import routes.user_auth


@app.route('/')
def index():
    # home page
    return flask.render_template('index.html')

app.config["TEMPLATES_AUTO_RELOAD"] = True

if __name__ == "__main__":
    app.run(debug=True)

