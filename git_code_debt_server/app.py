import flask

from git_code_debt_server.render_mako import render_template
from git_code_debt_server.servlets.graph import graph

app = flask.Flask(__name__)

app.register_blueprint(graph)

@app.route('/')
def index():
    return render_template('index.mako')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
