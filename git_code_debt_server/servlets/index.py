import flask

from git_code_debt_server.render_mako import render_template

index = flask.Blueprint('index', __name__)

@index.route('/')
def show():
    return render_template('index.mako', metrics=[
        {'title': 'self_dot_display', 'occurrences': 250, 'files': 32, 'change': -4, 'href': 'http://localhost:5000/graph/self_dot_display?repo=yelp_main&ref=master&start=1380585600&end=1383264000'}
    ])
