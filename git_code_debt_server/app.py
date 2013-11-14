import flask

from git_code_debt_server.servlets.graph import graph
from git_code_debt_server.servlets.index import index

app = flask.Flask(__name__)

app.register_blueprint(index)
app.register_blueprint(graph)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
